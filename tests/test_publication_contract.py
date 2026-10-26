from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PublicationContractTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_english_materials_preserve_no_go_and_safety_boundary(self) -> None:
        for path in ("docs/video-script-en.md", "docs/linkedin-post-en.md"):
            content = self._read(path).lower()
            self.assertIn("synthetic", content)
            self.assertRegex(content, r"10[.]80")
            self.assertRegex(content, r"limit (was|at|of) 10|limit was declared at 10")
            self.assertTrue("rejected" in content or "no-go" in content)
            self.assertTrue("no external action" in content or "no booking" in content)

    def test_portuguese_materials_preserve_no_go_and_safety_boundary(self) -> None:
        for path in ("docs/video-script-pt.md", "docs/linkedin-post-pt.md"):
            content = self._read(path).lower()
            normalized = " ".join(content.split())
            self.assertIn("sintétic", content)
            self.assertRegex(content, r"10,80")
            self.assertRegex(normalized, r"limite .{0,45}10")
            self.assertTrue("rejeit" in content or "no-go" in content)
            self.assertTrue("nenhuma ação externa" in content or "não agenda" in content)

    def test_video_scripts_use_the_same_observed_numbers(self) -> None:
        english = self._read("docs/video-script-en.md")
        portuguese = self._read("docs/video-script-pt.md")

        english_numbers = set(re.findall(r"\b(?:40|60|120|10[.]80)\b", english))
        portuguese_numbers = set(
            value.replace(",", ".")
            for value in re.findall(r"\b(?:40|60|120|10,80)\b", portuguese)
        )
        self.assertEqual(english_numbers, portuguese_numbers)

    def test_readme_relative_markdown_links_resolve(self) -> None:
        readme = self._read("README.md")
        relative_targets = [
            target
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", readme)
            if "://" not in target and not target.startswith("#")
        ]

        self.assertTrue(relative_targets)
        for target in relative_targets:
            self.assertTrue((ROOT / target).exists(), target)


if __name__ == "__main__":
    unittest.main()
