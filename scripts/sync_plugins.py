"""Sync skill packages into plugins/ for ecosystem packaging.

Currently plugins/ is a reserved packaging slot and does not contain a
fleet-skills (or similar) package. This script is a safe no-op until a real
plugin layout is reintroduced.
"""

from pathlib import Path


def sync_fleet_skills() -> None:
    """Sync skills into plugins/ when a plugin package exists."""
    repo_root = Path(__file__).resolve().parent.parent
    plugins_dir = repo_root / "plugins"
    fleet_dir = plugins_dir / "fleet-skills" / "skills"

    if not fleet_dir.exists():
        print(
            "No plugins/fleet-skills package found — nothing to sync.\n"
            "Active skills live under figma-agent/ at the repository root.\n"
            "plugins/ is reserved for future ecosystem packaging."
        )
        return

    # Future: symlink package skills into fleet-skills when that layout returns.
    print(f"Plugin package present at {fleet_dir}; manual packaging required for now.")


if __name__ == "__main__":
    sync_fleet_skills()
    print("Plugin sync completed.")
