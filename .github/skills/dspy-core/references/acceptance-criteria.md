# DSPy Core — Acceptance Criteria

Validates that generated DSPy code follows the current DSPy API (>= 2.6) as documented at https://dspy.ai.

## Language Model Configuration

LM setup must use the modern `dspy.LM` + `dspy.configure` API.

### ✅ Correct
```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)
```

### ❌ Incorrect
```python
import dspy

# DEPRECATED: dspy.OpenAI is removed in modern DSPy
lm = dspy.OpenAI(model="gpt-4", max_tokens=1000)
dspy.settings.configure(lm=lm)
```

## Signature Definition

Signatures should use class-based definitions with type annotations on fields.

### ✅ Correct
```python
import dspy
from typing import Literal

class SentimentAnalysis(dspy.Signature):
    """Classify the sentiment of a given sentence."""
    sentence: str = dspy.InputField(desc="The sentence to analyze")
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(desc="Sentiment label")
    confidence: float = dspy.OutputField(desc="Confidence score from 0.0 to 1.0")
```

### ✅ Correct — Inline string signatures
```python
import dspy

qa = dspy.Predict("question -> answer")
rag = dspy.Predict("context: list[str], question: str -> answer: str")
```

## Module Construction

Modules must inherit from `dspy.Module`, call `super().__init__()`, implement `forward`, and return `dspy.Prediction`.

### ✅ Correct
```python
import dspy

class TextSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeText)

    def forward(self, document: str):
        result = self.summarize(document=document)
        return dspy.Prediction(summary=result.summary)
```

### ❌ Incorrect — returning raw value instead of Prediction
```python
import dspy

class BadModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(MySignature)

    def forward(self, input_data: str):
        return self.process(input=input_data).output
```

## Chain of Thought

`dspy.ChainOfThought` wraps a signature. It does NOT accept `max_tokens` or `temperature` as constructor kwargs.

### ✅ Correct
```python
import dspy

class TaskPlanner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(AnalyzeTask)

    def forward(self, task: str):
        result = self.analyze(task=task)
        return dspy.Prediction(plan=result.plan, reasoning=result.rationale)
```

### ❌ Incorrect — passing max_tokens/temperature to ChainOfThought
```python
import dspy

self.reason = dspy.ChainOfThought(
    MySignature,
    max_tokens=1000,
    temperature=0.7
)
```

## Saving and Loading Programs

Use the built-in `.save()` / `.load()` methods. Prefer JSON. Do NOT use raw `pickle`.

### ✅ Correct
```python
compiled_program.save("./my_program/program.json")

loaded = dspy.ChainOfThought("question -> answer")
loaded.load("./my_program/program.json")

compiled_program.save("./my_program_dir/", save_program=True)
loaded_full = dspy.load("./my_program_dir/", allow_pickle=True)
```

### ❌ Incorrect — raw pickle
```python
import pickle

with open("compiled_program.pkl", "wb") as f:
    pickle.dump(compiled_program, f)
```
