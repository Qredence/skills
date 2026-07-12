"""Keep Figma upload documents synchronized with canonical skill documents."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIGMA_SKILLS_ROOT = REPO_ROOT / "skills" / "figma-agent"


def iter_skill_directories() -> list[Path]:
    if not FIGMA_SKILLS_ROOT.is_dir():
        return []
    return sorted(path for path in FIGMA_SKILLS_ROOT.iterdir() if path.is_dir())


def synchronize(*, check: bool) -> int:
    errors: list[str] = []
    changed = 0

    for skill_dir in iter_skill_directories():
        canonical = skill_dir / "SKILL.md"
        figma_upload = skill_dir / "SKILLS.md"
        if not canonical.is_file():
            errors.append(
                f"Missing canonical document: {canonical.relative_to(REPO_ROOT)}"
            )
            continue

        expected = canonical.read_bytes()
        if figma_upload.is_file() and figma_upload.read_bytes() == expected:
            continue

        if check:
            errors.append(
                f"Out-of-sync Figma document: {figma_upload.relative_to(REPO_ROOT)}"
            )
            continue

        figma_upload.write_bytes(expected)
        changed += 1

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    action = "Checked" if check else "Synchronized"
    print(
        f"{action} {len(iter_skill_directories())} Figma skill documents ({changed} changed)."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when SKILLS.md does not match the canonical SKILL.md.",
    )
    args = parser.parse_args()
    return synchronize(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
