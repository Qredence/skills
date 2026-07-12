# Contributing

## Create a skill

```bash
uv run python scripts/init_skill.py my-new-skill
```

Edit `skills/figma-agent/my-new-skill/SKILL.md`. The directory name and frontmatter `name` must match and use kebab-case. Then generate the Figma upload document:

```bash
uv run python scripts/sync_figma_documents.py
```

## Validate

```bash
uv run python scripts/sync_figma_documents.py --check
uv run python scripts/validate_skills.py
uv run python tests/test_skills_catalog.py
uv run ruff check .
uv run ruff format --check .
```

`SKILL.md` is the skills.sh source of truth. `SKILLS.md` is generated for Figma Design Agents and must remain byte-identical.

Archived material belongs in `archive/` and must not include a `SKILL.md` file.
