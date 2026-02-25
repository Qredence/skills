import argparse
import os
import textwrap


def init_skill(name, path):
    skill_dir = os.path.join(path, name)
    if os.path.exists(skill_dir):
        print(f"Error: Skill directory '{skill_dir}' already exists.")
        return False

    os.makedirs(skill_dir)
    os.makedirs(os.path.join(skill_dir, "scripts"))
    os.makedirs(os.path.join(skill_dir, "references"))
    os.makedirs(os.path.join(skill_dir, "assets"))

    skill_md_content = textwrap.dedent(f"""\
        ---
        name: {name}
        description: A brief description of the {name} skill.
        ---

        # {name}

        ## System Prompt
        Write the prompt instructions for your skill here.
        """)

    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(skill_md_content)

    print(f"Successfully initialized skill '{name}' in '{skill_dir}'")

    # Sync plugins to ensure the new skill is linked properly
    try:
        from sync_plugins import sync_fleet_skills

        sync_fleet_skills()
        print("Successfully synced plugins.")
    except Exception as e:
        print(f"Warning: Failed to sync plugins automatically: {e}")
        print("You may need to run 'uv run python scripts/sync_plugins.py' manually.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a new skill.")
    parser.add_argument("name", help="Name of the skill to create")
    parser.add_argument(
        "--path",
        default="skills/",
        help="Path where the skill directory will be created",
    )
    args = parser.parse_args()

    init_skill(args.name, args.path)
