# Qredence Skills Registry

A Python-first registry of DSPy Module/Signature skills for agent orchestration. This repository provides a structured framework for building, validating, and cataloging reusable AI agent skills powered by DSPy.

## Features

- 🎯 **Structured Skills**: Each skill includes metadata, DSPy modules, signatures, IO schemas, and safety permissions
- 🔍 **Validation Tooling**: Automatic validation of skill structure and metadata
- 📦 **Auto-Generated Catalog**: JSON catalog of all skills with searchable metadata
- 🧪 **Testing Framework**: Built-in support for unit tests and golden evaluations
- 🛠️ **Template Scaffold**: Quick skill generation from reusable templates
- 🔄 **CI/CD Ready**: GitHub Actions workflow for continuous testing and validation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Qredence/skills.git
cd skills

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using a Skill

```python
from skills.web_summarizer import WebSummarizer

# Initialize the skill
skill = WebSummarizer()

# Check metadata
print(f"Skill: {skill.metadata.name}")
print(f"Description: {skill.metadata.description}")

# Execute the skill
result = skill.execute(url="https://example.com", max_length=200)
```

### Creating a New Skill

```bash
# Use the CLI to generate a new skill from template
python scripts/skills_cli.py create my_new_skill \
    --description "My awesome skill" \
    --author "Your Name" \
    --tags nlp processing

# This creates:
# - skills/my_new_skill/
#   - skill.yaml (metadata)
#   - __init__.py (implementation)
#   - golden_eval.py (evaluation examples)
# - tests/skills/test_my_new_skill.py (tests)
```

## Available Skills

### 1. Web Summarizer
**Path**: `skills/web_summarizer`

Summarizes web content into concise, actionable insights with key points extraction.

**Usage**:
```python
from skills.web_summarizer import WebSummarizer
skill = WebSummarizer()
```

**Safety Permissions**: Requires internet access, makes external API calls

### 2. Document Transformer
**Path**: `skills/doc_transformer`

Transforms documents between different formats (markdown, HTML, plain text) and writing styles.

**Usage**:
```python
from skills.doc_transformer import DocTransformer
skill = DocTransformer()
```

**Safety Permissions**: No special permissions required

### 3. Task Planner
**Path**: `skills/task_planner`

Plans and breaks down complex tasks into actionable subtasks with dependencies.

**Usage**:
```python
from skills.task_planner import TaskPlanner
skill = TaskPlanner()
```

**Safety Permissions**: No special permissions required

## Skill Structure

Each skill follows this structure:

```
skills/
  skill_name/
    skill.yaml          # Metadata and configuration
    __init__.py         # DSPy module and skill implementation
    golden_eval.py      # Golden evaluation examples
tests/
  skills/
    test_skill_name.py  # Unit tests
```

### skill.yaml Format

```yaml
name: skill_name
version: "0.1.0"
description: "Skill description"
author: "Author Name"
tags:
  - tag1
  - tag2

module_class: "SkillModule"
signature_class: "SkillSignature"

input_schema:
  name: "SkillInput"
  description: "Input schema"
  schema:
    type: "object"
    properties:
      input_field:
        type: "string"
    required:
      - input_field

output_schema:
  name: "SkillOutput"
  description: "Output schema"
  schema:
    type: "object"
    properties:
      output_field:
        type: "string"
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

## CLI Tools

### Validate Skills

```bash
python scripts/skills_cli.py validate --skills-dir skills
```

### Generate Catalog

```bash
python scripts/skills_cli.py catalog \
    --skills-dir skills \
    --output catalog/skills.json
```

### Create New Skill

```bash
python scripts/skills_cli.py create skill_name \
    --description "Description" \
    --author "Author" \
    --tags tag1 tag2
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=skills --cov-report=term-missing

# Run specific test file
pytest tests/skills/test_web_summarizer.py -v
```

### Validation

```bash
# Validate all skills
python scripts/skills_cli.py validate

# Generate catalog
python scripts/skills_cli.py catalog
```

### Code Quality

```bash
# Format code
black skills/ tests/

# Lint code
ruff check skills/ tests/
```

## Architecture

### Core Components

- **`skills.core.base`**: Base classes for skills (Skill, SkillMetadata, SafetyPermissions)
- **`skills.registry.catalog`**: Skill discovery and catalog generation
- **`skills.validation.validator`**: Skill validation logic
- **`skills.template.generator`**: Template-based skill scaffolding

### Integration with DSPy

Each skill implements:
1. **DSPy Signature**: Defines input/output fields with descriptions
2. **DSPy Module**: Implements the skill logic using DSPy primitives (ChainOfThought, etc.)
3. **Skill Class**: Wraps the module with metadata and validation

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
- Runs tests on Python 3.9, 3.10, 3.11
- Validates all skills
- Checks code formatting
- Generates coverage reports
- Creates skills catalog artifact

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your skill using the template
4. Write tests and golden evaluations
5. Validate: `python scripts/skills_cli.py validate`
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Built with [DSPy](https://github.com/stanfordnlp/dspy) by Stanford NLP
