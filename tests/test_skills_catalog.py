"""Catalogue integrity checks for the active Figma skills collection."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from init_skill import init_skill  # noqa: E402
from validate_skills import FIGMA_SKILLS_ROOT, validate  # noqa: E402


class SkillsCatalogTests(unittest.TestCase):
    def test_catalogue_validates(self) -> None:
        errors = validate()
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_every_skill_dir_has_skill_md_only(self) -> None:
        self.assertTrue(FIGMA_SKILLS_ROOT.is_dir(), msg=f"Active skills root directory '{FIGMA_SKILLS_ROOT}' does not exist.")
        skill_dirs = sorted(p for p in FIGMA_SKILLS_ROOT.iterdir() if p.is_dir())
        self.assertGreater(len(skill_dirs), 0)
        self.assertFalse((REPO_ROOT / "figma-agent").exists())
        for skill_dir in skill_dirs:
            self.assertTrue(
                (skill_dir / "SKILL.md").is_file(),
                msg=f"Missing SKILL.md in {skill_dir.name}",
            )
            self.assertFalse(
                (skill_dir / "SKILLS.md").exists(),
                msg=f"Legacy SKILLS.md must not exist in {skill_dir.name}",
            )

    def test_initializer_creates_skill_md_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory) / "skills" / "figma-agent"
            skill_root.mkdir(parents=True)

            self.assertEqual(init_skill("example-skill", skill_root), 0)

            skill_dir = skill_root / "example-skill"
            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertFalse((skill_dir / "SKILLS.md").exists())


if __name__ == "__main__":
    unittest.main()
