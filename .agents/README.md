# Agent Configuration Directory

Specialized sub-agent configs for this monorepo. Agents use **Markdown + YAML frontmatter** (tool lists and rich instructions).

## Structure

```text
.agents/
├── sub-agents/           # Task-specific agent definitions (optional)
├── mcp/                  # MCP server configs (optional)
├── skills/               # Skill-specific agent configs (optional)
└── README.md
```

## Converting to TOML (Codex)

The converter lives in the archive:

```bash
python3 archive/agent-converter/scripts/convert_agent.py .agents/sub-agents/explorer.md
python3 archive/agent-converter/scripts/convert_agent.py --batch .agents/sub-agents/
```

## Typical agent roles

| Agent | Tools | Purpose |
|-------|-------|---------|
| **explorer** | Read, Grep, Glob | Locate files, symbols, imports; impact analysis |
| **tester** | Read, Bash, Glob, Grep | Run harness and Vitest |
| **implementer** | Read, Write, Edit, Bash, Glob, Grep | Implement features and refactors |
| **evaluator** | Read, Glob, Grep | Skill coverage and scenario mapping |

## Markdown format

```markdown
---
name: agent-name
description: >
  Multi-line description of the agent.
tools:
  - Read
  - Grep
  - Glob
---

# Agent Name

Detailed instructions...
```

## Tool permissions

| Tool | Read-Only Agents | Edit Agents |
|------|------------------|-------------|
| Read | ✅ | ✅ |
| Glob | ✅ | ✅ |
| Grep | ✅ | ✅ |
| Bash | ❌ | ✅ |
| Write | ❌ | ✅ |
| Edit | ❌ | ✅ |

**Sandbox mode:** only `Read`/`Grep`/`Glob` → read-only; any `Write`/`Edit`/`Bash` → allow-edits.

## Testing integration

Tester/evaluator agents use the harness under `tests/`. See `tests/AGENTS.md` and the root `README.md`.
