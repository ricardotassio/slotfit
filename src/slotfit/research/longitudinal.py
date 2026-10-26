from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace

from slotfit.domain.model import CandidatePlan, Scenario
from slotfit.research.evaluation import ScenarioEvaluation, evaluate_generated_plan
from slotfit.research.generation import (
    EvaluationSplit,
    GeneratedScenario,
    RequestAuditSlice,
    decision_checksum,
)


Strategy = Callable[[Scenario], CandidatePlan]
DebtAwareStrategy = Callable[[Scenario, Mapping[str, int]], CandidatePlan]


@dataclass(slots=True)
class _MutableHistory:
    eligible_opportunities: int = 0
    plan_exposures: int = 0
    unselected_compatible_opportunities: int = 0
    first_exposure_round: int | None = None


@dataclass(frozen=True, slots=True)
class OpportunityRound:
    round_number: int
    evaluation: ScenarioEvaluation


@dataclass(frozen=True, slots=True)
class LongitudinalRequestRecord:
    request_id: str
    audit_slice: RequestAuditSlice
    eligible_opportunities: int
    plan_exposures: int
    unselected_compatible_opportunities: int
    first_exposure_round: int | None


@dataclass(frozen=True, slots=True)
class LongitudinalEvaluation:
    seed: int
    split: EvaluationSplit
    strategy: str
    requested_rounds: int
    rounds: tuple[OpportunityRound, ...]
    requests: tuple[LongitudinalRequestRecord, ...]


def _round_scenario(
    generated: GeneratedScenario,
    active_request_ids: set[str],
    round_number: int,
) -> GeneratedScenario:
    scenario = replace(
        generated.scenario,
        scenario_id=f"{generated.scenario.scenario_id}-round-{round_number:02d}",
        wait_requests=tuple(
            request
            for request in generated.scenario.wait_requests
            if request.request_id in active_request_ids
        ),
    )
    manifest = replace(
        generated.manifest,
        decision_checksum=decision_checksum(scenario),
        audit_slices=tuple(
            audit_slice
            for audit_slice in generated.manifest.audit_slices
            if audit_slice.request_id in active_request_ids
        ),
    )
    return GeneratedScenario(scenario=scenario, manifest=manifest)


def simulate_opportunity_rounds(
    generated: GeneratedScenario,
    strategy: Strategy,
    *,
    rounds: int,
) -> LongitudinalEvaluation:
    """Replay a stable cohort through controlled compatible-opportunity rounds.

    This is deliberately an opportunity-count simulation, not a calendar or a
    patient-wait model. A request exposed by a plan is removed before the next
    round. The output provides inputs for a later, predeclared starvation rule but
    does not choose that rule or label a request as starved.
    """

    return _simulate_opportunity_rounds(
        generated,
        lambda scenario, _debt: strategy(scenario),
        rounds=rounds,
    )


def simulate_exposure_debt_rounds(
    generated: GeneratedScenario,
    strategy: DebtAwareStrategy,
    *,
    rounds: int,
) -> LongitudinalEvaluation:
    """Replay rounds while passing prior compatible misses to the strategy."""

    return _simulate_opportunity_rounds(generated, strategy, rounds=rounds)


def _simulate_opportunity_rounds(
    generated: GeneratedScenario,
    strategy: DebtAwareStrategy,
    *,
    rounds: int,
) -> LongitudinalEvaluation:
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    active_request_ids = {
        request.request_id for request in generated.scenario.wait_requests
    }
    audit_by_request = {
        audit_slice.request_id: audit_slice
        for audit_slice in generated.manifest.audit_slices
    }
    history = {request_id: _MutableHistory() for request_id in active_request_ids}
    round_results: list[OpportunityRound] = []
    strategy_name: str | None = None

    for round_number in range(1, rounds + 1):
        if not active_request_ids:
            break

        round_generated = _round_scenario(
            generated,
            active_request_ids,
            round_number,
        )
        exposure_debt = {
            request_id: history[request_id].unselected_compatible_opportunities
            for request_id in active_request_ids
        }
        plan = strategy(round_generated.scenario, exposure_debt)
        evaluation = evaluate_generated_plan(round_generated, plan)
        if strategy_name is None:
            strategy_name = plan.strategy
        elif strategy_name != plan.strategy:
            raise ValueError("strategy identifier changed between rounds")

        eligible_request_ids = {
            record.request_id
            for record in evaluation.requests
            if record.eligible_opportunity
        }
        selected_eligible_ids = {
            record.request_id
            for record in evaluation.requests
            if record.eligible_opportunity and record.selected
        }
        for request_id in eligible_request_ids:
            request_history = history[request_id]
            request_history.eligible_opportunities += 1
            if request_id in selected_eligible_ids:
                request_history.plan_exposures += 1
                if request_history.first_exposure_round is None:
                    request_history.first_exposure_round = round_number
            else:
                request_history.unselected_compatible_opportunities += 1

        round_results.append(
            OpportunityRound(round_number=round_number, evaluation=evaluation)
        )
        active_request_ids.difference_update(selected_eligible_ids)

    request_records = tuple(
        LongitudinalRequestRecord(
            request_id=request.request_id,
            audit_slice=audit_by_request[request.request_id],
            eligible_opportunities=history[request.request_id].eligible_opportunities,
            plan_exposures=history[request.request_id].plan_exposures,
            unselected_compatible_opportunities=(
                history[request.request_id].unselected_compatible_opportunities
            ),
            first_exposure_round=history[request.request_id].first_exposure_round,
        )
        for request in generated.scenario.wait_requests
    )
    return LongitudinalEvaluation(
        seed=generated.manifest.seed,
        split=generated.manifest.split,
        strategy=strategy_name or "not-run",
        requested_rounds=rounds,
        rounds=tuple(round_results),
        requests=request_records,
    )
