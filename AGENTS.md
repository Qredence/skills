# Agent Instructions: Qredence Skills Monorepo

This document provides comprehensive guidance for AI agents working in the Qredence Skills monorepo.

## Repository Overview

A centralized collection of agent skills designed for multiple AI ecosystems:
- **Claude Code** (`.claude-plugin/`, `.clauderules`)
- **Cursor** (`.cursor-plugin/`, `.cursorrules`)

Skills are domain-specific knowledge packages that enhance AI coding assistants with specialized expertise.

## Quick Reference Commands

```bash
# Package Management (ALWAYS use uv)
uv sync --dev                    # Install dependencies
uv add <package>                 # Add dependency
uv run python <script.py>        # Run Python script

# Code Quality (ALWAYS use ruff)
uv run ruff check .              # Lint
uv run ruff format .             # Format

# Skill Management
uv run python scripts/init_skill.py <name> --path skills/    # Create new skill
uv run python scripts/package_skill.py skills/<name>         # Validate & package
uv run python scripts/sync_plugins.py                        # Sync plugins

# Testing (from tests/ directory)
cd tests && pnpm install        # Install test dependencies
pnpm harness --list             # List available skills
pnpm harness <skill> --mock     # Run tests in mock mode
pnpm test                       # Run all tests
```

## Directory Structure

```
skills/                          # Single source of truth for skill definitions
├── fastapi-router-py/          # Example skill
│   ├── SKILL.md                # Required: skill definition with YAML frontmatter
│   ├── scripts/                # Optional: executable utilities
│   ├── references/             # Optional: detailed documentation
│   └── assets/                 # Optional: templates and static files

scripts/                         # Repository management utilities
├── init_skill.py               # Scaffold new skills
├── package_skill.py            # Validate and package skills
└── sync_plugins.py             # Sync symlinks to plugin directories

plugins/                         # Ecosystem-specific packaging (symlinks)
└── qredence-skills/            # Main plugin package

.agents/                         # Sub-agent definitions (Markdown + YAML frontmatter)
├── sub-agents/                 # Task-specific agents
│   ├── explorer.md             # Read-only code exploration
│   ├── tester.md               # Test execution
│   ├── implementer.md          # Code implementation
│   └── evaluator.md            # Skills evaluation
├── mcp/                        # MCP server configurations
└── skills/                     # Skill-specific agent configs

tests/                           # Microsoft skills testing harness
├── harness/                    # Evaluation framework
├── scenarios/                  # Test scenarios per skill
└── AGENTS.md                   # Testing-specific agent instructions

.github/
├── skills/                     # Skills with acceptance criteria
├── workflows/                  # CI/CD pipelines
└── CONTRIBUTING.md             # Contribution guidelines
```

## Development Workflows

### Creating a New Skill

1. **Scaffold the skill:**
   ```bash
   uv run python scripts/init_skill.py <skill-name> --path skills/
   ```

2. **Edit SKILL.md** with:
   - YAML frontmatter (`name`, `description`)
   - Usage instructions and examples
   - Reference links

3. **Add supporting files:**
   - `scripts/` - Executable utilities
   - `references/` - Detailed documentation
   - `assets/` - Templates and static files

4. **Validate and package:**
   ```bash
   uv run python scripts/package_skill.py skills/<skill-name>
   ```

### Packaging a Skill

The packaging script validates:
- Required `SKILL.md` exists
- YAML frontmatter has `name` and `description`
- Creates a `<name>.skill` zip archive

### Syncing Plugins

After creating or modifying skills, sync to plugin directories:
```bash
uv run python scripts/sync_plugins.py
```

## Skill Structure & Conventions

### Required: SKILL.md Format

```markdown
---
name: skill-name
description: One-line description of what this skill does.
---

# Skill Name

Brief overview and quick start instructions.

## Quick Start
...

## When to Use This Skill
...

## References
- [detailed-topic.md](references/detailed-topic.md)
```

### Standard Directories

| Directory | Purpose | Required |
|-----------|---------|----------|
| `SKILL.md` | Skill definition with frontmatter | Yes |
| `scripts/` | Executable Python/Shell utilities | No |
| `references/` | Detailed technical documentation | No |
| `assets/` | Templates, examples, static files | No |

### Naming Conventions

- Use kebab-case: `dspy-core`, `fastapi-router-py`
- Include language suffix when relevant: `-py`, `-ts`, `-go`
- Be specific: `azure-ai-projects-py` not `azure-ai`

## Sub-Agent System

The `.agents/sub-agents/` directory defines specialized agents for different tasks:

| Agent | Tools | Purpose |
|-------|-------|---------|
| **explorer** | Read, Grep, Glob | Locate files, symbols, imports; produce impact analysis |
| **tester** | Read, Bash, Glob, Grep | Run test harness, execute Vitest tests |
| **implementer** | Read, Write, Edit, Bash, Glob, Grep | Implement features, refactor code, create files |
| **evaluator** | Read, Glob, Grep | Analyze skill coverage, map scenarios to criteria |

### When to Use Each Agent

- **explorer**: Before making edits, to understand impact
- **tester**: After implementation, to verify changes
- **implementer**: When creating/modifying code
- **evaluator**: When assessing skill quality or coverage

### Tool Permissions Matrix

| Tool | explorer | tester | implementer | evaluator |
|------|:--------:|:------:|:-----------:|:---------:|
| Read | ✅ | ✅ | ✅ | ✅ |
| Glob | ✅ | ✅ | ✅ | ✅ |
| Grep | ✅ | ✅ | ✅ | ✅ |
| Bash | ❌ | ✅ | ✅ | ❌ |
| Write | ❌ | ❌ | ✅ | ❌ |
| Edit | ❌ | ❌ | ✅ | ❌ |

### Sandbox Mode Derivation

- Only `Read`, `Grep`, `Glob` → `read-only`
- Any `Write`, `Edit`, `Bash` → `allow-edits`

### Agent Format (Markdown + YAML Frontmatter)

```markdown
---
name: agent-name
description: >
  Multi-line description of the agent's purpose.
tools:
  - Read
  - Grep
  - Glob
---

# Agent Name

Detailed instructions in markdown...
```

## Code Quality Rules

### Python Package Management

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Package manager | `uv add <pkg>` | `pip install <pkg>` |
| Environment | `uv venv` | `python -m venv` |
| Run scripts | `uv run python script.py` | `python script.py` |

### Linting and Formatting

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Linter | `uv run ruff check .` | `flake8 .` |
| Formatter | `uv run ruff format .` | `black .` |
| Imports | ruff (auto-sorted) | `isort .` |

### Pre-commit Checklist

```bash
uv run ruff check .
uv run ruff format --check .
```

## Testing

### Microsoft Skills Harness

Located in `tests/`, the harness evaluates skill-generated code against acceptance criteria.

```bash
cd tests

# Install dependencies
pnpm install

# List available skills
pnpm harness --list

# Run tests for a skill
pnpm harness <skill-name> --mock --verbose

# Run specific scenario
pnpm harness <skill-name> --mock --filter <scenario-name>

# Run with Ralph Loop (iterative improvement)
pnpm harness <skill-name> --ralph --mock --max-iterations 5

# Run unit tests
pnpm test
```

### Acceptance Criteria Location

```
.github/skills/<skill-name>/references/acceptance-criteria.md
```

### Test Scenarios Location

```
tests/scenarios/<skill-name>/scenarios.yaml
```

For detailed testing instructions, see `tests/AGENTS.md`.

## Common Tasks

### Create a New Skill

```bash
uv run python scripts/init_skill.py my-new-skill --path skills/
# Edit skills/my-new-skill/SKILL.md
uv run python scripts/package_skill.py skills/my-new-skill
```

### Add Test Coverage for a Skill

1. Create acceptance criteria: `.github/skills/<name>/references/acceptance-criteria.md`
2. Create scenarios: `tests/scenarios/<name>/scenarios.yaml`
3. Verify: `cd tests && pnpm harness <name> --mock --verbose`

### Convert Agents to TOML (for Codex)

```bash
# Single agent
python3 skills/agent-converter/scripts/convert_agent.py .agents/sub-agents/explorer.md

# Batch convert
python3 skills/agent-converter/scripts/convert_agent.py --batch .agents/sub-agents/
```

### Run CI Checks Locally

```bash
uv sync --dev
uv run ruff check .
uv run ruff format --check .
```

## Important Notes

- **Branch Protection**: Main branch protection rules must be configured manually in GitHub UI
- **Plugin Manager**: The repository is designed to be managed by a `plugin-manager` skill
- **Monorepo Context**: Changes to root-level files (CI, scripts) should not break individual skills
