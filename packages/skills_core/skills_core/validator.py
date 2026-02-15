"""
Skill validation against JSON Schema and structural requirements
"""
import json
import jsonschema
from pathlib import Path
from typing import Dict, List, Tuple
from skills_core.loader import load_skill_metadata, discover_skills


class SkillValidationError(Exception):
    """Raised when skill validation fails"""
    pass


def validate_skill_structure(skill_path: Path) -> List[str]:
    """
    Validate that a skill has the required directory structure
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    required_files = [
        "skill.yaml",
        "README.md",
        "src/skill.py",
    ]
    
    required_dirs = [
        "src",
        "tests",
        "eval",
        "examples",
    ]
    
    # Check required files
    for file_path in required_files:
        if not (skill_path / file_path).exists():
            errors.append(f"Missing required file: {file_path}")
    
    # Check required directories
    for dir_path in required_dirs:
        if not (skill_path / dir_path).is_dir():
            errors.append(f"Missing required directory: {dir_path}/")
    
    # Check for golden eval set if specified
    try:
        metadata = load_skill_metadata(skill_path)
        golden_path = skill_path / metadata.eval.golden_set
        if not golden_path.exists():
            errors.append(f"Missing golden eval set: {metadata.eval.golden_set}")
    except Exception as e:
        errors.append(f"Failed to load metadata: {e}")
    
    return errors


def validate_skill_against_schema(skill_path: Path, schema_path: Path) -> List[str]:
    """
    Validate skill.yaml against JSON Schema
    
    Args:
        skill_path: Path to skill directory
        schema_path: Path to schema.skill.json
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    try:
        # Load skill metadata as raw dict
        import yaml
        with open(skill_path / "skill.yaml", 'r') as f:
            skill_data = yaml.safe_load(f)
        
        # Load JSON Schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Validate against schema
        jsonschema.validate(instance=skill_data, schema=schema)
        
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation error: {e.message}")
    except Exception as e:
        errors.append(f"Validation failed: {e}")
    
    return errors


def validate_dspy_imports(skill_path: Path) -> List[str]:
    """
    Validate that declared DSPy imports are accessible
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    try:
        metadata = load_skill_metadata(skill_path)
        
        # Check if skill.py exists
        skill_py = skill_path / "src" / "skill.py"
        if not skill_py.exists():
            errors.append("src/skill.py not found")
            return errors
        
        # Try to import the module
        import sys
        import importlib.util
        
        # Add parent to path temporarily
        repo_root = skill_path.parent.parent
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        try:
            # Try to import the declared module
            module_path, module_class = metadata.dspy.module.rsplit(':', 1)
            spec = importlib.util.find_spec(module_path.replace(':', '.'))
            
            if spec is None:
                errors.append(f"Cannot find DSPy module: {metadata.dspy.module}")
        except Exception as e:
            errors.append(f"Failed to import DSPy module: {e}")
        
    except Exception as e:
        errors.append(f"Import validation failed: {e}")
    
    return errors


def validate_skill(
    skill_path: Path,
    schema_path: Path,
    check_imports: bool = False
) -> Tuple[bool, List[str]]:
    """
    Comprehensive validation of a skill
    
    Args:
        skill_path: Path to skill directory
        schema_path: Path to schema.skill.json
        check_imports: Whether to validate DSPy imports
        
    Returns:
        Tuple of (is_valid, errors)
    """
    all_errors = []
    
    # Validate structure
    all_errors.extend(validate_skill_structure(skill_path))
    
    # Validate against schema
    all_errors.extend(validate_skill_against_schema(skill_path, schema_path))
    
    # Optionally validate imports
    if check_imports:
        all_errors.extend(validate_dspy_imports(skill_path))
    
    return len(all_errors) == 0, all_errors


def validate_all_skills(
    skills_dir: Path,
    schema_path: Path,
    check_imports: bool = False
) -> Dict[str, List[str]]:
    """
    Validate all skills in a directory
    
    Args:
        skills_dir: Path to skills directory
        schema_path: Path to schema.skill.json
        check_imports: Whether to validate DSPy imports
        
    Returns:
        Dictionary mapping skill ID to list of errors
    """
    results = {}
    
    # Discover all skills
    try:
        skills = discover_skills(skills_dir)
    except Exception as e:
        return {"_discovery_error": [str(e)]}
    
    # Validate each skill
    for metadata in skills:
        skill_path = skills_dir / metadata.id
        is_valid, errors = validate_skill(skill_path, schema_path, check_imports)
        results[metadata.id] = errors
    
    return results
