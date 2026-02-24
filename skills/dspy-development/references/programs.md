# DSPy Programs and Modules

DSPy programs are composed of modules that process inputs according to defined signatures. This guide covers program construction, module composition, and compilation workflows.

## Table of Contents

- [Basic Program Structure](#basic-program-structure)
- [Creating Modules](#creating-modules)
- [Module Composition](#module-composition)
- [Chain of Thought](#chain-of-thought)
- [Compilation Workflows](#compilation-workflows)
- [Program Patterns](#program-patterns)
- [Best Practices](#best-practices)

## Basic Program Structure

A DSPy program is a class that inherits from `dspy.Module` and defines a `forward` method:

```python
import dspy

class SimpleProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = MySignature

    def forward(self, **kwargs):
        return self.signature(**kwargs)
```

### Key Components

1. **Class inheritance**: Must inherit from `dspy.Module`
2. **`__init__`**: Initialize sub-modules and signatures
3. **`forward`**: Define the computation flow
4. **Sub-modules**: Compose multiple modules together

## Creating Modules

### Simple Module with a Signature

```python
class TextSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeText)

    def forward(self, document: str):
        return self.summarize(document=document)
```

### Module with Multiple Signatures

```python
class DocumentProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeText)
        self.extract_keywords = dspy.Predict(ExtractKeywords)

    def forward(self, document: str):
        summary = self.summarize(document=document)
        keywords = self.extract_keywords(document=document)
        return dspy.Prediction(
            summary=summary.summary,
            keywords=keywords.keywords
        )
```

### Module with Pre/Post Processing

```python
class SmartSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeText)

    def forward(self, document: str, max_length: int = 300):
        # Pre-processing: Truncate if too long
        if len(document) > max_length * 2:
            document = document[:max_length * 2]

        # Core processing
        result = self.summarize(document=document, max_length=max_length)

        # Post-processing: Ensure max length
        summary = result.summary[:max_length]

        return dspy.Prediction(summary=summary)
```

## Module Composition

### Sequential Composition

Modules execute in sequence:

```python
class PipelineProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.step1 = dspy.Predict(Step1Signature)
        self.step2 = dspy.Predict(Step2Signature)
        self.step3 = dspy.Predict(Step3Signature)

    def forward(self, input_data: str):
        result1 = self.step1(input=input_data)
        result2 = self.step2(intermediate=result1.output)
        result3 = self.step3(intermediate=result2.output)
        return dspy.Prediction(final_output=result3.output)
```

### Conditional Composition

Branch based on intermediate results:

```python
class ConditionalRouter(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classify = dspy.Predict(ClassifyInput)
        self.process_a = dspy.Predict(ProcessTypeA)
        self.process_b = dspy.Predict(ProcessTypeB)

    def forward(self, input_data: str):
        classification = self.classify(input=input_data)

        if classification.type == "A":
            result = self.process_a(input=input_data)
        else:
            result = self.process_b(input=input_data)

        return dspy.Prediction(output=result.output)
```

### Parallel Composition

Execute multiple modules in parallel:

```python
class MultiAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.sentiment = dspy.Predict(AnalyzeSentiment)
        self.keywords = dspy.Predict(ExtractKeywords)
        self.entities = dspy.Predict(ExtractEntities)

    def forward(self, text: str):
        sentiment = self.sentiment(text=text)
        keywords = self.keywords(text=text)
        entities = self.entities(text=text)

        return dspy.Prediction(
            sentiment=sentiment.sentiment,
            keywords=keywords.keywords,
            entities=entities.entities
        )
```

### Hierarchical Composition

Compose modules from other modules:

```python
class SubModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(SubSignature)

    def forward(self, data: str):
        return self.process(data=data)

class MainModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.sub1 = SubModule()
        self.sub2 = SubModule()
        self.combine = dspy.Predict(CombineResults)

    def forward(self, input_data: str):
        result1 = self.sub1(data=input_data)
        result2 = self.sub2(data=input_data)
        combined = self.combine(result1=result1.output, result2=result2.output)
        return dspy.Prediction(output=combined.output)
```

## Chain of Thought

### Basic Chain of Thought

Enable reasoning by using `dspy.ChainOfThought`:

```python
class ReasoningSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.ChainOfThought(SummarizeText)

    def forward(self, document: str):
        result = self.summarize(document=document)
        return dspy.Prediction(
            summary=result.summary,
            reasoning=result.rationale  # Access the chain of thought
        )
```

### Multi-Step Reasoning

```python
class MultiStepReasoner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(AnalyzeTask)
        self.plan = dspy.ChainOfThought(CreatePlan)
        self.execute = dspy.ChainOfThought(ExecutePlan)

    def forward(self, task: str):
        analysis = self.analyze(task=task)
        plan = self.plan(task=task, analysis=analysis.output)
        execution = self.execute(task=task, plan=plan.output)

        return dspy.Prediction(
            analysis=analysis.rationale,
            plan=plan.rationale,
            execution=execution.rationale,
            result=execution.output
        )
```

### Configuring Chain of Thought

To control generation parameters, configure them on the LM rather than on ChainOfThought:

```python
import dspy

# Set temperature and max_tokens on the LM
lm = dspy.LM("openai/gpt-4o", temperature=0.7, max_tokens=1000)
dspy.configure(lm=lm)

class CustomReasoner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.reason = dspy.ChainOfThought(MySignature)

    def forward(self, input_data: str):
        return self.reason(input=input_data)
```

## Compilation Workflows

### Basic Compilation

```python
# Define program
program = MyProgram()

# Define teleprompter
teleprompter = dspy.BootstrapFewShot()

# Compile
compiled_program = teleprompter.compile(program)

# Use compiled program
result = compiled_program(input_data="test")
```

### Compilation with Training Examples

```python
# Load training examples
trainset = [
    dspy.Example(input="example 1", output="result 1").with_inputs("input"),
    dspy.Example(input="example 2", output="result 2").with_inputs("input"),
]

# Compile with examples
teleprompter = dspy.BootstrapFewShot(max_labeled_demos=5)
compiled_program = teleprompter.compile(program, trainset=trainset)
```

### Compilation with Metrics

```python
def my_metric(example, pred, trace=None):
    """Custom metric for evaluation."""
    return example.output == pred.output

# Compile with metric
teleprompter = dspy.BootstrapFewShot(metric=my_metric)
compiled_program = teleprompter.compile(program, trainset=trainset)
```

### Saving and Loading Compiled Programs

```python
# Save state to JSON (recommended)
compiled_program.save("./compiled/program.json")

# Load: recreate the same program, then load state
loaded_program = MyProgram()
loaded_program.load("./compiled/program.json")

# Full program save (includes architecture)
compiled_program.save("./compiled_dir/", save_program=True)

# Full program load
loaded_full = dspy.load("./compiled_dir/", allow_pickle=True)
```

## Program Patterns

### 1. Map-Reduce Pattern

Process multiple items in parallel, then aggregate:

```python
class MapReduceProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.map = dspy.Predict(MapSignature)
        self.reduce = dspy.Predict(ReduceSignature)

    def forward(self, items: List[str]):
        # Map: Process each item
        mapped_results = [self.map(item=item) for item in items]

        # Reduce: Aggregate results
        aggregated = self.reduce(results=[r.output for r in mapped_results])

        return dspy.Prediction(output=aggregated.output)
```

### 2. Refine Pattern

Iteratively improve output:

```python
class Refiner(dspy.Module):
    def __init__(self, max_iterations=3):
        super().__init__()
        self.max_iterations = max_iterations
        self.generate = dspy.Predict(GenerateSignature)
        self.refine = dspy.Predict(RefineSignature)

    def forward(self, input_data: str):
        # Initial generation
        current = self.generate(input=input_data)

        # Iterative refinement
        for i in range(self.max_iterations):
            refined = self.refine(
                input=input_data,
                current=current.output,
                iteration=i + 1
            )

            if refined.improvement_score > 0.8:
                break

            current = refined

        return dspy.Prediction(output=current.output)
```

### 3. Ensemble Pattern

Combine multiple programs for better results:

```python
class Ensemble(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program1 = Program1()
        self.program2 = Program2()
        self.program3 = Program3()
        self.aggregate = dspy.Predict(AggregateSignature)

    def forward(self, input_data: str):
        result1 = self.program1(input=input_data)
        result2 = self.program2(input=input_data)
        result3 = self.program3(input=input_data)

        aggregated = self.aggregate(
            result1=result1.output,
            result2=result2.output,
            result3=result3.output
        )

        return dspy.Prediction(output=aggregated.output)
```

### 4. Retrieval-Augmented Generation (RAG)

```python
class RAGProcessor(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever
        self.generate = dspy.Predict(GenerateWithContext)

    def forward(self, query: str):
        # Retrieve relevant documents
        documents = self.retriever.retrieve(query, k=3)

        # Generate with context
        result = self.generate(
            query=query,
            context="\n\n".join(documents)
        )

        return dspy.Prediction(
            answer=result.answer,
            sources=documents
        )
```

## Best Practices

### 1. Use Type Hints

```python
class TypedModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.process = dspy.Predict(MySignature)

    def forward(self, input_data: str) -> dspy.Prediction:
        return self.process(input=input_data)
```

### 2. Return dspy.Prediction

Always return `dspy.Prediction` for consistency:

```python
class GoodModule(dspy.Module):
    def forward(self, input_data: str):
        result = self.process(input=input_data)
        return dspy.Prediction(output=result.output)

# Bad: Don't return raw values
class BadModule(dspy.Module):
    def forward(self, input_data: str):
        return self.process(input=input_data).output  # Wrong!
```

### 3. Handle Errors Gracefully

```python
class RobustModule(dspy.Module):
    def forward(self, input_data: str):
        try:
            result = self.process(input=input_data)
            return dspy.Prediction(output=result.output, success=True)
        except Exception as e:
            return dspy.Prediction(
                output=None,
                success=False,
                error=str(e)
            )
```

### 4. Document Your Modules

```python
class DocumentedModule(dspy.Module):
    """
    A module that processes text and extracts key information.

    Usage:
        module = DocumentedModule()
        result = module.forward(text="Your text here")

    Args:
        text: Input text to process

    Returns:
        dspy.Prediction with:
            - summary: Text summary
            - keywords: List of keywords
            - entities: List of entities
    """

    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeSignature)
        self.extract = dspy.Predict(ExtractSignature)

    def forward(self, text: str):
        # Implementation
        pass
```

### 5. Use Configuration

```python
class ConfigurableModule(dspy.Module):
    def __init__(self, max_length: int = 300, temperature: float = 0.7):
        super().__init__()
        self.max_length = max_length
        self.temperature = temperature
        self.process = dspy.Predict(
            MySignature,
            temperature=temperature
        )

    def forward(self, input_data: str):
        result = self.process(input=input_data, max_length=self.max_length)
        return dspy.Prediction(output=result.output)
```

## AgenticFleet Examples

### DSPyReasoner Module

```python
class DSPyReasoner(dspy.Module):
    """Main reasoning module for AgenticFleet."""

    def __init__(self):
        super().__init__()
        self.task_analyzer = dspy.Predict(TaskAnalysis)
        self.task_router = dspy.Predict(TaskRouting)
        self.quality_assessor = dspy.Predict(QualityAssessment)

    def forward(self, task_description: str, context: str = ""):
        # Analyze task
        analysis = self.task_analyzer(
            task_description=task_description,
            context=context
        )

        # Route to appropriate agent
        routing = self.task_router(
            task=task_description,
            analysis=analysis.task_type
        )

        # Return analysis and routing
        return dspy.Prediction(
            task_type=analysis.task_type,
            agent_id=routing.agent_id,
            confidence=routing.confidence
        )
```

### TaskAnalysisModule

```python
class TaskAnalysisModule(dspy.Module):
    """Analyze tasks to determine complexity and requirements."""

    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(TaskAnalysis)

    def forward(self, task_description: str, context: str = ""):
        result = self.analyze(
            task_description=task_description,
            context=context
        )

        return dspy.Prediction(
            task_type=result.task_type,
            complexity=result.complexity,
            required_agents=result.required_agents,
            estimated_steps=result.estimated_steps,
            reasoning=result.rationale
        )
```

## Common Issues and Solutions

### Issue: Program not compiling

**Problem**: Compilation fails with cryptic errors

**Solution**:
1. Check that all signatures are valid (use `test-signature.py`)
2. Verify all sub-modules are properly initialized
3. Ensure type hints match signature fields
4. Clear cache and retry

### Issue: Poor performance after compilation

**Problem**: Compiled program performs worse than uncompiled

**Solution**:
1. Use more training examples
2. Adjust teleprompter parameters (e.g., `max_labeled_demos`)
3. Use a better metric for optimization
4. Try different teleprompters (BootstrapFewShot, KNNFewShot)

### Issue: Chain of Thought too verbose

**Problem**: Rationale is too long and expensive

**Solution**: Configure token limits on the LM:
```python
# Limit reasoning tokens via the LM configuration
lm = dspy.LM("openai/gpt-4o-mini", max_tokens=500)
dspy.configure(lm=lm)

self.reason = dspy.ChainOfThought(MySignature)
```

### Issue: Module composition complexity

**Problem**: Too many nested modules, hard to debug

**Solution**:
1. Break into smaller, focused modules
2. Use clear naming conventions
3. Add logging to trace execution
4. Test modules individually before composing
