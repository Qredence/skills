#!/usr/bin/env python3
"""
Minimal example - demonstrates basic skill usage
"""
import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from skills.SKILL_ID.src.skill import run


def main():
    print("=" * 60)
    print("Skill Example")
    print("=" * 60)
    print()
    
    # Example usage
    result = run(input_field="example input")
    
    print(f"Input: example input")
    print(f"Output: {result.output_field}")
    print()


if __name__ == "__main__":
    main()
