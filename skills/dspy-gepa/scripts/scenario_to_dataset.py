#!/usr/bin/env python3
"""Convert scenario YAML files to DSPy-compatible datasets.

Usage:
    python scenario_to_dataset.py --scenarios PATH [--output PATH] [--filter-tags TAG,...] [--validate]
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None

try:
    import dspy
except ImportError:
    dspy = None


SCHEMA_PATH = (
    Path(__file__).resolve().parents[3]
    / "tests"
    / "schemas"
    / "skill-scenarios.schema.json"
)


def load_scenarios(path: str) -> dict:
    """Load and parse a scenarios YAML file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def validate_scenarios(data: dict) -> None:
    """Validate scenario data against the JSON schema."""
    if jsonschema is None:
        print("Warning: jsonschema not installed, skipping validation", file=sys.stderr)
        return
    if not SCHEMA_PATH.exists():
        print(
            f"Warning: schema not found at {SCHEMA_PATH}, skipping validation",
            file=sys.stderr,
        )
        return
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)
    jsonschema.validate(data, schema)
    print("Schema validation passed.", file=sys.stderr)


def scenario_to_dict(scenario: dict) -> dict:
    """Convert a single scenario to a dataset-compatible dict."""
    return {
        "prompt": scenario["prompt"],
        "expected_patterns": scenario["expected_patterns"],
        "forbidden_patterns": scenario["forbidden_patterns"],
        "mock_response": scenario.get("mock_response", ""),
        "name": scenario.get("name", ""),
        "tags": scenario.get("tags", []),
    }


def scenario_to_example(scenario: dict):
    """Convert a single scenario to a dspy.Example (requires dspy)."""
    if dspy is None:
        raise ImportError(
            "dspy is required for Example conversion. Install with: pip install dspy-ai"
        )
    return dspy.Example(
        prompt=scenario["prompt"],
        expected_patterns=scenario["expected_patterns"],
        forbidden_patterns=scenario["forbidden_patterns"],
        mock_response=scenario.get("mock_response", ""),
        name=scenario.get("name", ""),
        tags=scenario.get("tags", []),
    ).with_inputs("prompt")


def convert(
    scenarios_path: str, filter_tags: list[str] | None = None, do_validate: bool = False
) -> list[dict]:
    """Load scenarios YAML and convert to dataset dicts."""
    data = load_scenarios(scenarios_path)
    if do_validate:
        validate_scenarios(data)

    scenarios = data.get("scenarios", [])
    if filter_tags:
        tag_set = set(filter_tags)
        scenarios = [s for s in scenarios if tag_set.intersection(s.get("tags", []))]

    return [scenario_to_dict(s) for s in scenarios]


def main():
    parser = argparse.ArgumentParser(
        description="Convert scenario YAML to DSPy-compatible JSON dataset."
    )
    parser.add_argument(
        "--scenarios", required=True, help="Path to scenarios.yaml file"
    )
    parser.add_argument(
        "--output", default=None, help="Output JSON file path (default: stdout)"
    )
    parser.add_argument(
        "--filter-tags", default=None, help="Comma-separated tags to filter scenarios"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate YAML against schema before conversion",
    )
    args = parser.parse_args()

    filter_tags = args.filter_tags.split(",") if args.filter_tags else None
    dataset = convert(
        args.scenarios, filter_tags=filter_tags, do_validate=args.validate
    )

    output = json.dumps(dataset, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Wrote {len(dataset)} examples to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
