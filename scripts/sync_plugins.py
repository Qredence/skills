import os
import sys
from pathlib import Path

def sync_qredence_skills():
    """
    Ensures that every skill in the root 'skills/' directory has a corresponding 
    symlink in 'plugins/qredence-skills/skills/'. Also removes dead/orphaned symlinks.
    """
    repo_root = Path(__file__).resolve().parent.parent
    source_skills_dir = repo_root / "skills"
    plugin_skills_dir = repo_root / "plugins" / "qredence-skills" / "skills"

    if not source_skills_dir.exists():
        print(f"Error: Source skills directory '{source_skills_dir}' does not exist.")
        sys.exit(1)

    # Ensure the target directory exists
    plugin_skills_dir.mkdir(parents=True, exist_ok=True)

    # 1. Identify all valid skills in the root
    valid_skills = set()
    for item in source_skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            valid_skills.add(item.name)

    # 2. Sync / Create symlinks in the plugin directory
    for skill_name in valid_skills:
        target_link = plugin_skills_dir / skill_name
        # The target needs to point from `plugins/qredence-skills/skills/<skill>` to `../../../skills/<skill>`
        # Relative path from target link location to the actual skill directory
        relative_target = Path("..") / ".." / ".." / "skills" / skill_name
        
        if target_link.exists() or target_link.is_symlink():
            if target_link.is_symlink():
                # Check if it points to the correct location
                if os.readlink(target_link) != str(relative_target):
                    target_link.unlink()
                    target_link.symlink_to(relative_target)
                    print(f"Updated symlink for '{skill_name}'")
            else:
                print(f"Warning: '{target_link}' exists but is not a symlink. Skipping.")
        else:
            target_link.symlink_to(relative_target)
            print(f"Created symlink for '{skill_name}'")

    # 3. Clean up orphaned symlinks in the plugin directory
    for item in plugin_skills_dir.iterdir():
        if item.is_symlink() and item.name not in valid_skills:
            print(f"Removing orphaned symlink: '{item.name}'")
            item.unlink()

if __name__ == "__main__":
    sync_qredence_skills()
    print("Plugin sync completed successfully.")
