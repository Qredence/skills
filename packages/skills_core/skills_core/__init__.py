"""
Skills Core - Core library for Qredence DSPy Skills Registry
"""

__version__ = "0.1.0"

from skills_core.types import (
    SkillMetadata,
    SafetyLevel,
    CatalogEntry,
    Catalog,
    PermissionsModel,
    SafetyModel,
)
from skills_core.loader import load_skill_metadata, discover_skills, get_skill_by_id
from skills_core.validator import validate_skill, validate_all_skills
from skills_core.catalog import generate_catalog, load_catalog, compare_catalogs
from skills_core.dspy_contract import (
    import_from_path,
    is_dspy_module,
    is_dspy_signature,
    verify_skill_contract,
)
from skills_core.evals import run_skill_eval, EvalResult

__all__ = [
    "SkillMetadata",
    "SafetyLevel",
    "CatalogEntry",
    "Catalog",
    "PermissionsModel",
    "SafetyModel",
    "load_skill_metadata",
    "discover_skills",
    "get_skill_by_id",
    "validate_skill",
    "validate_all_skills",
    "generate_catalog",
    "load_catalog",
    "compare_catalogs",
    "import_from_path",
    "is_dspy_module",
    "is_dspy_signature",
    "verify_skill_contract",
    "run_skill_eval",
    "EvalResult",
]
