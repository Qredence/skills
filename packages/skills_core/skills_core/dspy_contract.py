"""
DSPy Module and Signature reflection utilities
"""
import importlib
import inspect
from typing import Any, List, Optional, Type
from pathlib import Path


def import_from_path(import_path: str) -> Any:
    """
    Import a Python object from a module:object path
    
    Args:
        import_path: String in format "module.path:ObjectName"
        
    Returns:
        The imported object
        
    Raises:
        ImportError: If import fails
    """
    if ':' not in import_path:
        raise ValueError(f"Invalid import path format: {import_path}. Expected 'module:object'")
    
    module_path, obj_name = import_path.rsplit(':', 1)
    module = importlib.import_module(module_path)
    
    if not hasattr(module, obj_name):
        raise ImportError(f"Object '{obj_name}' not found in module '{module_path}'")
    
    return getattr(module, obj_name)


def is_dspy_module(obj: Any) -> bool:
    """
    Check if an object is a DSPy Module class
    
    Args:
        obj: Object to check
        
    Returns:
        True if obj is a DSPy Module class
    """
    try:
        import dspy
        return inspect.isclass(obj) and issubclass(obj, dspy.Module)
    except ImportError:
        return False


def is_dspy_signature(obj: Any) -> bool:
    """
    Check if an object is a DSPy Signature class
    
    Args:
        obj: Object to check
        
    Returns:
        True if obj is a DSPy Signature class
    """
    try:
        import dspy
        return inspect.isclass(obj) and issubclass(obj, dspy.Signature)
    except ImportError:
        return False


def get_signature_fields(signature_class: Type) -> dict:
    """
    Extract input and output fields from a DSPy Signature
    
    Args:
        signature_class: DSPy Signature class
        
    Returns:
        Dictionary with 'inputs' and 'outputs' field lists
    """
    try:
        import dspy
        
        if not is_dspy_signature(signature_class):
            raise ValueError(f"{signature_class} is not a DSPy Signature")
        
        inputs = []
        outputs = []
        
        # Get class annotations
        annotations = getattr(signature_class, '__annotations__', {})
        
        for field_name, field_type in annotations.items():
            # Check if it's an InputField or OutputField
            field_value = getattr(signature_class, field_name, None)
            
            if hasattr(field_value, '__class__'):
                field_class_name = field_value.__class__.__name__
                
                if 'Input' in field_class_name:
                    inputs.append({
                        'name': field_name,
                        'type': str(field_type),
                        'description': getattr(field_value, 'desc', '')
                    })
                elif 'Output' in field_class_name:
                    outputs.append({
                        'name': field_name,
                        'type': str(field_type),
                        'description': getattr(field_value, 'desc', '')
                    })
        
        return {'inputs': inputs, 'outputs': outputs}
    
    except Exception as e:
        return {'inputs': [], 'outputs': [], 'error': str(e)}


def verify_skill_contract(skill_path: Path, module_path: str, signature_paths: List[str]) -> dict:
    """
    Verify that a skill implements the DSPy contract correctly
    
    Args:
        skill_path: Path to skill directory
        module_path: Import path to DSPy Module
        signature_paths: List of import paths to DSPy Signatures
        
    Returns:
        Dictionary with verification results
    """
    results = {
        'module_valid': False,
        'signatures_valid': [],
        'errors': []
    }
    
    try:
        # Import and validate module
        module_class = import_from_path(module_path)
        
        if not is_dspy_module(module_class):
            results['errors'].append(f"{module_path} is not a DSPy Module")
        else:
            results['module_valid'] = True
        
        # Import and validate signatures
        for sig_path in signature_paths:
            try:
                sig_class = import_from_path(sig_path)
                
                if not is_dspy_signature(sig_class):
                    results['errors'].append(f"{sig_path} is not a DSPy Signature")
                    results['signatures_valid'].append(False)
                else:
                    results['signatures_valid'].append(True)
            except Exception as e:
                results['errors'].append(f"Failed to import {sig_path}: {e}")
                results['signatures_valid'].append(False)
        
    except Exception as e:
        results['errors'].append(f"Failed to verify contract: {e}")
    
    return results
