# Qredence's Collection of Agent Skills

[![Python CI](https://github.com/Qredence/skills/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Qredence/skills/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository serves as a centralized collection of agent skills, designed to be compatible with multiple AI agent ecosystems including Claude Code and Cursor.

## Installation

You can install any skill from this repository using the `skills.sh` CLI. Since this is a monorepo containing multiple skills, you need to specify the path to the specific skill you want to install.

For example, to install the `fastapi-router-py` skill from this repository:

```bash
npx skills add Qredence/skills/skills/fastapi-router-py
```

Or globally:

```bash
npx skills add -g Qredence/skills/skills/fastapi-router-py
```

## Repository Structure

- `skills/`: The single source of truth for all raw skill definitions. Each skill is contained in its own directory.
- `plugins/`: Ecosystem-specific packaging and symlinks.
- `scripts/`: Management utilities for creating, validating, and packaging skills.
- `.claude-plugin/`: Claude Code marketplace manifests.
- `.cursor-plugin/`: Cursor marketplace manifests.

For detailed guidelines on how to contribute or create new skills, please see our [Contributing Guide](.github/CONTRIBUTING.md).

## Creating a New Skill

You can scaffold a new skill using the provided utility script. This ensures the skill follows the correct directory structure and includes the required `SKILL.md` format.

```bash
uv run python scripts/init_skill.py <skill-name> --path skills/
```

This will create:
```
skills/<skill-name>/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Packaging a Skill

To validate a skill's structure and package it for distribution, use the packaging script:

```bash
uv run python scripts/package_skill.py skills/<skill-name>
```

This will generate a `<skill-name>.skill` zip archive if the skill is valid.

## Plugin Manager

The repository is designed to be managed by a `plugin-manager` skill, which can handle wiring marketplace manifests, setting up skill symlinks, and assigning per-plugin configurations.

## Important Note for Maintainers

> **Branch Protection**: Branch protection rules for the `main` branch (such as requiring pull request reviews or passing status checks) must be configured manually in the GitHub UI. They cannot be set automatically via files in this repository.
