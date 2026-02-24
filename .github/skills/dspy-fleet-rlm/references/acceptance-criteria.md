# DSPy fleet-rlm — Acceptance Criteria

Validates that fleet-rlm DSPy integration code uses correct module paths and conventions from the `qredence/fleet-rlm-dspy` codebase.

## Import Conventions

Must use `fleet_rlm` package paths. Never use deprecated `agentic_fleet` or `dspy_modules`.

### ✅ Correct
```python
from fleet_rlm.signatures import AnalyzeLongDocument, CodeChangePlan
from fleet_rlm.core.interpreter import Interpreter
from fleet_rlm.core.config import get_dspy_config
```

### ❌ Incorrect — deprecated module paths
```python
from agentic_fleet.dspy_modules.signatures import TaskAnalysis
from agentic_fleet.dspy_modules.reasoner import DSPyReasoner
```

## Signature Placement

New signatures go in `src/fleet_rlm/signatures_prod.py` (production) or `src/fleet_rlm/signatures_demo.py` (demo), then re-export from `signatures.py`.

### ✅ Correct
```python
# In src/fleet_rlm/signatures_prod.py
import dspy

class MyNewSignature(dspy.Signature):
    """Docstring with Input Fields / Output Fields sections."""
    input_field: str = dspy.InputField(desc="...")
    output_field: str = dspy.OutputField(desc="...")

# In src/fleet_rlm/signatures.py — add re-export:
# from .signatures_prod import MyNewSignature
```

## Language Model Configuration

Must use `dspy.LM` + `dspy.configure`.

### ✅ Correct
```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)
```

### ❌ Incorrect
```python
lm = dspy.OpenAI(model="gpt-4")
dspy.settings.configure(lm=lm)
```

## Environment Setup

Must use `uv` for package management. Never use raw `pip`.

### ✅ Correct
```bash
uv venv && source .venv/bin/activate
uv pip install dspy
uv run scripts/compile-dspy.py
```

### ❌ Incorrect
```bash
pip install dspy
python scripts/compile-dspy.py
```
