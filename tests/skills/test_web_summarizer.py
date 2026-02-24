"""
Tests for web_summarizer skill
"""
import pytest
from pathlib import Path

from skills.web_summarizer import WebSummarizer


def test_web_summarizer_initialization():
    """Test skill initialization"""
    skill = WebSummarizer()
    assert skill.metadata is not None
    assert skill.metadata.name == "web_summarizer"
    assert skill.metadata.version == "0.1.0"


def test_web_summarizer_module():
    """Test skill module"""
    skill = WebSummarizer()
    module = skill.get_module()
    assert module is not None


def test_web_summarizer_signature():
    """Test skill signature"""
    skill = WebSummarizer()
    signature = skill.get_signature()
    assert signature is not None


def test_web_summarizer_validate_input():
    """Test input validation"""
    skill = WebSummarizer()
    
    # Valid input
    assert skill.validate_input({"url": "https://example.com"})
    
    # Invalid input (missing required field)
    assert not skill.validate_input({})


def test_web_summarizer_metadata():
    """Test metadata properties"""
    skill = WebSummarizer()
    
    assert skill.metadata.author == "Qredence"
    assert "summarization" in skill.metadata.tags
    assert skill.metadata.safety_permissions.internet_access is True
    assert skill.metadata.has_golden_evals is True
