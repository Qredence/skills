#!/usr/bin/env python3
"""
Scaffold a new skill from templates

Creates a complete skill structure with all required files.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "packages" / "skills_core"))


def create_skill_yaml(skill_id: str, name: str, description: str, tags: list, **kwargs) -> str:
    """Generate skill.yaml content"""
    tags_yaml = '\n'.join(f'  - {tag}' for tag in tags)
    
    template = f'''id: {skill_id}
name: "{name}"
version: "0.1.0"
description: "{description}"
tags:
{tags_yaml}

dspy:
  module: "skills.{skill_id}.src.skill:Skill"
  signatures:
    - "skills.{skill_id}.src.skill:SkillSignature"
  dependencies:
    - "dspy-ai>=2.5.0"

io:
  inputs_schema:
    type: "object"
    properties:
      input_text:
        type: "string"
        description: "Input text to process"
    required:
      - input_text
  
  outputs_schema:
    type: "object"
    properties:
      output_text:
        type: "string"
        description: "Processed output"
    required:
      - output_text

behavior:
  deterministic: false
  temperature_hint: 0.0
  notes:
    - "Replace with actual behavioral notes"

permissions:
  network: false
  filesystem_read: false
  filesystem_write: false
  external_tools: []

safety:
  level: "low"
  risks:
    - "No known risks for pure computation"
  mitigations:
    - "No mitigations needed"
  data_policy:
    - "No data persistence"
    - "No PII handling"

eval:
  golden_set: "eval/golden.jsonl"
  metrics:
    - "json_schema_valid"
'''
    
    if kwargs.get('owner'):
        template += f'\nowner: "{kwargs["owner"]}"'
    
    return template


def create_skill_py(skill_id: str, name: str) -> str:
    """Generate src/skill.py content"""
    class_name = ''.join(word.capitalize() for word in skill_id.split('_'))
    
    return f'''"""
{name} - DSPy skill implementation
"""
import dspy
from typing import Any


class SkillSignature(dspy.Signature):
    """DSPy signature for {name}"""
    
    input_text: str = dspy.InputField(desc="Input text to process")
    output_text: str = dspy.OutputField(desc="Processed output text")


class Skill(dspy.Module):
    """
    {name}
    
    Main DSPy Module implementing the skill logic.
    """
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(SkillSignature)
    
    def forward(self, input_text: str) -> dspy.Prediction:
        """
        Execute the skill
        
        Args:
            input_text: Input text to process
            
        Returns:
            DSPy prediction with output_text
        """
        return self.prog(input_text=input_text)


def run(**kwargs) -> Any:
    """
    Convenience function to run the skill
    
    Args:
        **kwargs: Skill inputs
        
    Returns:
        Skill outputs
    """
    skill = Skill()
    return skill.forward(**kwargs)


# Export required objects
SIGNATURES = [SkillSignature]
__all__ = ['Skill', 'SkillSignature', 'run', 'SIGNATURES']
'''


def create_test_contract(skill_id: str) -> str:
    """Generate tests/test_contract.py content"""
    return f'''"""
Contract tests for {skill_id}

Validates that the skill implements the required DSPy contract.
"""
import pytest
from pathlib import Path
import sys

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from skills.{skill_id}.src.skill import Skill, SkillSignature, SIGNATURES
import dspy


def test_skill_class_exists():
    """Verify Skill class is defined"""
    assert Skill is not None
    assert issubclass(Skill, dspy.Module)


def test_signature_exists():
    """Verify Signature class is defined"""
    assert SkillSignature is not None
    assert issubclass(SkillSignature, dspy.Signature)


def test_signatures_export():
    """Verify SIGNATURES list is exported"""
    assert SIGNATURES is not None
    assert len(SIGNATURES) > 0
    assert SkillSignature in SIGNATURES


def test_skill_instantiation():
    """Verify skill can be instantiated"""
    skill = Skill()
    assert skill is not None


def test_skill_has_forward():
    """Verify skill has forward method"""
    skill = Skill()
    assert hasattr(skill, 'forward')
    assert callable(skill.forward)


# Add functional tests below
def test_skill_basic_execution():
    """Test basic skill execution"""
    # TODO: Add actual execution test
    pass
'''


def create_golden_jsonl(skill_id: str) -> str:
    """Generate eval/golden.jsonl content"""
    return '''{"name": "example_1", "input": {"input_text": "test input"}, "expected": {"type": "object", "properties": {"output_text": {"type": "string"}}, "required": ["output_text"]}, "match": "json_schema_valid"}
{"name": "example_2", "input": {"input_text": "another test"}, "expected": {"type": "object", "properties": {"output_text": {"type": "string"}}, "required": ["output_text"]}, "match": "json_schema_valid"}
'''


def create_minimal_example(skill_id: str, name: str) -> str:
    """Generate examples/minimal.py content"""
    return f'''#!/usr/bin/env python3
"""
Minimal example of using {name}
"""
import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from skills.{skill_id}.src.skill import run


def main():
    print("=" * 60)
    print(f"{{name}} Example")
    print("=" * 60)
    print()
    
    # Example usage
    result = run(input_text="Hello, world!")
    
    print(f"Input: Hello, world!")
    print(f"Output: {{result.output_text}}")
    print()


if __name__ == "__main__":
    main()
'''


def create_readme(skill_id: str, name: str, description: str) -> str:
    """Generate README.md content"""
    return f'''# {name}

{description}

## Usage

```python
from skills.{skill_id}.src.skill import run

result = run(input_text="your input here")
print(result.output_text)
```

## Inputs

- `input_text` (string): Input text to process

## Outputs

- `output_text` (string): Processed output

## Safety

**Level**: Low
**Permissions**: None
**Risks**: No known risks

## Evaluation

See `eval/golden.jsonl` for evaluation examples.

## Development

```bash
# Run tests
pytest skills/{skill_id}/tests/

# Run example
python skills/{skill_id}/examples/minimal.py
```
'''


def scaffold_skill(
    skill_id: str,
    name: str,
    description: str,
    tags: list,
    output_dir: Path,
    **kwargs
) -> Path:
    """
    Create a new skill scaffold
    
    Args:
        skill_id: Skill ID (kebab_case)
        name: Human-readable name
        description: Short description
        tags: List of tags
        output_dir: Skills directory
        **kwargs: Additional options (owner, etc.)
        
    Returns:
        Path to created skill directory
    """
    skill_dir = output_dir / skill_id
    
    if skill_dir.exists():
        raise ValueError(f"Skill directory already exists: {skill_dir}")
    
    # Create directory structure
    skill_dir.mkdir(parents=True)
    (skill_dir / "src").mkdir()
    (skill_dir / "tests").mkdir()
    (skill_dir / "eval").mkdir()
    (skill_dir / "examples").mkdir()
    
    # Create files
    (skill_dir / "skill.yaml").write_text(
        create_skill_yaml(skill_id, name, description, tags, **kwargs)
    )
    
    (skill_dir / "src" / "skill.py").write_text(
        create_skill_py(skill_id, name)
    )
    
    (skill_dir / "src" / "__init__.py").write_text(
        f'"""Skill: {name}"""\n'
    )
    
    (skill_dir / "tests" / "__init__.py").write_text(
        f'"""Tests for {skill_id}"""\n'
    )
    
    (skill_dir / "tests" / "test_contract.py").write_text(
        create_test_contract(skill_id)
    )
    
    (skill_dir / "eval" / "golden.jsonl").write_text(
        create_golden_jsonl(skill_id)
    )
    
    (skill_dir / "examples" / "minimal.py").write_text(
        create_minimal_example(skill_id, name)
    )
    
    (skill_dir / "README.md").write_text(
        create_readme(skill_id, name, description)
    )
    
    return skill_dir


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create a new DSPy skill from template"
    )
    parser.add_argument(
        "skill_id",
        help="Skill ID in snake_case (e.g., my_new_skill)"
    )
    parser.add_argument(
        "--name",
        help="Human-readable name (defaults to title case of ID)"
    )
    parser.add_argument(
        "--description",
        required=True,
        help="Short description (1-2 sentences)"
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        required=True,
        help="Tags for the skill"
    )
    parser.add_argument(
        "--owner",
        help="Skill owner/maintainer"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("skills"),
        help="Output directory for skills"
    )
    
    args = parser.parse_args()
    
    # Generate name if not provided
    name = args.name or ' '.join(word.capitalize() for word in args.skill_id.split('_'))
    
    print(f"Creating skill: {args.skill_id}")
    print(f"Name: {name}")
    print(f"Description: {args.description}")
    print(f"Tags: {', '.join(args.tags)}")
    print()
    
    try:
        skill_dir = scaffold_skill(
            args.skill_id,
            name,
            args.description,
            args.tags,
            args.output_dir,
            owner=args.owner
        )
        
        print(f"✅ Skill created: {skill_dir}")
        print()
        print("Next steps:")
        print(f"  1. Edit {skill_dir}/skill.yaml to customize metadata")
        print(f"  2. Implement logic in {skill_dir}/src/skill.py")
        print(f"  3. Add tests in {skill_dir}/tests/")
        print(f"  4. Add golden examples in {skill_dir}/eval/golden.jsonl")
        print(f"  5. Run: python tools/validate.py")
        print()
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
