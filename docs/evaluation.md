# Golden Evaluation Framework

Golden evaluations provide deterministic, version-controlled test cases for DSPy skills. They validate behavior and prevent regressions.

## Overview

Golden evaluations use **JSONL** (JSON Lines) format for portability and git-friendliness. Each line is a self-contained test case.

## Golden Set Format

### File Location

`eval/golden.jsonl` in each skill directory.

### Line Format

Each line is a JSON object with required fields:

```json
{
  "name": "test_case_name",
  "input": {...},
  "expected": {...},
  "match": "exact_match|contains|json_schema_valid"
}
```

### Fields

- **`name`** (string, required): Unique test case identifier
- **`input`** (object, required): Input matching skill's input schema
- **`expected`** (any, required): Expected output or schema
- **`match`** (string, required): Match type for evaluation

### Match Types

#### 1. exact_match

Output must **exactly** match expected value.

```jsonl
{"name": "deterministic_output", "input": {"text": "hello"}, "expected": {"result": "HELLO"}, "match": "exact_match"}
```

Use for:
- Deterministic transformations
- Fixed outputs
- Exact string matching

#### 2. contains

Output must **contain** expected value.

For strings:
```jsonl
{"name": "substring_check", "input": {"text": "analyze this"}, "expected": "analysis", "match": "contains"}
```

For lists:
```jsonl
{"name": "list_element", "input": {"items": [1,2,3]}, "expected": 2, "match": "contains"}
```

For objects (checks if all expected key-value pairs exist):
```jsonl
{"name": "partial_match", "input": {"x": 1}, "expected": {"status": "success"}, "match": "contains"}
```

Use for:
- Non-deterministic outputs with predictable content
- Checking for specific keywords or phrases
- Partial object matching

#### 3. json_schema_valid

Output must **validate** against expected JSON Schema.

```jsonl
{"name": "schema_check", "input": {"text": "hello"}, "expected": {"type": "object", "properties": {"result": {"type": "string"}}, "required": ["result"]}, "match": "json_schema_valid"}
```

Use for:
- Non-deterministic outputs with predictable structure
- Complex nested objects
- When exact values vary but structure is consistent

## Example Golden Sets

### Web Summarizer

```jsonl
{"name": "basic_summary", "input": {"url": "https://example.com", "max_length": 100}, "expected": {"type": "object", "properties": {"summary": {"type": "string"}, "key_points": {"type": "array", "items": {"type": "string"}}}, "required": ["summary", "key_points"]}, "match": "json_schema_valid"}
{"name": "contains_keywords", "input": {"url": "https://example.com/tech"}, "expected": "technology", "match": "contains"}
```

### Document Transformer

```jsonl
{"name": "markdown_to_html", "input": {"document": "# Title", "source_format": "markdown", "target_format": "html"}, "expected": "<h1>", "match": "contains"}
{"name": "output_structure", "input": {"document": "text", "source_format": "plain", "target_format": "markdown"}, "expected": {"type": "object", "properties": {"transformed_document": {"type": "string"}}, "required": ["transformed_document"]}, "match": "json_schema_valid"}
```

### Task Planner

```jsonl
{"name": "plan_structure", "input": {"goal": "Build a website", "constraints": ["budget"]}, "expected": {"type": "object", "properties": {"plan": {"type": "object"}, "reasoning": {"type": "string"}}, "required": ["plan", "reasoning"]}, "match": "json_schema_valid"}
{"name": "mentions_steps", "input": {"goal": "Write a report"}, "expected": "steps", "match": "contains"}
```

## Running Evaluations

### Dry Run (Format Validation Only)

```bash
python tools/run_eval.py --dry-run
```

Validates:
- JSONL file is parseable
- All required fields present
- Input matches input schema
- Expected value is valid for match type

### Full Evaluation (with LLM)

```bash
python tools/run_eval.py --execute
```

Actually runs the skill and evaluates outputs.

### Single Skill

```bash
python tools/run_eval.py --skill web_summarizer --dry-run
```

### Starter Skills Only (Fast)

```bash
python tools/run_eval.py --starter-only --dry-run
```

## Creating Golden Sets

### Step 1: Define Test Cases

Identify key scenarios:
- **Happy path**: Normal usage
- **Edge cases**: Empty inputs, extremes
- **Error cases**: Invalid inputs
- **Variations**: Different input types

### Step 2: Write JSONL

Start with 2-5 examples:

```jsonl
{"name": "happy_path", "input": {"text": "hello"}, "expected": {"type": "object", "properties": {"result": {"type": "string"}}, "required": ["result"]}, "match": "json_schema_valid"}
{"name": "empty_input", "input": {"text": ""}, "expected": {"type": "object", "properties": {"result": {"type": "string"}}, "required": ["result"]}, "match": "json_schema_valid"}
```

### Step 3: Run and Refine

```bash
python tools/run_eval.py --skill my_skill --dry-run
```

Fix any format errors.

### Step 4: Execute and Validate

```bash
python tools/run_eval.py --skill my_skill --execute
```

Verify outputs match expectations.

### Step 5: Expand Coverage

Add more cases:
- Different input variations
- Edge cases discovered during testing
- Regression tests for bugs

## Best Practices

### Coverage

- **Minimum**: 2-3 golden examples per skill
- **Recommended**: 5-10 covering main scenarios
- **Comprehensive**: 20+ including edge cases

### Determinism

For **deterministic** skills:
- Use `exact_match` when possible
- Test all code paths
- Include edge cases

For **non-deterministic** skills:
- Use `json_schema_valid` for structure
- Use `contains` for keywords/themes
- Focus on structural invariants

### Maintainability

- Use descriptive `name` fields
- One logical test per line
- Group related tests
- Add comments in README

### Evolution

- Add tests when fixing bugs
- Update tests when changing behavior (MAJOR version)
- Never delete tests (deprecate with comments)

## Integration with CI

Evaluations run in CI:

```yaml
# .github/workflows/ci.yml
- name: Run Golden Evals
  run: python tools/run_eval.py --starter-only --dry-run
```

Full execution (with LLM) runs:
- On demand
- Before releases
- In dedicated test environments

## Metrics

### Success Rate

```
success_rate = passed_tests / total_tests
```

Target: **100%** for deterministic skills, **>90%** for non-deterministic.

### Match Type Distribution

Track which match types are used:
- High `exact_match` → Highly deterministic
- High `json_schema_valid` → Structured but variable
- High `contains` → Less deterministic

## Troubleshooting

### Test Fails: Format Validation

Check:
- Valid JSON on each line
- All required fields present
- Input matches input_schema

### Test Fails: Execution

Check:
- Skill forward() method works
- Input is valid
- Expected value is correct
- Match type is appropriate

### Flaky Tests

If tests pass inconsistently:
- Switch from `exact_match` to `contains` or `json_schema_valid`
- Make expectations more flexible
- Set temperature to 0.0 for more determinism

## Examples Repository

See `skills/*/eval/golden.jsonl` for real examples in:
- `web_summarizer`
- `doc_transformer`
- `task_planner`

## Future Enhancements

Planned features:
- Automatic golden set generation
- Coverage analysis
- Diff visualization
- Performance benchmarking
- LLM-as-judge evaluation
