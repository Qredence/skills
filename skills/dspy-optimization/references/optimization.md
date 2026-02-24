# DSPy Optimization

DSPy optimization improves program performance by finding the best prompts and demonstrations for your modules. This guide covers teleprompters, metrics, and optimization strategies.

## Table of Contents

- [Understanding Optimization](#understanding-optimization)
- [Teleprompters](#teleprompters)
- [Metrics](#metrics)
- [Optimization Strategies](#optimization-strategies)
- [Evaluation](#evaluation)
- [Best Practices](#best-practices)

## Understanding Optimization

### What is Optimization?

DSPy optimization is the process of automatically finding the best prompts and examples (demonstrations) to improve your program's performance. It's similar to training a machine learning model, but for prompt engineering.

### Why Optimize?

- **Better performance**: Higher quality outputs
- **Consistency**: More reliable results
- **Efficiency**: Fewer tokens, faster execution
- **Robustness**: Better handling of edge cases

### The Optimization Process

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Program   │───►│Teleprompter │───►│  Optimized  │
│  (Module)   │    │  (Strategy) │    │   Program   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Training   │    │   Metrics   │    │  Compiled   │
│  Examples   │    │  (Scoring)  │    │  Artifacts  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Teleprompters

### BootstrapFewShot

The most common teleprompter. Uses few-shot learning with demonstrations.

```python
teleprompter = dspy.BootstrapFewShot(
    max_labeled_demos=5,      # Number of demonstrations
    max_bootstrapped_demos=10 # Maximum demonstrations to generate
)

compiled = teleprompter.compile(
    program,
    trainset=trainset
)
```

**When to use**:
- You have labeled training examples
- You want automatic demonstration generation
- Good balance of performance and cost

**Parameters**:
- `max_labeled_demos`: Number of examples from your training set
- `max_bootstrapped_demos`: Total demonstrations (labeled + generated)
- `max_rounds`: Number of optimization rounds
- `metric`: Evaluation metric function

### KNNFewShot

Uses k-nearest neighbors to select relevant examples.

```python
teleprompter = dspy.KNNFewShot(
    k=4,                    # Number of neighbors
    trainset=trainset
)

compiled = teleprompter.compile(program)
```

**When to use**:
- Large training sets
- Need efficient example selection
- Want context-aware demonstrations

**Parameters**:
- `k`: Number of neighbors to select
- `trainset`: Training examples
- `metric`: Distance metric (optional)

### ChainOfThought

Enables reasoning in the optimization process.

```python
teleprompter = dspy.BootstrapFewShot(
    max_labeled_demos=3
)

program_with_cot = dspy.ChainOfThought(MySignature)
compiled = teleprompter.compile(program_with_cot, trainset=trainset)
```

**When to use**:
- Tasks requiring reasoning
- Complex problem-solving
- Need step-by-step explanations

### LabeledFewShot

Uses only provided demonstrations without generation.

```python
teleprompter = dspy.LabeledFewShot(
    k=5,                    # Number of demonstrations
    trainset=trainset
)

compiled = teleprompter.compile(program)
```

**When to use**:
- You have high-quality demonstrations
- Don't want automatic generation
- Need full control over examples

### Signature Comparison

| Teleprompter | Use Case | Training Data | Cost | Performance |
|--------------|----------|---------------|------|-------------|
| BootstrapFewShot | General purpose | Required | Medium | High |
| KNNFewShot | Large datasets | Required | Low | Medium-High |
| LabeledFewShot | Controlled prompts | Required | Low | Medium |
| ChainOfThought | Reasoning tasks | Optional | High | High (complex tasks) |

## Metrics

### Defining a Metric

A metric function evaluates how well your program performs:

```python
def accuracy_metric(example, pred, trace=None):
    """
    Simple accuracy metric.

    Args:
        example: The ground truth example
        pred: The program's prediction
        trace: Optional execution trace for debugging

    Returns:
        bool: True if prediction matches example
    """
    return example.output == pred.output
```

### Using Metrics in Optimization

```python
# Define metric
def quality_metric(example, pred, trace=None):
    return example.quality_score >= pred.quality_score

# Use in teleprompter
teleprompter = dspy.BootstrapFewShot(
    metric=quality_metric,
    max_labeled_demos=5
)

compiled = teleprompter.compile(program, trainset=trainset)
```

### Common Metric Patterns

#### Exact Match

```python
def exact_match(example, pred, trace=None):
    return example.output == pred.output
```

#### Semantic Similarity

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(example, pred, trace=None):
    emb1 = model.encode(example.output)
    emb2 = model.encode(pred.output)
    similarity = (emb1 @ emb2.T).item()
    return similarity > 0.8  # Threshold
```

#### Structured Evaluation

```python
def structured_metric(example, pred, trace=None):
    score = 0

    # Check required fields
    if hasattr(pred, 'summary') and pred.summary:
        score += 0.3

    if hasattr(pred, 'keywords') and pred.keywords:
        score += 0.3

    # Check quality
    if hasattr(pred, 'confidence') and pred.confidence > 0.7:
        score += 0.4

    return score >= 0.7  # Threshold
```

#### Multi-Criteria Metric

```python
def multi_criteria_metric(example, pred, trace=None):
    criteria = {
        'accuracy': example.output == pred.output,
        'completeness': len(pred.output) >= len(example.output) * 0.8,
        'relevance': any(keyword in pred.output for keyword in example.keywords)
    }

    # Weighted average
    weights = {'accuracy': 0.5, 'completeness': 0.3, 'relevance': 0.2}
    score = sum(criteria[k] * weights[k] for k in criteria)

    return score >= 0.6
```

### Debugging with Traces

```python
def debug_metric(example, pred, trace=None):
    """Metric with debugging information."""
    if trace:
        print(f"Trace: {trace}")

    result = example.output == pred.output

    if not result:
        print(f"Expected: {example.output}")
        print(f"Got: {pred.output}")

    return result
```

## Optimization Strategies

### Strategy 1: Start Simple

Begin with basic optimization, then iterate:

```python
# Step 1: Simple few-shot
teleprompter = dspy.LabeledFewShot(k=3)
compiled = teleprompter.compile(program, trainset=trainset)

# Evaluate
score = evaluate(compiled, devset)

# Step 2: Add bootstrap if needed
if score < 0.7:
    teleprompter = dspy.BootstrapFewShot(max_labeled_demos=3)
    compiled = teleprompter.compile(program, trainset=trainset)
```

### Strategy 2: Progressive Enhancement

Increase complexity gradually:

```python
# Level 1: No optimization
baseline = program()
score1 = evaluate(baseline, devset)

# Level 2: Labeled few-shot
teleprompter = dspy.LabeledFewShot(k=3)
compiled1 = teleprompter.compile(program, trainset=trainset)
score2 = evaluate(compiled1, devset)

# Level 3: Bootstrap
teleprompter = dspy.BootstrapFewShot(max_labeled_demos=5)
compiled2 = teleprompter.compile(program, trainset=trainset)
score3 = evaluate(compiled2, devset)

# Choose best
best = max([(baseline, score1), (compiled1, score2), (compiled2, score3)],
           key=lambda x: x[1])
```

### Strategy 3: Multi-Stage Optimization

Optimize different parts separately:

```python
# Stage 1: Optimize sub-module 1
teleprompter1 = dspy.BootstrapFewShot(max_labeled_demos=3)
program.submodule1 = teleprompter1.compile(program.submodule1, trainset=trainset1)

# Stage 2: Optimize sub-module 2
teleprompter2 = dspy.KNNFewShot(k=4, trainset=trainset2)
program.submodule2 = teleprompter2.compile(program.submodule2)

# Stage 3: Optimize entire program
teleprompter3 = dspy.BootstrapFewShot(max_labeled_demos=5)
compiled = teleprompter3.compile(program, trainset=trainset3)
```

### Strategy 4: Hyperparameter Tuning

Search for optimal parameters:

```python
import itertools

# Parameter grid
params = {
    'max_labeled_demos': [3, 5, 7],
    'max_bootstrapped_demos': [5, 10, 15],
    'max_rounds': [1, 2, 3]
}

best_score = 0
best_config = None
best_program = None

for config in itertools.product(*params.values()):
    config_dict = dict(zip(params.keys(), config))

    teleprompter = dspy.BootstrapFewShot(**config_dict)
    compiled = teleprompter.compile(program, trainset=trainset)

    score = evaluate(compiled, devset)

    if score > best_score:
        best_score = score
        best_config = config_dict
        best_program = compiled

print(f"Best config: {best_config}")
print(f"Best score: {best_score}")
```

## Evaluation

### Evaluation Function

```python
def evaluate(program, devset, metric=None):
    """
    Evaluate a program on a development set.

    Args:
        program: Compiled program to evaluate
        devset: Development examples
        metric: Metric function (uses default if None)

    Returns:
        float: Average score across examples
    """
    if metric is None:
        metric = lambda example, pred, trace=None: example.output == pred.output

    scores = []
    for example in devset:
        pred = program(**example.inputs())
        score = metric(example, pred)
        scores.append(score)

    return sum(scores) / len(scores)
```

### Cross-Validation

```python
from sklearn.model_selection import KFold

def cross_validate(program, trainset, k=5):
    """Perform k-fold cross-validation."""
    kf = KFold(n_splits=k)
    scores = []

    for train_idx, val_idx in kf.split(trainset):
        train_fold = [trainset[i] for i in train_idx]
        val_fold = [trainset[i] for i in val_idx]

        # Compile
        teleprompter = dspy.BootstrapFewShot(max_labeled_demos=3)
        compiled = teleprompter.compile(program, trainset=train_fold)

        # Evaluate
        score = evaluate(compiled, val_fold)
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    print(f"Cross-validation scores: {scores}")
    print(f"Average: {avg_score}")

    return avg_score
```

### Error Analysis

```python
def analyze_errors(program, devset):
    """Analyze prediction errors."""
    errors = []

    for example in devset:
        pred = program(**example.inputs())

        if example.output != pred.output:
            errors.append({
                'input': example.inputs(),
                'expected': example.output,
                'predicted': pred.output,
                'type': 'mismatch'
            })

    # Group by error type
    from collections import Counter
    error_types = Counter(e['type'] for e in errors)

    print(f"Total errors: {len(errors)}")
    print(f"Error types: {error_types}")

    # Show examples
    print("\nSample errors:")
    for error in errors[:5]:
        print(f"  Input: {error['input']}")
        print(f"  Expected: {error['expected']}")
        print(f"  Predicted: {error['predicted']}")
        print()

    return errors
```

## Best Practices

### 1. Use Separate Train/Dev/Test Sets

```python
# Split data
trainset = data[:800]
devset = data[800:900]
testset = data[900:]

# Optimize on trainset
teleprompter = dspy.BootstrapFewShot(max_labeled_demos=5)
compiled = teleprompter.compile(program, trainset=trainset)

# Tune on devset
# ... hyperparameter tuning ...

# Final evaluation on testset
final_score = evaluate(compiled, testset)
```

### 2. Start with High-Quality Examples

```python
# Curate diverse, representative examples
trainset = [
    dspy.Example(input="...", output="...").with_inputs("input"),  # Easy case
    dspy.Example(input="...", output="...").with_inputs("input"),  # Medium case
    dspy.Example(input="...", output="...").with_inputs("input"),  # Hard case
    dspy.Example(input="...", output="...").with_inputs("input"),  # Edge case
]
```

### 3. Monitor Token Usage

```python
import dspy

# Configure LM
lm = dspy.LM("openai/gpt-4o", max_tokens=1000)
dspy.configure(lm=lm)

# After running your program, inspect history
for entry in program.history:
    print(entry)
```

### 4. Save and Reuse Compiled Programs

```python
# Save (prefer JSON for safety and readability)
compiled.save("./optimized_program/program.json")

# Load: recreate the same program, then load state
loaded_program = MyProgram()
loaded_program.load("./optimized_program/program.json")
```

### 5. Document Optimization Process

```python
"""
Optimization Log for MyProgram

Date: 2024-01-15
Teleprompter: BootstrapFewShot
Parameters:
  - max_labeled_demos: 5
  - max_bootstrapped_demos: 10
  - max_rounds: 2

Training Set: 100 examples
Dev Set: 20 examples

Results:
  - Baseline: 0.65
  - Optimized: 0.82
  - Improvement: +0.17

Notes:
  - Best performance with 5 demonstrations
  - More rounds didn't improve results
  - Consider adding more edge cases to training set
"""
```

## fleet-rlm Examples

### Optimizing Task Routing

```python
# Define metric
def routing_accuracy(example, pred, trace=None):
    return example.agent_id == pred.agent_id

# Load training data
trainset = load_routing_examples("data/routing_train.jsonl")

# Optimize
teleprompter = dspy.BootstrapFewShot(
    metric=routing_accuracy,
    max_labeled_demos=5
)

compiled_router = teleprompter.compile(
    program.router,
    trainset=trainset
)

# Save
save_compiled(compiled_router, ".var/cache/dspy/optimized_router.pkl")
```

### Optimizing Quality Assessment

```python
def quality_correlation(example, pred, trace=None):
    """Correlation with human quality scores."""
    from scipy.stats import spearmanr
    correlation, _ = spearmanr(
        [example.quality_score],
        [pred.quality_score]
    )
    return correlation > 0.8

teleprompter = dspy.BootstrapFewShot(
    metric=quality_correlation,
    max_labeled_demos=7
)

compiled_assessor = teleprompter.compile(
    program.assessor,
    trainset=quality_examples
)
```

## Common Issues and Solutions

### Issue: Overfitting

**Problem**: Great performance on training data, poor on test data

**Solution**:
1. Use fewer demonstrations (`max_labeled_demos`)
2. Add regularization (fewer rounds)
3. Use cross-validation
4. Increase training data diversity

### Issue: Underfitting

**Problem**: Poor performance on all data

**Solution**:
1. Increase demonstrations
2. Use Chain of Thought
3. Improve training data quality
4. Try different teleprompters

### Issue: Slow Optimization

**Problem**: Optimization takes too long

**Solution**:
1. Use smaller training set for tuning
2. Reduce `max_labeled_demos`
3. Use KNNFewShot instead of BootstrapFewShot
4. Cache intermediate results

### Issue: Unstable Results

**Problem**: Different results on each run

**Solution**:
1. Set random seed
2. Use more training examples
3. Increase `max_bootstrapped_demos`
4. Use deterministic teleprompters (LabeledFewShot)
