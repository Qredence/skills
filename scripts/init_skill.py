import argparse
import textwrap
from pathlib import Path


def init_skill(name: str, path: str) -> bool:
    skill_dir = Path(path) / name
    if skill_dir.exists():
        print(f"Error: Skill directory '{skill_dir}' already exists.")
        return False

    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "assets").mkdir()

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

    canonical_document = skill_dir / "SKILL.md"
    canonical_document.write_text(skill_md_content, encoding="utf-8")

    path_norm = Path(path).as_posix().rstrip("/")
    if path_norm == "skills/figma-agent" or path_norm.endswith("/skills/figma-agent"):
        (skill_dir / "SKILLS.md").write_text(skill_md_content, encoding="utf-8")

    print(f"Successfully initialized skill '{name}' in '{skill_dir}'")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a new skill.")
    parser.add_argument("name", help="Name of the skill to create")
    parser.add_argument(
        "--path",
        default="skills/figma-agent/",
        help="Path where the skill directory will be created (default: skills/figma-agent/)",
    )
    args = parser.parse_args()

    init_skill(args.name, args.path)
