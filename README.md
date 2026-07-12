# Qredence Skills

Practical Figma design and product skills for AI agents.

## Quickstart (30 seconds)

Install the skills you want with [`skills.sh`](https://www.skills.sh/docs):

```bash
npx skills@latest add qredence/skills
```

Choose skills from the Figma catalogue, then choose the agents where you want them installed.

## Browse the catalogue

The active collection lives in [`skills/figma-agent/`](skills/figma-agent/). It includes skills for accessibility, design systems, components, prototyping, research, content, and developer handoff.

Start with:

- [`accessibility-audit`](skills/figma-agent/accessibility-audit/)
- [`component-audit`](skills/figma-agent/component-audit/)
- [`design-tokens-sync`](skills/figma-agent/design-tokens-sync/)
- [`figma-to-code-component`](skills/figma-agent/figma-to-code-component/)
- [`prototype-from-flow`](skills/figma-agent/prototype-from-flow/)
- [`dev-handoff-prep`](skills/figma-agent/dev-handoff-prep/)

## Use a skill in Figma

Each package exposes the same skill in two formats:

- `SKILL.md` is the canonical document installed by `skills.sh`.
- `SKILLS.md` is the byte-identical Figma upload document. In Figma Design Agents, use **Add skill** and upload it directly.

## Contributing

See [AGENTS.md](AGENTS.md) and [the contribution guide](.github/CONTRIBUTING.md) for the creation and validation workflow.

Historical, non-installable material is retained in [`archive/`](archive/).

## License

[MIT](LICENSE)
