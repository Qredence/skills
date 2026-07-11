# Agent Format Specification

This document describes the two supported agent definition formats.

## Markdown Format (`.md`)

Uses YAML frontmatter followed by markdown content.

### Structure

```markdown
---
name: agent-name
description: >
  Multi-line description of the agent's purpose.
  Can span multiple lines using the > syntax.
tools:
  - Read
  - Grep
  - Glob
---

# Agent Title

Markdown content with detailed instructions...
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier for the agent |
| `description` | string | Brief description of the agent's role |
| `tools` | list | Allowed tools for this agent |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Format version |
| `author` | string | Agent author |

### Tool Values

| Tool | Permission Type |
|------|-----------------|
| `Read` | Read-only |
| `Glob` | Read-only |
| `Grep` | Read-only |
| `Write` | Edit |
| `Edit` | Edit |
| `Bash` | Edit |

## TOML Format (`.toml`)

Simple key-value format for Codex-style agents.

### Structure

```toml
sandbox_mode = "read-only"

developer_instructions = """
Role: Description of the agent.

Tools: Read, Grep, Glob

---

Detailed instructions in plain text...
"""
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `sandbox_mode` | string | Either `"read-only"` or `"allow-edits"` |
| `developer_instructions` | string | Multi-line instructions for the agent |

### Sandbox Modes

| Mode | Description |
|------|-------------|
| `read-only` | Agent can only read files, no modifications |
| `allow-edits` | Agent has full read/write permissions |

## Conversion Rules

### Tools → Sandbox Mode

```python
if tools ⊆ {Read, Grep, Glob}:
    sandbox_mode = "read-only"
else:
    sandbox_mode = "allow-edits"
```

### Sandbox Mode → Tools

```python
if sandbox_mode == "read-only":
    tools = [Read, Grep, Glob]
else:
    tools = [Read, Write, Edit, Bash, Glob, Grep]
```

### Description Handling

- MD `description` → Prepended to TOML `developer_instructions` as "Role:"
- TOML instructions starting with "Role:" → Extracted to MD `description`

## Examples

### Read-Only Agent (MD)

```markdown
---
name: explorer
description: >
  Read-only codebase explorer for locating files
  and producing impact analysis.
tools:
  - Read
  - Grep
  - Glob
---

# Explorer

You are a read-only explorer agent...
```

### Read-Only Agent (TOML)

```toml
sandbox_mode = "read-only"

developer_instructions = """
Role: Read-only codebase explorer for locating files and producing impact analysis.

Tools: Read, Grep, Glob

---

# Explorer

You are a read-only explorer agent...
"""
```

### Edit Agent (MD)

```markdown
---
name: implementer
description: Code implementation specialist.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Implementer

You are a code implementation agent...
```

### Edit Agent (TOML)

```toml
sandbox_mode = "allow-edits"

developer_instructions = """
Role: Code implementation specialist.

Tools: Read, Write, Edit, Bash, Glob, Grep

---

# Implementer

You are a code implementation agent...
"""
```