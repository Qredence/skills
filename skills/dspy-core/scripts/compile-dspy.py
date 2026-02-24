#!/usr/bin/env python3
"""
Compile DSPy modules with proper caching and validation.

This script compiles DSPy modules and saves artifacts to the cache directory.
It handles cache validation and provides detailed logging.

Usage:
    uv run compile-dspy.py --module <module_name> --teleprompter <teleprompter_name>
    uv run compile-dspy.py --module reasoner --teleprompter bootstrap

Options:
    --module: Name of the DSPy module to compile (e.g., reasoner, task_analyzer)
    --teleprompter: Name of the teleprompter to use (e.g., bootstrap, cot)
    --cache-dir: Cache directory (default: .var/cache/dspy)
    --output: Output file path (default: .var/logs/compiled_<module>.json)
    --verbose: Enable verbose logging
"""

import argparse
import sys
from pathlib import Path

try:
    import dspy  # noqa: F401
except ImportError:
    print("Error: dspy is not installed. Install with: uv pip install dspy")
    sys.exit(1)


def compile_module(
    module_name: str,
    teleprompter_name: str,
    cache_dir: Path,
    output: Path,
    verbose: bool,
):
    """Compile a DSPy module with the specified teleprompter."""
    print(f"Compiling module: {module_name}")
    print(f"Teleprompter: {teleprompter_name}")
    print(f"Cache directory: {cache_dir}")
    print(f"Output file: {output}")

    # Import the module dynamically
    try:
        if module_name == "reasoner":
            from fleet_rlm.core.interpreter import DSPyReasoner

            module = DSPyReasoner()
        elif module_name == "task_analyzer":
            from fleet_rlm.core import TaskAnalysisModule

            module = TaskAnalysisModule()
        else:
            print(f"Error: Unknown module '{module_name}'")
            print("Available modules: reasoner, task_analyzer")
            sys.exit(1)
    except ImportError as e:
        print(f"Error importing module: {e}")
        sys.exit(1)

    # Select teleprompter
    from dspy.teleprompt import BootstrapFewShot, LabeledFewShot, KNNFewShot

    teleprompters = {
        "bootstrap": BootstrapFewShot,
        "labeled": LabeledFewShot,
        "knn": KNNFewShot,
    }

    if teleprompter_name not in teleprompters:
        print(f"Error: Unknown teleprompter '{teleprompter_name}'")
        print(f"Available teleprompters: {', '.join(teleprompters.keys())}")
        sys.exit(1)

    teleprompter_class = teleprompters[teleprompter_name]

    # Create teleprompter instance
    try:
        teleprompter = teleprompter_class()
    except Exception as e:
        print(f"Error creating teleprompter: {e}")
        sys.exit(1)

    # Compile the module
    try:
        print("Compiling...")
        compiled = teleprompter.compile(module)
        print("Compilation successful!")
    except Exception as e:
        print(f"Compilation failed: {e}")
        sys.exit(1)

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    # Save compiled module
    try:
        compiled.save(str(output))
        print(f"Saved compiled module to: {output}")
    except Exception as e:
        print(f"Error saving compiled module: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Compile DSPy modules")
    parser.add_argument(
        "--module", required=True, help="Name of the DSPy module to compile"
    )
    parser.add_argument(
        "--teleprompter", required=True, help="Name of the teleprompter"
    )
    parser.add_argument(
        "--cache-dir", default=".var/cache/dspy", help="Cache directory"
    )
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    output = (
        Path(args.output)
        if args.output
        else Path(f".var/logs/compiled_{args.module}.json")
    )

    compile_module(args.module, args.teleprompter, cache_dir, output, args.verbose)


if __name__ == "__main__":
    main()
