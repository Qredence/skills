# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to security@qredence.ai.

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:

* Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Preferred Languages

We prefer all communications to be in English.

## Policy

We follow the principle of [Coordinated Vulnerability Disclosure](https://vuls.cert.org/confluence/display/CVD).

## Security Considerations for Skills

### Skill Safety Levels

Skills are classified by safety level:

* **Low**: No network access, no file system access, pure computation
* **Medium**: Requires controlled external resources (APIs with keys, read-only file access)
* **High**: Requires write access, executes code, or handles sensitive data

### Permission System

All skills must declare explicit permissions in `skill.yaml`:

```yaml
permissions:
  network: false
  filesystem_read: false
  filesystem_write: false
  external_tools: []
```

**Never run skills with permissions you don't understand.**

### Data Handling

* Skills should **never** persist sensitive data without explicit user consent
* Skills must document data retention policies
* Skills handling PII must explicitly state this in `safety.risks`

### Supply Chain Security

* All skill dependencies must be explicitly declared with version ranges
* CI validates that no unauthorized dependencies are added
* Regular security audits of dependencies via `pip-audit` or similar

## Known Limitations

* Skills are **not sandboxed** by default - they run with the permissions of the Python process
* LLM outputs are **non-deterministic** - golden evals provide guidance but not guarantees
* Skills may call external APIs - review `permissions.network` before use

## Future Security Enhancements

We are considering:

* Runtime sandboxing via containers or restricted Python environments
* Cryptographic signing of skills
* Automated security scanning in CI
* Rate limiting for API-calling skills

## Acknowledgments

We thank the security research community for helping us keep this project secure.
