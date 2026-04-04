#!/usr/bin/env python3
"""
LiteLLM-based skill evaluator.

Evaluates skills by:
1. Loading scenarios from tests/scenarios/<skill>/scenarios.yaml
2. Loading acceptance criteria from .github/skills/<skill>/references/acceptance-criteria.md
3. Calling LiteLLM proxy with skill context
4. Evaluating responses against expected/forbidden patterns
5. Reporting results in similar format to the harness
"""

import os
import re
import sys
from pathlib import Path
from typing import Any
import yaml
import requests

# Configuration
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "")
LITELLM_PROXY_URL = os.getenv("LITELLM_PROXY_URL", "https://litellm-proxy-gojcb5mtua-uc.a.run.app")
LITELLM_MODEL = os.getenv("LITELLM_DEFAULT_MODEL", "vertex-glm-5")

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "tests" / "scenarios"
CRITERIA_DIR = REPO_ROOT / ".github" / "skills"


def load_scenarios(skill_name: str) -> dict[str, Any]:
    """Load scenarios.yaml for a skill."""
    path = SCENARIOS_DIR / skill_name / "scenarios.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Scenarios not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def load_criteria(skill_name: str) -> str:
    """Load acceptance-criteria.md for a skill."""
    path = CRITERIA_DIR / skill_name / "references" / "acceptance-criteria.md"
    if not path.exists():
        return ""
    with open(path) as f:
        return f.read()


def call_litellm(prompt: str, skill_context: str, model: str = LITELLM_MODEL) -> str:
    """Call LiteLLM proxy to generate code."""
    headers = {
        "Authorization": f"Bearer {LITELLM_API_KEY}",
        "Content-Type": "application/json",
    }
    
    system_prompt = f"""You are an expert Python developer. You have knowledge of this skill:

{skill_context}

Generate correct, working code that follows the patterns and best practices documented in the skill."""
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }
    
    try:
        response = requests.post(
            f"{LITELLM_PROXY_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] LiteLLM call failed: {e}")
        raise


def pattern_matches(code: str, pattern: str) -> bool:
    """Check if a regex pattern matches in code."""
    try:
        return bool(re.search(pattern, code, re.MULTILINE | re.DOTALL))
    except Exception as e:
        print(f"[REGEX ERROR] Pattern '{pattern}' failed: {e}")
        return False


def evaluate_scenario(
    skill_name: str,
    scenario: dict[str, Any],
    skill_context: str,
) -> dict[str, Any]:
    """Evaluate a single scenario."""
    name = scenario.get("name", "unnamed")
    prompt = scenario.get("prompt", "")
    expected_patterns = scenario.get("expected_patterns", [])
    forbidden_patterns = scenario.get("forbidden_patterns", [])
    
    print(f"  Running scenario: {name}")
    
    # Generate code with LiteLLM
    try:
        code = call_litellm(prompt, skill_context)
    except Exception as e:
        print(f"    ✗ Generation failed: {e}")
        return {
            "name": name,
            "passed": False,
            "score": 0.0,
            "error": str(e),
        }
    
    # Check expected patterns
    expected_passed = 0
    expected_warnings = []
    for pattern in expected_patterns:
        if pattern_matches(code, pattern):
            print(f"      ✓ Expected: {pattern}")
            expected_passed += 1
        else:
            print(f"      ✗ Expected: {pattern}")
            expected_warnings.append(pattern)
    
    # Check forbidden patterns
    forbidden_violations = []
    for pattern in forbidden_patterns:
        if pattern_matches(code, pattern):
            print(f"      ✗ Forbidden: {pattern}")
            forbidden_violations.append(pattern)
        else:
            print(f"      ✓ Forbidden: {pattern}")
    
    # Calculate score
    expected_total = len(expected_patterns)
    forbidden_total = len(forbidden_patterns)
    
    if expected_total == 0:
        expected_score = 100.0
    else:
        expected_score = (expected_passed / expected_total) * 100
    
    if forbidden_total == 0:
        forbidden_score = 100.0
    else:
        forbidden_score = ((forbidden_total - len(forbidden_violations)) / forbidden_total) * 100
    
    # Overall score (weight equally)
    overall_score = (expected_score + forbidden_score) / 2
    
    # Passed if all expected patterns matched and no forbidden patterns
    passed = (expected_passed == expected_total) and (len(forbidden_violations) == 0)
    
    result = {
        "name": name,
        "passed": passed,
        "score": round(overall_score, 1),
        "expected_matched": expected_passed,
        "expected_total": expected_total,
        "forbidden_violations": len(forbidden_violations),
        "forbidden_total": forbidden_total,
        "warnings": expected_warnings if expected_warnings else None,
    }
    
    if passed:
        print(f"    ✓ Score: {overall_score:.1f}")
    else:
        print(f"    ✗ Score: {overall_score:.1f}")
    
    return result


def evaluate_skill(skill_name: str, limit: int = None) -> dict[str, Any]:
    """Evaluate all scenarios for a skill."""
    print(f"\nEvaluating skill: {skill_name}")
    print("=" * 50)
    
    # Load scenarios and criteria
    data = load_scenarios(skill_name)
    skill_context = load_criteria(skill_name)
    
    scenarios = data.get("scenarios", [])
    if limit:
        scenarios = scenarios[:limit]
    
    # Evaluate each scenario
    results = []
    for scenario in scenarios:
        result = evaluate_scenario(skill_name, scenario, skill_context)
        results.append(result)
    
    # Summary
    passed_count = sum(1 for r in results if r.get("passed"))
    total_count = len(results)
    avg_score = sum(r.get("score", 0) for r in results) / total_count if total_count > 0 else 0
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0
    
    print()
    print("Evaluation Summary: " + skill_name)
    print("=" * 50)
    print(f"Scenarios: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    print(f"Average Score: {avg_score:.1f}")
    print()
    
    return {
        "skill": skill_name,
        "total": total_count,
        "passed": passed_count,
        "failed": total_count - passed_count,
        "pass_rate": round(pass_rate, 1),
        "avg_score": round(avg_score, 1),
        "scenarios": results,
    }


def main():
    """Evaluate specified skills or all RLM skills."""
    skills = sys.argv[1:] if sys.argv[1:] else [
        "rlm",
        "rlm-batch",
        "rlm-debug",
        "rlm-execute",
        "rlm-long-context",
        "rlm-memory",
        "rlm-run",
        "rlm-test-suite",
    ]
    
    all_results = []
    for skill in skills:
        try:
            result = evaluate_skill(skill)
            all_results.append(result)
        except Exception as e:
            print(f"[ERROR] Failed to evaluate {skill}: {e}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    for result in all_results:
        skill = result["skill"]
        passed = result["passed"]
        total = result["total"]
        rate = result["pass_rate"]
        score = result["avg_score"]
        print(f"{skill:25} | {passed:2}/{total:2} ({rate:5.1f}%) | avg score: {score:5.1f}")


if __name__ == "__main__":
    main()
