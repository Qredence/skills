## Description

<!-- Provide a brief description of your changes -->

## Type of Change

- [ ] New skill
- [ ] Bug fix
- [ ] Enhancement to existing skill
- [ ] Documentation update
- [ ] Infrastructure/tooling change

## Skill Checklist (if applicable)

- [ ] `skill.yaml` is complete and valid against schema
- [ ] All required files present (README, src/skill.py, tests/, eval/, examples/)
- [ ] DSPy Module and Signatures are properly implemented
- [ ] Input/output schemas are defined and validated
- [ ] Safety permissions are explicitly declared
- [ ] Safety level and risks are documented
- [ ] Golden evaluation set (`eval/golden.jsonl`) is provided
- [ ] All tests pass (`pytest`)
- [ ] Validation passes (`python tools/validate.py`)
- [ ] Eval passes (`python tools/run_eval.py --skill <id>`)
- [ ] Example is runnable (`python skills/<id>/examples/minimal.py`)
- [ ] README documents purpose, usage, limitations, and safety

## General Checklist

- [ ] Code follows style guidelines (`ruff check .`)
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or documented if breaking)
- [ ] Changelog updated

## Testing

<!-- Describe testing performed -->

```bash
# Commands run:
pytest
python tools/validate.py
python tools/run_eval.py --skill <id>
```

## Safety Review

- [ ] Skill has appropriate safety level (low/medium/high)
- [ ] All permissions are necessary and justified
- [ ] Risks and mitigations are documented
- [ ] No secrets or credentials included
- [ ] Data handling policy is clear

## Additional Context

<!-- Add any other context, screenshots, or information -->
