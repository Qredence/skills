# DSPy Optimization — Acceptance Criteria

Validates that DSPy optimization code follows the current DSPy API (>= 2.6) as documented at https://dspy.ai.

## Optimization with Teleprompters

Optimizers live in `dspy.teleprompt`. Use `BootstrapFewShot`, `MIPROv2`, `KNNFewShot`, etc.

### ✅ Correct
```python
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(
    metric=my_metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=16,
    max_rounds=1,
)
compiled = optimizer.compile(program, trainset=trainset)
```

### ✅ Correct — MIPROv2
```python
from dspy.teleprompt import MIPROv2
from copy import deepcopy

optimizer = MIPROv2(metric=my_metric, auto="light")
optimized = optimizer.compile(
    deepcopy(program),
    trainset=trainset,
    max_bootstrapped_demos=3,
    max_labeled_demos=4,
    requires_permission_to_run=False,
)
```

## Training Examples

Use `dspy.Example` with `.with_inputs()` to mark which fields are inputs.

### ✅ Correct
```python
import dspy

trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="Capital of France?", answer="Paris").with_inputs("question"),
]
```

### ❌ Incorrect — missing with_inputs
```python
import dspy

trainset = [
    dspy.Example(input="example 1", output="result 1"),
]
```

## Evaluation

Use `dspy.evaluate.Evaluate` for structured evaluation.

### ✅ Correct
```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=devset,
    metric=accuracy_metric,
    num_threads=4,
    display_progress=True,
    display_table=5,
)
evaluator(my_compiled_program)
```

## Saving and Loading Programs

Use `.save()` / `.load()`. Prefer JSON. Do NOT use raw `pickle`.

### ✅ Correct
```python
compiled_program.save("./my_program/program.json")

loaded = dspy.ChainOfThought("question -> answer")
loaded.load("./my_program/program.json")
```

### ❌ Incorrect — raw pickle
```python
import pickle

with open("compiled_program.pkl", "wb") as f:
    pickle.dump(compiled_program, f)
```

## Language Model Configuration

Must use `dspy.LM` + `dspy.configure`.

### ✅ Correct
```python
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)
```

### ❌ Incorrect
```python
lm = dspy.OpenAI(model="gpt-4")
dspy.settings.configure(lm=lm)
```
