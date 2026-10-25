from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

from slotfit.evaluation import evaluate_generated_plan
from slotfit.generation import EvaluationSplit, generate_scenario
from slotfit.longitudinal import simulate_opportunity_rounds
from slotfit.optimizer import optimize_plan
from slotfit.scenarios import demo_scenario, multi_slot_counterexample
from slotfit.strategies import best_fit_plan, fifo_plan


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"cannot serialize {type(value).__name__}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a SlotFit synthetic scenario")
    parser.add_argument("--seed", type=int, default=1400)
    parser.add_argument(
        "--mode",
        choices=("fixture", "multi-slot", "generated"),
        default="fixture",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=0,
        help="run controlled opportunity rounds (generated mode only)",
    )
    parser.add_argument(
        "--split",
        choices=tuple(item.value for item in EvaluationSplit),
        default=EvaluationSplit.DEVELOPMENT.value,
    )
    args = parser.parse_args()
    if args.rounds < 0:
        parser.error("--rounds cannot be negative")
    if args.rounds and args.mode != "generated":
        parser.error("--rounds requires --mode generated")

    generated = None
    if args.mode == "generated":
        generated = generate_scenario(args.seed, split=EvaluationSplit(args.split))
        scenario = generated.scenario
    elif args.mode == "multi-slot":
        scenario = multi_slot_counterexample(seed=args.seed)
    else:
        scenario = demo_scenario(seed=args.seed)

    optimizer_result = optimize_plan(scenario) if args.mode == "multi-slot" else None
    plans = (fifo_plan(scenario), best_fit_plan(scenario))
    if optimizer_result is not None:
        plans += (optimizer_result.plan,)
    output = {
        "scenario_id": scenario.scenario_id,
        "synthetic": True,
        "scenario_source": args.mode,
        "plans": [asdict(plan) for plan in plans],
        "automatic_action": "none",
    }
    if generated is not None:
        output["audit_manifest"] = asdict(generated.manifest)
        output["event_evaluations"] = [
            asdict(evaluate_generated_plan(generated, plan)) for plan in plans
        ]
        if args.rounds:
            output["opportunity_simulations"] = [
                asdict(simulate_opportunity_rounds(generated, strategy, rounds=args.rounds))
                for strategy in (fifo_plan, best_fit_plan)
            ]
    if optimizer_result is not None:
        output["optimizer_evidence"] = asdict(optimizer_result)
    print(json.dumps(output, default=_json_default, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
