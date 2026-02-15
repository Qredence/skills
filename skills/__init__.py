"""
Qredence Skills - Python-first registry of DSPy Module/Signature skills
"""

__version__ = "0.1.0"

from skills.core.base import Skill, SkillMetadata
from skills.registry.catalog import SkillRegistry

__all__ = ["Skill", "SkillMetadata", "SkillRegistry"]
