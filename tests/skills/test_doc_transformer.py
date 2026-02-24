"""
Tests for doc_transformer skill
"""
import pytest
from pathlib import Path

from skills.doc_transformer import DocTransformer


def test_doc_transformer_initialization():
    """Test skill initialization"""
    skill = DocTransformer()
    assert skill.metadata is not None
    assert skill.metadata.name == "doc_transformer"
    assert skill.metadata.version == "0.1.0"


def test_doc_transformer_module():
    """Test skill module"""
    skill = DocTransformer()
    module = skill.get_module()
    assert module is not None


def test_doc_transformer_signature():
    """Test skill signature"""
    skill = DocTransformer()
    signature = skill.get_signature()
    assert signature is not None


def test_doc_transformer_validate_input():
    """Test input validation"""
    skill = DocTransformer()
    
    # Valid input
    valid_input = {
        "document": "test",
        "source_format": "markdown",
        "target_format": "html"
    }
    assert skill.validate_input(valid_input)
    
    # Invalid input (missing required fields)
    assert not skill.validate_input({"document": "test"})


def test_doc_transformer_metadata():
    """Test metadata properties"""
    skill = DocTransformer()
    
    assert skill.metadata.author == "Qredence"
    assert "transformation" in skill.metadata.tags
    assert skill.metadata.safety_permissions.internet_access is False
    assert skill.metadata.has_golden_evals is True
