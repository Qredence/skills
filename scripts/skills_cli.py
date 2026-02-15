#!/usr/bin/env python3
"""
CLI tool for managing the skills registry
"""
import argparse
import sys
from pathlib import Path

from skills.registry.catalog import SkillRegistry
from skills.validation.validator import validate_skill_directory
from skills.template.generator import SkillTemplate


def generate_catalog(args):
    """Generate skills catalog"""
    skills_dir = Path(args.skills_dir)
    output_path = Path(args.output)
    
    registry = SkillRegistry(skills_dir)
    skills = registry.discover_skills()
    
    print(f"Discovered {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill.name} (v{skill.version})")
    
    registry.generate_catalog(output_path)
    print(f"\nCatalog generated: {output_path}")


def validate_skills(args):
    """Validate all skills"""
    skills_dir = Path(args.skills_dir)
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        sys.exit(1)
    
    all_valid = True
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        
        # Skip non-skill directories
        if skill_dir.name.startswith('_') or skill_dir.name in ['core', 'registry', 'validation', 'template']:
            continue
        
        is_valid, errors = validate_skill_directory(skill_dir)
        
        if is_valid:
            print(f"✓ {skill_dir.name}")
        else:
            print(f"✗ {skill_dir.name}")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
    
    if not all_valid:
        sys.exit(1)


def create_skill(args):
    """Create a new skill from template"""
    skill_name = args.name
    skills_dir = Path(args.skills_dir)
    
    print(f"Creating skill: {skill_name}")
    
    skill_dir = SkillTemplate.generate(
        skill_name=skill_name,
        output_dir=skills_dir,
        description=args.description or "A new skill",
        author=args.author or "Qredence",
        tags=args.tags or []
    )
    
    print(f"✓ Skill created: {skill_dir}")
    print(f"  - Edit {skill_dir}/skill.yaml to customize metadata")
    print(f"  - Edit {skill_dir}/__init__.py to implement skill logic")
    print(f"  - Edit tests/skills/test_{skill_name}.py to add tests")


def main():
    parser = argparse.ArgumentParser(
        description="Qredence Skills Registry Management"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Catalog generation command
    catalog_parser = subparsers.add_parser('catalog', help='Generate skills catalog')
    catalog_parser.add_argument(
        '--skills-dir',
        default='skills',
        help='Directory containing skills'
    )
    catalog_parser.add_argument(
        '--output',
        default='catalog/skills.json',
        help='Output path for catalog'
    )
    catalog_parser.set_defaults(func=generate_catalog)
    
    # Validation command
    validate_parser = subparsers.add_parser('validate', help='Validate all skills')
    validate_parser.add_argument(
        '--skills-dir',
        default='skills',
        help='Directory containing skills'
    )
    validate_parser.set_defaults(func=validate_skills)
    
    # Create skill command
    create_parser = subparsers.add_parser('create', help='Create a new skill from template')
    create_parser.add_argument('name', help='Skill name (snake_case)')
    create_parser.add_argument('--skills-dir', default='skills', help='Skills directory')
    create_parser.add_argument('--description', help='Skill description')
    create_parser.add_argument('--author', help='Skill author')
    create_parser.add_argument('--tags', nargs='*', help='Skill tags')
    create_parser.set_defaults(func=create_skill)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
