# DSPy Patterns and Debugging

This guide covers fleet-rlm-specific DSPy patterns, debugging techniques, and common issues with solutions.

## Table of Contents

- [fleet-rlm DSPy Architecture](#agenticfleet-dspy-architecture)
- [Common Patterns](#common-patterns)
- [Debugging Techniques](#debugging-techniques)
- [Performance Optimization](#performance-optimization)
- [Testing Strategies](#testing-strategies)
- [Common Issues and Solutions](#common-issues-and-solutions)

## fleet-rlm DSPy Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    fleet-rlm                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────────────────┐   │
│  │   Workflow   │─────►│   DSPy Reasoner          │   │
│  │  Orchestrator│      │  (dspy_modules/reasoner) │   │
│  └──────────────┘      └──────────────────────────┘   │
│                                │                        │
│                                ▼                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │          DSPy Modules (reasoner_modules.py)       │  │
│  │  - TaskAnalysisModule                            │  │
│  │  - TaskRoutingModule                              │  │
│  │  - QualityAssessmentModule                        │  │
│  └──────────────────────────────────────────────────┘  │
│                                │                        │
│                                ▼                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │          DSPy Signatures (signatures.py)          │  │
│  │  - TaskAnalysis                                   │  │
│  │  - TaskRouting                                    │  │
│  │  - QualityAssessment                              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Components

1. **DSPyReasoner**: Main orchestrator in `dspy_modules/reasoner.py`
2. **Modules**: Specific DSPy modules in `dspy_modules/reasoner_modules.py`
3. **Signatures**: Input/output contracts in `dspy_modules/signatures.py`
4. **Cache**: Compiled artifacts in `.var/cache/dspy/`

### Data Flow

```
User Task
    │
    ▼
SupervisorWorkflow
    │
    ▼
DSPyReasoner.analyze_task()
    │
    ├─► TaskAnalysisModule
    │       │
    │       └─► TaskAnalysis signature
    │
    ├─► TaskRoutingModule
    │       │
    │       └─► TaskRouting signature
    │
    └─► Returns: task_type, agent_id, confidence
```

## Common Patterns

### Pattern 1: Analysis → Routing → Execution

The core fleet-rlm pattern:

```python
class AnalysisRoutingPattern(dspy.Module):
    """Analyze task, route to agent, execute."""

    def __init__(self):
        super().__init__()
        self.analyze = dspy.Predict(TaskAnalysis)
        self.route = dspy.Predict(TaskRouting)
        self.execute = dspy.Predict(ExecuteTask)

    def forward(self, task: str, context: str = ""):
        # Step 1: Analyze
        analysis = self.analyze(
            task_description=task,
            context=context
        )

        # Step 2: Route
        routing = self.route(
            task=task,
            task_type=analysis.task_type
        )

        # Step 3: Execute (via agent)
        execution = self.execute(
            task=task,
            agent_id=routing.agent_id
        )

        return dspy.Prediction(
            agent_id=routing.agent_id,
            confidence=routing.confidence,
            result=execution.result
        )
```

### Pattern 2: Quality Gate

Check quality before proceeding:

```python
class QualityGatePattern(dspy.Module):
    """Execute with quality checks."""

    def __init__(self):
        super().__init__()
        self.execute = dspy.Predict(ExecuteTask)
        self.assess = dspy.Predict(QualityAssessment)

    def forward(self, task: str, agent_id: str):
        # Execute
        result = self.execute(task=task, agent_id=agent_id)

        # Assess quality
        quality = self.assess(
            task=task,
            result=result.result
        )

        # Gate based on quality
        if quality.score < 0.7:
            # Retry or escalate
            return dspy.Prediction(
                result=None,
                quality_score=quality.score,
                needs_retry=True
            )

        return dspy.Prediction(
            result=result.result,
            quality_score=quality.score,
            needs_retry=False
        )
```

### Pattern 3: Multi-Agent Coordination

Coordinate multiple agents:

```python
class MultiAgentPattern(dspy.Module):
    """Coordinate multiple agents for complex tasks."""

    def __init__(self):
        super().__init__()
        self.decompose = dspy.Predict(DecomposeTask)
        self.route = dspy.Predict(TaskRouting)
        self.synthesize = dspy.Predict(SynthesizeResults)

    def forward(self, task: str):
        # Decompose task
        subtasks = self.decompose(task=task)

        # Route each subtask
        results = []
        for subtask in subtasks.subtasks:
            routing = self.route(task=subtask)
            # Execute via agent (simplified)
            results.append({
                'subtask': subtask,
                'agent': routing.agent_id,
                'result': execute_agent(subtask, routing.agent_id)
            })

        # Synthesize results
        final = self.synthesize(
            original_task=task,
            subtask_results=results
        )

        return dspy.Prediction(result=final.synthesis)
```

### Pattern 4: Progressive Refinement

Iteratively improve results:

```python
class ProgressiveRefinementPattern(dspy.Module):
    """Iteratively refine results until quality threshold."""

    def __init__(self, max_iterations=3):
        super().__init__()
        self.max_iterations = max_iterations
        self.execute = dspy.Predict(ExecuteTask)
        self.assess = dspy.Predict(QualityAssessment)
        self.refine = dspy.Predict(RefineResult)

    def forward(self, task: str, agent_id: str):
        # Initial execution
        current = self.execute(task=task, agent_id=agent_id)
        quality = self.assess(task=task, result=current.result)

        # Iterate until quality threshold
        for i in range(self.max_iterations):
            if quality.score >= 0.9:
                break

            # Refine
            refined = self.refine(
                task=task,
                current_result=current.result,
                feedback=quality.feedback
            )

            # Reassess
            current = refined
            quality = self.assess(task=task, result=current.result)

        return dspy.Prediction(
            result=current.result,
            quality_score=quality.score,
            iterations=i + 1
        )
```

## Debugging Techniques

### Technique 1: Enable Tracing

Track execution flow:

```python
import dspy

# Enable tracing
lm = dspy.LM("openai/gpt-4")
dspy.configure(lm=lm)

# Run program
result = program(input_data="test")

# Inspect the module's history
for entry in program.history:
    print(f"Entry: {entry}")
    print()
```

### Technique 2: Logging

Add logging to understand behavior:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

class LoggedModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(MySignature)

    def forward(self, input_data: str):
        logging.debug(f"Input: {input_data}")

        result = self.process(input=input_data)

        logging.debug(f"Output: {result.output}")
        logging.debug(f"Confidence: {getattr(result, 'confidence', 'N/A')}")

        return dspy.Prediction(output=result.output)
```

### Technique 3: Intermediate Outputs

Save intermediate results:

```python
class DebugModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.step1 = dspy.Predict(Step1Signature)
        self.step2 = dspy.Predict(Step2Signature)
        self.step3 = dspy.Predict(Step3Signature)

    def forward(self, input_data: str):
        # Step 1
        result1 = self.step1(input=input_data)
        print(f"Step 1 output: {result1.output}")

        # Step 2
        result2 = self.step2(intermediate=result1.output)
        print(f"Step 2 output: {result2.output}")

        # Step 3
        result3 = self.step3(intermediate=result2.output)
        print(f"Step 3 output: {result3.output}")

        return dspy.Prediction(
            final_output=result3.output,
            intermediate={
                'step1': result1.output,
                'step2': result2.output
            }
        )
```

### Technique 4: Signature Validation

Validate signatures before use:

```python
# Use the test-signature script
uv run scripts/test-signature.py --signature TaskAnalysis --strict

# Or validate programmatically
def validate_signature(signature_class):
    """Validate a DSPy signature."""
    import dspy

    if not issubclass(signature_class, dspy.Signature):
        print(f"❌ {signature_class.__name__} is not a dspy.Signature")
        return False

    # Check fields
    fields = signature_class.__annotations__
    if not fields:
        print(f"❌ No fields defined")
        return False

    print(f"✓ {signature_class.__name__} is valid")
    return True
```

### Technique 5: Performance Profiling

Measure execution time:

```python
import time

class ProfiledModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(MySignature)

    def forward(self, input_data: str):
        start = time.time()

        result = self.process(input=input_data)

        elapsed = time.time() - start
        print(f"Execution time: {elapsed:.2f}s")

        return dspy.Prediction(output=result.output, time=elapsed)
```

## Performance Optimization

### Optimization 1: Reduce Demonstration Count

Fewer demonstrations = faster execution:

```python
# Before: Too many demos
teleprompter = dspy.BootstrapFewShot(max_labeled_demos=10)

# After: Optimal number
teleprompter = dspy.BootstrapFewShot(max_labeled_demos=5)
```

### Optimization 2: Use Caching

Cache compiled programs:

```python
import os

# Check cache first
if os.path.exists("compiled_program.json"):
    program = MyModule()
    program.load("compiled_program.json")
else:
    # Compile and cache
    teleprompter = dspy.BootstrapFewShot(max_labeled_demos=16)
    program = teleprompter.compile(module, trainset=trainset)
    program.save("compiled_program.json")
```

### Optimization 3: Batch Processing

Process multiple inputs efficiently:

```python
class BatchProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(MySignature)

    def forward_batch(self, inputs: List[str]):
        """Process multiple inputs."""
        results = []
        for input_data in inputs:
            result = self.process(input=input_data)
            results.append(result.output)
        return results
```

### Optimization 4: Model Selection

Use appropriate models for different tasks:

```python
# Fast model for simple tasks
fast_lm = dspy.LM("openai/gpt-4o-mini", max_tokens=500)

# High-quality model for complex tasks
quality_lm = dspy.LM("openai/gpt-4o", max_tokens=1000)

class SmartModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.fast_process = dspy.Predict(SimpleSignature, lm=fast_lm)
        self.quality_process = dspy.Predict(ComplexSignature, lm=quality_lm)

    def forward(self, input_data: str, use_quality: bool = False):
        if use_quality:
            return self.quality_process(input=input_data)
        else:
            return self.fast_process(input=input_data)
```

## Testing Strategies

### Strategy 1: Unit Testing

Test individual modules:

```python
import pytest

def test_task_analysis_module():
    """Test TaskAnalysisModule."""
    module = TaskAnalysisModule()

    result = module.forward(
        task_description="Write a Python function",
        context="Code generation task"
    )

    assert hasattr(result, 'task_type')
    assert result.task_type in ['coding', 'research', 'analysis']
    assert result.complexity in ['simple', 'medium', 'complex']
```

### Strategy 2: Integration Testing

Test module composition:

```python
def test_analysis_routing_integration():
    """Test analysis → routing pipeline."""
    module = AnalysisRoutingPattern()

    result = module.forward(
        task="Research quantum computing",
        context="Academic research"
    )

    assert result.agent_id is not None
    assert result.confidence > 0.5
    assert result.result is not None
```

### Strategy 3: Property-Based Testing

Test with generated inputs:

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=10, max_size=100))
def test_module_with_various_inputs(task):
    """Test module with various inputs."""
    module = TaskAnalysisModule()

    result = module.forward(task_description=task)

    assert hasattr(result, 'task_type')
    assert hasattr(result, 'complexity')
```

### Strategy 4: Regression Testing

Ensure optimizations don't break existing behavior:

```python
def test_regression():
    """Test that optimizations don't break behavior."""
    # Load baseline
    baseline = MyModule()
    baseline.load("baseline_program.json")

    # Load optimized
    optimized = MyModule()
    optimized.load("optimized_program.json")

    # Test on same inputs
    test_input = "Test task"

    baseline_result = baseline(input=test_input)
    optimized_result = optimized(input=test_input)

    # Should produce similar results
    assert baseline_result.output == optimized_result.output
```

## Common Issues and Solutions

### Issue: "Module not found" errors

**Problem**:
```
ModuleNotFoundError: No module named 'fleet_rlm'
```

**Solution**:
1. Ensure you're in the project root
2. Install dependencies: `uv sync`
3. Use absolute imports: `from fleet_rlm import ...`

### Issue: Compilation fails with "cache not found"

**Problem**:
```
ValueError: Compiled artifacts not found
```

**Solution**:
1. Clear cache: `uv run scripts/clear-cache.py`
2. Recompile: `uv run scripts/compile-dspy.py --module reasoner`
3. Set `require_compiled: false` in config (for development only)

### Issue: Poor routing decisions

**Problem**: Tasks routed to wrong agents

**Solution**:
1. Improve training data for routing
2. Add more diverse examples
3. Use Chain of Thought for routing
4. Adjust confidence threshold

```python
# Use Chain of Thought for better routing
self.route = dspy.ChainOfThought(TaskRouting)
```

### Issue: Quality assessment inconsistent

**Problem**: Quality scores vary widely

**Solution**:
1. Define clear quality criteria
2. Use specific metrics
3. Add examples of good/bad outputs
4. Calibrate with human ratings

```python
def quality_metric(example, pred, trace=None):
    """More specific quality metric."""
    score = 0

    # Check completeness
    if len(pred.output) >= len(example.output) * 0.8:
        score += 0.3

    # Check accuracy
    if pred.accuracy > 0.8:
        score += 0.4

    # Check format
    if pred.format_valid:
        score += 0.3

    return score >= 0.7
```

### Issue: Slow execution

**Problem**: Programs take too long to execute

**Solution**:
1. Reduce demonstration count
2. Use faster models for simple tasks
3. Cache compiled programs
4. Parallelize independent operations

```python
# Parallel processing
from concurrent.futures import ThreadPoolExecutor

class ParallelModule(dspy.Module):
    def forward_parallel(self, inputs: List[str]):
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.process, inputs))
        return results
```

### Issue: Memory leaks

**Problem**: Memory usage grows over time

**Solution**:
1. Clear module history: `program.history.clear()`
2. Limit cache size
3. Use generators for large datasets
4. Profile memory usage

```python
import tracemalloc

tracemalloc.start()

# Run program
result = program(input_data="test")

# Check memory
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

### Issue: Compiled program incompatible

**Problem**: Old compiled program doesn't work with new code

**Solution**:
1. Always recompile after code changes
2. Use versioning for compiled artifacts
3. Clear cache before recompiling

```bash
# Full recompilation workflow
uv run scripts/clear-cache.py
uv run scripts/compile-dspy.py --module reasoner
uv run scripts/test-signature.py --signature TaskAnalysis
```

## Best Practices Summary

1. **Always clear cache after DSPy changes**
2. **Use absolute imports in fleet-rlm**
3. **Set `require_compiled: true` in production**
4. **Validate signatures with test-signature.py**
5. **Monitor token usage during optimization**
6. **Save and version compiled programs**
7. **Use separate train/dev/test sets**
8. **Document optimization parameters**
9. **Test modules individually before composing**
10. **Enable tracing for debugging**
