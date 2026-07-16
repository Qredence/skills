# Contributing

## Create a skill

```bash
uv run python scripts/init_skill.py my-new-skill
```

Edit `skills/figma-agent/my-new-skill/SKILL.md`. The directory name and frontmatter `name` must match and use kebab-case.

## Validate

```bash
uv run python scripts/validate_skills.py
uv run python tests/test_skills_catalog.py
uv run ruff check .
uv run ruff format --check .
```

Each installable skill is a single `SKILL.md`. Do not add a `SKILLS.md` duplicate.

Archived material belongs in `archive/` and must not include a `SKILL.md` file.
