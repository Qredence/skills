"""Skill template scaffold generator"""
from pathlib import Path
from typing import Optional
import os


class SkillTemplate:
    """Generate skill template scaffold"""
    
    SKILL_YAML_TEMPLATE = """name: {name}
version: "0.1.0"
description: "{description}"
author: "{author}"
tags: {tags}

# DSPy configuration
module_class: "{module_class}"
signature_class: "{signature_class}"

# Input schema
input_schema:
  name: "{name}Input"
  description: "Input schema for {name}"
  schema:
    type: "object"
    properties:
      input_text:
        type: "string"
        description: "Input text"
    required:
      - input_text

# Output schema
output_schema:
  name: "{name}Output"
  description: "Output schema for {name}"
  schema:
    type: "object"
    properties:
      output_text:
        type: "string"
        description: "Output text"
    required:
      - output_text

# Safety permissions
safety_permissions:
  internet_access: false
  file_system_read: false
  file_system_write: false
  external_api_calls: false
  data_persistence: false
  user_interaction: false
  sensitive_data: false

# Testing
has_tests: true
has_golden_evals: false
"""
    
    SKILL_INIT_TEMPLATE = '''"""
{name} skill implementation
"""
from typing import Type
from pathlib import Path
import dspy

from skills.core.base import Skill


class {signature_class}(dspy.Signature):
    """DSPy signature for {name}"""
    
    input_text: str = dspy.InputField(desc="Input text to process")
    output_text: str = dspy.OutputField(desc="Processed output text")


class {module_class}(dspy.Module):
    """DSPy module for {name}"""
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought({signature_class})
    
    def forward(self, input_text: str) -> dspy.Prediction:
        """
        Execute the skill
        
        Args:
            input_text: Input text to process
            
        Returns:
            DSPy prediction with output_text
        """
        return self.prog(input_text=input_text)


class {class_name}(Skill):
    """
    {description}
    """
    
    def __init__(self, metadata_path: Path = None):
        if metadata_path is None:
            metadata_path = Path(__file__).parent / "skill.yaml"
        super().__init__(metadata_path)
        self._module = {module_class}()
        self._signature = {signature_class}
    
    def get_module(self) -> dspy.Module:
        """Return the DSPy Module"""
        return self._module
    
    def get_signature(self) -> Type[dspy.Signature]:
        """Return the DSPy Signature"""
        return self._signature
'''
    
    TEST_TEMPLATE = '''"""
Tests for {name} skill
"""
import pytest
from pathlib import Path

from skills.{name} import {class_name}


def test_{name}_initialization():
    """Test skill initialization"""
    skill = {class_name}()
    assert skill.metadata is not None
    assert skill.metadata.name == "{name}"


def test_{name}_module():
    """Test skill module"""
    skill = {class_name}()
    module = skill.get_module()
    assert module is not None


def test_{name}_signature():
    """Test skill signature"""
    skill = {class_name}()
    signature = skill.get_signature()
    assert signature is not None


def test_{name}_validate_input():
    """Test input validation"""
    skill = {class_name}()
    
    # Valid input
    assert skill.validate_input({{"input_text": "test"}})
    
    # Invalid input (missing required field)
    assert not skill.validate_input({{}})


# Add more tests specific to your skill
'''
    
    GOLDEN_EVAL_TEMPLATE = '''"""
Golden evaluation examples for {name}
"""

# Define golden examples as a list of (input, expected_output) tuples
GOLDEN_EXAMPLES = [
    (
        {{"input_text": "example input 1"}},
        {{"output_text": "expected output 1"}}
    ),
    (
        {{"input_text": "example input 2"}},
        {{"output_text": "expected output 2"}}
    ),
]


def get_golden_examples():
    """Return golden evaluation examples"""
    return GOLDEN_EXAMPLES
'''
    
    @staticmethod
    def generate(
        skill_name: str,
        output_dir: Path,
        description: str = "A new skill",
        author: str = "Qredence",
        tags: Optional[list] = None
    ) -> Path:
        """
        Generate a new skill scaffold
        
        Args:
            skill_name: Name of the skill (snake_case)
            output_dir: Directory to create the skill in
            description: Skill description
            author: Skill author
            tags: List of tags
            
        Returns:
            Path to created skill directory
        """
        if tags is None:
            tags = []
        
        # Create skill directory
        skill_dir = Path(output_dir) / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate class names
        class_name = ''.join(word.capitalize() for word in skill_name.split('_'))
        module_class = f"{class_name}Module"
        signature_class = f"{class_name}Signature"
        
        # Create skill.yaml
        skill_yaml_content = SkillTemplate.SKILL_YAML_TEMPLATE.format(
            name=skill_name,
            description=description,
            author=author,
            tags=tags,
            module_class=module_class,
            signature_class=signature_class
        )
        
        with open(skill_dir / "skill.yaml", 'w') as f:
            f.write(skill_yaml_content)
        
        # Create __init__.py
        skill_init_content = SkillTemplate.SKILL_INIT_TEMPLATE.format(
            name=skill_name,
            description=description,
            class_name=class_name,
            module_class=module_class,
            signature_class=signature_class
        )
        
        with open(skill_dir / "__init__.py", 'w') as f:
            f.write(skill_init_content)
        
        # Create test file
        test_dir = Path(output_dir).parent / "tests" / "skills"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_content = SkillTemplate.TEST_TEMPLATE.format(
            name=skill_name,
            class_name=class_name
        )
        
        with open(test_dir / f"test_{skill_name}.py", 'w') as f:
            f.write(test_content)
        
        # Create golden_eval.py
        golden_eval_content = SkillTemplate.GOLDEN_EVAL_TEMPLATE.format(
            name=skill_name
        )
        
        with open(skill_dir / "golden_eval.py", 'w') as f:
            f.write(golden_eval_content)
        
        return skill_dir
