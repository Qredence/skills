# GEPA Architecture

GEPA maps to DSPy constructs as follows:

| Phase | Action | DSPy Construct |
|---|---|---|
| **Generate** | Run DSPy program on each scenario prompt | `dspy.Module.__call__()` or `ScenarioGenerator` |
| **Evaluate** | Score output against expected/forbidden patterns | `dspy.Evaluate` + `pattern_match_metric` |
| **Propose** | Select teleprompter for optimization | `BootstrapFewShot` or `MIPROv2` |
| **Apply** | Compile optimized program and persist | `teleprompter.compile()` → `program.save()` |

## Scenario Generation Flow

The `generate` subcommand uses a `ScenarioSignature` that takes:
- `skill_name` — identifier for the skill
- `skill_description` — what the skill does
- `existing_scenarios` — summary of existing scenarios for context
- `variation_hint` — what aspect the new scenario should test

It outputs `scenario_yaml` — a complete YAML scenario object.

Each generated scenario is validated:
1. Parsed from YAML string to dict
2. Required fields checked (name, prompt, expected_patterns, forbidden_patterns, tags, mock_response)
3. `mock_response` scored against its own patterns (must score ≥ 0.8)
4. Failed scenarios are retried up to 2 times

## Optimization Flow

1. Load scenario YAML → `List[dspy.Example]`
2. Split into trainset / devset (80/20)
3. Evaluate baseline on devset
4. Compile with teleprompter using trainset
5. Evaluate optimized on devset
6. Save program + report
