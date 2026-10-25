from __future__ import annotations

import json
from dataclasses import asdict

from slotfit.alternative_diagnostic import diagnose_development_alternatives


def main() -> None:
    report = diagnose_development_alternatives()
    print(json.dumps(asdict(report), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
