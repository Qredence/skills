#!/usr/bin/env python3
"""
Example usage of Qredence Skills Registry

This demonstrates how to:
1. Load and use individual skills
2. Access skill metadata
3. Validate inputs
4. Use the registry to discover skills
"""

from pathlib import Path

# Import individual skills
from skills.web_summarizer import WebSummarizer
from skills.doc_transformer import DocTransformer
from skills.task_planner import TaskPlanner

# Import registry components
from skills.registry.catalog import SkillRegistry


def demonstrate_web_summarizer():
    """Demonstrate web summarizer skill"""
    print("=" * 60)
    print("Web Summarizer Skill Demo")
    print("=" * 60)
    
    skill = WebSummarizer()
    
    # Print metadata
    print(f"Name: {skill.metadata.name}")
    print(f"Version: {skill.metadata.version}")
    print(f"Description: {skill.metadata.description}")
    print(f"Author: {skill.metadata.author}")
    print(f"Tags: {', '.join(skill.metadata.tags)}")
    
    # Check safety permissions
    print(f"\nSafety Permissions:")
    print(f"  Internet Access: {skill.metadata.safety_permissions.internet_access}")
    print(f"  External API Calls: {skill.metadata.safety_permissions.external_api_calls}")
    
    # Validate input
    valid_input = {"url": "https://example.com", "max_length": 150}
    print(f"\nValidating input: {valid_input}")
    print(f"Valid: {skill.validate_input(valid_input)}")
    
    print()


def demonstrate_doc_transformer():
    """Demonstrate document transformer skill"""
    print("=" * 60)
    print("Document Transformer Skill Demo")
    print("=" * 60)
    
    skill = DocTransformer()
    
    print(f"Name: {skill.metadata.name}")
    print(f"Description: {skill.metadata.description}")
    print(f"Tags: {', '.join(skill.metadata.tags)}")
    
    # Show input schema
    print(f"\nInput Schema:")
    print(f"  Name: {skill.metadata.input_schema.name}")
    required = skill.metadata.input_schema.schema_.get("required", [])
    print(f"  Required Fields: {', '.join(required)}")
    
    # Validate inputs
    valid_input = {
        "document": "Sample text",
        "source_format": "plain",
        "target_format": "markdown"
    }
    print(f"\nValidating input: {valid_input}")
    print(f"Valid: {skill.validate_input(valid_input)}")
    
    print()


def demonstrate_task_planner():
    """Demonstrate task planner skill"""
    print("=" * 60)
    print("Task Planner Skill Demo")
    print("=" * 60)
    
    skill = TaskPlanner()
    
    print(f"Name: {skill.metadata.name}")
    print(f"Description: {skill.metadata.description}")
    print(f"Tags: {', '.join(skill.metadata.tags)}")
    
    # Show output schema
    print(f"\nOutput Schema:")
    print(f"  Name: {skill.metadata.output_schema.name}")
    required = skill.metadata.output_schema.schema_.get("required", [])
    print(f"  Required Fields: {', '.join(required)}")
    
    # Validate input
    valid_input = {"goal": "Build a web application"}
    print(f"\nValidating input: {valid_input}")
    print(f"Valid: {skill.validate_input(valid_input)}")
    
    print()


def demonstrate_registry():
    """Demonstrate skill registry"""
    print("=" * 60)
    print("Skill Registry Demo")
    print("=" * 60)
    
    skills_dir = Path(__file__).parent.parent / "skills"
    registry = SkillRegistry(skills_dir)
    
    # Discover all skills
    skills = registry.discover_skills()
    print(f"Discovered {len(skills)} skills:\n")
    
    for skill_metadata in skills:
        print(f"  • {skill_metadata.name} v{skill_metadata.version}")
        print(f"    {skill_metadata.description}")
        print(f"    Author: {skill_metadata.author}")
        print(f"    Tags: {', '.join(skill_metadata.tags)}")
        print()
    
    # Validate all skills
    print("Validation Results:")
    validation_results = registry.validate_all_skills()
    for skill_name, errors in validation_results.items():
        if errors:
            print(f"  ✗ {skill_name}: {len(errors)} errors")
            for error in errors:
                print(f"    - {error}")
        else:
            print(f"  ✓ {skill_name}")
    
    print()


def main():
    """Main demo function"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Qredence Skills Registry Demo" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    demonstrate_web_summarizer()
    demonstrate_doc_transformer()
    demonstrate_task_planner()
    demonstrate_registry()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Create your own skill: python scripts/skills_cli.py create my_skill")
    print("  2. Run tests: pytest tests/")
    print("  3. Generate catalog: python scripts/skills_cli.py catalog")
    print()


if __name__ == "__main__":
    main()
