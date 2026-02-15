"""
Document Transformer skill implementation
"""
from typing import Type, Dict, Any
from pathlib import Path
import dspy

from skills.core.base import Skill


class DocTransformerSignature(dspy.Signature):
    """DSPy signature for document transformation"""
    
    document: str = dspy.InputField(desc="Document content to transform")
    source_format: str = dspy.InputField(desc="Source format")
    target_format: str = dspy.InputField(desc="Target format")
    style: str = dspy.InputField(desc="Target style")
    transformed_document: str = dspy.OutputField(desc="Transformed document")
    changes_made: str = dspy.OutputField(desc="List of changes as comma-separated")


class DocTransformerModule(dspy.Module):
    """DSPy module for document transformation"""
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(DocTransformerSignature)
    
    def forward(
        self,
        document: str,
        source_format: str,
        target_format: str,
        style: str = "formal"
    ) -> dspy.Prediction:
        """
        Transform document
        
        Args:
            document: Document content to transform
            source_format: Source format
            target_format: Target format
            style: Target style
            
        Returns:
            DSPy prediction with transformed_document and changes_made
        """
        result = self.prog(
            document=document,
            source_format=source_format,
            target_format=target_format,
            style=style
        )
        
        return result


class DocTransformer(Skill):
    """
    Transforms documents between different formats and styles
    """
    
    def __init__(self, metadata_path: Path = None):
        if metadata_path is None:
            metadata_path = Path(__file__).parent / "skill.yaml"
        super().__init__(metadata_path)
        self._module = DocTransformerModule()
        self._signature = DocTransformerSignature
    
    def get_module(self) -> dspy.Module:
        """Return the DSPy Module"""
        return self._module
    
    def get_signature(self) -> Type[dspy.Signature]:
        """Return the DSPy Signature"""
        return self._signature
