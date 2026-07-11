# Test Harness Agent Instructions

This folder contains a test harness for evaluating skill-guided generation against active skills in the monorepo.

## Quick Context

**What we test:** Active skill packages at the repo root (currently `../figma-agent/`).

**How it works:**
1. Each active skill has a `SKILL.md` or `SKILLS.md` document
2. Optional **scenarios** prompt generation and validate output patterns
3. Skills without scenarios get a default smoke scenario
4. Archived skills under `../archive/` are **excluded** from discovery
5. For real-LLM evaluation without Copilot SDK, use `../scripts/evaluate_skills_litellm.py`

## Current State

| Surface | Source | Evaluation |
|---------|--------|------------|
| Active skills | `../figma-agent/<name>/SKILLS.md` | Discoverable (`figma-agent/<name>`) |
| Targeted checks | `tests/scenarios/figma-agent/<name>/scenarios.yaml` | Optional |
| Skills without scenarios | Skill document only | Smoke scenario |
| Archive | `../archive/` | Excluded |

Run `pnpm harness --list` from `tests/` (or `./node_modules/.bin/tsx harness/runner.ts --list`) to list active skills (~54 Figma skills).

---

## Task: Add Test Coverage for a Skill

### Step 1: Confirm the skill is discoverable

```bash
cd tests
pnpm harness --list | grep figma-agent/<skill-name>
```

### Step 2: Create optional scenarios

**Location:** `tests/scenarios/figma-agent/<skill-name>/scenarios.yaml`

```yaml
config:
  model: gpt-4
  max_tokens: 2000
  temperature: 0.3

scenarios:
  - name: scenario_name
    prompt: |
      Clear instruction for what the agent should produce.
    expected_patterns:
      - "Pattern that MUST appear"
    forbidden_patterns:
      - "Pattern that must NOT appear"
    tags:
      - basic
    mock_response: |
      # Complete working mock response
```

**Scenario design principles:**
- Each scenario tests one specific behavior
- Prefer Figma/design-agent outcomes over unrelated code SDK patterns
- `mock_response` must pass when using `--mock`

### Step 3: Verify

```bash
cd tests
pnpm harness figma-agent/<skill-name> --mock --verbose
pnpm harness figma-agent/<skill-name> --mock --filter scenario_name
pnpm test
```

---

## File Structure

```text
tests/
├── harness/
│   ├── criteria-loader.ts    # Discovers skill documents at repo root
│   ├── copilot-client.ts
│   ├── evaluator.ts
│   ├── runner.ts
│   ├── ralph-loop.ts
│   ├── skill-catalog.test.ts
│   └── reporters/
├── scenarios/                # Optional
│   └── figma-agent/<skill>/scenarios.yaml
├── schemas/
│   └── skill-scenarios.schema.json
├── package.json
└── README.md
```

---

## Commands Cheat Sheet

```bash
# From tests/
./node_modules/.bin/tsx harness/runner.ts --list
./node_modules/.bin/tsx harness/runner.ts figma-agent/accessibility-audit --mock --verbose
./node_modules/.bin/vitest run

# Ralph loop
./node_modules/.bin/tsx harness/runner.ts figma-agent/accessibility-audit --ralph --mock --max-iterations 5
```

## Real-LLM evaluation

```bash
# From repo root
LITELLM_API_KEY="..." LITELLM_PROXY_URL="..." LITELLM_DEFAULT_MODEL="..." \
  uv run python scripts/evaluate_skills_litellm.py figma-agent/accessibility-audit
```
