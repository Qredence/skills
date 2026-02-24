# Contributing to Qredence Skills

Thank you for your interest in contributing to Qredence Skills! We welcome contributions of new skills, improvements to existing ones, and enhancements to our tooling.

## Development Environment

We use **[uv](https://github.com/astral-sh/uv)** as our primary Python package and environment manager, and **ruff** for linting and formatting.

### Setup

1. Install `uv` if you haven't already: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone the repository.
3. Install dependencies: `uv sync --dev`

### Code Quality

Before submitting a pull request, ensure your code passes our quality checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

We use GitHub Actions to enforce these checks on all PRs.

## Creating a New Skill

1. Use our scaffold script to generate the correct directory structure:
   ```bash
   uv run python scripts/init_skill.py <skill-name> --path skills/
   ```
2. Develop your skill in the newly created `skills/<skill-name>/` directory.
3. Update the `SKILL.md` file with relevant information, examples, and tool descriptions.

## Packaging a Skill

To validate a skill's structure and package it:

```bash
uv run python scripts/package_skill.py skills/<skill-name>
```

## Pull Request Process

1. Create a new branch from `main` (`git checkout -b feature/your-feature`).
2. Make your changes, following the style guidelines.
3. Run the tests/linters locally.
4. Push to your fork and submit a Pull Request.
5. Fill out the provided Pull Request template.

## Rules and Conventions

- **Always use `uv`**: Do not use `pip`, `poetry`, or `venv` directly.
- **Strict Linting**: Address all `ruff` warnings. If a rule must be ignored (e.g. for incomplete template files), use `# noqa: <RULE>` with a comment explaining why.
- **Skill Structure**: All skills must be contained in their own directory under `skills/` and must include a valid `SKILL.md` file.

Thank you for contributing!
