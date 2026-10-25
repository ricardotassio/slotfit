from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from slotfit.comparison import compare_engineering_split
from slotfit.generation import EvaluationSplit


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a SlotFit engineering-split comparison report",
    )
    parser.add_argument(
        "--split",
        choices=tuple(item.value for item in EvaluationSplit),
        default=EvaluationSplit.DEVELOPMENT.value,
    )
    args = parser.parse_args()
    report = compare_engineering_split(EvaluationSplit(args.split))
    print(json.dumps(asdict(report), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
