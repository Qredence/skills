# Sample GEPA Run

## Generate Scenarios

```bash
$ python scripts/gepa.py generate \
    --skill-name fastapi-router-py \
    --skill-description "Creates FastAPI routers with CRUD endpoints, pagination, and error handling" \
    --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
    --num-scenarios 3 \
    --model openai/gpt-4o \
    --output generated-scenarios.yaml

Generating scenario 1/3: Test edge cases and error handling
  ✓ Generated: error_handling_middleware
Generating scenario 2/3: Test security-related patterns
  ✓ Generated: auth_protected_router
Generating scenario 3/3: Test async/concurrent patterns
  ✓ Generated: async_background_tasks

Wrote 3 scenarios to generated-scenarios.yaml

Summary: 3 generated, 0 failed
```

## Evaluate Scenarios (Offline)

```bash
$ python scripts/gepa_evaluate.py \
    --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
    --offline

{
  "aggregate_score": 0.95,
  "total_scenarios": 6,
  "passed": 6,
  "failed": 0,
  "threshold": 0.8,
  "scenarios": [
    {"name": "basic_crud_router", "score": 1.0, "passed": true, ...},
    ...
  ]
}

Score: 0.95 | Passed: 6 | Failed: 0 | Threshold: 0.8
```

## Convert to Dataset

```bash
$ python scripts/scenario_to_dataset.py \
    --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
    --filter-tags basic \
    --output dataset.json

Wrote 2 examples to dataset.json
```
