from __future__ import annotations

import json
from dataclasses import asdict

from slotfit.exposure_frontier import build_local_exposure_frontier


def main() -> None:
    frontier = build_local_exposure_frontier()
    print(json.dumps(asdict(frontier), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
