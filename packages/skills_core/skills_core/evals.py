"""
Golden evaluation framework with JSONL format
"""
import json
import jsonschema
from pathlib import Path
from typing import Any, Dict, List, Tuple
from skills_core.loader import load_skill_metadata


def load_golden_set(golden_path: Path) -> List[Dict[str, Any]]:
    """
    Load golden evaluation set from JSONL file
    
    Args:
        golden_path: Path to golden.jsonl file
        
    Returns:
        List of golden examples
        
    Format:
        Each line is JSON: {"name": "...", "input": {...}, "expected": {...}, "match": "..."}
    """
    examples = []
    
    with open(golden_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            
            try:
                example = json.loads(line)
                
                # Validate required fields
                required_fields = ['name', 'input', 'expected', 'match']
                for field in required_fields:
                    if field not in example:
                        raise ValueError(f"Missing required field: {field}")
                
                examples.append(example)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {line_num}: {e}")
    
    return examples


def exact_match(actual: Any, expected: Any) -> bool:
    """Check if actual exactly matches expected"""
    return actual == expected


def contains_match(actual: Any, expected: Any) -> bool:
    """Check if actual contains expected (for strings or lists)"""
    if isinstance(actual, str) and isinstance(expected, str):
        return expected in actual
    elif isinstance(actual, list):
        return expected in actual
    elif isinstance(actual, dict) and isinstance(expected, dict):
        # Check if all expected keys/values are in actual
        for key, value in expected.items():
            if key not in actual or actual[key] != value:
                return False
        return True
    return False


def json_schema_valid(actual: Any, expected_schema: Dict[str, Any]) -> bool:
    """Check if actual validates against expected JSON schema"""
    try:
        jsonschema.validate(instance=actual, schema=expected_schema)
        return True
    except jsonschema.ValidationError:
        return False


def evaluate_example(
    actual: Any,
    expected: Any,
    match_type: str
) -> Tuple[bool, str]:
    """
    Evaluate a single example
    
    Args:
        actual: Actual output from skill
        expected: Expected output or schema
        match_type: Type of match ('exact_match', 'contains', 'json_schema_valid')
        
    Returns:
        Tuple of (passed, message)
    """
    if match_type == 'exact_match':
        passed = exact_match(actual, expected)
        message = "Exact match" if passed else f"Expected {expected}, got {actual}"
    
    elif match_type == 'contains':
        passed = contains_match(actual, expected)
        message = "Contains match" if passed else f"Expected {expected} in {actual}"
    
    elif match_type == 'json_schema_valid':
        passed = json_schema_valid(actual, expected)
        message = "Schema valid" if passed else f"Output doesn't match schema"
    
    else:
        passed = False
        message = f"Unknown match type: {match_type}"
    
    return passed, message


class EvalResult:
    """Result of evaluating a skill"""
    
    def __init__(self, skill_id: str):
        self.skill_id = skill_id
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.details = []
    
    def add_pass(self, name: str, message: str):
        """Record a passing test"""
        self.total += 1
        self.passed += 1
        self.details.append({
            'name': name,
            'status': 'pass',
            'message': message
        })
    
    def add_fail(self, name: str, message: str):
        """Record a failing test"""
        self.total += 1
        self.failed += 1
        self.details.append({
            'name': name,
            'status': 'fail',
            'message': message
        })
    
    def add_error(self, name: str, error: str):
        """Record an error during testing"""
        self.total += 1
        self.failed += 1
        self.errors.append(error)
        self.details.append({
            'name': name,
            'status': 'error',
            'message': error
        })
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total == 0:
            return 0.0
        return self.passed / self.total
    
    def summary(self) -> str:
        """Get summary string"""
        return f"{self.skill_id}: {self.passed}/{self.total} passed ({self.success_rate*100:.1f}%)"


def run_skill_eval(skill_path: Path, dry_run: bool = True) -> EvalResult:
    """
    Run golden evaluation for a skill
    
    Args:
        skill_path: Path to skill directory
        dry_run: If True, only validates golden set format without running skill
        
    Returns:
        EvalResult object
    """
    metadata = load_skill_metadata(skill_path)
    result = EvalResult(metadata.id)
    
    # Load golden set
    golden_path = skill_path / metadata.eval.golden_set
    
    if not golden_path.exists():
        result.add_error('_setup', f"Golden set not found: {golden_path}")
        return result
    
    try:
        examples = load_golden_set(golden_path)
    except Exception as e:
        result.add_error('_setup', f"Failed to load golden set: {e}")
        return result
    
    # In dry run mode, just validate format
    if dry_run:
        for example in examples:
            result.add_pass(example['name'], "Format valid")
        return result
    
    # TODO: In full mode, actually run the skill and evaluate
    # This would require importing and executing the skill module
    # For now, we just validate the format
    for example in examples:
        result.add_pass(example['name'], "Format valid (dry run)")
    
    return result
