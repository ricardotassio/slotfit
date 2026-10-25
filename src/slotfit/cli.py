from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

from slotfit.scenarios import demo_scenario
from slotfit.strategies import best_fit_plan, fifo_plan


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"cannot serialize {type(value).__name__}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the first SlotFit synthetic scenario")
    parser.add_argument("--seed", type=int, default=1400)
    args = parser.parse_args()

    scenario = demo_scenario(seed=args.seed)
    output = {
        "scenario_id": scenario.scenario_id,
        "synthetic": True,
        "plans": [asdict(fifo_plan(scenario)), asdict(best_fit_plan(scenario))],
        "automatic_action": "none",
    }
    print(json.dumps(output, default=_json_default, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

