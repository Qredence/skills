# Pattern-Matching Metrics

## Scoring Function

The `pattern_match_metric` scores generated code against expected and forbidden regex patterns:

```python
score = (expected_score + forbidden_score) / 2.0
```

Where:
- `expected_score` = fraction of expected patterns found in output (0.0–1.0)
- `forbidden_score` = fraction of forbidden patterns absent from output (0.0–1.0)

## Thresholds

- Default pass/fail threshold: **0.8**
- A scenario passes when `score >= threshold`
- Both expected and forbidden scores must be high for a good overall score

## Pattern Matching

- Patterns are Python regex strings matched with `re.search(pattern, code, re.DOTALL)`
- This mirrors the TypeScript evaluator in `tests/harness/evaluator.ts`
- Invalid regex patterns are counted as misses (not crashes)

## Scenario Validation

When generating new scenarios, the `mock_response` is validated against its own patterns:
- All expected patterns should match the mock_response
- No forbidden patterns should match the mock_response
- Scenarios scoring below 0.8 are retried automatically
