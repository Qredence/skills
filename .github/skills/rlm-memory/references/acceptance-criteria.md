# RLM Memory — Acceptance Criteria

Validates that generated memory/persistence code uses the correct Daytona
durable volume paths, directory structure, and buffer patterns.

## Volume Root Path

All durable storage lives under `/home/daytona/memory/` inside the sandbox.
Never store persistent data in `/tmp/` or other ephemeral paths.

### ✅ Correct
```python
import json, os
os.makedirs('/home/daytona/memory/artifacts', exist_ok=True)
with open('/home/daytona/memory/artifacts/analysis.json', 'w') as f:
    json.dump({'result': 'my-finding'}, f)
```

### ❌ Incorrect — /tmp is ephemeral
```python
# Wrong: /tmp is ephemeral and NOT part of the durable volume
with open('/tmp/analysis.json', 'w') as f:
    json.dump({'result': 'my-finding'}, f)
```

## Canonical Directory Structure

Use the canonical subdirectories for their intended purposes.

### ✅ Correct
```python
# memory/   — key-value and named memory items
# artifacts/ — produced outputs and saved results
# buffers/   — named buffer lists (session logs, staging)
# meta/      — session manifests and workspace metadata

os.makedirs('/home/daytona/memory/memory', exist_ok=True)
os.makedirs('/home/daytona/memory/artifacts', exist_ok=True)
os.makedirs('/home/daytona/memory/buffers', exist_ok=True)
os.makedirs('/home/daytona/memory/meta', exist_ok=True)
```

### ❌ Incorrect — arbitrary directory names
```python
# Wrong: use canonical dirs, not arbitrary names
os.makedirs('/home/daytona/memory/my_custom_dir', exist_ok=True)
os.makedirs('/home/daytona/memory/outputs', exist_ok=True)
```

## Structured Data — json.dump / json.load

Use `json.dump` / `json.load` for structured data persistence. Do not use
pickle or raw text for structured objects.

### ✅ Correct
```python
import json

# Write
with open('/home/daytona/memory/artifacts/data.json', 'w') as f:
    json.dump({'key': 'value', 'count': 42}, f)

# Read
with open('/home/daytona/memory/artifacts/data.json') as f:
    data = json.load(f)
```

### ❌ Incorrect — pickle for structured data
```python
import pickle
# Wrong: use json for structured data persistence
with open('/home/daytona/memory/artifacts/data.pkl', 'wb') as f:
    pickle.dump({'key': 'value'}, f)
```

## Buffer Pattern

`add_buffer` / `get_buffer` persist named lists within a single sandbox
session only. They do not persist across sessions.

### ✅ Correct
```python
# Buffers persist within a single sandbox session
interp.execute('add_buffer("log", "Step 1: setup")')
interp.execute('add_buffer("log", "Step 2: done")')
result = interp.execute('SUBMIT(log=get_buffer("log"))')
print(result.log)  # ["Step 1: setup", "Step 2: done"]
```

### ❌ Incorrect — using buffers for cross-session persistence
```python
# Wrong: buffers do NOT persist across sessions
# Use /home/daytona/memory/ with json.dump for cross-session persistence
```

## Session Manifest Path

Session manifests live at a specific canonical path structure.

### ✅ Correct
```python
# Canonical path:
# /home/daytona/memory/meta/workspaces/<ws_id>/users/<user_id>/react-session-<session_id>.json
manifest_path = (
    f'/home/daytona/memory/meta/workspaces/{ws_id}'
    f'/users/{user_id}/react-session-{session_id}.json'
)
```

### ❌ Incorrect — wrong manifest path
```python
# Wrong: manifest must be under meta/workspaces/, not directly under meta/
manifest_path = f'/home/daytona/memory/meta/session-{session_id}.json'
```

## Volume Name for Cross-Session Persistence

Provide a `volume_name` when creating the `DaytonaInterpreter` to attach the
same durable volume across sessions.

### ✅ Correct
```python
interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    volume_name="rlm-volume-dspy",  # Same name = same durable volume
    timeout=120,
)
```

### ❌ Incorrect — different volume names each session
```python
import uuid
interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    volume_name=f"vol-{uuid.uuid4()}",  # Wrong: new volume every session
)
```
