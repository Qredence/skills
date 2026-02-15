"""
Tests for task_planner skill
"""
import pytest
from pathlib import Path

from skills.task_planner import TaskPlanner


def test_task_planner_initialization():
    """Test skill initialization"""
    skill = TaskPlanner()
    assert skill.metadata is not None
    assert skill.metadata.name == "task_planner"
    assert skill.metadata.version == "0.1.0"


def test_task_planner_module():
    """Test skill module"""
    skill = TaskPlanner()
    module = skill.get_module()
    assert module is not None


def test_task_planner_signature():
    """Test skill signature"""
    skill = TaskPlanner()
    signature = skill.get_signature()
    assert signature is not None


def test_task_planner_validate_input():
    """Test input validation"""
    skill = TaskPlanner()
    
    # Valid input
    assert skill.validate_input({"goal": "Build something"})
    
    # Invalid input (missing required field)
    assert not skill.validate_input({})


def test_task_planner_metadata():
    """Test metadata properties"""
    skill = TaskPlanner()
    
    assert skill.metadata.author == "Qredence"
    assert "planning" in skill.metadata.tags
    assert skill.metadata.safety_permissions.internet_access is False
    assert skill.metadata.has_golden_evals is True
