"""Validate the public skills.sh catalogue without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
FIGMA_SKILLS_ROOT = SKILLS_ROOT / "figma-agent"
FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
NAME = re.compile(r"^name:\s*[\"']?(?P<name>[a-z0-9-]+)[\"']?\s*$", re.MULTILINE)
DESCRIPTION = re.compile(r"^description:\s*.+$", re.MULTILINE)
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate() -> list[str]:
    errors: list[str] = []
    if not FIGMA_SKILLS_ROOT.is_dir():
        return ["Missing active skills root: skills/figma-agent"]
    if (REPO_ROOT / "figma-agent").exists():
        errors.append("Legacy active skills root must not exist: figma-agent")

    skill_dirs = sorted(path for path in FIGMA_SKILLS_ROOT.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("No active skills found under skills/figma-agent")

    for skill_dir in skill_dirs:
        relative_dir = skill_dir.relative_to(REPO_ROOT)
        if not KEBAB.match(skill_dir.name):
            errors.append(f"Skill directory must be kebab-case: {relative_dir}")

        canonical = skill_dir / "SKILL.md"
        if not canonical.is_file():
            errors.append(f"Missing canonical document: {relative_dir}/SKILL.md")
            continue

        legacy_upload = skill_dir / "SKILLS.md"
        if legacy_upload.is_file():
            errors.append(
                f"Legacy Figma duplicate must not exist: {relative_dir}/SKILLS.md"
            )

        content = canonical.read_text(encoding="utf-8")
        match = FRONTMATTER.match(content)
        if not match:
            errors.append(f"Missing YAML frontmatter: {relative_dir}/SKILL.md")
            continue
        name_match = NAME.search(match.group("body"))
        if not name_match:
            errors.append(f"Missing frontmatter name: {relative_dir}/SKILL.md")
        elif name_match.group("name") != skill_dir.name:
            errors.append(
                f"Frontmatter name does not match directory: {relative_dir}/SKILL.md"
            )
        if not DESCRIPTION.search(match.group("body")):
            errors.append(f"Missing frontmatter description: {relative_dir}/SKILL.md")

    for archived_document in (REPO_ROOT / "archive").rglob("SKILL.md"):
        errors.append(
            "Archived documents must not be discoverable: "
            f"{archived_document.relative_to(REPO_ROOT)}"
        )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    count = len(list(FIGMA_SKILLS_ROOT.glob("*/SKILL.md")))
    print(f"Validated {count} active skills in skills/figma-agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
