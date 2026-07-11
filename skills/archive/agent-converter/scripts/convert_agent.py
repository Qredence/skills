#!/usr/bin/env python3
"""
Agent Converter - Convert between MD (YAML frontmatter) and TOML formats.

Usage:
    python3 convert_agent.py <input.md> [--output <dir>]
    python3 convert_agent.py <input.toml> --to-md [--output <dir>]
    python3 convert_agent.py --batch <input_dir> [--output <dir>]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

# Read-only tools that don't modify state
READ_ONLY_TOOLS = {"Read", "Grep", "Glob"}
# Tools that indicate edit permissions
EDIT_TOOLS = {"Write", "Edit", "Bash"}


def parse_md_frontmatter(content: str) -> tuple[dict, str]:
    """Parse markdown file with YAML frontmatter."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Use PyYAML for proper parsing
    metadata = yaml.safe_load(frontmatter_text) or {}

    return metadata, body


def tools_to_sandbox_mode(tools: list[str]) -> str:
    """Determine sandbox mode from tool list."""
    if not tools:
        return "allow-edits"

    tools_set = set(tools)

    # If only read-only tools, sandbox is read-only
    if tools_set.issubset(READ_ONLY_TOOLS) and not tools_set.intersection(EDIT_TOOLS):
        return "read-only"

    # If any edit tools present, sandbox is allow-edits
    if tools_set.intersection(EDIT_TOOLS):
        return "allow-edits"

    return "allow-edits"


def sandbox_mode_to_tools(sandbox_mode: str) -> list[str]:
    """Determine tool list from sandbox mode."""
    if sandbox_mode == "read-only":
        return list(READ_ONLY_TOOLS)
    else:
        return list(READ_ONLY_TOOLS | EDIT_TOOLS)


def md_to_toml(metadata: dict, body: str) -> str:
    """Convert MD metadata and body to TOML format."""
    sandbox_mode = tools_to_sandbox_mode(metadata.get("tools", []))

    # Build developer instructions
    lines = []

    # Add role from description if present
    if "description" in metadata:
        desc = metadata["description"]
        # Handle multi-line descriptions
        desc = desc.replace("\n", " ").strip()
        lines.append(f"Role: {desc}")
        lines.append("")

    # Add tools if present
    if "tools" in metadata:
        tools = metadata["tools"]
        lines.append(f"Tools: {', '.join(tools)}")
        lines.append("")

    # Add separator and body
    lines.append("---")
    lines.append("")
    lines.append(body)

    developer_instructions = "\n".join(lines)

    # Escape triple quotes for TOML
    developer_instructions = developer_instructions.replace('"""', '\\"\\"\\"')

    # Build TOML output
    toml_lines = [
        f'sandbox_mode = "{sandbox_mode}"',
        "",
        'developer_instructions = """',
        developer_instructions,
        '"""',
    ]

    return "\n".join(toml_lines)


def parse_toml(content: str) -> tuple[dict, str]:
    """Parse simple TOML file (sandbox_mode and developer_instructions only)."""
    metadata = {}
    instructions = ""

    lines = content.split("\n")
    in_instructions = False
    instruction_lines = []

    for line in lines:
        if in_instructions:
            if line.strip() == '"""':
                in_instructions = False
            else:
                instruction_lines.append(line)
        elif line.startswith("sandbox_mode"):
            # Extract value (supports hyphens like "read-only", "allow-edits")
            match = re.search(r'sandbox_mode\s*=\s*["\']?([a-z-]+)["\']?', line)
            if match:
                metadata["sandbox_mode"] = match.group(1)
        elif line.startswith('developer_instructions = """'):
            in_instructions = True

    instructions = "\n".join(instruction_lines)
    return metadata, instructions


def toml_to_md(metadata: dict, instructions: str) -> str:
    """Convert TOML metadata and instructions to MD format."""
    sandbox_mode = metadata.get("sandbox_mode", "allow-edits")
    tools = sandbox_mode_to_tools(sandbox_mode)

    # Extract role from instructions if present
    description = ""
    role_match = re.search(r"^Role:\s*(.+)$", instructions, re.MULTILINE)
    if role_match:
        description = role_match.group(1).strip()

    # Build frontmatter
    lines = [
        "---",
        'name: "agent"',  # Generic name, user should customize
    ]

    if description:
        lines.append("description: >")
        lines.append(f"  {description}")

    lines.append("tools:")
    for tool in tools:
        lines.append(f"  - {tool}")

    lines.append("---")
    lines.append("")
    lines.append(instructions)

    return "\n".join(lines)


def convert_file(
    input_path: Path, output_dir: Path = None, to_md: bool = False
) -> Path:
    """Convert a single file."""
    content = input_path.read_text()

    if to_md:
        # TOML → MD
        metadata, instructions = parse_toml(content)
        output_content = toml_to_md(metadata, instructions)
        output_name = input_path.stem + ".md"
    else:
        # MD → TOML
        metadata, instructions = parse_md_frontmatter(content)
        output_content = md_to_toml(metadata, instructions)
        output_name = input_path.stem + ".toml"

    # Determine output path
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_name
    else:
        output_path = input_path.parent / output_name

    output_path.write_text(output_content + "\n")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert agent definitions between MD and TOML formats"
    )
    parser.add_argument("input", nargs="?", help="Input file or directory")
    parser.add_argument(
        "--batch", metavar="DIR", help="Convert all agents in directory"
    )
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--to-md", action="store_true", help="Convert TOML to MD")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing files"
    )

    args = parser.parse_args()

    if args.batch:
        input_dir = Path(args.batch)
        output_dir = Path(args.output) if args.output else None

        # Find all agent files
        patterns = ["*.toml"] if args.to_md else ["*.md"]
        files = []
        for pattern in patterns:
            files.extend(input_dir.glob(pattern))

        if not files:
            print(f"No {'TOML' if args.to_md else 'MD'} files found in {input_dir}")
            sys.exit(1)

        for f in files:
            output_path = convert_file(f, output_dir, args.to_md)
            print(f"Converted: {f} → {output_path}")

    elif args.input:
        input_path = Path(args.input)
        output_dir = Path(args.output) if args.output else None
        output_path = convert_file(input_path, output_dir, args.to_md)
        print(f"Converted: {input_path} → {output_path}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
