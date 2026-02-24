#!/usr/bin/env python3
"""
Run golden evaluations for skills

Loads JSONL golden sets and evaluates skill outputs.
"""
import sys
from pathlib import Path

# Add parent to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "packages" / "skills_core"))

from skills_core import discover_skills, run_skill_eval, get_skill_by_id


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run golden evaluations for DSPy skills"
    )
    parser.add_argument(
        "--skill",
        type=str,
        help="Specific skill ID to evaluate (default: all)"
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("skills"),
        help="Path to skills directory"
    )
    parser.add_argument(
        "--starter-only",
        action="store_true",
        help="Only evaluate starter skills (fast)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Only validate golden set format (default)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute skills (requires LLM)"
    )
    
    args = parser.parse_args()
    
    skills_dir = args.skills_dir.resolve()
    
    # Determine dry run mode
    dry_run = not args.execute
    
    print("=" * 60)
    print(f"Golden Evaluation {'(Dry Run)' if dry_run else ''}")
    print("=" * 60)
    print()
    
    if dry_run:
        print("ℹ️  Running in dry-run mode (format validation only)")
        print("   Use --execute to actually run skills\n")
    
    # Get skills to evaluate
    if args.skill:
        # Single skill
        metadata = get_skill_by_id(skills_dir, args.skill)
        if not metadata:
            print(f"❌ Skill not found: {args.skill}")
            return 1
        skills = [metadata]
    else:
        # All skills or starter only
        skills = discover_skills(skills_dir)
        
        if args.starter_only:
            starter_ids = {'web_summarizer', 'doc_transformer', 'task_planner'}
            skills = [s for s in skills if s.id in starter_ids]
    
    print(f"Evaluating {len(skills)} skill(s)...\n")
    
    # Run evaluations
    all_passed = True
    results = []
    
    for metadata in skills:
        skill_path = skills_dir / metadata.id
        
        print(f"📊 {metadata.id}...")
        
        try:
            result = run_skill_eval(skill_path, dry_run=dry_run)
            results.append(result)
            
            if result.total == 0:
                print(f"   ⚠️  No golden examples found")
            elif result.failed > 0:
                print(f"   ✗ {result.passed}/{result.total} passed")
                for detail in result.details:
                    if detail['status'] != 'pass':
                        print(f"      - {detail['name']}: {detail['message']}")
                all_passed = False
            else:
                print(f"   ✓ {result.passed}/{result.total} passed")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
    
    print()
    print("=" * 60)
    
    # Summary
    total_tests = sum(r.total for r in results)
    total_passed = sum(r.passed for r in results)
    
    print(f"Summary: {total_passed}/{total_tests} tests passed")
    
    if all_passed:
        print("✅ All evaluations passed")
        return 0
    else:
        print("❌ Some evaluations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
