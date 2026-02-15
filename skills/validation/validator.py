"""Skill validation utilities"""
from pathlib import Path
from typing import List, Dict, Any
import yaml
import jsonschema

from skills.core.base import SkillMetadata


class SkillValidator:
    """Validator for skill metadata and structure"""
    
    def __init__(self, skill_dir: Path):
        """
        Initialize validator
        
        Args:
            skill_dir: Directory containing the skill
        """
        self.skill_dir = Path(skill_dir)
        self.errors: List[str] = []
    
    def validate(self) -> bool:
        """
        Validate skill structure and metadata
        
        Returns:
            True if valid, False otherwise
        """
        self.errors = []
        
        # Check required files
        if not self._validate_structure():
            return False
        
        # Validate metadata
        if not self._validate_metadata():
            return False
        
        # Validate schemas
        if not self._validate_schemas():
            return False
        
        return len(self.errors) == 0
    
    def _validate_structure(self) -> bool:
        """Validate skill directory structure"""
        required_files = ["skill.yaml", "__init__.py"]
        
        for file in required_files:
            file_path = self.skill_dir / file
            if not file_path.exists():
                self.errors.append(f"Required file missing: {file}")
        
        return len(self.errors) == 0
    
    def _validate_metadata(self) -> bool:
        """Validate skill.yaml metadata"""
        metadata_file = self.skill_dir / "skill.yaml"
        
        if not metadata_file.exists():
            return False
        
        try:
            with open(metadata_file, 'r') as f:
                data = yaml.safe_load(f)
            
            # Try to create SkillMetadata object
            metadata = SkillMetadata(**data)
            
            # Additional validation
            if not metadata.name.islower() or ' ' in metadata.name:
                self.errors.append("Skill name must be lowercase and use underscores")
            
            # Validate version format (simple semver check)
            version_parts = metadata.version.split('.')
            if len(version_parts) != 3:
                self.errors.append("Version must be in semver format (x.y.z)")
            
        except Exception as e:
            self.errors.append(f"Invalid metadata: {str(e)}")
            return False
        
        return len(self.errors) == 0
    
    def _validate_schemas(self) -> bool:
        """Validate input/output schemas"""
        metadata_file = self.skill_dir / "skill.yaml"
        
        try:
            with open(metadata_file, 'r') as f:
                data = yaml.safe_load(f)
            
            metadata = SkillMetadata(**data)
            
            # Validate that schemas have required properties
            for schema_name, schema in [
                ("input_schema", metadata.input_schema),
                ("output_schema", metadata.output_schema)
            ]:
                if "type" not in schema.schema:
                    self.errors.append(f"{schema_name} must have 'type' property")
                
                if "properties" not in schema.schema and schema.schema.get("type") == "object":
                    self.errors.append(f"{schema_name} of type 'object' must have 'properties'")
        
        except Exception as e:
            self.errors.append(f"Schema validation error: {str(e)}")
            return False
        
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """Get validation errors"""
        return self.errors


def validate_skill_directory(skill_dir: Path) -> tuple[bool, List[str]]:
    """
    Validate a skill directory
    
    Args:
        skill_dir: Path to skill directory
        
    Returns:
        Tuple of (is_valid, errors)
    """
    validator = SkillValidator(skill_dir)
    is_valid = validator.validate()
    return is_valid, validator.get_errors()
