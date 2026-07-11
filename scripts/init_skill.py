import argparse
import os
import textwrap
from pathlib import Path


def init_skill(name: str, path: str) -> bool:
    skill_dir = os.path.join(path, name)
    if os.path.exists(skill_dir):
        print(f"Error: Skill directory '{skill_dir}' already exists.")
        return False

    os.makedirs(skill_dir)
    os.makedirs(os.path.join(skill_dir, "scripts"))
    os.makedirs(os.path.join(skill_dir, "references"))
    os.makedirs(os.path.join(skill_dir, "assets"))

    # Figma Design Agent packages use SKILLS.md; everything else uses SKILL.md.
    path_norm = Path(path).as_posix().rstrip("/")
    use_figma_doc = path_norm == "figma-agent" or path_norm.endswith("/figma-agent")
    doc_name = "SKILLS.md" if use_figma_doc else "SKILL.md"

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

    doc_path = os.path.join(skill_dir, doc_name)
    with open(doc_path, "w") as f:
        f.write(skill_md_content)

    print(f"Successfully initialized skill '{name}' in '{skill_dir}' ({doc_name})")

    # Best-effort plugin sync (no-op when plugins/ has no package).
    try:
        from sync_plugins import sync_fleet_skills

        sync_fleet_skills()
    except Exception as e:
        print(f"Warning: Plugin sync skipped: {e}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a new skill.")
    parser.add_argument("name", help="Name of the skill to create")
    parser.add_argument(
        "--path",
        default="figma-agent/",
        help="Path where the skill directory will be created (default: figma-agent/)",
    )
    args = parser.parse_args()

    init_skill(args.name, args.path)
