# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Phase 2: Planning wizard (work breakdown structure)
- OpenProject sync implementation
- Project type templates (YAML)
- ISSUES.md ↔ OpenProject bidirectional sync
- Docker deployment
- FastAPI web interface (optional)

## [0.1.0] - 2025-11-03

### Added
- Interactive charter creation wizard (Phase 1: Initiation)
- Pydantic models for charter data structure
- Jinja2 document generation (PROJECT_CHARTER.md, README.md)
- Repository bootstrapper with standardized folder structure
- CLI with Click framework (`project-wizard init`, `plan`, `sync`)
- Automatic git initialization
- Charter data saved as JSON
- Comprehensive Makefile for development workflows
- Setup.py for pip installation

### Documentation
- README.md with quick start guide
- DEVELOPMENT_SUMMARY.md with technical details
- Reference docs (PROJECT_STEP_BY_STEP.md, PROJECT_GUIDELINES.md)

### Technical
- Python 3.8+ compatibility
- Dependencies: click, jinja2, pydantic, requests, rich, questionary
- Git repository initialized

---

## Version History

- **0.1.0** (2025-11-03) - Initial release with Phase 1 charter wizard
