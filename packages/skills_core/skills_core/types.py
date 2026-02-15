"""
Pydantic models for DSPy skill metadata and catalog entries
"""
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class SafetyLevel(str, Enum):
    """Safety classification for skills"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PermissionsModel(BaseModel):
    """Permission requirements for skill execution"""
    network: bool = Field(default=False, description="Requires network access")
    filesystem_read: bool = Field(default=False, description="Requires filesystem read")
    filesystem_write: bool = Field(default=False, description="Requires filesystem write")
    external_tools: List[str] = Field(default_factory=list, description="External tools required")


class SafetyModel(BaseModel):
    """Safety declaration for a skill"""
    level: SafetyLevel = Field(..., description="Safety classification")
    risks: List[str] = Field(default_factory=list, description="Known risks")
    mitigations: List[str] = Field(default_factory=list, description="Risk mitigations")
    data_policy: List[str] = Field(default_factory=list, description="Data handling policies")


class DSPyConfigModel(BaseModel):
    """DSPy Module and Signature configuration"""
    module: str = Field(..., description="Import path to DSPy Module class")
    signatures: List[str] = Field(..., description="Import paths to DSPy Signature classes")
    dependencies: List[str] = Field(default_factory=list, description="Python dependencies")


class IOModel(BaseModel):
    """Input/Output schema definitions"""
    inputs_schema: Dict[str, Any] = Field(..., description="JSON Schema for inputs")
    outputs_schema: Dict[str, Any] = Field(..., description="JSON Schema for outputs")


class BehaviorModel(BaseModel):
    """Behavioral characteristics of the skill"""
    deterministic: bool = Field(..., description="Whether outputs are deterministic")
    temperature_hint: float = Field(default=0.0, ge=0.0, le=2.0, description="Recommended temperature")
    max_tokens_hint: Optional[int] = Field(default=None, ge=1, description="Recommended max tokens")
    notes: List[str] = Field(default_factory=list, description="Behavioral notes")


class EvalModel(BaseModel):
    """Evaluation configuration"""
    golden_set: str = Field(..., description="Path to golden evaluation set (JSONL)")
    metrics: List[str] = Field(..., description="Evaluation metrics to use")
    
    @field_validator('golden_set')
    @classmethod
    def validate_golden_set_path(cls, v: str) -> str:
        if not v.startswith('eval/') or not v.endswith('.jsonl'):
            raise ValueError("golden_set must be a path starting with 'eval/' and ending with '.jsonl'")
        return v
    
    @field_validator('metrics')
    @classmethod
    def validate_metrics(cls, v: List[str]) -> List[str]:
        allowed_metrics = {'exact_match', 'contains', 'json_schema_valid'}
        for metric in v:
            if metric not in allowed_metrics:
                raise ValueError(f"Invalid metric: {metric}. Must be one of {allowed_metrics}")
        return v


class SkillMetadata(BaseModel):
    """Complete metadata for a DSPy skill"""
    id: str = Field(..., description="Unique kebab-case identifier", pattern=r'^[a-z][a-z0-9_]*$')
    name: str = Field(..., min_length=1, description="Human-readable skill name")
    version: str = Field(..., description="Semantic version", pattern=r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$')
    description: str = Field(..., min_length=10, max_length=200, description="1-2 sentence description")
    tags: List[str] = Field(..., min_items=1, description="Searchable tags")
    
    dspy: DSPyConfigModel = Field(..., description="DSPy configuration")
    io: IOModel = Field(..., description="Input/output schemas")
    behavior: BehaviorModel = Field(..., description="Behavioral characteristics")
    permissions: PermissionsModel = Field(..., description="Permission requirements")
    safety: SafetyModel = Field(..., description="Safety declaration")
    eval: EvalModel = Field(..., description="Evaluation configuration")
    
    owner: Optional[str] = Field(default=None, description="Skill owner")
    resources: List[str] = Field(default_factory=list, description="Additional resources")
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        for tag in v:
            if not tag.islower() or not tag.replace('-', '').replace('_', '').isalnum():
                raise ValueError(f"Tag must be lowercase alphanumeric with hyphens/underscores: {tag}")
        return v
    
    model_config = {"extra": "forbid"}


class CatalogEntry(BaseModel):
    """Entry in the skills catalog"""
    id: str
    name: str
    version: str
    description: str
    tags: List[str]
    safety_level: SafetyLevel
    permissions: PermissionsModel
    dspy_module: str
    owner: Optional[str] = None


class Catalog(BaseModel):
    """Complete skills catalog"""
    version: str = Field(..., description="Catalog format version")
    generated_at: str = Field(..., description="ISO 8601 timestamp")
    skills: List[CatalogEntry] = Field(..., description="List of skills sorted by ID")
