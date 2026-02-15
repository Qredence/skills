# DSPy Skill Contract

This document defines what constitutes a valid DSPy skill in the Qredence Skills Registry.

## Overview

A **skill** is a versioned, reusable DSPy Module with:
- Declared DSPy Signature(s)
- Explicit input/output schemas (JSON Schema)
- Golden evaluation dataset (JSONL)
- Explicit permissions and safety declaration
- Complete test coverage

## Directory Structure

Every skill must follow this exact structure:

```
skills/
  {skill_id}/
    skill.yaml          # Canonical metadata (REQUIRED)
    README.md           # Skill documentation (REQUIRED)
    
    src/
      skill.py          # DSPy Module implementation (REQUIRED)
      __init__.py
    
    tests/
      test_contract.py  # Contract validation tests (REQUIRED)
      __init__.py
    
    eval/
      golden.jsonl      # Golden evaluation set (REQUIRED)
    
    examples/
      minimal.py        # Runnable example (REQUIRED)
```

## skill.yaml Format

The `skill.yaml` file is the **single source of truth** for skill metadata. It must validate against `catalog/schema.skill.json`.

### Required Fields

```yaml
id: "skill_name"              # snake_case, unique
name: "Human Readable Name"
version: "X.Y.Z"              # Semantic versioning
description: "1-2 sentence description (10-200 chars)"
tags:                         # At least one tag
  - "category"
  - "function"

dspy:
  module: "skills.{id}.src.skill:Skill"
  signatures:
    - "skills.{id}.src.skill:SkillSignature"
  dependencies:
    - "dspy-ai>=2.5.0"

io:
  inputs_schema:              # JSON Schema
    type: "object"
    properties: {...}
    required: [...]
  outputs_schema:             # JSON Schema
    type: "object"
    properties: {...}
    required: [...]

behavior:
  deterministic: true|false
  temperature_hint: 0.0       # 0.0-2.0
  max_tokens_hint: 512        # Optional
  notes:
    - "Behavioral note"

permissions:
  network: false              # Default false
  filesystem_read: false      # Default false
  filesystem_write: false     # Default false
  external_tools: []          # Default empty

safety:
  level: "low"|"medium"|"high"
  risks:
    - "Known risk"
  mitigations:
    - "Mitigation strategy"
  data_policy:
    - "Data handling policy"

eval:
  golden_set: "eval/golden.jsonl"
  metrics:
    - "exact_match"
    - "contains"
    - "json_schema_valid"
```

### Optional Fields

```yaml
owner: "maintainer-name"
resources:
  - "https://docs.example.com"
```

## DSPy Module Contract

### src/skill.py

Must export:

1. **SIGNATURES** - List of DSPy Signature classes
2. **Skill** - Main DSPy Module class (subclass of `dspy.Module`)
3. **run()** - Convenience function

Example:

```python
import dspy

class SkillSignature(dspy.Signature):
    """DSPy signature"""
    input_field: str = dspy.InputField(desc="...")
    output_field: str = dspy.OutputField(desc="...")

class Skill(dspy.Module):
    """Main skill module"""
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(SkillSignature)
    
    def forward(self, **kwargs) -> dspy.Prediction:
        return self.prog(**kwargs)

def run(**kwargs):
    """Convenience function"""
    return Skill().forward(**kwargs)

SIGNATURES = [SkillSignature]
```

### Requirements

- Skill class **must** subclass `dspy.Module`
- Skill **must** have `forward()` method
- Signatures **must** subclass `dspy.Signature`
- All signatures **must** be listed in `SIGNATURES`
- Import paths in skill.yaml **must** match actual code

## Input/Output Schemas

Use JSON Schema (Draft 7) to define inputs and outputs:

```json
{
  "type": "object",
  "properties": {
    "field_name": {
      "type": "string|number|boolean|array|object",
      "description": "Field description"
    }
  },
  "required": ["field_name"]
}
```

### Schema Best Practices

- Always specify `type` and `properties`
- List all `required` fields
- Provide clear `description` for each field
- Use appropriate types
- Consider validation constraints (min, max, pattern, etc.)

## Testing Requirements

### tests/test_contract.py

Minimum tests:

1. **Skill class exists** and subclasses `dspy.Module`
2. **Signature exists** and subclasses `dspy.Signature`
3. **SIGNATURES exported** correctly
4. **Skill instantiates** without errors
5. **forward() method exists** and is callable

### Functional Tests

Add tests for:
- Input validation
- Output schema compliance
- Edge cases
- Error handling

## Golden Evaluation

### eval/golden.jsonl Format

Each line is a JSON object:

```json
{"name": "test_case_1", "input": {"field": "value"}, "expected": {...}, "match": "exact_match|contains|json_schema_valid"}
```

### Match Types

- **exact_match**: Output must exactly match expected
- **contains**: Output must contain expected (strings, lists, dicts)
- **json_schema_valid**: Output must validate against expected schema

### Example

```jsonl
{"name": "basic_test", "input": {"text": "hello"}, "expected": {"type": "object", "properties": {"result": {"type": "string"}}, "required": ["result"]}, "match": "json_schema_valid"}
{"name": "specific_output", "input": {"text": "test"}, "expected": {"result": "processed: test"}, "match": "exact_match"}
```

## Examples

### examples/minimal.py

Must be a **runnable** Python script demonstrating skill usage:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from skills.{skill_id}.src.skill import run

def main():
    result = run(input_field="value")
    print(f"Result: {result.output_field}")

if __name__ == "__main__":
    main()
```

## Validation

All skills are validated by `tools/validate.py`:

```bash
python tools/validate.py
```

This checks:
- skill.yaml validates against JSON Schema
- All required files exist
- DSPy imports are valid
- Catalog regenerates deterministically

## Versioning

Skills follow **Semantic Versioning**:
- **MAJOR**: Breaking changes to API or behavior
- **MINOR**: Backwards-compatible additions
- **PATCH**: Backwards-compatible fixes

See `docs/versioning.md` for details.
