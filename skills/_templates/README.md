# Skill Templates

This directory contains templates for creating new DSPy skills. Use `tools/new_skill.py` to generate a new skill from these templates.

## Usage

```bash
python tools/new_skill.py my_new_skill \
  --description "Brief description of what this skill does" \
  --tags tag1 tag2 tag3 \
  --owner "Your Name"
```

This generates:
- `skills/my_new_skill/skill.yaml` - Metadata
- `skills/my_new_skill/src/skill.py` - Implementation
- `skills/my_new_skill/tests/test_contract.py` - Tests
- `skills/my_new_skill/eval/golden.jsonl` - Evaluations
- `skills/my_new_skill/examples/minimal.py` - Example
- `skills/my_new_skill/README.md` - Documentation

## Template Files

- `skill.yaml` - Metadata template
- `src/skill.py` - DSPy Module template
- `tests/test_contract.py` - Test template
- `eval/golden.jsonl` - Evaluation template
- `examples/minimal.py` - Example template

## Customization

After generation:

1. **Edit skill.yaml**: Update schemas, permissions, safety level
2. **Implement src/skill.py**: Add your DSPy Module logic
3. **Add tests**: Write comprehensive tests
4. **Create golden set**: Add evaluation examples
5. **Update README**: Document usage and limitations

## See Also

- [Skill Contract](../../docs/skill_contract.md) - Complete contract specification
- [Tagging](../../docs/tagging.md) - Tag taxonomy
- [Safety](../../docs/safety.md) - Safety framework
