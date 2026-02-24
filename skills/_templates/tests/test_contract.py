"""
Template contract tests - validates DSPy skill contract
"""
import pytest
from pathlib import Path
import sys

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from skills.SKILL_ID.src.skill import Skill, SkillSignature, SIGNATURES
import dspy


def test_skill_class_exists():
    """Verify Skill class is defined and is a DSPy Module"""
    assert Skill is not None
    assert issubclass(Skill, dspy.Module)


def test_signature_exists():
    """Verify Signature class is defined and is a DSPy Signature"""
    assert SkillSignature is not None
    assert issubclass(SkillSignature, dspy.Signature)


def test_signatures_export():
    """Verify SIGNATURES list is exported"""
    assert SIGNATURES is not None
    assert len(SIGNATURES) > 0
    assert SkillSignature in SIGNATURES


def test_skill_instantiation():
    """Verify skill can be instantiated"""
    skill = Skill()
    assert skill is not None


def test_skill_has_forward():
    """Verify skill has forward method"""
    skill = Skill()
    assert hasattr(skill, 'forward')
    assert callable(skill.forward)


# Add functional tests below
def test_skill_execution():
    """Test basic skill execution"""
    # TODO: Implement actual execution test
    pass
