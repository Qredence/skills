# Skills Core

Core library for the Qredence DSPy Skills Registry. Provides validation, catalog generation, and evaluation tools.

## Installation

```bash
pip install -e packages/skills_core
```

## Usage

### Load Skill Metadata

```python
from pathlib import Path
from skills_core import load_skill_metadata, discover_skills

# Load single skill
metadata = load_skill_metadata(Path("skills/web_summarizer"))
print(f"{metadata.name} v{metadata.version}")

# Discover all skills
skills = discover_skills(Path("skills"))
for skill in skills:
    print(f"  - {skill.id}: {skill.description}")
```

### Validate Skills

```python
from skills_core import validate_skill, validate_all_skills

# Validate single skill
is_valid, errors = validate_skill(
    Path("skills/web_summarizer"),
    Path("catalog/schema.skill.json")
)

if not is_valid:
    for error in errors:
        print(f"  ✗ {error}")

# Validate all skills
results = validate_all_skills(
    Path("skills"),
    Path("catalog/schema.skill.json")
)
```

### Generate Catalog

```python
from skills_core import generate_catalog

catalog = generate_catalog(
    Path("skills"),
    Path("catalog/skills.json")
)

print(f"Generated catalog with {len(catalog.skills)} skills")
```

### Run Evaluations

```python
from skills_core import run_skill_eval

result = run_skill_eval(Path("skills/web_summarizer"), dry_run=True)
print(result.summary())
```

## Modules

- **types.py**: Pydantic models for skill metadata and catalog
- **loader.py**: Skill discovery and metadata loading
- **validator.py**: JSON Schema validation and structural checks
- **catalog.py**: Deterministic catalog generation
- **dspy_contract.py**: DSPy Module/Signature reflection
- **evals.py**: Golden evaluation framework

## Development

```bash
# Install dev dependencies
pip install -e "packages/skills_core[dev]"

# Run tests
pytest packages/skills_core/tests/

# Lint
ruff check packages/skills_core/
```
