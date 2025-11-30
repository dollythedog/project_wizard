# Changelog

All notable changes to Project Wizard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0-phase1] - 2025-11-30

### Added - Phase 1: Blueprint System Foundation

#### Blueprint System
- **Blueprint Schema**: Complete JSON schema for declarative template definitions (`docs/BLUEPRINT_SCHEMA.md`)
- **Pydantic Models**: Full validation models in `app/models/blueprint.py` (765 lines)
- **Blueprint Registry**: Service for loading, validating, and caching blueprints (`app/services/blueprint_registry.py`)
- **Document Templates**: Three complete blueprints with prompts
  - `patterns/project_charter/` - 24 inputs, 13 sections, 5 verification questions, 4-criteria rubric
  - `patterns/work_plan/` - 5 inputs, 3 sections, 3 verification questions, 4-criteria rubric
  - `patterns/proposal/` - 8 inputs, 6 sections, 2 verification questions, 3-criteria rubric

#### AI Prompts System
- **prompts.json Structure**: AI agent instructions for each template
  - `step_back_prompts` - Strategic clarification questions
  - `draft_generation` - Detailed generation instructions with quality standards
  - `verification` - Quality checks organized by category
  - `memory_logging` - Learning patterns for continuous improvement
- **Anti-Hallucination Safeguards**: Critical rules in proposal template to prevent fabricated content

#### CLI Commands
- `project-wizard templates list` - List all available templates
- `project-wizard templates list -v` - Show detailed template information
- `project-wizard templates show <name>` - Display complete template details
- `project-wizard templates validate <name>` - Validate specific template
- `project-wizard templates validate --all` - Validate all templates

#### Document Generator
- **Blueprint Mode**: New `use_blueprints` parameter (default=False for backward compatibility)
- **generate_from_blueprint()** method for blueprint-based generation
- Updated `generate_charter()` and `generate_project_plan()` to support both modes

#### Testing
- `tests/test_blueprint_models.py` - 30+ test cases for Pydantic models
- `tests/test_blueprint_registry.py` - 20+ test cases for registry service
- `tests/test_integration_blueprints.py` - 5 integration tests
- `tests/test_cli_templates.py` - 7 CLI command tests
- `tests/test_phase1_integration.py` - 14 comprehensive end-to-end tests
- **Test Coverage**: 62+ tests, 100% pass rate

#### Documentation
- `docs/BLUEPRINT_SCHEMA.md` - Complete blueprint JSON schema reference
- `docs/BLUEPRINT_IMPLEMENTATION_GUIDE.md` - Step-by-step implementation guide
- `docs/PHASE1_COMPLETION.md` - Phase 1 completion report
- `docs/TASK_1.3.4_COMPLETION.md` - CLI commands completion report
- `patterns/README.md` - Pattern directory structure documentation

### Changed
- **DocumentGenerator**: Extended to support blueprint-based generation while maintaining full backward compatibility
- **CLI**: Added `templates` command group with subcommands
- **Architecture**: Separated template data (blueprints) from code for extensibility

### Technical Details
- **Lines Added**: ~5,700+
- **Files Created**: 22 new files
- **Files Modified**: 2 files (document_generator.py, main.py)
- **Backward Compatibility**: 100% maintained - all v0.4.2 functionality unchanged

### Migration Notes
- No breaking changes
- Existing projects continue to work without modification
- New blueprint system is opt-in via `use_blueprints=True`
- CLI commands remain unchanged from v0.4.2

## [0.4.2] - 2025-11-04

### Added
- AI prompt generator for planning wizard
- Comprehensive test specifications

### Fixed
- Critical parser and template issues
- Charter template fixes
- Missing documentation
- HIPAA detection improvements

## [0.4.1] - 2025-11-03

### Fixed
- Charter template corrections
- Added missing documentation
- Improved HIPAA compliance detection

## [0.4.0] - 2025-11-02

### Added
- RPG-style project management framework
- Quest map visualization with phases and gates
- Gamified progress tracking
- Phase management system

## [0.3.0] - Initial CLI Release

### Added
- Interactive charter creation wizard
- Project planning wizard
- Automatic document generation
- Repository structure bootstrapping
- Git initialization
- OpenProject integration planning

---

## Versioning Strategy

Starting with v3.0.0, Project Wizard follows semantic versioning:

- **MAJOR** (3.x.x): Breaking changes, major architecture shifts
- **MINOR** (x.Y.x): New features, backward compatible
- **PATCH** (x.x.Z): Bug fixes, minor improvements

Phase releases (3.0.0-phase1, 3.0.0-phase2, etc.) indicate incremental progress toward v3.0.0 stable.
