# Qredence Skills Registry

A Python-first registry of **DSPy Module/Signature skills** for agent orchestration. Production-grade, eval-driven, safety-first, and AgenticFleet-compatible.

[![CI](https://github.com/Qredence/skills/workflows/CI/badge.svg)](https://github.com/Qredence/skills/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is This?

The Qredence Skills Registry is a curated collection of **reusable DSPy skills** - versioned reasoning components that can be:
- **Discovered** via semantic tags
- **Composed** into agent workflows
- **Validated** against strict contracts
- **Evaluated** with golden test sets
- **Orchestrated** by AgenticFleet-style planners

Each skill is a **DSPy Module** with explicit inputs/outputs, safety permissions, and comprehensive testing.

## Quick Start

```bash
# Install
git clone https://github.com/Qredence/skills.git
cd skills
pip install -r requirements.txt
pip install -e packages/skills_core

# Browse skills
python tools/validate.py --list

# Use a skill
python skills/web_summarizer/examples/minimal.py

# Create your own
python tools/new_skill.py my_skill --description "..." --tags tag1 tag2
```

See [QUICKSTART.md](QUICKSTART.md) for detailed guide.

## Features

### 🎯 Strict Contracts
- **JSON Schema validation** for all metadata
- **DSPy Module/Signature** contract enforcement
- **Input/output schemas** with type validation
- **Deterministic catalog** generation

### 🔍 Discoverability
- **AgenticFleet tag taxonomy** (reasoning, planning, memory, etc.)
- **Semantic routing** compatible
- **Auto-generated catalog** (catalog/skills.json)
- **CLI search** by tags, safety level, permissions

### 🛡️ Safety First
- **Three-tier safety levels** (low/medium/high)
- **Explicit permissions** (network, filesystem, tools)
- **Risk assessment** and mitigations
- **Data handling policies**

### 🧪 Eval-Driven
- **Golden evaluation sets** (JSONL format)
- **Three match types** (exact, contains, schema)
- **CI integration** for regression testing
- **Dry-run mode** for fast validation

### 📦 Composable
- **Versioned skills** (semantic versioning)
- **Clear dependencies** declared
- **Planner-compatible** design
- **Independent loading** and execution

## Repository Structure

```
skills/
├── catalog/                    # Generated skill catalog
│   ├── schema.skill.json       # JSON Schema for skill.yaml
│   ├── schema.catalog.json     # JSON Schema for catalog
│   └── skills.json             # Generated index (DO NOT EDIT)
├── skills/                     # All skills
│   ├── _templates/             # Skill templates
│   ├── web_summarizer/         # Example: Web summarizer
│   ├── doc_transformer/        # Example: Document transformer
│   └── task_planner/           # Example: Task planner
├── packages/skills_core/       # Core validation library
├── tools/                      # CLI tools
│   ├── validate.py             # Validate & regenerate catalog
│   ├── new_skill.py            # Scaffold new skills
│   └── run_eval.py             # Run golden evaluations
├── docs/                       # Documentation
│   ├── skill_contract.md       # Skill specification
│   ├── tagging.md              # Tag taxonomy
│   ├── versioning.md           # Semver rules
│   ├── evaluation.md           # Golden eval guide
│   └── safety.md               # Safety framework
└── tests/                      # Test suite
```

## Skill Structure

Each skill follows a strict contract:

```
skills/{skill_id}/
├── skill.yaml              # Canonical metadata
├── README.md               # Documentation
├── src/
│   └── skill.py            # DSPy Module implementation
├── tests/
│   └── test_contract.py    # Contract tests
├── eval/
│   └── golden.jsonl        # Golden evaluation set
└── examples/
    └── minimal.py          # Runnable example
```

## Available Skills

### Web Summarizer
**Tags**: `summarization`, `extraction`, `web`, `nlp`  
**Safety**: Medium (requires network access)

Summarizes web content into concise insights with key points extraction.

### Document Transformer
**Tags**: `transform`, `formatting`, `documents`  
**Safety**: Low (pure computation)

Transforms documents between formats (markdown, HTML, plain text) and styles.

### Task Planner
**Tags**: `planning`, `decomposition`, `reasoning`, `orchestration`  
**Safety**: Low (pure computation)

Plans and breaks down complex tasks into actionable subtasks with dependencies.

## CLI Tools

### Validate Skills

```bash
# Validate all skills and regenerate catalog
python tools/validate.py

# List all skills
python tools/validate.py --list

# Filter by tag
python tools/validate.py --list --tag nlp

# Show skill details
python tools/validate.py --info web_summarizer
```

### Create New Skill

```bash
python tools/new_skill.py sentiment_analyzer \
  --description "Analyzes sentiment of text" \
  --tags nlp analysis classification \
  --owner "Your Name"
```

### Run Evaluations

```bash
# Dry run (format validation)
python tools/run_eval.py --dry-run

# Run specific skill
python tools/run_eval.py --skill web_summarizer --dry-run

# Run starter skills only
python tools/run_eval.py --starter-only
```

## AgenticFleet Integration

Skills use a semantic tag taxonomy optimized for agent orchestration:

```python
# Route based on intent and tags
planner.route_to_skill(
    intent="summarize this article",
    required_tags=["summarization", "web"]
)
```

### Tag Categories

- **Core Reasoning**: `reasoning`, `planning`, `decision`, `decomposition`, `reflection`
- **Memory & Knowledge**: `memory`, `retrieval`, `knowledge`, `embedding`
- **Execution**: `orchestration`, `tool_use`, `workflow`, `routing`
- **IO & Transform**: `transform`, `summarization`, `extraction`, `classification`
- **Safety**: `safety`, `validation`, `moderation`
- **System**: `agent`, `skill`, `planner`, `meta`

See [docs/tagging.md](docs/tagging.md) for complete taxonomy.

## Safety Framework

All skills declare explicit permissions and safety levels:

```yaml
permissions:
  network: true           # Can access internet
  filesystem_read: false  # Cannot read files
  filesystem_write: false # Cannot write files
  external_tools: []      # No external tools

safety:
  level: "medium"         # low/medium/high
  risks:
    - "Fetches content from user-specified URLs"
  mitigations:
    - "URL validation and timeout limits"
  data_policy:
    - "No data persistence"
```

See [docs/safety.md](docs/safety.md) for details.

## Development

### Install Dev Dependencies

```bash
pip install -r requirements.txt
pip install -e "packages/skills_core[dev]"
```

### Run Tests

```bash
# All tests
pytest

# Specific skill
pytest skills/web_summarizer/tests/

# With coverage
pytest --cov=skills --cov=packages/skills_core
```

### Lint and Format

```bash
# Check formatting
ruff check .
black --check .

# Auto-fix
ruff check . --fix
black .
```

### Validate

```bash
# Validate all skills
python tools/validate.py

# Check for changes
git diff catalog/skills.json
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[docs/skill_contract.md](docs/skill_contract.md)** - Complete skill specification
- **[docs/tagging.md](docs/tagging.md)** - Tag taxonomy and guidelines
- **[docs/versioning.md](docs/versioning.md)** - Semantic versioning rules
- **[docs/evaluation.md](docs/evaluation.md)** - Golden evaluation framework
- **[docs/safety.md](docs/safety.md)** - Safety levels and permissions

## Contributing

We welcome contributions! To add a new skill:

1. **Create** using `python tools/new_skill.py <name>`
2. **Implement** DSPy Module in `src/skill.py`
3. **Test** with `pytest` and `tools/run_eval.py`
4. **Validate** with `python tools/validate.py`
5. **Submit** PR with completed skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Built with [DSPy](https://github.com/stanfordnlp/dspy) by Stanford NLP.

Optimized for [AgenticFleet](https://github.com/Qredence/AgenticFleet) orchestration.

## Community

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and ideas
- **Pull Requests**: Contribute new skills

---

**Status**: Production-ready • **Version**: 0.1.0 • **Skills**: 3+ and growing
