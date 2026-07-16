"""Initialize a new Figma agent skill directory."""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = REPO_ROOT / "skills" / "figma-agent"
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def init_skill(name: str, path: Path) -> int:
    if not KEBAB.match(name):
        print(
            f"Error: Skill name must be kebab-case (got '{name}').",
            file=sys.stderr,
        )
        return 1

    if path.exists() and not path.is_dir():
        print(f"Error: Path '{path}' is not a directory.", file=sys.stderr)
        return 1

    skill_dir = path / name
    if skill_dir.exists():
        print(f"Error: Skill directory '{skill_dir}' already exists.", file=sys.stderr)
        return 1

    skill_dir.mkdir(parents=True)
    skill_md_content = textwrap.dedent(f"""\
        ---
        name: {name}
        description: "A brief description of the {name} skill."
        ---

        # {name}

        ## Purpose
        Describe what this skill does and when to use it.

        ## Workflow
        1. Clarify scope from the current selection or user request.
        2. Apply the skill with concrete, evidence-backed steps.
        3. Report findings or deliverables clearly.
        """)

    (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
    print(f"Successfully initialized skill '{name}' in '{skill_dir}'")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Kebab-case name of the skill to create")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_SKILLS_ROOT,
        help=f"Directory for the new skill (default: {DEFAULT_SKILLS_ROOT})",
    )
    args = parser.parse_args()
    return init_skill(args.name, args.path.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
