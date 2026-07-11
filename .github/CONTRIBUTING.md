# Contributing to Qredence Skills

Thank you for contributing. We welcome new skills, improvements to existing ones, and tooling upgrades.

## Development environment

- **Python:** [uv](https://github.com/astral-sh/uv) + **ruff**
- **Tests:** Node.js 20+ and **pnpm** (under `tests/`)

### Setup

```bash
# Install uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --dev
cd tests && pnpm install
```

### Code quality

```bash
uv run ruff check .
uv run ruff format --check .
cd tests && pnpm test
```

## Creating a new skill

Active Figma skills live under `figma-agent/`:

```bash
uv run python scripts/init_skill.py my-new-skill --path figma-agent/
```

1. Edit `figma-agent/my-new-skill/SKILLS.md` (or `SKILL.md` for generic skills).
2. Use YAML frontmatter with at least `name` and `description`.
3. Package/validate:

```bash
uv run python scripts/package_skill.py figma-agent/my-new-skill
```

For Figma Design Agents, upload the skill’s `SKILLS.md` via **Add skill**.

## Optional test scenarios

```text
tests/scenarios/figma-agent/<skill-name>/scenarios.yaml
```

```bash
cd tests
pnpm harness figma-agent/<skill-name> --mock --verbose
```

## Pull request process

1. Branch from `main`.
2. Keep changes focused; update docs when layout or commands change.
3. Run ruff + harness unit tests locally.
4. Open a PR and fill out the template.

## Conventions

- **Always use `uv`** for Python (not bare `pip` / `venv`).
- **Always use `ruff`** for lint/format.
- Skill packages live at the repo root (`figma-agent/`, etc.); `archive/` is historical only.
- Main skill documents: `SKILLS.md` (Figma-native) or `SKILL.md` (generic).
- Use kebab-case skill directory names.

Thank you for contributing!
