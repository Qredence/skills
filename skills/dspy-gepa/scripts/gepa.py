#!/usr/bin/env python3
"""DSPy GEPA — Generate, Evaluate, Propose, Apply.

Subcommands:
    generate   Generate new scenario YAML files for a skill
    optimize   Full GEPA optimization loop (evaluate → optimize → save)

Usage:
    python gepa.py generate --skill-name NAME --skill-description DESC [OPTIONS]
    python gepa.py optimize --scenarios PATH [OPTIONS]
"""

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

import yaml

try:
    import dspy
except ImportError:
    dspy = None

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

SCHEMA_PATH = (
    Path(__file__).resolve().parents[3]
    / "tests"
    / "schemas"
    / "skill-scenarios.schema.json"
)


def load_scenarios(path: str) -> dict:
    """Load a full scenarios YAML file (config + scenarios)."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _require_dspy():
    if dspy is None:
        print(
            "Error: dspy is required. Install with: pip install dspy-ai",
            file=sys.stderr,
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# GENERATE — DSPy-powered scenario generation
# ---------------------------------------------------------------------------

# ScenarioSignature and ScenarioGenerator are defined lazily to avoid
# requiring dspy at import time (allows --help and offline tools to work).

_ScenarioSignature = None
_ScenarioGenerator = None


def _build_dspy_classes():
    """Build DSPy Signature/Module classes (requires dspy to be imported)."""
    global _ScenarioSignature, _ScenarioGenerator
    if _ScenarioSignature is not None:
        return

    class ScenarioSignature(dspy.Signature):
        """Generate a test scenario for an agent skill.

        Given a skill name, description, and optional existing scenarios as context,
        produce a new scenario with: name, prompt, expected_patterns (regex list),
        forbidden_patterns (regex list), tags, and a mock_response that satisfies
        the patterns.
        """

        skill_name: str = dspy.InputField(
            desc="Short identifier of the skill (e.g. 'fastapi-router-py')"
        )
        skill_description: str = dspy.InputField(
            desc="What the skill does, in one or two sentences"
        )
        existing_scenarios: str = dspy.InputField(
            desc="YAML of existing scenarios for context (may be empty)"
        )
        variation_hint: str = dspy.InputField(
            desc="Brief hint for what this new scenario should test"
        )

        scenario_yaml: str = dspy.OutputField(
            desc="A single YAML scenario object (name, prompt, expected_patterns, forbidden_patterns, tags, mock_response)"
        )

    class ScenarioGenerator(dspy.Module):
        """DSPy module that generates a single scenario."""

        def __init__(self):
            super().__init__()
            self.generate = dspy.ChainOfThought(ScenarioSignature)

        def forward(
            self,
            skill_name,
            skill_description,
            existing_scenarios="",
            variation_hint="",
        ):
            return self.generate(
                skill_name=skill_name,
                skill_description=skill_description,
                existing_scenarios=existing_scenarios,
                variation_hint=variation_hint,
            )

    _ScenarioSignature = ScenarioSignature
    _ScenarioGenerator = ScenarioGenerator


def _parse_scenario_yaml(raw: str) -> dict | None:
    """Parse a generated scenario YAML string into a dict, with validation."""
    # Strip markdown fences if present
    raw = re.sub(r"^```(?:yaml)?\s*\n?", "", raw.strip())
    raw = re.sub(r"\n?```\s*$", "", raw.strip())

    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None

    if isinstance(parsed, list) and len(parsed) == 1:
        parsed = parsed[0]
    if not isinstance(parsed, dict):
        return None

    # Validate required fields
    required = {
        "name",
        "prompt",
        "expected_patterns",
        "forbidden_patterns",
        "tags",
        "mock_response",
    }
    if not required.issubset(parsed.keys()):
        return None

    # Ensure list fields are lists
    for field in ("expected_patterns", "forbidden_patterns", "tags"):
        if not isinstance(parsed[field], list):
            parsed[field] = [parsed[field]] if parsed[field] else []

    # Ensure string fields are strings
    for field in ("name", "prompt", "mock_response"):
        if not isinstance(parsed[field], str):
            parsed[field] = str(parsed[field])

    return parsed


def _validate_scenario_patterns(scenario: dict) -> dict:
    """Validate that mock_response satisfies expected/forbidden patterns.

    Returns a dict with validation details.
    """
    code = scenario.get("mock_response", "")
    expected = scenario.get("expected_patterns", [])
    forbidden = scenario.get("forbidden_patterns", [])

    matched_expected = []
    missed_expected = []
    for p in expected:
        try:
            if re.search(p, code, re.DOTALL):
                matched_expected.append(p)
            else:
                missed_expected.append(p)
        except re.error:
            missed_expected.append(p)

    triggered_forbidden = []
    for p in forbidden:
        try:
            if re.search(p, code, re.DOTALL):
                triggered_forbidden.append(p)
        except re.error:
            pass

    expected_score = len(matched_expected) / len(expected) if expected else 1.0
    forbidden_score = (
        (len(forbidden) - len(triggered_forbidden)) / len(forbidden)
        if forbidden
        else 1.0
    )
    score = (expected_score + forbidden_score) / 2.0

    return {
        "score": round(score, 4),
        "matched_expected": matched_expected,
        "missed_expected": missed_expected,
        "triggered_forbidden": triggered_forbidden,
        "valid": score >= 0.8,
    }


def _generate_variation_hints(
    skill_name: str, skill_description: str, existing_names: list[str], count: int
) -> list[str]:
    """Generate variation hints for new scenarios."""
    base_hints = [
        f"Test a basic/simple use case of {skill_name}",
        "Test an advanced/complex use case with multiple features",
        "Test edge cases and error handling",
        "Test integration with external dependencies",
        "Test performance-sensitive patterns",
        "Test configuration and customization options",
        "Test security-related patterns",
        "Test input validation and sanitization",
        "Test async/concurrent patterns",
        "Test backward compatibility patterns",
    ]
    # Filter out hints that overlap with existing scenario names
    if existing_names:
        name_str = " ".join(existing_names).lower()
        filtered = [
            h
            for h in base_hints
            if not any(word in name_str for word in h.lower().split()[:3])
        ]
        hints = filtered or base_hints
    else:
        hints = base_hints

    # Cycle through hints if we need more than available
    result = []
    for i in range(count):
        result.append(hints[i % len(hints)])
    return result


def cmd_generate(args):
    """Generate new scenarios for a skill."""
    _require_dspy()
    _build_dspy_classes()

    # Configure DSPy LM
    if args.model:
        lm = dspy.LM(args.model)
        dspy.configure(lm=lm)

    generator = _ScenarioGenerator()

    # Load existing scenarios for context
    existing_yaml = ""
    existing_names = []
    existing_config = {"model": "gpt-4", "max_tokens": 2000, "temperature": 0.3}
    if args.scenarios:
        data = load_scenarios(args.scenarios)
        existing_config = data.get("config", existing_config)
        existing_scenarios = data.get("scenarios", [])
        existing_names = [s.get("name", "") for s in existing_scenarios]
        # Provide a summary of existing scenarios as context (not full YAML to save tokens)
        summaries = []
        for s in existing_scenarios[:10]:  # Cap at 10 for context window
            summaries.append(
                f"- {s.get('name', 'unnamed')}: {s.get('prompt', '')[:100]}..."
            )
        existing_yaml = "\n".join(summaries) if summaries else ""

    hints = _generate_variation_hints(
        args.skill_name, args.skill_description, existing_names, args.num_scenarios
    )

    generated = []
    failed = 0
    max_retries = 2

    for i, hint in enumerate(hints):
        print(
            f"Generating scenario {i + 1}/{args.num_scenarios}: {hint}", file=sys.stderr
        )

        scenario = None
        for attempt in range(max_retries + 1):
            try:
                result = generator(
                    skill_name=args.skill_name,
                    skill_description=args.skill_description,
                    existing_scenarios=existing_yaml,
                    variation_hint=hint,
                )
                scenario = _parse_scenario_yaml(result.scenario_yaml)
                if scenario:
                    # Validate patterns against mock_response
                    validation = _validate_scenario_patterns(scenario)
                    if validation["valid"]:
                        scenario["_validation"] = validation
                        break
                    else:
                        print(
                            f"  Retry {attempt + 1}: patterns don't match mock_response (score={validation['score']})",
                            file=sys.stderr,
                        )
                        scenario = None
                else:
                    print(
                        f"  Retry {attempt + 1}: failed to parse YAML output",
                        file=sys.stderr,
                    )
            except Exception as e:
                print(f"  Retry {attempt + 1}: {e}", file=sys.stderr)

        if scenario:
            # Remove internal validation metadata before output
            scenario.pop("_validation", None)
            generated.append(scenario)
            print(f"  ✓ Generated: {scenario.get('name', 'unnamed')}", file=sys.stderr)
        else:
            failed += 1
            print(f"  ✗ Failed after {max_retries + 1} attempts", file=sys.stderr)

    if not generated:
        print("Error: No scenarios were generated successfully.", file=sys.stderr)
        sys.exit(1)

    # Build output YAML
    output_data = {
        "config": existing_config,
        "scenarios": generated,
    }

    yaml_output = yaml.dump(
        output_data, default_flow_style=False, sort_keys=False, allow_unicode=True
    )

    # Add header comment
    header = textwrap.dedent(f"""\
    # Generated scenarios for {args.skill_name}
    # Generated by GEPA (dspy-gepa skill)
    # {len(generated)} scenarios generated, {failed} failed
    """)
    yaml_output = header + yaml_output

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(yaml_output)
        print(f"\nWrote {len(generated)} scenarios to {args.output}", file=sys.stderr)
    else:
        print(yaml_output)

    # Print summary
    print(f"\nSummary: {len(generated)} generated, {failed} failed", file=sys.stderr)


# ---------------------------------------------------------------------------
# OPTIMIZE — Full GEPA loop
# ---------------------------------------------------------------------------


def cmd_optimize(args):
    """Full GEPA loop: evaluate baseline → optimize → evaluate optimized → save."""
    _require_dspy()

    from scenario_to_dataset import scenario_to_example
    from gepa_evaluate import pattern_match_metric

    # Configure DSPy LM
    if args.model:
        lm = dspy.LM(args.model)
        dspy.configure(lm=lm)

    # Load scenarios as DSPy examples
    scenarios = load_scenarios(args.scenarios).get("scenarios", [])
    if not scenarios:
        print("Error: No scenarios found.", file=sys.stderr)
        sys.exit(1)

    examples = [scenario_to_example(s) for s in scenarios]

    # Split into train/dev
    split_idx = int(len(examples) * args.train_split)
    trainset = examples[:split_idx]
    devset = examples[split_idx:] if split_idx < len(examples) else examples

    print(
        f"Dataset: {len(examples)} total, {len(trainset)} train, {len(devset)} dev",
        file=sys.stderr,
    )

    # Instantiate baseline module
    module = dspy.ChainOfThought(args.signature)

    # Evaluate baseline
    print("\n--- Baseline Evaluation ---", file=sys.stderr)
    evaluator = dspy.Evaluate(
        devset=devset,
        metric=pattern_match_metric,
        num_threads=args.threads,
        display_progress=True,
    )
    baseline_score = evaluator(module)
    print(f"Baseline score: {baseline_score}", file=sys.stderr)

    # Select teleprompter and optimize
    print(f"\n--- Optimizing with {args.teleprompter} ---", file=sys.stderr)
    if args.teleprompter == "bootstrap":
        teleprompter = dspy.BootstrapFewShot(
            metric=pattern_match_metric,
            max_bootstrapped_demos=args.max_demos,
            max_rounds=args.max_rounds,
        )
    elif args.teleprompter == "mipro":
        teleprompter = dspy.MIPROv2(
            metric=pattern_match_metric,
            num_candidates=args.max_demos,
            max_bootstrapped_demos=args.max_demos,
        )
    else:
        print(f"Error: Unknown teleprompter '{args.teleprompter}'", file=sys.stderr)
        sys.exit(1)

    compiled = teleprompter.compile(module, trainset=trainset)

    # Evaluate optimized
    print("\n--- Optimized Evaluation ---", file=sys.stderr)
    optimized_score = evaluator(compiled)
    print(f"Optimized score: {optimized_score}", file=sys.stderr)

    # Save
    compiled.save(args.output)
    print(f"\nOptimized program saved to {args.output}", file=sys.stderr)

    # Report
    report = {
        "baseline_score": round(baseline_score, 4),
        "optimized_score": round(optimized_score, 4),
        "delta": round(optimized_score - baseline_score, 4),
        "teleprompter": args.teleprompter,
        "train_size": len(trainset),
        "dev_size": len(devset),
        "output": args.output,
    }

    report_json = json.dumps(report, indent=2)
    if args.report:
        Path(args.report).write_text(report_json)
        print(f"Report saved to {args.report}", file=sys.stderr)
    else:
        print(report_json)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="DSPy GEPA — Generate, Evaluate, Propose, Apply",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              # Generate 5 new scenarios for a skill
              python gepa.py generate --skill-name fastapi-router-py \\
                --skill-description "Creates FastAPI routers with CRUD endpoints" \\
                --num-scenarios 5 --output new-scenarios.yaml

              # Generate scenarios using existing ones as context
              python gepa.py generate --skill-name fastapi-router-py \\
                --skill-description "Creates FastAPI routers" \\
                --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \\
                --num-scenarios 3 --output more-scenarios.yaml

              # Full GEPA optimization loop
              python gepa.py optimize --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \\
                --output optimized_program.json
        """),
    )
    subparsers = parser.add_subparsers(dest="command", help="GEPA subcommand")

    # --- generate ---
    gen_parser = subparsers.add_parser(
        "generate", help="Generate new scenario YAML files for a skill"
    )
    gen_parser.add_argument(
        "--skill-name",
        required=True,
        help="Skill identifier (e.g. 'fastapi-router-py')",
    )
    gen_parser.add_argument(
        "--skill-description", required=True, help="What the skill does"
    )
    gen_parser.add_argument(
        "--scenarios",
        default=None,
        help="Existing scenarios.yaml for context (optional)",
    )
    gen_parser.add_argument(
        "--num-scenarios",
        type=int,
        default=3,
        help="Number of scenarios to generate (default: 3)",
    )
    gen_parser.add_argument(
        "--model", default=None, help="DSPy LM model string (e.g. 'openai/gpt-4o')"
    )
    gen_parser.add_argument(
        "--output", default=None, help="Output YAML file path (default: stdout)"
    )

    # --- optimize ---
    opt_parser = subparsers.add_parser("optimize", help="Full GEPA optimization loop")
    opt_parser.add_argument(
        "--scenarios", required=True, help="Path to scenarios.yaml file"
    )
    opt_parser.add_argument(
        "--signature", default="prompt -> code", help="DSPy signature string"
    )
    opt_parser.add_argument(
        "--teleprompter",
        default="bootstrap",
        choices=["bootstrap", "mipro"],
        help="Optimizer",
    )
    opt_parser.add_argument(
        "--max-rounds", type=int, default=1, help="Max optimization rounds"
    )
    opt_parser.add_argument(
        "--max-demos", type=int, default=4, help="Max bootstrapped demos"
    )
    opt_parser.add_argument(
        "--train-split", type=float, default=0.8, help="Train/dev split ratio"
    )
    opt_parser.add_argument(
        "--threshold", type=float, default=0.8, help="Pass/fail threshold"
    )
    opt_parser.add_argument("--threads", type=int, default=4, help="Evaluation threads")
    opt_parser.add_argument("--model", default=None, help="DSPy LM model string")
    opt_parser.add_argument(
        "--output", default="optimized_program.json", help="Save optimized program path"
    )
    opt_parser.add_argument(
        "--report", default=None, help="Save evaluation report path"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "optimize":
        cmd_optimize(args)


if __name__ == "__main__":
    main()
