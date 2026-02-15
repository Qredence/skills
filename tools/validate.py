#!/usr/bin/env python3
"""
Validate all skills and regenerate catalog deterministically

This tool:
1. Discovers all skills in skills/ directory
2. Validates each against catalog/schema.skill.json
3. Checks directory structure and required files
4. Regenerates catalog/skills.json deterministically
5. Fails if regenerated catalog differs from committed version
"""
import sys
import json
from pathlib import Path

# Add parent to path to import skills_core
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "packages" / "skills_core"))

from skills_core import (
    discover_skills,
    validate_all_skills,
    generate_catalog,
    load_catalog,
    compare_catalogs,
)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate skills and regenerate catalog"
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("skills"),
        help="Path to skills directory"
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("catalog/schema.skill.json"),
        help="Path to skill schema"
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("catalog/skills.json"),
        help="Path to catalog output"
    )
    parser.add_argument(
        "--check-imports",
        action="store_true",
        help="Validate DSPy imports (slower)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all skills"
    )
    parser.add_argument(
        "--info",
        type=str,
        help="Show detailed info for a skill"
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Filter by tag (with --list)"
    )
    
    args = parser.parse_args()
    
    # Make paths absolute
    skills_dir = args.skills_dir.resolve()
    schema_path = args.schema.resolve()
    catalog_path = args.catalog.resolve()
    
    # Handle --list command
    if args.list:
        list_skills(skills_dir, args.tag)
        return 0
    
    # Handle --info command
    if args.info:
        show_skill_info(skills_dir, args.info)
        return 0
    
    print("=" * 60)
    print("Qredence Skills Validation")
    print("=" * 60)
    print()
    
    # Discover skills
    print(f"📂 Discovering skills in {skills_dir}...")
    try:
        skills = discover_skills(skills_dir)
        print(f"   Found {len(skills)} skills\n")
    except Exception as e:
        print(f"   ✗ Discovery failed: {e}")
        return 1
    
    # Validate all skills
    print(f"🔍 Validating skills against schema...")
    results = validate_all_skills(skills_dir, schema_path, args.check_imports)
    
    all_valid = True
    for skill_id, errors in sorted(results.items()):
        if errors:
            print(f"   ✗ {skill_id}")
            for error in errors:
                print(f"      - {error}")
            all_valid = False
        else:
            print(f"   ✓ {skill_id}")
    
    print()
    
    if not all_valid:
        print("❌ Validation failed\n")
        return 1
    
    print("✅ All skills valid\n")
    
    # Generate catalog
    print(f"📋 Generating catalog...")
    try:
        # Save to temporary file first
        temp_catalog_path = catalog_path.parent / ".skills.json.tmp"
        new_catalog = generate_catalog(skills_dir, temp_catalog_path)
        print(f"   Generated catalog with {len(new_catalog.skills)} skills\n")
    except Exception as e:
        print(f"   ✗ Catalog generation failed: {e}\n")
        return 1
    
    # Compare with existing catalog
    print(f"🔄 Checking for catalog changes...")
    
    if catalog_path.exists():
        try:
            existing_catalog = load_catalog(catalog_path)
            catalogs_match = compare_catalogs(existing_catalog, new_catalog)
            
            if catalogs_match:
                print(f"   ✓ Catalog is up to date")
                # Replace with new catalog (updates timestamp)
                temp_catalog_path.rename(catalog_path)
            else:
                print(f"   ✗ Catalog has changed!")
                print(f"   The committed catalog differs from the generated one.")
                print(f"   Please regenerate and commit the updated catalog:")
                print(f"   $ python tools/validate.py")
                
                # Show what changed
                print(f"\n   Generated catalog saved to: {temp_catalog_path}")
                print(f"   Review changes and commit if correct.")
                
                return 1
        except Exception as e:
            print(f"   ⚠ Could not compare catalogs: {e}")
            print(f"   Using newly generated catalog.")
            temp_catalog_path.rename(catalog_path)
    else:
        print(f"   ✓ Created new catalog")
        temp_catalog_path.rename(catalog_path)
    
    print()
    print("=" * 60)
    print("✅ Validation Complete")
    print("=" * 60)
    
    return 0


def list_skills(skills_dir: Path, tag_filter: str = None):
    """List all skills with optional tag filtering"""
    skills = discover_skills(skills_dir)
    
    if tag_filter:
        skills = [s for s in skills if tag_filter in s.tags]
    
    print(f"Skills ({len(skills)}):\n")
    
    for skill in skills:
        print(f"  • {skill.id} (v{skill.version}) - {skill.safety.level}")
        print(f"    {skill.description}")
        print(f"    Tags: {', '.join(skill.tags)}")
        print()


def show_skill_info(skills_dir: Path, skill_id: str):
    """Show detailed information about a skill"""
    from skills_core import get_skill_by_id
    
    skill = get_skill_by_id(skills_dir, skill_id)
    
    if not skill:
        print(f"Skill not found: {skill_id}")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Skill: {skill.name}")
    print(f"{'=' * 60}\n")
    
    print(f"ID: {skill.id}")
    print(f"Version: {skill.version}")
    print(f"Description: {skill.description}")
    print(f"Author: {skill.owner or 'N/A'}")
    print(f"\nTags: {', '.join(skill.tags)}")
    
    print(f"\nSafety:")
    print(f"  Level: {skill.safety.level.value}")
    print(f"  Risks: {', '.join(skill.safety.risks) if skill.safety.risks else 'None'}")
    
    print(f"\nPermissions:")
    print(f"  Network: {skill.permissions.network}")
    print(f"  Filesystem Read: {skill.permissions.filesystem_read}")
    print(f"  Filesystem Write: {skill.permissions.filesystem_write}")
    print(f"  External Tools: {', '.join(skill.permissions.external_tools) if skill.permissions.external_tools else 'None'}")
    
    print(f"\nBehavior:")
    print(f"  Deterministic: {skill.behavior.deterministic}")
    print(f"  Temperature: {skill.behavior.temperature_hint}")
    
    print(f"\nDSPy:")
    print(f"  Module: {skill.dspy.module}")
    print(f"  Signatures: {len(skill.dspy.signatures)}")
    for sig in skill.dspy.signatures:
        print(f"    - {sig}")
    
    print()


if __name__ == "__main__":
    sys.exit(main())
