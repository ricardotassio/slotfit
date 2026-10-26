"""Architecture test: every module lives in a layer package and imports only inward.

The rules mirror ADR-0004. They are checked with ``ast`` so the test needs no
third-party linter and runs with the rest of the suite.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[1] / "src" / "slotfit"
PACKAGE = "slotfit"

LAYERS = ("domain", "application", "solver", "research", "adapters", "composition")

# Each layer may import itself and the layers listed here.
ALLOWED_INWARD = {
    "domain": frozenset(),
    "application": frozenset({"domain"}),
    "solver": frozenset({"domain", "application"}),
    "research": frozenset({"domain", "application", "solver"}),
    "adapters": frozenset({"domain", "application", "solver", "research"}),
    "composition": frozenset(LAYERS),
}

# A framework may appear only inside the package that adapts it.
FRAMEWORK_HOME = {
    "ortools": "solver",
    "fastapi": "adapters.api",
    "pydantic": "adapters.api",
    "sqlite3": "adapters.persistence",
}

LOOSE_MODULES_ALLOWED = frozenset({"__init__", "composition"})


def _modules() -> list[tuple[str, Path]]:
    found = []
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        relative = path.relative_to(PACKAGE_ROOT).with_suffix("")
        found.append((".".join(relative.parts), path))
    return found


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _layer_of(dotted: str) -> str | None:
    head = dotted.split(".")[0]
    return head if head in LAYERS else None


class ArchitectureTests(unittest.TestCase):
    def test_every_module_lives_in_a_layer(self) -> None:
        loose = [
            dotted
            for dotted, _ in _modules()
            if "." not in dotted and dotted not in LOOSE_MODULES_ALLOWED
        ]
        self.assertEqual(loose, [], f"modules outside a layer package: {loose}")
        present = {dotted.split(".")[0] for dotted, _ in _modules()}
        for layer in LAYERS:
            self.assertIn(layer, present, f"missing layer package: {layer}")

    def test_package_imports_point_inward(self) -> None:
        violations = []
        for dotted, path in _modules():
            layer = _layer_of(dotted)
            if layer is None:
                continue
            for name in _imports(path):
                if not name.startswith(PACKAGE + "."):
                    continue
                target = _layer_of(name.removeprefix(PACKAGE + "."))
                if target is None or target == layer:
                    continue
                if target not in ALLOWED_INWARD[layer]:
                    violations.append(f"{dotted} -> {name}")
        self.assertEqual(violations, [])

    def test_frameworks_stay_inside_their_adapter(self) -> None:
        violations = []
        for dotted, path in _modules():
            for name in _imports(path):
                root = name.split(".")[0]
                home = FRAMEWORK_HOME.get(root)
                inside_home = dotted.startswith(home + ".") if home else True
                if not inside_home and dotted != "composition":
                    violations.append(f"{dotted} imports {root}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
