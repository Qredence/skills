# Skill Evaluation Test Harness

TypeScript harness for discovering skills and evaluating skill-guided generation.

## Quick Start

```bash
cd tests
pnpm install
pnpm harness --list                                      # List active skills
pnpm harness figma-agent/accessibility-audit --mock --verbose
pnpm test                                                # Unit tests
```

> **Note:** If `pnpm` hooks fail in some environments, run binaries directly:
> `./node_modules/.bin/vitest run` and `./node_modules/.bin/tsx harness/runner.ts --list`.

## Overview

Active skills live at the **repository root** under package directories (currently `figma-agent/`). The harness:

1. Discovers `SKILL.md` / `SKILLS.md` under skill packages (excludes `archive/`)
2. Loads optional scenarios from `tests/scenarios/<skill-id>/scenarios.yaml`
3. Falls back to a smoke scenario when no scenario file exists
4. Generates code via the [GitHub Copilot SDK](https://github.com/github/copilot-sdk) (or mocks)
5. Scores output against optional acceptance criteria patterns

Skill IDs are hierarchical, e.g. `figma-agent/accessibility-audit`.

## Architecture

```text
tests/
├── harness/
│   ├── types.ts
│   ├── criteria-loader.ts    # Discovers skill documents
│   ├── evaluator.ts
│   ├── copilot-client.ts
│   ├── runner.ts             # CLI entry (pnpm harness)
│   ├── ralph-loop.ts
│   ├── feedback-builder.ts
│   ├── skill-catalog.test.ts
│   └── reporters/
├── scenarios/                # Optional per-skill scenarios
│   └── figma-agent/<skill>/scenarios.yaml
├── schemas/
│   └── skill-scenarios.schema.json
├── package.json
└── vitest.config.ts
```

## CLI Usage

```bash
pnpm harness <skill-id>

pnpm harness figma-agent/accessibility-audit \
    --mock \
    --verbose \
    --filter basic \
    --output json \
    --output-file report.json

# Ralph Loop (iterative improvement)
pnpm harness figma-agent/accessibility-audit \
    --ralph \
    --max-iterations 5 \
    --threshold 80 \
    --mock
```

## Adding scenarios for a skill

Scenarios are optional. Create:

```text
tests/scenarios/figma-agent/<skill-name>/scenarios.yaml
```

```yaml
config:
  model: gpt-4
  max_tokens: 2000
  temperature: 0.3

scenarios:
  - name: basic_usage
    prompt: |
      Summarize how this skill should be applied to a Figma selection.
    expected_patterns:
      - "selection"
    forbidden_patterns:
      - "TODO"
    tags:
      - basic
    mock_response: |
      # Mock response used in --mock mode
```

Then:

```bash
pnpm harness figma-agent/<skill-name> --mock --verbose
pnpm test
```

## Real SDK evaluation

### Local (Copilot CLI)

1. `npm install -g @github/copilot`
2. Authenticate with `/login`
3. Run without `--mock`

### CI / PAT

Set `GH_TOKEN` or `GITHUB_TOKEN` with **Copilot Requests** permission:

```bash
export GH_TOKEN="..."
pnpm harness figma-agent/accessibility-audit --verbose
```

## Real-LLM evaluation (LiteLLM)

From the repo root (alternative to Copilot SDK):

```bash
LITELLM_API_KEY="..." \
LITELLM_PROXY_URL="..." \
LITELLM_DEFAULT_MODEL="..." \
uv run python scripts/evaluate_skills_litellm.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No skills found | Ensure `figma-agent/<skill>/SKILLS.md` exists and you run from `tests/` or pass the repo root correctly |
| Archive skills appear | They should not; `archive/` is excluded from discovery |
| Copilot SDK unavailable | Use `--mock` or configure PAT auth |

See also [`AGENTS.md`](AGENTS.md) for agent-oriented testing instructions.
