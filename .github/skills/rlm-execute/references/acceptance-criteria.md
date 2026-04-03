# RLM Execute — Acceptance Criteria

Validates that generated Daytona sandbox execution code follows correct
lifecycle, persistence, and result-access patterns.

## Import and Configuration

Import `DaytonaInterpreter` from the correct module and always call
`configure_planner_from_env()` before instantiating the interpreter.

### ✅ Correct
```python
from fleet_rlm.runtime.config import configure_planner_from_env
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

configure_planner_from_env()

interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    timeout=600,
)
interp.start()
```

### ❌ Incorrect — missing configure call
```python
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

# Wrong: configure_planner_from_env() not called
interp = DaytonaInterpreter(repo_url="https://github.com/your-org/your-repo")
interp.start()
```

## Lifecycle — try/finally

Always wrap execution in a `try/finally` block and call `interp.shutdown()` in
the `finally` clause.

### ✅ Correct
```python
interp.start()
try:
    result = interp.execute("""
import math
SUBMIT(answer=math.factorial(15))
""")
    print(result.answer)
finally:
    interp.shutdown()
```

### ❌ Incorrect — no finally
```python
interp.start()
result = interp.execute("SUBMIT(answer=42)")
interp.shutdown()  # Skipped if execute() raises
```

## Result Access — Dot Notation

Access `FinalOutput` fields via dot notation. Subscript access is wrong.

### ✅ Correct
```python
result = interp.execute("SUBMIT(answer=42, items=['a', 'b'])")
print(result.answer)   # 42
print(result.items)    # ['a', 'b']
```

### ❌ Incorrect — subscript
```python
result = interp.execute("SUBMIT(answer=42)")
print(result["answer"])   # Wrong: FinalOutput is not subscriptable
```

## Durable Volume Persistence

Data written to `/home/daytona/memory/` persists across sessions when a
`volume_name` is provided. Do NOT store persistent data in `/tmp/`.

### ✅ Correct
```python
interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    volume_name="my-data",
    timeout=600,
)
interp.start()
try:
    interp.execute("""
import json, os
os.makedirs('/home/daytona/memory/artifacts', exist_ok=True)
with open('/home/daytona/memory/artifacts/results.json', 'w') as f:
    json.dump({"processed": True}, f)
SUBMIT(status='saved')
""")
finally:
    interp.shutdown()
```

### ❌ Incorrect — storing in /tmp
```python
# Wrong: /tmp is ephemeral and not part of the durable volume
interp.execute("""
with open('/tmp/results.json', 'w') as f:
    json.dump({"processed": True}, f)
""")
```

## SUBMIT Usage

Use `SUBMIT(**kwargs)` to return structured results from sandbox code. Always
include it at the end of code that produces output.

### ✅ Correct
```python
result = interp.execute("""
import math
factorial = math.factorial(15)
SUBMIT(answer=factorial, computed=True)
""")
print(result.answer)
```

### ❌ Incorrect — relying on print instead of SUBMIT
```python
# Wrong: print() output is available as str but not as structured FinalOutput
result = interp.execute("import math; print(math.factorial(15))")
print(result.answer)  # AttributeError: str has no attribute 'answer'
```

## Buffer Usage

`add_buffer` / `get_buffer` persist named lists within a single sandbox
session. They do not persist across sessions.

### ✅ Correct
```python
interp.execute('add_buffer("findings", "step 1 complete")')
interp.execute('add_buffer("findings", "step 2 complete")')
result = interp.execute('SUBMIT(log=get_buffer("findings"))')
print(result.log)  # ["step 1 complete", "step 2 complete"]
```

### ❌ Incorrect — expecting buffers to persist across sessions
```python
# New interpreter instance — buffers from previous session are gone
interp2 = DaytonaInterpreter(repo_url="...")
interp2.start()
try:
    result = interp2.execute('SUBMIT(log=get_buffer("findings"))')
    # Wrong expectation: will return [] not the previous session's buffer
finally:
    interp2.shutdown()
```
