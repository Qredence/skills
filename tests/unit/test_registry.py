"""
Tests for skill registry
"""
import pytest
from pathlib import Path
import tempfile
import json

from skills.registry.catalog import SkillRegistry


def test_registry_initialization():
    """Test registry initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SkillRegistry(Path(tmpdir))
        assert registry.skills_dir == Path(tmpdir)
        assert len(registry.skills) == 0


def test_registry_discover_skills():
    """Test skill discovery"""
    # Use actual skills directory
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    registry = SkillRegistry(skills_dir)
    
    skills = registry.discover_skills()
    
    # Should find at least our 3 starter skills
    assert len(skills) >= 3
    
    skill_names = [s.name for s in skills]
    assert "web_summarizer" in skill_names
    assert "doc_transformer" in skill_names
    assert "task_planner" in skill_names


def test_registry_get_skill():
    """Test getting a skill by name"""
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    registry = SkillRegistry(skills_dir)
    registry.discover_skills()
    
    skill = registry.get_skill("web_summarizer")
    assert skill is not None
    assert skill.name == "web_summarizer"


def test_registry_generate_catalog():
    """Test catalog generation"""
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    registry = SkillRegistry(skills_dir)
    registry.discover_skills()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        catalog_path = Path(tmpdir) / "catalog" / "skills.json"
        registry.generate_catalog(catalog_path)
        
        assert catalog_path.exists()
        
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        assert "version" in catalog
        assert "skills" in catalog
        assert len(catalog["skills"]) >= 3


def test_registry_validate_all_skills():
    """Test validation of all skills"""
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    registry = SkillRegistry(skills_dir)
    registry.discover_skills()
    
    validation_results = registry.validate_all_skills()
    
    # All our skills should have no errors
    for skill_name, errors in validation_results.items():
        assert len(errors) == 0, f"Skill {skill_name} has errors: {errors}"
