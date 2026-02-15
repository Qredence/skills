"""Core base classes for DSPy skills"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from pathlib import Path
import yaml

from pydantic import BaseModel, Field, ValidationError
import dspy


class SafetyPermissions(BaseModel):
    """Safety permissions for skill execution"""
    
    internet_access: bool = Field(default=False, description="Requires internet access")
    file_system_read: bool = Field(default=False, description="Requires file system read access")
    file_system_write: bool = Field(default=False, description="Requires file system write access")
    external_api_calls: bool = Field(default=False, description="Makes external API calls")
    data_persistence: bool = Field(default=False, description="Persists data")
    user_interaction: bool = Field(default=False, description="Requires user interaction")
    sensitive_data: bool = Field(default=False, description="Handles sensitive data")


class IOSchema(BaseModel):
    """Input/Output schema definition"""
    
    name: str = Field(..., description="Schema name")
    description: str = Field(..., description="Schema description")
    schema_: Dict[str, Any] = Field(..., description="JSON schema definition", alias="schema")
    
    model_config = {"populate_by_name": True}


class SkillMetadata(BaseModel):
    """Metadata for a skill"""
    
    name: str = Field(..., description="Skill name (snake_case)")
    version: str = Field(..., description="Skill version (semver)")
    description: str = Field(..., description="Short description of the skill")
    author: str = Field(..., description="Skill author")
    tags: List[str] = Field(default_factory=list, description="Skill tags")
    
    # DSPy configuration
    module_class: str = Field(..., description="DSPy Module class name")
    signature_class: str = Field(..., description="DSPy Signature class name")
    
    # Schemas
    input_schema: IOSchema = Field(..., description="Input schema")
    output_schema: IOSchema = Field(..., description="Output schema")
    
    # Safety
    safety_permissions: SafetyPermissions = Field(
        default_factory=SafetyPermissions,
        description="Required safety permissions"
    )
    
    # Testing
    has_tests: bool = Field(default=True, description="Has unit tests")
    has_golden_evals: bool = Field(default=False, description="Has golden evaluation examples")


class Skill(ABC):
    """Base class for all DSPy skills"""
    
    def __init__(self, metadata_path: Optional[Path] = None):
        """
        Initialize skill
        
        Args:
            metadata_path: Path to skill.yaml metadata file
        """
        self.metadata: Optional[SkillMetadata] = None
        self._module: Optional[dspy.Module] = None
        self._signature: Optional[Type[dspy.Signature]] = None
        
        if metadata_path:
            self.load_metadata(metadata_path)
    
    def load_metadata(self, path: Path) -> None:
        """Load metadata from skill.yaml"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        self.metadata = SkillMetadata(**data)
    
    @abstractmethod
    def get_module(self) -> dspy.Module:
        """Return the DSPy Module for this skill"""
        pass
    
    @abstractmethod
    def get_signature(self) -> Type[dspy.Signature]:
        """Return the DSPy Signature for this skill"""
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against input schema"""
        if not self.metadata:
            raise ValueError("Metadata not loaded")
        
        # Simple validation - in production, use jsonschema
        required_fields = self.metadata.input_schema.schema_.get("required", [])
        for field in required_fields:
            if field not in input_data:
                return False
        return True
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output against output schema"""
        if not self.metadata:
            raise ValueError("Metadata not loaded")
        
        # Simple validation - in production, use jsonschema
        required_fields = self.metadata.output_schema.schema_.get("required", [])
        for field in required_fields:
            if field not in output_data:
                return False
        return True
    
    def execute(self, **kwargs) -> Any:
        """
        Execute the skill with given inputs
        
        Args:
            **kwargs: Input parameters
            
        Returns:
            Skill output
        """
        if not self.validate_input(kwargs):
            raise ValueError("Invalid input data")
        
        module = self.get_module()
        result = module(**kwargs)
        
        return result
