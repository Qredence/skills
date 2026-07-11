# RLM Debug — Acceptance Criteria

Validates that generated debugging and diagnostic code follows the correct
patterns for diagnosing `daytona_pilot` failures, API/websocket contract
problems, and sandbox persistence issues.

## Pre-Debug Smoke Test

Always run `daytona-smoke` before debugging `daytona_pilot` failures. This
validates the Daytona environment is reachable and functional.

### ✅ Correct
```bash
uv run fleet-rlm daytona-smoke --repo <url> [--ref <branch>]
env | grep DAYTONA
```

### ❌ Incorrect — jumping straight to code changes
```bash
# Wrong: debugging runtime code without first verifying environment readiness
grep -r "DaytonaInterpreter" src/ | head -20
```

## DAYTONA_TARGET Usage

`DAYTONA_TARGET` is a target profile name, NOT a workspace ID or volume name.
Do not use it as a volume identifier.

### ✅ Correct
```bash
env | grep DAYTONA
# DAYTONA_TARGET=production   <- target profile name only
# DAYTONA_VOLUME_NAME=my-vol  <- separate volume identifier
```

### ❌ Incorrect — treating DAYTONA_TARGET as workspace/volume
```python
# Wrong: DAYTONA_TARGET is not a volume name
volume = os.environ["DAYTONA_TARGET"]
interp = DaytonaInterpreter(volume_name=volume)
```

## Durable Storage Path

Inspect durable storage under `/home/daytona/memory/{memory,artifacts,buffers,meta}`.
The live workspace is transient; do not look for persistent data there.

### ✅ Correct
```python
# Correct: inspect durable volume paths
result = interp.execute("""
import os
for d in ['memory', 'artifacts', 'buffers', 'meta']:
    path = f'/home/daytona/memory/{d}'
    exists = os.path.exists(path)
    print(f'{d}: {exists}')
SUBMIT(status='checked')
""")
```

### ❌ Incorrect — looking in transient workspace
```python
# Wrong: /workspace is transient, not where durable data lives
result = interp.execute("""
import os
files = os.listdir('/workspace/memory')
SUBMIT(files=files)
""")
```

## sandbox_output vs Canonical Stream

`sandbox_output` frames are transcript/debug traces. The canonical workbench
stream is `/api/v1/ws/execution`. Do not treat `sandbox_output` as the
primary data stream.

### ✅ Correct
```python
# Canonical stream for workbench output
# /api/v1/ws/execution  <- use this for workbench streaming
# sandbox_output frames <- debug/transcript only
```

### ❌ Incorrect — parsing sandbox_output as canonical
```python
# Wrong: sandbox_output is debug trace, not the canonical stream
for frame in websocket_frames:
    if frame["type"] == "sandbox_output":
        parse_final_result(frame["data"])  # Incorrect
```

## Contract Debugging — openapi.yaml

When symptoms involve the workspace UI, check the contract surfaces:
`openapi.yaml`, `/api/v1/runtime/*`, `/api/v1/ws/chat`, `/api/v1/ws/execution`.

### ✅ Correct
```bash
# Check openapi.yaml for contract drift after backend changes
diff openapi.yaml <(uv run fleet-rlm serve-api --export-openapi)

# Focus debugging on high-risk files
# src/fleet_rlm/api/routers/ws/stream.py
# src/fleet_rlm/api/routers/ws/turn_lifecycle.py
```

## Delegation for Cross-Runtime Debugging

Use `rlm-specialist` for cross-runtime debugging and architecture fixes.
Use `daytona-runtime` for Daytona-specific volume and execution issues.

### ✅ Correct
```yaml
# Route to the right specialist
- Cross-runtime / architecture fix → rlm-specialist
- Daytona volume / session → daytona-runtime
- Runtime mode mismatch → rlm-debug → rlm-specialist
```
