"""
Tests for skill validation
"""
import pytest
from pathlib import Path
import tempfile
import os

from skills.validation.validator import SkillValidator, validate_skill_directory


def test_validator_with_valid_skill():
    """Test validator with a valid skill"""
    skills_dir = Path(__file__).parent.parent.parent / "skills" / "web_summarizer"
    
    validator = SkillValidator(skills_dir)
    is_valid = validator.validate()
    
    assert is_valid
    assert len(validator.get_errors()) == 0


def test_validator_with_missing_files():
    """Test validator with missing required files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir) / "test_skill"
        skill_dir.mkdir()
        
        validator = SkillValidator(skill_dir)
        is_valid = validator.validate()
        
        assert not is_valid
        errors = validator.get_errors()
        assert any("skill.yaml" in error for error in errors)


def test_validate_skill_directory():
    """Test validate_skill_directory helper function"""
    skills_dir = Path(__file__).parent.parent.parent / "skills" / "doc_transformer"
    
    is_valid, errors = validate_skill_directory(skills_dir)
    
    assert is_valid
    assert len(errors) == 0


def test_validator_all_starter_skills():
    """Test that all starter skills are valid"""
    skills_base = Path(__file__).parent.parent.parent / "skills"
    
    starter_skills = ["web_summarizer", "doc_transformer", "task_planner"]
    
    for skill_name in starter_skills:
        skill_dir = skills_base / skill_name
        if skill_dir.exists():
            is_valid, errors = validate_skill_directory(skill_dir)
            assert is_valid, f"Skill {skill_name} is invalid: {errors}"
