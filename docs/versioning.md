# Skill Versioning

Qredence Skills follow **Semantic Versioning** (semver) to communicate changes clearly to users.

## Semver Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

Examples:
- `1.0.0` - Initial stable release
- `1.2.3` - Minor improvements and patches
- `2.0.0` - Breaking changes
- `1.0.0-alpha.1` - Pre-release
- `1.0.0+20240215` - Build metadata

## Version Components

### MAJOR (X.0.0)

Increment when you make **incompatible** changes:

**Breaking Changes**:
- Removing or renaming input fields
- Removing or renaming output fields
- Changing field types incompatibly
- Changing required fields
- Removing functionality
- Changing behavior that breaks existing use cases
- Changing determinism guarantees (deterministic → non-deterministic)
- Adding required fields without defaults

**Examples**:
```yaml
# Before (v1.0.0)
io:
  inputs_schema:
    properties:
      text: {type: "string"}
    required: ["text"]

# After (v2.0.0) - BREAKING: renamed field
io:
  inputs_schema:
    properties:
      input_text: {type: "string"}  # Renamed from 'text'
    required: ["input_text"]
```

### MINOR (0.X.0)

Increment when you add **backwards-compatible** functionality:

**Non-Breaking Additions**:
- Adding optional input fields
- Adding new output fields
- Adding new functionality
- Improving performance without changing behavior
- Adding new optional parameters with defaults
- Enhancing documentation

**Examples**:
```yaml
# Before (v1.0.0)
io:
  inputs_schema:
    properties:
      text: {type: "string"}
    required: ["text"]

# After (v1.1.0) - Non-breaking: added optional field
io:
  inputs_schema:
    properties:
      text: {type: "string"}
      max_length: {type: "integer", default: 100}  # New optional field
    required: ["text"]
```

### PATCH (0.0.X)

Increment when you make **backwards-compatible** bug fixes:

**Bug Fixes**:
- Fixing incorrect behavior
- Fixing edge cases
- Performance improvements
- Documentation fixes
- Dependency updates (non-breaking)
- Internal refactoring

**Examples**:
- Fixed handling of empty strings
- Corrected output schema validation
- Improved error messages
- Fixed memory leak

## Pre-Release Versions

Use pre-release identifiers for unstable versions:

- `1.0.0-alpha.1` - Alpha release (early testing)
- `1.0.0-beta.1` - Beta release (feature complete, testing)
- `1.0.0-rc.1` - Release candidate (final testing)

Pre-releases are **not** considered stable and may have breaking changes.

## Version Lifecycle

### 1. Initial Development (0.x.y)

- Major version `0` indicates initial development
- **Anything may change** at any time
- API should not be considered stable
- Example: `0.1.0`, `0.2.0`, `0.3.1`

### 2. First Stable Release (1.0.0)

- Indicates stable, public API
- Commits to semantic versioning
- Breaking changes require major version bump

### 3. Ongoing Development

- PATCH for fixes (1.0.1, 1.0.2)
- MINOR for features (1.1.0, 1.2.0)
- MAJOR for breaking changes (2.0.0)

## Deprecation Policy

When deprecating features:

1. **Mark as deprecated** in MINOR version
   - Add deprecation notice in documentation
   - Add warnings in code
   - Provide migration guide

2. **Remove in MAJOR version**
   - At least one MINOR version must pass
   - Clear communication in CHANGELOG

**Example Timeline**:
- v1.5.0: Deprecate `old_field`, add `new_field`
- v1.6.0: Keep both, warn on `old_field` usage
- v2.0.0: Remove `old_field`

## Skill Dependencies

### Pinning Dependencies

In `skill.yaml`:

```yaml
dspy:
  dependencies:
    - "dspy-ai>=2.5.0,<3.0.0"  # Allow MINOR and PATCH updates
    - "pydantic>=2.0.0,<3.0.0"
```

**Best Practices**:
- Use `>=X.Y.0,<(X+1).0.0` for flexibility
- Test against minimum and maximum versions
- Update regularly for security patches

### Breaking Dependency Updates

If a dependency has breaking changes:
- Bump MAJOR version of your skill
- Update dependency version range
- Test thoroughly
- Document migration

## Version Compatibility

### Input/Output Compatibility

**Backwards Compatible** (MINOR/PATCH):
```python
# v1.0.0 → v1.1.0
# Old code still works
result = skill.run(text="hello")  # Still works

# New optional parameter
result = skill.run(text="hello", max_length=50)  # Also works
```

**Backwards Incompatible** (MAJOR):
```python
# v1.0.0 → v2.0.0
# Old code breaks
result = skill.run(text="hello")  # ERROR: 'text' renamed to 'input_text'

# Must update
result = skill.run(input_text="hello")  # New API
```

## CHANGELOG Entries

Document all changes in `CHANGELOG.md`:

```markdown
## [2.0.0] - 2024-02-15

### Changed (BREAKING)
- Renamed input field `text` to `input_text` for consistency

### Migration Guide
Update all calls:
- Before: `skill.run(text="...")`
- After: `skill.run(input_text="...")`

## [1.1.0] - 2024-02-01

### Added
- New optional `max_length` parameter
- Support for batch processing

## [1.0.1] - 2024-01-15

### Fixed
- Handle empty string inputs correctly
- Fix schema validation for nested objects
```

## Version Review Checklist

Before releasing:

- [ ] Version number follows semver
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Migration guide provided (if MAJOR)
- [ ] Tests pass
- [ ] Golden evals pass
- [ ] Documentation updated
- [ ] Dependencies reviewed

## Querying Versions

```bash
# List all versions of a skill (from git tags)
git tag | grep "web_summarizer-v"

# Check current version
cat skills/web_summarizer/skill.yaml | grep version
```

## Best Practices

1. **Start at 0.1.0** for new skills
2. **Bump to 1.0.0** when stable and ready for production
3. **Communicate** breaking changes clearly
4. **Test** against multiple dependency versions
5. **Document** all changes in CHANGELOG
6. **Consider** impact on downstream users
7. **Use** pre-releases for experimental features

## Common Mistakes

❌ **Incrementing PATCH for new features**
✅ Increment MINOR for new features

❌ **Making breaking changes in MINOR version**
✅ Bump MAJOR for breaking changes

❌ **Not documenting breaking changes**
✅ Always provide migration guide

❌ **Reusing version numbers**
✅ Never reuse or change published versions
