from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import ortools
from ortools.sat.python import cp_model

from slotfit.domain import Assignment, CandidatePlan, Scenario
from slotfit.eligibility import evaluate_request, scheduled_window


class SolverStatus(StrEnum):
    OPTIMAL = "OPTIMAL"
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    MODEL_INVALID = "MODEL_INVALID"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class SolverConfig:
    num_workers: int = 1
    random_seed: int = 1
    max_deterministic_time: float = 0.25
    max_time_in_seconds: float = 1.0
    log_search_progress: bool = False

    def __post_init__(self) -> None:
        if self.num_workers != 1:
            raise ValueError("num_workers must remain 1 for the deterministic POC")
        if self.max_deterministic_time <= 0:
            raise ValueError("max_deterministic_time must be positive")
        if self.max_time_in_seconds <= 0:
            raise ValueError("max_time_in_seconds must be positive")


@dataclass(frozen=True, slots=True)
class SolverPhase:
    name: str
    status: SolverStatus
    objective_value: int | None
    best_objective_bound: float | None
    wall_time_seconds: float


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    status: SolverStatus
    optimized: bool
    plan: CandidatePlan
    phases: tuple[SolverPhase, ...]
    config: SolverConfig
    engine_version: str


DEFAULT_SOLVER_CONFIG = SolverConfig()


def _configured_solver(config: SolverConfig) -> cp_model.CpSolver:
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = config.num_workers
    solver.parameters.random_seed = config.random_seed
    solver.parameters.max_deterministic_time = config.max_deterministic_time
    solver.parameters.max_time_in_seconds = config.max_time_in_seconds
    solver.parameters.log_search_progress = config.log_search_progress
    return solver


def _status(solver: cp_model.CpSolver, status: cp_model.CpSolverStatus) -> SolverStatus:
    return SolverStatus(solver.status_name(status))


def optimize_plan(
    scenario: Scenario,
    *,
    config: SolverConfig = DEFAULT_SOLVER_CONFIG,
) -> OptimizationResult:
    """Solve a global assignment with three explicit lexicographic phases."""

    intervals = tuple(
        sorted(
            scenario.open_intervals,
            key=lambda item: (
                item.window.start,
                item.window.end,
                item.window.duration_minutes,
            ),
        )
    )
    requests = tuple(sorted(scenario.wait_requests, key=lambda item: item.joined_order))
    request_by_id = {request.request_id: request for request in requests}
    interval_by_id = {interval.interval_id: interval for interval in intervals}
    evaluations = tuple(
        evaluate_request(scenario, interval, request)
        for interval in intervals
        for request in requests
    )

    model = cp_model.CpModel()
    variables: dict[tuple[str, str], cp_model.IntVar] = {}
    for request_position, request in enumerate(requests, start=1):
        for interval_position, interval in enumerate(intervals, start=1):
            evaluation = next(
                item
                for item in evaluations
                if item.request_id == request.request_id
                and item.interval_id == interval.interval_id
            )
            if evaluation.eligible:
                variables[(request.request_id, interval.interval_id)] = model.new_bool_var(
                    f"assign_r{request_position}_i{interval_position}"
                )

    for request in requests:
        model.add(
            sum(
                variable
                for (request_id, _interval_id), variable in variables.items()
                if request_id == request.request_id
            )
            <= 1
        )
    for interval in intervals:
        model.add(
            sum(
                variable
                for (_request_id, interval_id), variable in variables.items()
                if interval_id == interval.interval_id
            )
            <= 1
        )

    recovered_minutes = sum(
        request_by_id[request_id].duration_minutes * variable
        for (request_id, _interval_id), variable in variables.items()
    )
    requests_served = sum(variables.values())
    wait_age_score = sum(
        (len(requests) + 1 - request_by_id[request_id].joined_order) * variable
        for (request_id, _interval_id), variable in variables.items()
    )
    phase_contract = (
        ("recovered-minutes", recovered_minutes),
        ("requests-served", requests_served),
        ("wait-age-score", wait_age_score),
    )

    phase_results: list[SolverPhase] = []
    selected_keys: set[tuple[str, str]] = set()
    final_status = SolverStatus.UNKNOWN

    for phase_name, objective in phase_contract:
        model.maximize(objective)
        solver = _configured_solver(config)
        raw_status = solver.solve(model)
        final_status = _status(solver, raw_status)
        has_solution = final_status in (SolverStatus.OPTIMAL, SolverStatus.FEASIBLE)
        objective_value = int(round(solver.objective_value)) if has_solution else None
        best_bound = float(solver.best_objective_bound) if has_solution else None
        phase_results.append(
            SolverPhase(
                name=phase_name,
                status=final_status,
                objective_value=objective_value,
                best_objective_bound=best_bound,
                wall_time_seconds=float(solver.wall_time),
            )
        )
        if has_solution:
            selected_keys = {
                key for key, variable in variables.items() if solver.value(variable) == 1
            }
        if final_status is not SolverStatus.OPTIMAL:
            break
        assert objective_value is not None
        model.add(objective == objective_value)

    assignments = tuple(
        Assignment(
            request_id=request_id,
            interval_id=interval_id,
            scheduled_window=scheduled_window(
                interval_by_id[interval_id],
                request_by_id[request_id],
            ),
        )
        for request_id, interval_id in sorted(
            selected_keys,
            key=lambda key: (
                interval_by_id[key[1]].window.start,
                request_by_id[key[0]].joined_order,
            ),
        )
    )
    recovered_value = sum(item.scheduled_window.duration_minutes for item in assignments)
    open_minutes = sum(interval.window.duration_minutes for interval in intervals)
    plan = CandidatePlan(
        strategy="cp-sat-lexicographic@0.1.0",
        assignments=assignments,
        recovered_minutes=recovered_value,
        remaining_gap_minutes=open_minutes - recovered_value,
        evaluations=evaluations,
    )
    return OptimizationResult(
        status=final_status,
        optimized=(
            len(phase_results) == len(phase_contract)
            and all(phase.status is SolverStatus.OPTIMAL for phase in phase_results)
        ),
        plan=plan,
        phases=tuple(phase_results),
        config=config,
        engine_version=ortools.__version__,
    )
