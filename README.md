# Fleet Skills — Agent Skills Collection

[![Python CI](https://github.com/Qredence/skills/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Qredence/skills/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository serves as a centralized collection of agent skills, designed to be compatible with multiple AI agent ecosystems including Claude Code and Cursor.

## Quick Start — Install a Skill

Install any skill directly from this repository using npx:

```bash
# Install a specific skill
npx skills add Qredence/skills/skills/fastapi-router-py

# Install globally
npx skills add -g Qredence/skills/skills/fastapi-router-py
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `fastapi-router-py` | FastAPI router utilities |
| `dspy-core` | DSPy core patterns |
| `dspy-development` | DSPy development workflows |
| `dspy-fleet-rlm` | DSPy fleet RLM integration |
| `dspy-gepa` | DSPy Gepa patterns |
| `dspy-optimization` | DSPy optimization techniques |
| `agent-converter` | Agent format converter |
| `babysit-pr` | PR babysitting automation |

## Repository Structure

```
skills/                  # Single source of truth for skill definitions
├── fastapi-router-py/  # Individual skill directories
├── dspy-core/
└── ...

plugins/                # Ecosystem-specific packaging
├── fleet-skills/       # Main plugin package
│   ├── .claude-plugin/
│   ├── .cursor-plugin/
│   ├── agents/         # Sub-agent definitions
│   └── skills/         # Symlinked skills

scripts/                # Management utilities
├── init_skill.py       # Scaffold new skills
├── package_skill.py    # Validate & package skills
└── sync_plugins.py     # Sync to plugin directories
```

## Creating a New Skill

```bash
uv run python scripts/init_skill.py <skill-name> --path skills/
```

This creates:
```
skills/<skill-name>/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Packaging a Skill

```bash
uv run python scripts/package_skill.py skills/<skill-name>
```

Generates a `<skill-name>.skill` zip archive if valid.

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines on creating and packaging skills.
