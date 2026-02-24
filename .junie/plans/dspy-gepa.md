# DSPy GEPA Tool — Detailed Implementation Plan

## Problem Statement

Skills are evaluated today via a TypeScript test harness (`tests/harness/`) that runs scenarios from YAML files against an LLM and checks expected/forbidden regex patterns. This process is **static** — there is no optimization loop that iteratively improves a skill's prompt or few-shot examples based on evaluation results.

**GEPA** (Generate → Evaluate → Propose → Apply) introduces a DSPy-powered optimization loop that:

1. Loads scenario YAML files as structured DSPy datasets
2. Evaluates a baseline DSPy program against those scenarios using pattern-matching metrics
3. Optimizes the program via DSPy teleprompters (BootstrapFewShot, MIPROv2)
4. Saves the optimized program for reuse

This closes the feedback loop: scenarios become training data, pattern criteria become metrics, and DSPy handles prompt optimization automatically.

---

## User Workflow

```
Point GEPA at scenario YAML
        │
        ▼
  Load as DSPy Examples (scenario_to_dataset.py)
        │
        ▼
  Baseline Evaluate (gepa_evaluate.py)
        │
        ▼
  Optimize via teleprompter (gepa.py)
        │
        ▼
  Save optimized program + report
```

**Typical CLI session:**

```bash
# 1. Convert scenarios to DSPy dataset (optional standalone step)
python scenario_to_dataset.py --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml --output dataset.json

# 2. Evaluate baseline (optional standalone step)
python gepa_evaluate.py --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml --module dspy.ChainOfThought --signature "prompt -> code"

# 3. Full GEPA loop: evaluate baseline → optimize → save
python gepa.py --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml --output optimized_program.json
```

---

## GEPA Loop Architecture

The four GEPA phases map to DSPy constructs:

| GEPA Phase | Action | DSPy Construct |
|---|---|---|
| **Generate** | Run the DSPy program on each scenario prompt to produce code output | `dspy.Module.__call__()` (e.g., `dspy.ChainOfThought`) |
| **Evaluate** | Score each output against expected/forbidden patterns | `dspy.Evaluate` with a custom `pattern_match_metric` |
| **Propose** | Select and configure a teleprompter to find better prompts/demos | `BootstrapFewShot` or `MIPROv2` teleprompter |
| **Apply** | Compile the optimized program and persist it | `teleprompter.compile()` → `program.save()` |

### Loop Flow (inside `gepa.py`)

```
1. Load scenario YAML → List[dspy.Example]
2. Split into trainset / devset (80/20 or configurable)
3. Instantiate baseline module (default: ChainOfThought("prompt -> code"))
4. EVALUATE baseline on devset → baseline_score
5. PROPOSE: select teleprompter (BootstrapFewShot or MIPROv2)
6. APPLY: compiled_program = teleprompter.compile(module, trainset=trainset, metric=pattern_match_metric)
7. EVALUATE optimized on devset → optimized_score
8. Save compiled_program + emit JSON report {baseline_score, optimized_score, delta}
```

---

## Data Model: Scenario YAML → dspy.Example

### Source Schema (`tests/schemas/skill-scenarios.schema.json`)

Each scenario object has:
- `name` (string) — scenario identifier
- `prompt` (string) — the generation prompt
- `expected_patterns` (string[]) — regex patterns that MUST appear in output
- `forbidden_patterns` (string[]) — regex patterns that MUST NOT appear in output
- `tags` (string[]) — category tags
- `mock_response` (string) — reference "gold" output

### Mapping to dspy.Example

```python
def scenario_to_example(scenario: dict) -> dspy.Example:
    return dspy.Example(
        prompt=scenario["prompt"],
        expected_patterns=scenario["expected_patterns"],
        forbidden_patterns=scenario["forbidden_patterns"],
        mock_response=scenario.get("mock_response", ""),
        name=scenario.get("name", ""),
        tags=scenario.get("tags", []),
    ).with_inputs("prompt")
```

**Input fields:** `prompt`
**Label/metadata fields:** `expected_patterns`, `forbidden_patterns`, `mock_response`, `name`, `tags`

The `mock_response` serves dual purpose:
- As a reference answer for few-shot demonstrations during optimization
- As a gold standard for optional exact-match scoring

---

## Metric Design: Pattern-Matching Scoring

The metric mirrors the existing TypeScript evaluator logic (`tests/harness/evaluator.ts`) but implemented in Python:

```python
import re

def pattern_match_metric(example, pred, trace=None) -> float:
    """
    Score a prediction against expected/forbidden patterns.
    Returns a float in [0.0, 1.0].
    """
    code = pred.code  # generated output

    # Score expected patterns (should match)
    expected = example.expected_patterns or []
    if expected:
        expected_hits = sum(1 for p in expected if re.search(p, code, re.DOTALL))
        expected_score = expected_hits / len(expected)
    else:
        expected_score = 1.0

    # Score forbidden patterns (should NOT match)
    forbidden = example.forbidden_patterns or []
    if forbidden:
        forbidden_misses = sum(1 for p in forbidden if not re.search(p, code, re.DOTALL))
        forbidden_score = forbidden_misses / len(forbidden)
    else:
        forbidden_score = 1.0

    # Combined score: both must be high
    return (expected_score + forbidden_score) / 2.0
```

**Scoring breakdown:**
- `expected_score` = fraction of expected patterns found in output
- `forbidden_score` = fraction of forbidden patterns absent from output
- Final score = arithmetic mean of both (range 0.0–1.0)

**Threshold for pass/fail:** configurable, default `0.8`

---

## CLI Interface Specs

### Script 1: `scenario_to_dataset.py`

**Purpose:** Convert scenario YAML to a DSPy-compatible JSON dataset.

```
Usage: scenario_to_dataset.py [OPTIONS]

Options:
  --scenarios PATH    Path to scenarios.yaml file (required)
  --output PATH       Output JSON file path (default: stdout)
  --filter-tags TEXT   Comma-separated tags to filter scenarios (optional)
  --validate          Validate YAML against schema before conversion (flag)
```

**Output format:** JSON array of objects with fields matching dspy.Example constructor args.

### Script 2: `gepa_evaluate.py`

**Purpose:** Evaluate a DSPy program against scenarios without optimization (baseline measurement).

```
Usage: gepa_evaluate.py [OPTIONS]

Options:
  --scenarios PATH       Path to scenarios.yaml file (required)
  --module TEXT          DSPy module class (default: "dspy.ChainOfThought")
  --signature TEXT       DSPy signature string (default: "prompt -> code")
  --program PATH        Path to a saved/optimized program to load (optional)
  --threshold FLOAT     Pass/fail threshold (default: 0.8)
  --threads INT         Number of evaluation threads (default: 4)
  --output PATH         Output JSON report path (optional)
```

**Output:** JSON report with per-scenario scores and aggregate metrics.

### Script 3: `gepa.py`

**Purpose:** Full GEPA loop — evaluate baseline, optimize, evaluate optimized, save.

```
Usage: gepa.py [OPTIONS]

Options:
  --scenarios PATH       Path to scenarios.yaml file (required)
  --module TEXT          DSPy module class (default: "dspy.ChainOfThought")
  --signature TEXT       DSPy signature string (default: "prompt -> code")
  --teleprompter TEXT   Optimizer: "bootstrap" or "mipro" (default: "bootstrap")
  --max-rounds INT      Max optimization rounds (default: 1)
  --max-demos INT       Max bootstrapped demos (default: 4)
  --train-split FLOAT   Train/dev split ratio (default: 0.8)
  --threshold FLOAT     Pass/fail threshold (default: 0.8)
  --output PATH         Path to save optimized program (default: optimized_program.json)
  --report PATH         Path to save evaluation report (default: gepa_report.json)
```

**Output:** Saved optimized program + JSON report with baseline vs. optimized scores.

---

## File Structure for the New Skill

```
skills/dspy-gepa/
├── SKILL.md                          # Skill definition (frontmatter + body)
├── scripts/
│   ├── gepa.py                       # Full GEPA optimization loop
│   ├── gepa_evaluate.py              # Standalone evaluation
│   └── scenario_to_dataset.py        # YAML → DSPy dataset converter
├── references/
│   ├── gepa-architecture.md          # GEPA loop explanation & DSPy mapping
│   └── metrics.md                    # Metric design & scoring details
└── examples/
    └── sample-run.md                 # Example CLI session with output
```

### SKILL.md Frontmatter

```yaml
---
name: dspy-gepa
description: >-
  Evaluates and optimizes agent skills using a DSPy-powered GEPA
  (Generate/Evaluate/Propose/Apply) loop. Loads scenario YAML files as
  DSPy datasets, scores outputs with pattern-matching metrics, and
  optimizes prompts via BootstrapFewShot or MIPROv2 teleprompters.
---
```

---

## Integration with Existing Test Harness and Schema

### Schema Reuse

- `scenario_to_dataset.py` validates input YAML against `tests/schemas/skill-scenarios.schema.json` (via `jsonschema` Python package) when `--validate` is passed.
- The same scenario files used by the TypeScript harness (`tests/scenarios/<skill>/scenarios.yaml`) are consumed directly — no duplication.

### Metric Parity

- The Python `pattern_match_metric` replicates the logic in `tests/harness/evaluator.ts` (`CodeEvaluator.evaluate()`), which compiles `expected_patterns` and `forbidden_patterns` as regexes and checks matches.
- Both systems use the same regex dialect (PCRE-compatible) ensuring consistent scoring.

### Test Scenarios as Datasets

- Existing scenario directories under `tests/scenarios/` serve as ready-made datasets.
- Each scenario's `mock_response` field provides gold-standard outputs for few-shot bootstrapping.
- Tags enable filtering subsets for targeted optimization.

### New Test Coverage

Add a test scenario file at `tests/scenarios/dspy-gepa/scenarios.yaml` that validates the GEPA skill itself (meta-evaluation), with scenarios like:
- "Generate a pattern-matching metric function"
- "Convert a scenario YAML to dspy.Example"
- "Run a GEPA optimization loop"

---

## Success Criteria

1. **`scenario_to_dataset.py`** correctly converts any valid `scenarios.yaml` into a list of `dspy.Example` objects with proper input field designation.
2. **`gepa_evaluate.py`** produces a JSON report with per-scenario and aggregate scores that match the TypeScript evaluator's scoring on the same scenarios.
3. **`gepa.py`** completes a full GEPA loop: baseline eval → optimize → optimized eval → save, with `optimized_score >= baseline_score` on the devset.
4. **Pattern metric** scores are in `[0.0, 1.0]` and correctly penalize missing expected patterns and present forbidden patterns.
5. **All 3 scripts** run standalone via `python <script>.py --help` with clear usage output.
6. **Schema validation** mode catches malformed scenario YAML before processing.
7. **Existing tests** remain green — no regressions (`pnpm test` passes all 46 tests).
8. **SKILL.md** passes all best-practice checks: name ≤64 chars, description ≤1024 chars, body <800 words, no hardcoded paths, third-person description.
