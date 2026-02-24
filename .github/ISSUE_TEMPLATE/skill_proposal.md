---
name: Skill Proposal
about: Propose a new skill you'd like to contribute
title: '[SKILL PROPOSAL] '
labels: skill-proposal
assignees: ''
---

## Skill ID

<!-- kebab-case identifier, e.g., my-skill -->

## Skill Name

<!-- Human-readable name -->

## Description

<!-- 1-2 sentence description -->

## Implementation Plan

### DSPy Module

<!-- Describe the DSPy Module implementation -->

### Signatures

<!-- List all DSPy Signatures -->

```python
class SkillSignature(dspy.Signature):
    """..."""
    # Define fields
```

### Input/Output Schemas

<!-- Provide JSON Schema sketches -->

```json
{
  "inputs_schema": {},
  "outputs_schema": {}
}
```

## Behavior

- Deterministic: [ ] Yes / [ ] No
- Temperature hint: 
- Max tokens hint: 

## Permissions

- [ ] network
- [ ] filesystem_read
- [ ] filesystem_write
- [ ] external_tools: []

## Safety

- Level: [ ] low / [ ] medium / [ ] high
- Risks: 
- Mitigations: 
- Data policy: 

## Evaluation Plan

<!-- How will you test this skill? -->

- Golden set size: 
- Metrics: [ ] exact_match [ ] contains [ ] json_schema_valid
- Edge cases covered: 

## Implementation Timeline

<!-- When do you plan to have this ready? -->

## Questions for Reviewers

<!-- Any specific feedback you're looking for? -->

## Checklist

- [ ] I've read CONTRIBUTING.md
- [ ] I've checked for similar existing skills
- [ ] I've considered security and safety implications
- [ ] I'm prepared to maintain this skill
