"""Structural checks for the public skills catalogue."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from init_skill import init_skill  # noqa: E402


class SkillsCatalogTests(unittest.TestCase):
    def test_active_figma_skills_are_published_from_standard_root(self) -> None:
        active_skills = sorted((REPO_ROOT / "skills" / "figma-agent").glob("*/SKILL.md"))

        self.assertEqual(len(active_skills), 55)
        self.assertFalse((REPO_ROOT / "figma-agent").exists())

    def test_validator_accepts_the_catalogue(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_skills.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_initializer_creates_matching_canonical_and_figma_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory) / "skills" / "figma-agent"
            skill_root.mkdir(parents=True)

            self.assertTrue(init_skill("example-skill", str(skill_root)))

            skill_dir = skill_root / "example-skill"
            self.assertEqual(
                (skill_dir / "SKILL.md").read_bytes(),
                (skill_dir / "SKILLS.md").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
