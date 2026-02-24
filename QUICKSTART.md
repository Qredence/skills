# Quickstart Guide

Get started with the Qredence DSPy Skills Registry in 5 minutes.

## Prerequisites

- Python 3.11+
- Git

## Installation

```bash
# Clone the repository
git clone https://github.com/Qredence/skills.git
cd skills

# Install dependencies
pip install -r requirements.txt

# Install skills_core package
pip install -e packages/skills_core
```

## Browse Skills

```bash
# List all available skills
python tools/validate.py --list

# Show detailed info for a skill
python tools/validate.py --info web_summarizer

# Filter by tag
python tools/validate.py --list --tag summarization
```

## Use a Skill

```python
from pathlib import Path
import sys

# Add repo to path
sys.path.insert(0, str(Path.cwd()))

# Import and use
from skills.web_summarizer.src.skill import run

result = run(url="https://example.com", max_length=150)
print(result.summary)
```

## Create a New Skill

```bash
# Generate scaffold
python tools/new_skill.py sentiment_analyzer \
  --description "Analyzes sentiment of text input" \
  --tags nlp analysis classification \
  --owner "Your Name"

# This creates:
# skills/sentiment_analyzer/
#   skill.yaml          - Metadata
#   src/skill.py        - Implementation
#   tests/              - Tests
#   eval/golden.jsonl   - Evaluations
#   examples/minimal.py - Example
#   README.md           - Documentation
```

## Implement Your Skill

### 1. Edit skill.yaml

Update metadata, schemas, and permissions:

```yaml
id: sentiment_analyzer
name: "Sentiment Analyzer"
version: "0.1.0"
description: "Analyzes sentiment of text (positive, negative, neutral)"
tags:
  - nlp
  - analysis
  - classification

# ... rest of metadata
```

### 2. Implement src/skill.py

Add your DSPy Module logic:

```python
import dspy

class SentimentSignature(dspy.Signature):
    text: str = dspy.InputField(desc="Text to analyze")
    sentiment: str = dspy.OutputField(desc="Sentiment: positive/negative/neutral")
    confidence: float = dspy.OutputField(desc="Confidence score 0-1")

class Skill(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(SentimentSignature)
    
    def forward(self, text: str) -> dspy.Prediction:
        return self.prog(text=text)
```

### 3. Add Golden Evaluations

Create test cases in `eval/golden.jsonl`:

```jsonl
{"name": "positive_text", "input": {"text": "I love this!"}, "expected": "positive", "match": "contains"}
{"name": "negative_text", "input": {"text": "This is terrible"}, "expected": "negative", "match": "contains"}
```

### 4. Write Tests

Add tests in `tests/test_contract.py` and additional test files.

## Validate Your Skill

```bash
# Validate structure and metadata
python tools/validate.py

# Run evaluations (format check)
python tools/run_eval.py --skill sentiment_analyzer --dry-run

# Run tests
pytest skills/sentiment_analyzer/tests/
```

## Submit Your Skill

```bash
# Ensure everything passes
python tools/validate.py
pytest

# Commit and push
git add skills/sentiment_analyzer/
git commit -m "Add sentiment_analyzer skill"
git push origin feature/sentiment-analyzer

# Open pull request on GitHub
```

## Learn More

- [Skill Contract](docs/skill_contract.md) - Complete specification
- [Tagging Guide](docs/tagging.md) - Tag taxonomy
- [Safety Framework](docs/safety.md) - Safety levels and permissions
- [Evaluation Guide](docs/evaluation.md) - Golden evaluations
- [Versioning](docs/versioning.md) - Semantic versioning

## Common Commands

```bash
# Validate all skills
python tools/validate.py

# Create new skill
python tools/new_skill.py <name> --description "..." --tags tag1 tag2

# List skills
python tools/validate.py --list

# Run evaluations
python tools/run_eval.py --dry-run

# Run tests
pytest tests/
```

## Next Steps

1. Browse existing skills in `skills/`
2. Read the [Skill Contract](docs/skill_contract.md)
3. Create your first skill
4. Join the community discussions

## Getting Help

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share ideas
- Documentation: Comprehensive guides in `docs/`

Happy skill building! 🚀
