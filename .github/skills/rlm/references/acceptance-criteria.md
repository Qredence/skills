# RLM — Acceptance Criteria

Validates that generated `fleet-rlm` / `dspy.RLM` code follows the current
`daytona_pilot` runtime model and Claude Code translation layer patterns.

## Interpreter Import and Configuration

The DaytonaInterpreter must be imported from the correct module and
`configure_planner_from_env()` must be called before any interpreter use.

### ✅ Correct
```python
import dspy
from fleet_rlm.runtime.config import configure_planner_from_env
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

configure_planner_from_env()

interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    volume_name="rlm-volume-dspy",
    timeout=900,
)
interp.start()
```

### ❌ Incorrect — missing configure_planner_from_env
```python
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

# Wrong: configure_planner_from_env() was never called
interp = DaytonaInterpreter(repo_url="https://github.com/your-org/your-repo")
interp.start()
```

## Lifecycle — try/finally with shutdown

`interp.shutdown()` must always be called in a `finally` block to ensure the
sandbox session is terminated even if an exception occurs.

### ✅ Correct
```python
interp.start()
try:
    result = interp.execute("SUBMIT(answer=42)")
    print(result.answer)
finally:
    interp.shutdown()
```

### ❌ Incorrect — no finally block
```python
interp.start()
result = interp.execute("SUBMIT(answer=42)")
interp.shutdown()  # Will not run if execute() raises
```

## Result Access — dot notation

Results returned by `interp.execute()` when using `SUBMIT(...)` are
`FinalOutput` objects. Access fields with dot notation, never subscript.

### ✅ Correct
```python
result = interp.execute("SUBMIT(answer='Paris', confidence=0.99)")
print(result.answer)
print(result.confidence)
```

### ❌ Incorrect — subscript access
```python
result = interp.execute("SUBMIT(answer='Paris')")
print(result["answer"])   # AttributeError: FinalOutput is not a dict
```

## dspy.RLM Construction

Use `dspy.RLM` with a `signature` and `interpreter` argument. Always access
outputs via dot notation on the returned prediction object.

### ✅ Correct
```python
rlm = dspy.RLM(
    signature=SummarizeLongDocument,
    interpreter=interp,
    max_iterations=20,
    max_llm_calls=30,
    verbose=True,
)
result = rlm(document=doc, focus="key design decisions")
print(result.summary)
print(result.key_points)
```

### ❌ Incorrect — subscript on RLM result
```python
result = rlm(document=doc, focus="key design decisions")
print(result["summary"])  # Wrong: use result.summary
```

## Document Tool Usage (PDFs and Binary Docs)

For PDFs and binary documents, use the ReAct document tools (`load_document`,
`read_file_slice`). Do NOT use raw `read_text()` on binary files.

### ✅ Correct
```python
# Inside sandbox code — use document tools
result = interp.execute("""
doc = load_document('/home/daytona/memory/artifacts/report.pdf')
section = read_file_slice(doc, start=0, length=5000)
SUBMIT(content=section)
""")
```

### ❌ Incorrect — raw read_text on binary
```python
result = interp.execute("""
content = open('/home/daytona/memory/artifacts/report.pdf').read()
SUBMIT(content=content)
""")
```

## Entrypoint Selection

Use `fleet web` for workspace-first product work. Use `fleet-rlm serve-api`
only when you need the backend surface explicitly.

### ✅ Correct
```bash
# Workspace-first (default)
uv run fleet web

# Backend surface only
uv run fleet-rlm serve-api --port 8000
```

### ❌ Incorrect — always using serve-api for UI work
```bash
# Wrong: serve-api is not the workspace UI entrypoint
uv run fleet-rlm serve-api --port 8000  # for UI-only tasks
```

## Sub-Work Delegation

Long-context orchestration goes to `rlm-orchestrator`, runtime/integration
debugging to `rlm-specialist`, and leaf chunk analysis to `rlm-subcall`.

### ✅ Correct
```yaml
# Leaf chunk analysis delegation
subagent: rlm-subcall
input:
  chunk_path: /tmp/chunks/chunk_0001.txt
  query: "What modules does DSPy provide?"
  chunk_id: chunk_0001
```

### ❌ Incorrect — delegating everything to a single agent
```yaml
# Wrong: should delegate to rlm-orchestrator, not main rlm
subagent: rlm
input:
  task: "Process all 200 chunks and synthesize"
```
