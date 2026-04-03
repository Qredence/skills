# RLM Long-Context — Acceptance Criteria

Validates that generated long-context processing code uses the correct
experimental scripts, delegation patterns, and synthesis approach.

> **Note:** This is an EXPERIMENTAL skill. For production use, prefer the
> `rlm` skill with the fleet-rlm package and Daytona sandboxes.

## Chunking Scripts

Use the provided scripts for chunking — do not hand-roll chunking logic.

### ✅ Correct
```bash
# Query-guided chunk selection (5-10x speedup)
python3 scripts/rank_chunks.py --query "find all timeout errors" --top-k 10

# Content-aware semantic chunking
python3 scripts/semantic_chunk.py --state .claude/rlm_state/state.pkl

# Codebase concatenation
python3 scripts/codebase_concat.py --root ./src --output codebase.txt
```

### ❌ Incorrect — fixed-size without overlap for structured data
```python
# Wrong: fixed-size chunking without boundaries for structured data
chunks = [content[i:i+200000] for i in range(0, len(content), 200000)]
# Missing: semantic boundary detection and overlap
```

## rlm-subcall Delegation

Delegate each selected chunk to `rlm-subcall` with `chunk_path`, `query`, and
`chunk_id`. Never paste entire chunks into main chat context.

### ✅ Correct
```yaml
subagent: rlm-subcall
input:
  query: "Find all ERROR entries and their timestamps"
  chunk_path: ".claude/rlm_state/chunks/chunk_001.txt"
  chunk_id: "chunk_001"
  format: "json"
```

### ❌ Incorrect — pasting chunks into main context
```python
# Wrong: causes context overflow
for chunk in chunks:
    response = main_agent.chat(f"Analyze this: {chunk}")  # DO NOT DO THIS
```

## rlm-subcall Return Format

`rlm-subcall` returns a JSON object with `relevant`, `missing`, and
`suggested_queries` fields. Filter by `high`/`medium` confidence.

### ✅ Correct
```python
# Expected response structure from rlm-subcall
{
    "chunk_id": "chunk_001",
    "relevant": [
        {"point": "...", "evidence": "...", "confidence": "high"}
    ],
    "missing": ["what could not be determined"],
    "suggested_queries": ["follow-up questions"]
}

# Filter during synthesis
findings = []
for r in all_results:
    for item in r.get('relevant', []):
        if item['confidence'] in ('high', 'medium'):
            findings.append(item)
```

### ❌ Incorrect — including low confidence results
```python
# Wrong: including low-confidence results pollutes synthesis
all_points = [item for r in all_results for item in r.get('relevant', [])]
# Missing confidence filter
```

## No Spawning Subagents from Subagents

Orchestration stays in the main agent. Never spawn `rlm-subcall` from within
another `rlm-subcall` — this causes exponential resource consumption.

### ✅ Correct
```
Main Agent (Orchestrator)
  └── rlm-subcall (chunk A)
  └── rlm-subcall (chunk B)
  └── rlm-subcall (chunk C)
```

### ❌ Incorrect — nested subagent spawning
```
rlm-subcall (chunk A)
  └── rlm-subcall (chunk A.1)  ← NEVER do this
  └── rlm-subcall (chunk A.2)
```

## Query-Guided Selection First

Before processing all chunks, use `rank_chunks.py` to filter by relevance.
Only process the top-K relevant chunks.

### ✅ Correct
```bash
python3 scripts/rank_chunks.py --query "timeout error" --top-k 10 -o relevant_chunks.txt
# Process only the 10 most relevant chunks, skip the rest
```

### ❌ Incorrect — processing all chunks regardless of relevance
```python
# Wrong: wastes resources when query is specific
for chunk_path in all_chunk_paths:  # Could be 200+ chunks
    delegate_to_rlm_subcall(chunk_path)
```

## EXPERIMENTAL Label

When generating code or documentation for this skill, always mark it as
EXPERIMENTAL and recommend `rlm` for production use.

### ✅ Correct
```python
# EXPERIMENTAL: Using rlm-long-context scripts for research/evaluation.
# For production use, prefer the rlm skill with fleet-rlm + Daytona.
```
