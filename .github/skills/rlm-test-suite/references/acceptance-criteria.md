# RLM Test Suite — Acceptance Criteria

Validates that generated test invocation commands use the correct lanes,
tooling, and test file targets for the fleet-rlm repository.

## Test Runner — uv run pytest

Always use `uv run pytest` to run tests. Never use `python -m pytest` or bare
`pytest`.

### ✅ Correct
```bash
uv run pytest -q tests/unit/test_daytona_interpreter.py
uv run pytest -q tests/ui/ws/test_chat_stream.py
```

### ❌ Incorrect — wrong runner
```bash
python -m pytest tests/unit/test_daytona_interpreter.py   # Wrong
pytest tests/unit/test_daytona_interpreter.py             # Wrong (no uv run)
```

## Make Targets for Confidence Lanes

Use `make test-fast` for fast confidence and `make quality-gate` for shared
contract confidence. Do not invent custom make targets.

### ✅ Correct
```bash
# Fast confidence (default starting point)
make test-fast

# Shared contract confidence (before merging)
make quality-gate
```

### ❌ Incorrect — too broad
```bash
# Wrong: pytest tests/ is too broad, runs everything including slow tests
uv run pytest tests/
```

## Daytona Tests — Specific File List

Run Daytona-focused tests using the specific test files listed in the skill.
Do not glob all Daytona files.

### ✅ Correct
```bash
uv run pytest -q \
  tests/unit/test_daytona_rlm_config.py \
  tests/unit/test_daytona_rlm_smoke.py \
  tests/unit/test_daytona_runtime.py \
  tests/unit/test_daytona_interpreter.py \
  tests/unit/test_daytona_rlm_chat_agent.py \
  tests/unit/test_daytona_workbench_chat_agent.py \
  tests/unit/test_daytona_async_tools.py
```

### ❌ Incorrect — too broad Daytona glob
```bash
# Wrong: may include tests that require cloud access or are slow
uv run pytest -q tests/unit/test_daytona_*.py
```

## Runtime / WS Tests — Specific File List

Run runtime and websocket tests using the specific file list.

### ✅ Correct
```bash
uv run pytest -q \
  tests/ui/server/test_api_contract_routes.py \
  tests/ui/server/test_router_runtime.py \
  tests/ui/ws/test_chat_stream.py \
  tests/ui/ws/test_commands.py \
  tests/unit/test_ws_chat_helpers.py
```

## Unit Test Pattern — monkeypatch for Providers

Unit tests must mock Daytona/DSPy providers using `monkeypatch` to avoid cloud
dependencies. Access results via dot notation.

### ✅ Correct
```python
def test_feature(monkeypatch):
    from unittest.mock import MagicMock
    mock_daytona = MagicMock()
    monkeypatch.setattr(
        "fleet_rlm.integrations.providers.daytona.interpreter.AsyncDaytona",
        mock_daytona,
    )

    interp = DaytonaInterpreter(timeout=60)
    interp.start()
    try:
        result = interp.execute("x = 42\nSUBMIT(answer=x)")
        assert result.answer == 42  # dot notation
    finally:
        interp.shutdown()
```

### ❌ Incorrect — subscript access in tests
```python
result = interp.execute("SUBMIT(answer=42)")
assert result["answer"] == 42  # Wrong: use result.answer
```

## Smallest Lane Principle

Use the smallest test lane that matches the change. Do not run the full suite
for a targeted change.

### ✅ Correct
```bash
# Changed only DaytonaInterpreter lifecycle? Run targeted Daytona tests.
uv run pytest -q tests/unit/test_daytona_interpreter.py

# Changed WS chat? Run WS-focused lane.
uv run pytest -q tests/ui/ws/test_chat_stream.py tests/ui/ws/test_commands.py
```

### ❌ Incorrect — always running full suite
```bash
# Wrong: wasteful for targeted changes
make quality-gate  # for every single-file change
```
