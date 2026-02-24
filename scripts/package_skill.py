import argparse
import os
import zipfile


def parse_frontmatter(content):
    if not content.startswith("---"):
        return None

    end_idx = content.find("---", 3)
    if end_idx == -1:
        return None

    frontmatter_text = content[3:end_idx].strip()
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            frontmatter[key.strip()] = val.strip()
    return frontmatter


def package_skill(skill_path):
    if not os.path.exists(skill_path) or not os.path.isdir(skill_path):
        print(f"Error: Skill path '{skill_path}' does not exist or is not a directory.")
        return False

    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        print(f"Error: SKILL.md not found in '{skill_path}'.")
        return False

    with open(skill_md_path, "r") as f:
        content = f.read()

    frontmatter = parse_frontmatter(content)
    if not frontmatter:
        print(f"Error: Invalid or missing YAML frontmatter in '{skill_md_path}'.")
        return False

    if "name" not in frontmatter:
        print("Error: Missing 'name' in YAML frontmatter.")
        return False

    if "description" not in frontmatter:
        print("Error: Missing 'description' in YAML frontmatter.")
        return False

    skill_name = os.path.basename(os.path.normpath(skill_path))
    output_filename = f"{skill_name}.skill"

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(skill_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_path)
                zipf.write(file_path, arcname)

    print(f"Successfully packaged skill to '{output_filename}'")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Package a skill into a .skill zip archive."
    )
    parser.add_argument("path", help="Path to the skill directory")
    args = parser.parse_args()

    package_skill(args.path)
