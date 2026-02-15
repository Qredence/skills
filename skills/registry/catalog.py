"""Skill registry and catalog management"""
import json
from pathlib import Path
from typing import Dict, List, Optional
import yaml

from skills.core.base import SkillMetadata


class SkillRegistry:
    """Registry for managing DSPy skills"""
    
    def __init__(self, skills_dir: Path):
        """
        Initialize skill registry
        
        Args:
            skills_dir: Directory containing skill subdirectories
        """
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, SkillMetadata] = {}
    
    def discover_skills(self) -> List[SkillMetadata]:
        """
        Discover all skills in the skills directory
        
        Returns:
            List of skill metadata objects
        """
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        # Look for skill.yaml in subdirectories
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            metadata_file = skill_dir / "skill.yaml"
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        data = yaml.safe_load(f)
                    metadata = SkillMetadata(**data)
                    skills.append(metadata)
                    self.skills[metadata.name] = metadata
                except Exception as e:
                    print(f"Error loading skill from {skill_dir}: {e}")
        
        return skills
    
    def get_skill(self, name: str) -> Optional[SkillMetadata]:
        """
        Get skill metadata by name
        
        Args:
            name: Skill name
            
        Returns:
            Skill metadata or None
        """
        return self.skills.get(name)
    
    def generate_catalog(self, output_path: Path) -> None:
        """
        Generate skills.json catalog from discovered skills
        
        Args:
            output_path: Path to output catalog file
        """
        catalog_data = {
            "version": "1.0",
            "skills": []
        }
        
        for skill_name, metadata in self.skills.items():
            catalog_data["skills"].append({
                "name": metadata.name,
                "version": metadata.version,
                "description": metadata.description,
                "author": metadata.author,
                "tags": metadata.tags,
                "module_class": metadata.module_class,
                "signature_class": metadata.signature_class,
                "input_schema": {
                    "name": metadata.input_schema.name,
                    "description": metadata.input_schema.description,
                    "schema": metadata.input_schema.schema
                },
                "output_schema": {
                    "name": metadata.output_schema.name,
                    "description": metadata.output_schema.description,
                    "schema": metadata.output_schema.schema
                },
                "safety_permissions": metadata.safety_permissions.model_dump(),
                "has_tests": metadata.has_tests,
                "has_golden_evals": metadata.has_golden_evals
            })
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(catalog_data, f, indent=2)
    
    def validate_all_skills(self) -> Dict[str, List[str]]:
        """
        Validate all discovered skills
        
        Returns:
            Dictionary mapping skill names to lists of validation errors
        """
        validation_results = {}
        
        for skill_name, metadata in self.skills.items():
            errors = []
            
            # Basic validation
            if not metadata.name:
                errors.append("Skill name is required")
            
            if not metadata.version:
                errors.append("Skill version is required")
            
            if not metadata.module_class:
                errors.append("Module class is required")
            
            if not metadata.signature_class:
                errors.append("Signature class is required")
            
            validation_results[skill_name] = errors
        
        return validation_results
