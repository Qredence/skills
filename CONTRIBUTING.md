# Contributing to Qredence Skills

Thank you for your interest in contributing to the Qredence Skills Registry! This guide will help you create high-quality skills that follow our standards.

## Quick Start

1. **Fork and clone** the repository
2. **Install dependencies**: `pip install -r requirements.txt && pip install -e .`
3. **Create a new skill**: `python scripts/skills_cli.py create your_skill_name`
4. **Implement your skill** in the generated files
5. **Write tests** for your skill
6. **Run validation**: `python scripts/skills_cli.py validate`
7. **Submit a pull request**

## Creating a New Skill

### Using the Template Generator

The easiest way to create a new skill is using our template generator:

```bash
python scripts/skills_cli.py create my_skill \
    --description "A brief description of what the skill does" \
    --author "Your Name" \
    --tags tag1 tag2 tag3
```

This creates:
- `skills/my_skill/skill.yaml` - Metadata configuration
- `skills/my_skill/__init__.py` - Skill implementation
- `skills/my_skill/golden_eval.py` - Golden evaluation examples
- `tests/skills/test_my_skill.py` - Unit tests

### Manual Skill Creation

If you prefer to create a skill manually, follow this structure:

#### 1. Create Directory Structure

```
skills/
  your_skill/
    skill.yaml
    __init__.py
    golden_eval.py
tests/
  skills/
    test_your_skill.py
```

#### 2. Define Metadata (skill.yaml)

```yaml
name: your_skill
version: "0.1.0"
description: "Brief description of your skill"
author: "Your Name"
tags:
  - relevant
  - tags

module_class: "YourSkillModule"
signature_class: "YourSkillSignature"

input_schema:
  name: "YourSkillInput"
  description: "Input schema description"
  schema:
    type: "object"
    properties:
      input_field:
        type: "string"
        description: "Field description"
    required:
      - input_field

output_schema:
  name: "YourSkillOutput"
  description: "Output schema description"
  schema:
    type: "object"
    properties:
      output_field:
        type: "string"
        description: "Field description"
    required:
      - output_field

safety_permissions:
  internet_access: false
  file_system_read: false
  file_system_write: false
  external_api_calls: false
  data_persistence: false
  user_interaction: false
  sensitive_data: false

has_tests: true
has_golden_evals: true
```

#### 3. Implement the Skill

```python
# skills/your_skill/__init__.py
from typing import Type
from pathlib import Path
import dspy
from skills.core.base import Skill

class YourSkillSignature(dspy.Signature):
    """DSPy signature for your skill"""
    input_field: str = dspy.InputField(desc="Input description")
    output_field: str = dspy.OutputField(desc="Output description")

class YourSkillModule(dspy.Module):
    """DSPy module for your skill"""
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(YourSkillSignature)
    
    def forward(self, input_field: str) -> dspy.Prediction:
        return self.prog(input_field=input_field)

class YourSkill(Skill):
    """Your skill description"""
    
    def __init__(self, metadata_path: Path = None):
        if metadata_path is None:
            metadata_path = Path(__file__).parent / "skill.yaml"
        super().__init__(metadata_path)
        self._module = YourSkillModule()
        self._signature = YourSkillSignature
    
    def get_module(self) -> dspy.Module:
        return self._module
    
    def get_signature(self) -> Type[dspy.Signature]:
        return self._signature
```

#### 4. Add Golden Evaluations

```python
# skills/your_skill/golden_eval.py
GOLDEN_EXAMPLES = [
    (
        {"input_field": "example input"},
        {"output_field": "expected output"}
    ),
]

def get_golden_examples():
    return GOLDEN_EXAMPLES
```

#### 5. Write Tests

```python
# tests/skills/test_your_skill.py
import pytest
from skills.your_skill import YourSkill

def test_your_skill_initialization():
    skill = YourSkill()
    assert skill.metadata is not None
    assert skill.metadata.name == "your_skill"

def test_your_skill_validate_input():
    skill = YourSkill()
    assert skill.validate_input({"input_field": "test"})
    assert not skill.validate_input({})

# Add more tests...
```

## Skill Guidelines

### Naming Conventions

- **Skill names**: Use `snake_case` (e.g., `web_summarizer`)
- **Class names**: Use `PascalCase` (e.g., `WebSummarizer`, `WebSummarizerModule`)
- **File names**: Use `snake_case` (e.g., `skill.yaml`, `golden_eval.py`)

### Safety Permissions

Be explicit about what your skill requires:

- **internet_access**: Set to `true` if the skill fetches data from the internet
- **file_system_read**: Set to `true` if the skill reads from the file system
- **file_system_write**: Set to `true` if the skill writes to the file system
- **external_api_calls**: Set to `true` if the skill calls external APIs
- **data_persistence**: Set to `true` if the skill stores data
- **user_interaction**: Set to `true` if the skill requires user input
- **sensitive_data**: Set to `true` if the skill handles sensitive information

### Schema Design

- Use JSON Schema format for input/output schemas
- Always specify `type` and `properties`
- List all `required` fields
- Provide clear `description` for each field
- Use appropriate data types (`string`, `integer`, `boolean`, `array`, `object`)

### Testing Requirements

Every skill must have:

1. **Initialization test**: Verify the skill loads correctly
2. **Module test**: Verify the DSPy module is created
3. **Signature test**: Verify the DSPy signature is defined
4. **Input validation test**: Verify input validation works
5. **Metadata test**: Verify metadata is correct
6. **Functional tests**: Test the skill's core functionality

Aim for **80%+ code coverage**.

### Documentation

- Add docstrings to all classes and methods
- Explain complex logic with comments
- Update README.md if adding new features
- Provide usage examples for your skill

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-skill
```

### 2. Implement Your Skill

Follow the structure outlined above.

### 3. Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/skills/test_your_skill.py -v

# Run with coverage
pytest tests/ --cov=skills --cov-report=term-missing
```

### 4. Validate Your Skill

```bash
python scripts/skills_cli.py validate --skills-dir skills
```

### 5. Check Code Quality

```bash
# Format code
black skills/ tests/

# Lint code
ruff check skills/ tests/
```

### 6. Generate Catalog

```bash
python scripts/skills_cli.py catalog \
    --skills-dir skills \
    --output catalog/skills.json
```

### 7. Test the Demo

```bash
python examples/demo.py
```

### 8. Commit Your Changes

```bash
git add .
git commit -m "Add new skill: your_skill"
```

### 9. Push and Create PR

```bash
git push origin feature/my-new-skill
```

Then create a pull request on GitHub.

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Skill follows naming conventions
- [ ] `skill.yaml` is complete and valid
- [ ] DSPy Module and Signature are implemented
- [ ] Input/output schemas are defined
- [ ] Safety permissions are set correctly
- [ ] All tests pass (`pytest tests/`)
- [ ] Code coverage is 80%+
- [ ] Skill validates (`python scripts/skills_cli.py validate`)
- [ ] Catalog generates (`python scripts/skills_cli.py catalog`)
- [ ] Code is formatted (`black`)
- [ ] No linting errors (`ruff`)
- [ ] Golden evaluations are provided
- [ ] Documentation is updated

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions small and focused
- Write self-documenting code
- Add docstrings for public APIs

## Getting Help

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Examples**: Check the `examples/` directory for usage examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
