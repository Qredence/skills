# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository structure
- Core skill framework with DSPy integration
- Skill metadata schema with JSON Schema validation
- Safety permission system
- Starter skills: web_summarizer, doc_transformer, task_planner
- Golden evaluation framework with JSONL format
- Validation tooling (`tools/validate.py`)
- Skill scaffolding tool (`tools/new_skill.py`)
- Evaluation runner (`tools/run_eval.py`)
- Automated catalog generation
- CI/CD with GitHub Actions
- Comprehensive documentation

### Security
- Explicit permission declarations for all skills
- Safety level classification system
- No credentials or secrets in repository

## [0.1.0] - 2024-02-15

### Added
- Initial release of Qredence Skills Registry
- Three starter DSPy skills with complete contracts
- Full test coverage with pytest
- GitHub Actions CI pipeline
- Developer documentation and contribution guidelines

[Unreleased]: https://github.com/Qredence/skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Qredence/skills/releases/tag/v0.1.0
