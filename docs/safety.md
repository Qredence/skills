# Safety Framework

Safety is a first-class concern in the Qredence Skills Registry. All skills must explicitly declare permissions and safety characteristics.

## Safety Levels

Every skill is classified by safety level based on potential risks.

### Low

**Characteristics**:
- No network access
- No file system access
- Pure computation on provided inputs
- No external dependencies beyond DSPy
- No PII or sensitive data handling
- Deterministic or near-deterministic

**Examples**:
- Text transformation
- Format conversion
- Mathematical calculations
- Schema validation

**Declaration**:
```yaml
safety:
  level: "low"
  risks:
    - "No known risks for pure computation"
  mitigations:
    - "Input validation only"
  data_policy:
    - "No data persistence"
    - "No PII handling"
```

### Medium

**Characteristics**:
- Controlled external resources (APIs with user keys)
- Read-only file access to specific directories
- May cache data temporarily
- Clear data retention policies
- Handles non-sensitive data

**Examples**:
- Web scraping (with user-provided URLs)
- API calling (with user-provided keys)
- Document parsing from disk
- Knowledge base retrieval

**Declaration**:
```yaml
safety:
  level: "medium"
  risks:
    - "Network requests to user-specified URLs"
    - "Temporary caching of fetched content"
  mitigations:
    - "URL validation and sanitization"
    - "Rate limiting"
    - "Cache expiration"
  data_policy:
    - "Temporary cache only (< 1 hour)"
    - "No PII persistence"
    - "User controls data sources"
```

### High

**Characteristics**:
- Write access to file system
- Executes arbitrary code
- Handles sensitive data (PII, credentials)
- Makes irreversible changes
- Requires additional security review

**Examples**:
- Code execution environments
- File system manipulation
- Database modifications
- Credential management

**Declaration**:
```yaml
safety:
  level: "high"
  risks:
    - "Executes arbitrary code"
    - "Can modify file system"
    - "Handles credentials"
  mitigations:
    - "Sandboxed execution environment"
    - "Input sanitization"
    - "Audit logging"
    - "Explicit user confirmation required"
  data_policy:
    - "Credentials encrypted at rest"
    - "PII handled per GDPR"
    - "Audit trail maintained"
```

## Permission System

All skills must declare explicit permissions. **Default is false/empty** - skills must opt-in.

### network

**When to set true**:
- Making HTTP requests
- Calling external APIs
- Fetching web content
- Network I/O of any kind

**Implications**:
- Skill can access internet
- May expose data externally
- May depend on external services
- Requires user network access

**Example**:
```yaml
permissions:
  network: true
```

### filesystem_read

**When to set true**:
- Reading files from disk
- Accessing local databases
- Loading resources from file system

**Implications**:
- Skill can read user files
- May expose file contents
- Requires disk access

**Best practices**:
- Validate and sanitize paths
- Restrict to specific directories
- Never read sensitive files (passwords, keys)

### filesystem_write

**When to set true**:
- Writing files to disk
- Creating directories
- Modifying existing files
- Appending to logs

**Implications**:
- Skill can modify user data
- May create files
- Requires disk write access
- Potential for data loss

**Best practices**:
- Confirm before writing
- Write to designated output directories
- Never overwrite without confirmation
- Implement rollback if possible

### external_tools

**When to set**:
List specific external tools required.

**Examples**:
```yaml
permissions:
  external_tools:
    - "browser"      # Web browser automation
    - "shell"        # Shell command execution
    - "docker"       # Docker containers
    - "git"          # Git operations
```

**Implications**:
- Skill depends on external executables
- May invoke system commands
- Requires tool availability
- Higher security risk

**Best practices**:
- Be specific about which tools
- Document why each tool is needed
- Implement safe defaults
- Validate tool outputs

## Risk Assessment

### Identifying Risks

Consider:
1. **Data exposure**: Can skill leak sensitive data?
2. **Irreversibility**: Can actions be undone?
3. **External dependencies**: What can fail?
4. **Input validation**: Are inputs sanitized?
5. **Output validation**: Are outputs safe?

### Common Risks

**Network-related**:
- Data exfiltration
- SSRF (Server-Side Request Forgery)
- Exposure of credentials
- Dependency on external services

**File system-related**:
- Path traversal
- Unauthorized access
- Data loss
- Resource exhaustion

**Execution-related**:
- Code injection
- Command injection
- Arbitrary code execution
- Resource exhaustion

**LLM-specific**:
- Prompt injection
- Jailbreaking
- PII exposure in prompts
- Non-deterministic behavior

## Mitigation Strategies

### Input Validation

```python
def validate_input(self, input_data):
    # Check required fields
    # Validate types
    # Sanitize strings
    # Range checks
    # Whitelist allowed values
```

### Output Sanitization

```python
def sanitize_output(self, output_data):
    # Remove PII
    # Filter sensitive fields
    # Validate against schema
    # Escape special characters
```

### Rate Limiting

```python
@rate_limit(calls=10, period=60)  # 10 calls per minute
def forward(self, **kwargs):
    # Implementation
```

### Sandboxing

```python
# Run in isolated environment
with sandbox():
    result = execute_untrusted_code(code)
```

### Audit Logging

```python
def forward(self, **kwargs):
    logger.audit(
        action="skill_execution",
        skill_id=self.metadata.id,
        inputs=kwargs,
        user=current_user
    )
    # Implementation
```

## Data Policy

### PII Handling

If skill handles PII:

```yaml
safety:
  data_policy:
    - "PII is not persisted"
    - "PII is not logged"
    - "PII is not sent to external services"
    - "PII is redacted in outputs when possible"
```

### Data Retention

Specify how long data is kept:

```yaml
safety:
  data_policy:
    - "Temporary cache only (< 1 hour)"
    - "No long-term storage"
    - "Data deleted after session"
```

### Data Sharing

Specify if data is shared:

```yaml
safety:
  data_policy:
    - "No data shared with third parties"
    - "Only used for stated purpose"
    - "User controls all data"
```

## Security Review

### Self-Review Checklist

Before submitting:

- [ ] Safety level is accurate
- [ ] All permissions are declared
- [ ] Risks are documented
- [ ] Mitigations are implemented
- [ ] Data policy is clear
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] Output sanitization present
- [ ] Tests cover security cases

### Maintainer Review

Maintainers will review:
- Safety classification accuracy
- Permission necessity
- Risk assessment completeness
- Mitigation effectiveness
- Code security practices

High safety level skills require additional review.

## Examples

### Low Safety: Document Formatter

```yaml
safety:
  level: "low"
  risks:
    - "No known risks - pure text transformation"
  mitigations:
    - "Input length validation"
  data_policy:
    - "No data persistence"
    - "In-memory processing only"

permissions:
  network: false
  filesystem_read: false
  filesystem_write: false
  external_tools: []
```

### Medium Safety: Web Summarizer

```yaml
safety:
  level: "medium"
  risks:
    - "Fetches content from user-specified URLs"
    - "May expose network requests"
  mitigations:
    - "URL validation (scheme, domain)"
    - "Timeout limits (30s)"
    - "No credential forwarding"
  data_policy:
    - "Fetched content not persisted"
    - "No PII in URLs"

permissions:
  network: true
  filesystem_read: false
  filesystem_write: false
  external_tools: []
```

### High Safety: Code Executor

```yaml
safety:
  level: "high"
  risks:
    - "Executes arbitrary user code"
    - "Potential for resource exhaustion"
    - "Can access host system"
  mitigations:
    - "Sandboxed execution (Docker)"
    - "Resource limits (CPU, memory, time)"
    - "Network isolation"
    - "Explicit user confirmation"
  data_policy:
    - "Code not persisted"
    - "Logs retained for audit (30 days)"
    - "No PII in code"

permissions:
  network: false
  filesystem_read: false
  filesystem_write: false
  external_tools:
    - "docker"
```

## Incident Response

If a security issue is discovered:

1. **Report** to security@qredence.ai (see SECURITY.md)
2. **Do not** disclose publicly until patched
3. **Maintainers** will assess and patch
4. **CVE** may be issued for serious issues
5. **Users** will be notified via security advisory

## Future Enhancements

Planned safety features:
- Runtime sandboxing
- Automated security scanning
- Permission enforcement at runtime
- Cryptographic signing of skills
- Security scorecard
