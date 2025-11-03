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

## [0.1.1] - 2025-11-03

### Fixed
- **Windows UTF-8 Encoding**: Fixed 'charmap' codec errors when generating documents with emoji characters on Windows
  - Added `encoding='utf-8'` to all file write operations in `document_generator.py` and `main.py`
- **Utility Script Copying**: Projects now include standard utility modules from project_template
  - Added `_copy_utility_scripts()` method to `RepoBootstrapper`
  - Copies config_loader.py, db_utils.py, email_utils.py, log_utils.py, time_utils.py
- **Charter Template Improvements**:
  - Fixed section numbering (sections 9-12 now sequential)
  - Improved selection criteria filtering (handles 'done' placeholder)
  - Reorganized Major Obstacles into Risks section
  - Better placement of optional sections

### Added
- GitHub issue tracking integration
  - Created issues #1-4 on GitHub for Phase 2 and Phase 3 work
  - Added GitHub links to ISSUES.md
- Code quality tooling
  - Added `make lint` command to check code quality with ruff
  - Added `make lint-fix` command to auto-fix linting issues
  - All code now passes linting checks (17 errors fixed)

### Changed
- Improved error handling in wizard with specific exception types instead of bare except
- Removed unnecessary f-strings and unused imports across codebase

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
