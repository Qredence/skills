#!/usr/bin/env python3
"""Evaluate a DSPy program against scenario patterns (baseline measurement).

Usage:
    python gepa_evaluate.py --scenarios PATH [--module TEXT] [--signature TEXT]
                            [--program PATH] [--threshold FLOAT] [--threads INT]
                            [--output PATH]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

try:
    import dspy
except ImportError:
    dspy = None


def load_scenarios(path: str) -> list[dict]:
    """Load scenarios from YAML file."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("scenarios", [])


def pattern_match_metric(example, pred, trace=None) -> float:
    """Score a prediction against expected/forbidden patterns.

    Returns a float in [0.0, 1.0].
    """
    code = getattr(pred, "code", "")

    expected = getattr(example, "expected_patterns", []) or []
    if expected:
        expected_hits = sum(1 for p in expected if re.search(p, code, re.DOTALL))
        expected_score = expected_hits / len(expected)
    else:
        expected_score = 1.0

    forbidden = getattr(example, "forbidden_patterns", []) or []
    if forbidden:
        forbidden_misses = sum(
            1 for p in forbidden if not re.search(p, code, re.DOTALL)
        )
        forbidden_score = forbidden_misses / len(forbidden)
    else:
        forbidden_score = 1.0

    return (expected_score + forbidden_score) / 2.0


def evaluate_scenarios_offline(scenarios: list[dict], threshold: float = 0.8) -> dict:
    """Evaluate scenarios using mock_response as the prediction (no LLM needed).

    This scores each scenario's mock_response against its own patterns,
    useful for validating that scenarios are well-formed.
    """
    results = []
    total_score = 0.0

    for scenario in scenarios:
        code = scenario.get("mock_response", "")
        expected = scenario.get("expected_patterns", [])
        forbidden = scenario.get("forbidden_patterns", [])

        if expected:
            expected_hits = sum(1 for p in expected if re.search(p, code, re.DOTALL))
            expected_score = expected_hits / len(expected)
            matched_expected = [p for p in expected if re.search(p, code, re.DOTALL)]
            missed_expected = [p for p in expected if not re.search(p, code, re.DOTALL)]
        else:
            expected_score = 1.0
            matched_expected = []
            missed_expected = []

        if forbidden:
            forbidden_misses = sum(
                1 for p in forbidden if not re.search(p, code, re.DOTALL)
            )
            forbidden_score = forbidden_misses / len(forbidden)
            triggered_forbidden = [
                p for p in forbidden if re.search(p, code, re.DOTALL)
            ]
        else:
            forbidden_score = 1.0
            triggered_forbidden = []

        score = (expected_score + forbidden_score) / 2.0
        total_score += score

        results.append(
            {
                "name": scenario.get("name", "unknown"),
                "score": round(score, 4),
                "passed": score >= threshold,
                "expected_score": round(expected_score, 4),
                "forbidden_score": round(forbidden_score, 4),
                "matched_expected": matched_expected,
                "missed_expected": missed_expected,
                "triggered_forbidden": triggered_forbidden,
            }
        )

    n = len(results)
    aggregate_score = round(total_score / n, 4) if n > 0 else 0.0

    return {
        "aggregate_score": aggregate_score,
        "total_scenarios": n,
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "threshold": threshold,
        "scenarios": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a DSPy program against scenario patterns."
    )
    parser.add_argument(
        "--scenarios", required=True, help="Path to scenarios.yaml file"
    )
    parser.add_argument(
        "--module",
        default="dspy.ChainOfThought",
        help="DSPy module class (default: dspy.ChainOfThought)",
    )
    parser.add_argument(
        "--signature",
        default="prompt -> code",
        help="DSPy signature string (default: 'prompt -> code')",
    )
    parser.add_argument(
        "--program", default=None, help="Path to a saved/optimized program to load"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Pass/fail threshold (default: 0.8)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="Number of evaluation threads (default: 4)",
    )
    parser.add_argument("--output", default=None, help="Output JSON report path")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Evaluate mock_response against patterns (no LLM)",
    )
    args = parser.parse_args()

    scenarios = load_scenarios(args.scenarios)
    if not scenarios:
        print("Error: No scenarios found.", file=sys.stderr)
        sys.exit(1)

    if args.offline or dspy is None:
        if dspy is None and not args.offline:
            print(
                "Warning: dspy not installed, falling back to offline evaluation",
                file=sys.stderr,
            )
        report = evaluate_scenarios_offline(scenarios, threshold=args.threshold)
    else:
        # Online evaluation with DSPy
        from scenario_to_dataset import scenario_to_example

        examples = [scenario_to_example(s) for s in scenarios]

        if args.program:
            module = dspy.ChainOfThought(args.signature)
            module.load(args.program)
        else:
            module_cls = eval(args.module)
            module = module_cls(args.signature)

        evaluator = dspy.Evaluate(
            devset=examples,
            metric=pattern_match_metric,
            num_threads=args.threads,
            display_progress=True,
        )
        aggregate = evaluator(module)

        report = {
            "aggregate_score": round(aggregate, 4),
            "total_scenarios": len(examples),
            "threshold": args.threshold,
            "mode": "online",
        }

    output = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    passed = report.get("passed", 0)
    failed = report.get("failed", 0)
    print(
        f"\nScore: {report['aggregate_score']} | Passed: {passed} | Failed: {failed} | Threshold: {args.threshold}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
