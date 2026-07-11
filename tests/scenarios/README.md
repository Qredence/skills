# Skill test scenarios

Optional scenario YAML files for the evaluation harness.

## Layout

Skill IDs are hierarchical. Place scenarios next to that ID:

```text
tests/scenarios/figma-agent/<skill-name>/scenarios.yaml
```

Example:

```text
tests/scenarios/figma-agent/accessibility-audit/scenarios.yaml
```

Skills without a scenario file use a default smoke scenario.

## Schema

See [`skill-scenarios.schema.json`](skill-scenarios.schema.json) in this directory
(or `../schemas/skill-scenarios.schema.json` if present).

## Running

```bash
cd tests
pnpm harness figma-agent/<skill-name> --mock --verbose
```
