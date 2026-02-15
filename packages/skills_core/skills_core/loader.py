"""
Skill discovery and metadata loading
"""
import yaml
from pathlib import Path
from typing import List, Optional
from skills_core.types import SkillMetadata


def load_skill_metadata(skill_path: Path) -> SkillMetadata:
    """
    Load and validate skill metadata from skill.yaml
    
    Args:
        skill_path: Path to skill directory containing skill.yaml
        
    Returns:
        Validated SkillMetadata object
        
    Raises:
        FileNotFoundError: If skill.yaml doesn't exist
        ValueError: If metadata is invalid
    """
    yaml_path = skill_path / "skill.yaml"
    
    if not yaml_path.exists():
        raise FileNotFoundError(f"skill.yaml not found in {skill_path}")
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Validate using Pydantic model
    metadata = SkillMetadata(**data)
    
    return metadata


def discover_skills(skills_dir: Path, skip_templates: bool = True) -> List[SkillMetadata]:
    """
    Discover all skills in a directory
    
    Args:
        skills_dir: Path to skills directory
        skip_templates: Whether to skip _templates directory
        
    Returns:
        List of SkillMetadata objects sorted by ID
    """
    skills = []
    
    if not skills_dir.exists():
        return skills
    
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        # Skip template directory and Python package directories
        if skip_templates and skill_dir.name.startswith('_'):
            continue
        
        # Skip non-skill directories (core, registry, etc.)
        if skill_dir.name in ['core', 'registry', 'validation', 'template']:
            continue
        
        # Check if skill.yaml exists
        yaml_path = skill_dir / "skill.yaml"
        if not yaml_path.exists():
            continue
        
        try:
            metadata = load_skill_metadata(skill_dir)
            skills.append(metadata)
        except Exception as e:
            print(f"Warning: Failed to load skill from {skill_dir}: {e}")
    
    # Sort by ID for deterministic ordering
    skills.sort(key=lambda s: s.id)
    
    return skills


def get_skill_by_id(skills_dir: Path, skill_id: str) -> Optional[SkillMetadata]:
    """
    Get a specific skill by ID
    
    Args:
        skills_dir: Path to skills directory
        skill_id: Skill ID to find
        
    Returns:
        SkillMetadata if found, None otherwise
    """
    skill_path = skills_dir / skill_id
    
    if not skill_path.exists():
        return None
    
    try:
        return load_skill_metadata(skill_path)
    except Exception:
        return None
