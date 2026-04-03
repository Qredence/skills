# RLM Batch — Acceptance Criteria

Validates that generated batched/parallel RLM code uses the correct patterns
for the `daytona_pilot` runtime: `rlm_query_batched` inside sandbox code and
`ThreadPoolExecutor` + `DaytonaInterpreter` for host-side parallelism.

## Inside-Sandbox Batching — rlm_query_batched

When delegating concurrent sub-tasks from inside a running Daytona sandbox,
use `rlm_query_batched(queries, concurrency=N)` and return results with
`SUBMIT(...)`.

### ✅ Correct
```python
# Inside Daytona sandbox code (not host Python):
results = rlm_query_batched(
    [
        "summarize this chunk: ...",
        "extract errors from: ...",
        "identify patterns in: ...",
    ],
    concurrency=3,
)
SUBMIT(summaries=results)
```

### ❌ Incorrect — using parallel_semantic_map from Daytona path
```python
# Wrong: do not use parallel_semantic_map from the Daytona path
results = parallel_semantic_map(chunks, query="find errors")
SUBMIT(results=results)
```

## Host-Side Parallelism — ThreadPoolExecutor

For independent jobs requiring separate sandboxes, use
`ThreadPoolExecutor` with multiple `DaytonaInterpreter` instances.

### ✅ Correct
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from fleet_rlm.integrations.providers.daytona.interpreter import DaytonaInterpreter

def run_task(code):
    interp = DaytonaInterpreter(
        repo_url="https://github.com/your-org/your-repo",
        timeout=120,
    )
    interp.start()
    try:
        return interp.execute(code)
    finally:
        interp.shutdown()

tasks = ["SUBMIT(x=1)", "SUBMIT(x=2)", "SUBMIT(x=3)"]
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(run_task, t): i for i, t in enumerate(tasks)}
    for future in as_completed(futures):
        result = future.result()
```

### ❌ Incorrect — reusing the same interpreter across threads
```python
# Wrong: DaytonaInterpreter is not thread-safe; create one per thread
interp = DaytonaInterpreter(repo_url="...")
interp.start()
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(interp.execute, t) for t in tasks]
interp.shutdown()
```

## Worker Limit

Daytona has workspace concurrency limits. Start with 2–3 workers and increase
only if needed.

### ✅ Correct
```python
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(run_task, t) for t in tasks]
```

### ❌ Incorrect — unlimited workers
```python
# Wrong: could exhaust Daytona workspace concurrency limits
with ThreadPoolExecutor() as pool:  # max_workers unset
    futures = [pool.submit(run_task, t) for t in tasks]
```

## batch_concurrency Control

The `batch_concurrency` field on the websocket request controls allowed
parallelism for `rlm_query_batched`. Set it appropriately on the initial
request.

### ✅ Correct
```python
# Set batch_concurrency on the DaytonaInterpreter or the WS request
interp = DaytonaInterpreter(
    repo_url="https://github.com/your-org/your-repo",
    timeout=300,
)
# Controlled inside sandbox via rlm_query_batched(queries, concurrency=3)
```

## Durable Volume for Large Outputs

Write large batch outputs to the durable volume instead of passing through
`SUBMIT(...)`.

### ✅ Correct
```python
code = (
    "import json, os\n"
    "os.makedirs('/home/daytona/memory/artifacts', exist_ok=True)\n"
    "with open('/home/daytona/memory/artifacts/chunk_0.json', 'w') as f:\n"
    "    json.dump(results, f)\n"
    "SUBMIT(status='saved')"
)
```

### ❌ Incorrect — passing huge data through SUBMIT
```python
code = f"huge_data = {repr(large_list)}\nSUBMIT(results=huge_data)"
# Wrong: SUBMIT is not designed for megabytes of data
```
