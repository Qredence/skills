# Qredence Skills

[![Python CI](https://github.com/Qredence/skills/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Qredence/skills/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A monorepo of **agent skills** — focused knowledge packages that guide AI coding and design agents. The active collection targets **Figma Design Agents**; packaging hooks remain for Claude Code and Cursor.

## What’s here

| Location | Status | Description |
|----------|--------|-------------|
| [`figma-agent/`](figma-agent/) | **Active** | 54 Figma Design Agent skills (`SKILLS.md` each) |
| [`archive/`](archive/) | Archived | Older RLM / agent-converter skills (not discovered by tooling) |
| [`scripts/`](scripts/) | Tooling | Scaffold, package, plugin sync, LiteLLM evaluator |
| [`tests/`](tests/) | Tooling | TypeScript evaluation harness (pnpm + Vitest) |

## Use a Figma skill

Each skill is a single markdown file ready for Figma Design Agents:

1. Open `figma-agent/<skill-name>/SKILLS.md`.
2. In Figma Design Agents, use **Add skill** and paste or upload that file.
3. Invoke the skill when its description matches your task (audits, tokens, handoff, workshops, etc.).

### Skill domains (examples)

Browse the full set under [`figma-agent/`](figma-agent/). Names group roughly as:

| Domain | Examples |
|--------|----------|
| Accessibility & QA | `accessibility-audit`, `visual-consistency-check`, `states-completeness-check`, `responsive-breakpoint-check` |
| Tokens & design system | `design-tokens-sync`, `semantic-color-audit`, `spacing-scale-enforcer`, `legacy-styles-to-variables` |
| Components & code | `component-audit`, `figma-to-code-component`, `code-connect-mapper`, `shadcn-component-structure`, `cva-variant-generator` |
| Prototyping & motion | `prototype-from-flow`, `wire-up-interactions`, `motion-spec-generator`, `prototype-qa` |
| Research & workshops | `persona-builder`, `journey-map-builder`, `affinity-mapping`, `workshop-facilitator`, `heuristic-evaluation` |
| Content & localization | `microcopy-generator`, `content-tone-review`, `localization-readiness` |
| Handoff & review | `dev-handoff-prep`, `handoff-summary`, `branch-review-summary`, `design-crit` |
| File hygiene | `file-cleanup`, `naming-convention-enforcer`, `rename-layers-batch`, `library-health-report` |

## Repository layout

```text
figma-agent/          Active Figma skills (one SKILLS.md per skill)
archive/              Historical skills (excluded from discovery)
scripts/              init / package / sync / LiteLLM eval
tests/                Evaluation harness + optional scenarios
plugins/              Reserved for ecosystem packaging (empty for now)
.agents/              Sub-agent configs
.github/              CI, CONTRIBUTING, issue templates
```

Skill IDs used by tooling are hierarchical, e.g. `figma-agent/accessibility-audit`.

Active Figma skills use **`SKILLS.md`**. Scaffolding for generic skills may still create **`SKILL.md`**. The harness accepts either name.

## Development

### Prerequisites

- [uv](https://github.com/astral-sh/uv) (Python 3.13+)
- Node.js + [pnpm](https://pnpm.io/) (for the test harness)

### Setup

```bash
uv sync --dev
cd tests && pnpm install
```

### Quality

```bash
uv run ruff check .
uv run ruff format --check .
```

### Create a skill

```bash
# Default path is figma-agent/
uv run python scripts/init_skill.py my-new-skill

# Or an explicit path
uv run python scripts/init_skill.py my-new-skill --path figma-agent/
```

Then edit the generated skill document (rename to `SKILLS.md` for Figma-native skills if needed).

### Package a skill

```bash
uv run python scripts/package_skill.py figma-agent/<skill-name>
```

### Test harness

```bash
cd tests
pnpm harness --list
pnpm harness figma-agent/accessibility-audit --mock --verbose
pnpm test
```

### Optional: real-LLM evaluation

```bash
LITELLM_API_KEY="..." \
LITELLM_PROXY_URL="..." \
LITELLM_DEFAULT_MODEL="..." \
uv run python scripts/evaluate_skills_litellm.py
```

## Contributing

See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for guidelines.

For agent-oriented repo instructions, see [`AGENTS.md`](AGENTS.md).

## Security

See [`SECURITY.md`](SECURITY.md).

## License

[MIT](LICENSE)
