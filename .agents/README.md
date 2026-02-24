# Agent Configuration Directory

This directory contains specialized sub-agent configurations for different tasks. Agents are defined in **Markdown format with YAML frontmatter**, which provides rich tool restrictions and formatting.

Use the `agent-converter` skill to convert these to TOML format for Codex agents.

## Structure

```
.agents/
├── sub-agents/           # Task-specific agent definitions
│   ├── explorer.md       # Read-only code exploration
│   ├── tester.md         # Test execution
│   ├── implementer.md    # Code implementation
│   └── evaluator.md      # Skills evaluation
└── README.md             # This file
```

## Converting to TOML

To convert agents for Codex:

```bash
# Convert single agent
python3 skills/agent-converter/scripts/convert_agent.py .agents/sub-agents/explorer.md

# Convert all agents
python3 skills/agent-converter/scripts/convert_agent.py --batch .agents/sub-agents/
```

## Agent Reference

| Agent | Tools | Purpose |
|-------|-------|---------|
| **explorer** | Read, Grep, Glob | Locate files, symbols, imports; produce impact analysis |
| **tester** | Read, Bash, Glob, Grep | Run Microsoft skills harness, execute Vitest tests |
| **implementer** | Read, Write, Edit, Bash, Glob, Grep | Implement features, refactor code, create files |
| **evaluator** | Read, Glob, Grep | Analyze skill coverage, map scenarios to criteria |

## Markdown Format

All agents use Markdown with YAML frontmatter:

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

Detailed instructions in markdown...
```

## Tool Permissions

| Tool | Read-Only Agents | Edit Agents |
|------|------------------|-------------|
| Read | ✅ | ✅ |
| Glob | ✅ | ✅ |
| Grep | ✅ | ✅ |
| Bash | ❌ | ✅ |
| Write | ❌ | ✅ |
| Edit | ❌ | ✅ |

**Sandbox mode is derived from tools:**
- Only `Read`, `Grep`, `Glob` → `read-only`
- Any `Write`, `Edit`, `Bash` → `allow-edits`

## Usage

These agents are invoked automatically by the orchestration system based on task requirements. The `developer_instructions` field (TOML) or markdown body (MD) provides context and constraints for each agent type.

## Integration with Microsoft Skills Framework

The **tester** and **evaluator** agents are designed to work with the Microsoft skills testing framework in `tests/`:

- **tester**: Runs `bun run harness` commands and Vitest tests
- **evaluator**: Analyzes acceptance criteria and scenario coverage

See `tests/AGENTS.md` for detailed testing harness documentation.