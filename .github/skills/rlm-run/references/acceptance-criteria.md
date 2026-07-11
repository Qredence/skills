# RLM Run — Acceptance Criteria

Validates that generated entrypoint selection and programmatic RLM usage code
follows the current public entrypoints and runtime conventions.

## Entrypoint Selection

Choose the right entrypoint for the task. `fleet web` for workspace-first UI
work, `serve-api` for backend surface, `serve-mcp` for MCP clients, `chat` for
terminal, `daytona-smoke` before any `daytona_pilot` workflow.

### ✅ Correct
```bash
# Workspace-first UI work
uv run fleet web

# Expose backend API surface
uv run fleet-rlm serve-api --port 8000

# MCP clients
uv run fleet-rlm serve-mcp --transport stdio

# Terminal chat
uv run fleet-rlm chat

# Pre-daytona validation
uv run fleet-rlm daytona-smoke --repo <url> [--ref <branch>]
```

### ❌ Incorrect — using serve-api when task is UI-driven
```bash
# Wrong: serve-api is not the workspace UI; use fleet web instead
uv run fleet-rlm serve-api --port 8000  # when task is workspace-first
```

## Daytona Smoke Before daytona_pilot

Always run `daytona-smoke` before any `daytona_pilot` workflow to validate
Daytona readiness.

### ✅ Correct
```bash
uv run fleet-rlm daytona-smoke --repo https://github.com/your-org/your-repo
# Then proceed with daytona_pilot workflows
```

### ❌ Incorrect — skipping smoke test
```python
# Wrong: jumping into daytona_pilot without smoke test
interp = DaytonaInterpreter(repo_url="https://github.com/your-org/your-repo")
interp.start()  # May fail silently if Daytona env is not ready
```

## Programmatic Usage — configure_planner_from_env First

Always call `configure_planner_from_env()` before creating a
`DaytonaInterpreter` or `dspy.RLM` instance.

### ✅ Correct
```python
import dspy
from fleet_rlm.runtime.config import configure_planner_from_env
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

configure_planner_from_env()

interpreter = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    volume_name="my-project",
    timeout=120,
)
rlm = dspy.RLM(
    signature="question -> answer, confidence",
    interpreter=interpreter,
    max_iterations=10,
)
```

### ❌ Incorrect — no configure_planner_from_env
```python
import dspy
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

# Wrong: planner LM is not configured
interpreter = DaytonaInterpreter(repo_url="https://github.com/your-org/your-repo")
```

## Result Access — Dot Notation

Access `dspy.RLM` results via dot notation, not subscript.

### ✅ Correct
```python
result = rlm(question="What is 15 factorial?")
print(result.answer)       # dot notation
print(result.confidence)
```

### ❌ Incorrect — subscript on RLM result
```python
result = rlm(question="What is 15 factorial?")
print(result["answer"])    # Wrong: use dot notation
```

## try/finally Shutdown

Always shut down the interpreter in a `finally` block.

### ✅ Correct
```python
interpreter.start()
try:
    result = rlm(question="Complex task")
    print(result.answer)
finally:
    interpreter.shutdown()
```

### ❌ Incorrect — no finally
```python
interpreter.start()
result = rlm(question="Complex task")
interpreter.shutdown()  # Skipped if rlm() raises
```

## uv run Prefix

All fleet-rlm commands must be run via `uv run`. Do not invoke Python
scripts or fleet commands directly.

### ✅ Correct
```bash
uv run fleet web
uv run fleet-rlm serve-api --port 8000
uv run fleet-rlm daytona-smoke --repo <url>
```

### ❌ Incorrect — direct invocation
```bash
fleet web                   # Wrong: missing uv run
python -m fleet_rlm serve   # Wrong: use uv run fleet-rlm
```
