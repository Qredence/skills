# Qredence Skills Repository

## Active catalogue

Installable skills live under `skills/figma-agent/<skill-name>/`.

- `SKILL.md` is the only skill document. It is installed by `skills.sh`.
- `archive/` is documentation only. It must never contain `SKILL.md`.
- Do not add duplicate upload documents (`SKILLS.md`) or plugin-manager stubs.

## Create or update a skill

```bash
uv run python scripts/init_skill.py my-new-skill
# edit skills/figma-agent/my-new-skill/SKILL.md
```

Use kebab-case names. Keep `name` and `description` in YAML frontmatter; `name` must match the directory name.

## Validation

```bash
uv run python scripts/validate_skills.py
uv run python tests/test_skills_catalog.py
uv run ruff check .
uv run ruff format --check .
```

Before releasing a catalogue change, verify remote discovery from a clean directory:

```bash
npx skills@latest add qredence/skills --list
```

Only active Figma skills should appear.

## Repository conventions

- Use `uv` for Python commands and `ruff` for formatting and linting.
- Keep README content user-focused; put maintenance details in this file.
- Do not add plugin-manager stubs, duplicate agent rules, or archived `SKILL.md` files.
