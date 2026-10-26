from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, replace
from enum import StrEnum

import ortools
from ortools.sat.python import cp_model

from slotfit.domain.eligibility import evaluate_request, scheduled_window
from slotfit.domain.model import (
    Assignment,
    CandidateEvaluation,
    CandidatePlan,
    OpenInterval,
    Scenario,
    WaitRequest,
)


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
DEFAULT_MINIMUM_RECOVERED_RATIO = 0.90


@dataclass(frozen=True, slots=True)
class ObjectiveProfile:
    """Which residual lexicographic phases a strategy variant enables."""

    strategy: str
    uses_exposure_debt: bool
    uses_placement_scarcity: bool
    minimum_recovered_ratio: float | None


LEXICOGRAPHIC_PROFILE = ObjectiveProfile(
    strategy="cp-sat-lexicographic@0.1.0",
    uses_exposure_debt=False,
    uses_placement_scarcity=False,
    minimum_recovered_ratio=None,
)
EXPOSURE_DEBT_PROFILE = ObjectiveProfile(
    strategy="cp-sat-exposure-debt@0.2.0",
    uses_exposure_debt=True,
    uses_placement_scarcity=False,
    minimum_recovered_ratio=None,
)
PLACEMENT_SCARCITY_PROFILE = ObjectiveProfile(
    strategy="cp-sat-placement-scarcity@0.3.0",
    uses_exposure_debt=True,
    uses_placement_scarcity=True,
    minimum_recovered_ratio=None,
)
BOUNDED_RECOVERY_PROFILE = ObjectiveProfile(
    strategy="cp-sat-bounded-recovery@0.4.0",
    uses_exposure_debt=True,
    uses_placement_scarcity=True,
    minimum_recovered_ratio=DEFAULT_MINIMUM_RECOVERED_RATIO,
)


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

    return _optimize_plan(
        scenario,
        profile=LEXICOGRAPHIC_PROFILE,
        config=config,
        exposure_debt_by_request_id=None,
    )


def optimize_plan_with_exposure_debt(
    scenario: Scenario,
    *,
    exposure_debt_by_request_id: Mapping[str, int],
    config: SolverConfig = DEFAULT_SOLVER_CONFIG,
) -> OptimizationResult:
    """Solve with prior compatible misses as a residual lexicographic objective."""

    _validate_exposure_debt(scenario, exposure_debt_by_request_id)

    return _optimize_plan(
        scenario,
        profile=EXPOSURE_DEBT_PROFILE,
        config=config,
        exposure_debt_by_request_id=exposure_debt_by_request_id,
    )


def optimize_plan_with_placement_scarcity(
    scenario: Scenario,
    *,
    exposure_debt_by_request_id: Mapping[str, int],
    config: SolverConfig = DEFAULT_SOLVER_CONFIG,
) -> OptimizationResult:
    """Solve with exposure debt and current eligible-interval scarcity."""

    _validate_exposure_debt(scenario, exposure_debt_by_request_id)
    return _optimize_plan(
        scenario,
        profile=PLACEMENT_SCARCITY_PROFILE,
        config=config,
        exposure_debt_by_request_id=exposure_debt_by_request_id,
    )


def optimize_plan_with_bounded_recovery(
    scenario: Scenario,
    *,
    exposure_debt_by_request_id: Mapping[str, int],
    minimum_recovered_ratio: float = DEFAULT_MINIMUM_RECOVERED_RATIO,
    config: SolverConfig = DEFAULT_SOLVER_CONFIG,
) -> OptimizationResult:
    """Solve residual objectives inside a declared recovered-minute floor."""

    if minimum_recovered_ratio <= 0 or minimum_recovered_ratio > 1:
        raise ValueError("minimum_recovered_ratio must be within (0, 1]")
    _validate_exposure_debt(scenario, exposure_debt_by_request_id)
    return _optimize_plan(
        scenario,
        profile=replace(
            BOUNDED_RECOVERY_PROFILE,
            minimum_recovered_ratio=minimum_recovered_ratio,
        ),
        config=config,
        exposure_debt_by_request_id=exposure_debt_by_request_id,
    )


def _validate_exposure_debt(
    scenario: Scenario,
    exposure_debt_by_request_id: Mapping[str, int],
) -> None:
    request_ids = {request.request_id for request in scenario.wait_requests}
    unknown_ids = set(exposure_debt_by_request_id) - request_ids
    if unknown_ids:
        raise ValueError(f"exposure debt contains unknown request IDs: {sorted(unknown_ids)}")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in exposure_debt_by_request_id.values()
    ):
        raise ValueError("exposure debt values must be non-negative integers")


_VariableKey = tuple[str, str]
_Variables = dict[_VariableKey, cp_model.IntVar]
_Objective = cp_model.LinearExpr | int
_PhaseContract = tuple[tuple[str, _Objective], ...]


@dataclass(frozen=True, slots=True)
class _OptimizationProblem:
    """Deterministically ordered inputs shared by every optimizer step."""

    requests: tuple[WaitRequest, ...]
    intervals: tuple[OpenInterval, ...]
    evaluations: tuple[CandidateEvaluation, ...]
    request_by_id: Mapping[str, WaitRequest]
    interval_by_id: Mapping[str, OpenInterval]


@dataclass(frozen=True, slots=True)
class _PhaseOutcome:
    phases: tuple[SolverPhase, ...]
    selected_keys: frozenset[_VariableKey]
    status: SolverStatus


def _optimize_plan(
    scenario: Scenario,
    *,
    profile: ObjectiveProfile,
    config: SolverConfig,
    exposure_debt_by_request_id: Mapping[str, int] | None,
) -> OptimizationResult:
    if profile.uses_exposure_debt and exposure_debt_by_request_id is None:
        raise ValueError(f"{profile.strategy} requires exposure_debt_by_request_id")

    problem = _build_problem(scenario)
    model = cp_model.CpModel()
    variables = _create_variables(model, problem)
    _add_exclusivity_constraints(model, problem, variables)
    contract = _phase_contract(profile, problem, variables, exposure_debt_by_request_id)
    outcome = _solve_phases(
        model, contract, config, profile.minimum_recovered_ratio, variables
    )
    return OptimizationResult(
        status=outcome.status,
        optimized=(
            len(outcome.phases) == len(contract)
            and all(phase.status is SolverStatus.OPTIMAL for phase in outcome.phases)
        ),
        plan=_build_plan(problem, outcome.selected_keys, profile.strategy),
        phases=outcome.phases,
        config=config,
        engine_version=ortools.__version__,
    )


def _build_problem(scenario: Scenario) -> _OptimizationProblem:
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
    evaluations = tuple(
        evaluate_request(scenario, interval, request)
        for interval in intervals
        for request in requests
    )
    return _OptimizationProblem(
        requests=requests,
        intervals=intervals,
        evaluations=evaluations,
        request_by_id={request.request_id: request for request in requests},
        interval_by_id={interval.interval_id: interval for interval in intervals},
    )


def _create_variables(model: cp_model.CpModel, problem: _OptimizationProblem) -> _Variables:
    """Create one boolean per eligible pair: requests outer, intervals inner."""

    evaluation_by_key = {
        (evaluation.request_id, evaluation.interval_id): evaluation
        for evaluation in problem.evaluations
    }
    variables: _Variables = {}
    for request_position, request in enumerate(problem.requests, start=1):
        for interval_position, interval in enumerate(problem.intervals, start=1):
            key = (request.request_id, interval.interval_id)
            if not evaluation_by_key[key].eligible:
                continue
            variables[key] = model.new_bool_var(
                f"assign_r{request_position}_i{interval_position}"
            )
    return variables


def _add_exclusivity_constraints(
    model: cp_model.CpModel,
    problem: _OptimizationProblem,
    variables: _Variables,
) -> None:
    for request in problem.requests:
        model.add(
            sum(
                variable
                for (request_id, _interval_id), variable in variables.items()
                if request_id == request.request_id
            )
            <= 1
        )
    for interval in problem.intervals:
        model.add(
            sum(
                variable
                for (_request_id, interval_id), variable in variables.items()
                if interval_id == interval.interval_id
            )
            <= 1
        )


def _phase_contract(
    profile: ObjectiveProfile,
    problem: _OptimizationProblem,
    variables: _Variables,
    exposure_debt_by_request_id: Mapping[str, int] | None,
) -> _PhaseContract:
    """Ordered lexicographic objectives for the profile; the order is the contract."""

    recovered_minutes_name = (
        "recovered-minutes-ceiling"
        if profile.minimum_recovered_ratio is not None
        else "recovered-minutes"
    )
    contract: list[tuple[str, _Objective]] = [
        (recovered_minutes_name, _recovered_minutes(problem, variables)),
        ("requests-served", sum(variables.values())),
    ]
    if profile.uses_exposure_debt and exposure_debt_by_request_id is not None:
        contract.append(
            (
                "exposure-debt-score",
                _exposure_debt_score(variables, exposure_debt_by_request_id),
            )
        )
    if profile.uses_placement_scarcity:
        contract.append(
            ("placement-scarcity-score", _placement_scarcity_score(problem, variables))
        )
    contract.append(("wait-age-score", _wait_age_score(problem, variables)))
    return tuple(contract)


def _recovered_minutes(
    problem: _OptimizationProblem,
    variables: _Variables,
) -> _Objective:
    return sum(
        problem.request_by_id[request_id].duration_minutes * variable
        for (request_id, _interval_id), variable in variables.items()
    )


def _wait_age_score(
    problem: _OptimizationProblem,
    variables: _Variables,
) -> _Objective:
    return sum(
        (len(problem.requests) + 1 - problem.request_by_id[request_id].joined_order)
        * variable
        for (request_id, _interval_id), variable in variables.items()
    )


def _exposure_debt_score(
    variables: _Variables,
    exposure_debt_by_request_id: Mapping[str, int],
) -> _Objective:
    return sum(
        exposure_debt_by_request_id.get(request_id, 0) * variable
        for (request_id, _interval_id), variable in variables.items()
    )


def _placement_scarcity_score(
    problem: _OptimizationProblem,
    variables: _Variables,
) -> _Objective:
    compatible_interval_counts = {
        request.request_id: sum(
            request_id == request.request_id for request_id, _interval_id in variables
        )
        for request in problem.requests
    }
    return sum(
        (len(problem.intervals) + 1 - compatible_interval_counts[request_id]) * variable
        for (request_id, _interval_id), variable in variables.items()
    )


def _solve_phases(
    model: cp_model.CpModel,
    contract: _PhaseContract,
    config: SolverConfig,
    minimum_recovered_ratio: float | None,
    variables: _Variables,
) -> _PhaseOutcome:
    """Solve each phase in order, fixing its optimum before the next one."""

    phases: list[SolverPhase] = []
    selected_keys: frozenset[_VariableKey] = frozenset()
    status = SolverStatus.UNKNOWN

    for phase_index, (phase_name, objective) in enumerate(contract):
        model.maximize(objective)
        solver = _configured_solver(config)
        status = _status(solver, solver.solve(model))
        phase = _phase_record(phase_name, solver, status)
        phases.append(phase)
        if phase.objective_value is not None:
            selected_keys = frozenset(
                key for key, variable in variables.items() if solver.value(variable) == 1
            )
        if status is not SolverStatus.OPTIMAL:
            break
        assert phase.objective_value is not None
        _fix_phase_optimum(
            model, objective, phase.objective_value, phase_index, minimum_recovered_ratio
        )

    return _PhaseOutcome(phases=tuple(phases), selected_keys=selected_keys, status=status)


def _phase_record(name: str, solver: cp_model.CpSolver, status: SolverStatus) -> SolverPhase:
    has_solution = status in (SolverStatus.OPTIMAL, SolverStatus.FEASIBLE)
    return SolverPhase(
        name=name,
        status=status,
        objective_value=int(round(solver.objective_value)) if has_solution else None,
        best_objective_bound=float(solver.best_objective_bound) if has_solution else None,
        wall_time_seconds=float(solver.wall_time),
    )


def _fix_phase_optimum(
    model: cp_model.CpModel,
    objective: _Objective,
    objective_value: int,
    phase_index: int,
    minimum_recovered_ratio: float | None,
) -> None:
    if phase_index == 0 and minimum_recovered_ratio is not None:
        model.add(objective >= math.ceil(objective_value * minimum_recovered_ratio))
        return
    model.add(objective == objective_value)


def _build_plan(
    problem: _OptimizationProblem,
    selected_keys: frozenset[_VariableKey],
    strategy: str,
) -> CandidatePlan:
    ordered_keys = sorted(
        selected_keys,
        key=lambda key: (
            problem.interval_by_id[key[1]].window.start,
            problem.request_by_id[key[0]].joined_order,
        ),
    )
    assignments = tuple(
        Assignment(
            request_id=request_id,
            interval_id=interval_id,
            scheduled_window=scheduled_window(
                problem.interval_by_id[interval_id],
                problem.request_by_id[request_id],
            ),
        )
        for request_id, interval_id in ordered_keys
    )
    recovered_value = sum(item.scheduled_window.duration_minutes for item in assignments)
    open_minutes = sum(interval.window.duration_minutes for interval in problem.intervals)
    return CandidatePlan(
        strategy=strategy,
        assignments=assignments,
        recovered_minutes=recovered_value,
        remaining_gap_minutes=open_minutes - recovered_value,
        evaluations=problem.evaluations,
    )
