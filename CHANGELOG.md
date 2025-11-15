# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2.7.0] - 2025-11-15

### Added
- **OpenProject Integration**: Export WORK_PLAN.md files directly to OpenProject
  - New service: `app/services/openproject_exporter.py`
  - Parses work plan structure and creates hierarchical work packages
  - One-click export button in Deliverables tab for WORK_PLAN.md and ISSUES.md
  - Automatic project creation/detection in OpenProject
  - Task metadata mapping (responsible party, duration, dependencies)
  - Duration to estimated hours conversion (e.g., "5 days" → 40 hours)
- Configuration: `.env.example` with OpenProject settings template
- Documentation: `docs/OPENPROJECT_INTEGRATION.md` with setup guide

### Changed
- Updated `app/ui/tabs/deliverables_tab.py` to support OpenProject export
  - Integrated OpenProjectExporter service
  - Replaced subprocess-based approach with direct API calls
  - Uses environment variables for secure credential management
  - Added support for WORK_PLAN.md in addition to ISSUES.md

### Technical
- OpenProject API authentication using HTTP Basic Auth with base64 encoding
- RESTful API integration for project and work package management
- Parsing engine for markdown table-based work plans
- Error handling and user-friendly status messages

### Files Added
- `app/services/openproject_exporter.py`
- `.env.example`
- `docs/OPENPROJECT_INTEGRATION.md`

### Files Modified
- `app/ui/tabs/deliverables_tab.py`

### Backups Created
- `app/ui/tabs/deliverables_tab.py.backup`

## [2.6.0] - 2025-11-14

### Added
- **Modular Architecture**: Refactored monolithic app into clean modular structure
  - `app/ui/tabs/` - Tab-based UI components (home, charter, docs, deliverables)
  - `app/ui/modals/` - Modal dialog components
  - `app/components/` - Reusable UI components
  - `app/services/` - Business logic services
  - `app/state/` - Session state management
  - `app/utils/` - Utility functions
- **New Patterns**:
  - `patterns/proposal/` - Project proposal generation
  - `patterns/work_plan/` - Work plan generation
- **Project Scaffolder**: Service to bootstrap new projects with folder structure
- **Document Registry**: Service to track and manage deliverables
- **Content Library**: Reusable input library for patterns (proposal pattern)
- **Project Selector UI**: Sidebar component for project navigation

### Changed
- **Main app file**: Migrated from `app_v2_5.py` to modular `app.py`
- **Tab structure**: Implemented tab-based navigation (Home, Charter, Documentation, Deliverables)
- **Pattern discovery**: Made fully automatic in Deliverables tab
- **Document editor**: Enhanced with better state management and chunked AI processing

### Removed
- Deprecated `app_v2_5.py` and related files
- Removed `SESSION_SUMMARY.md` and `PROJECT_MANAGEMENT_UPGRADE.md` (consolidated into docs)

### Technical
- Improved separation of concerns across services, UI, and business logic
- Better session state management to prevent data loss on reruns
- Enhanced error handling and user feedback

---

## [2.5.3] - 2025-11-14

### Fixed
- **Critical: Project charter generation now includes user inputs** - Fixed charter template to properly wrap AI-generated content instead of expecting variable substitution
- **Charter wizard pre-population** - When recreating an existing charter, wizard form now pre-populates with existing data
- Enhanced charter system prompt with explicit 14-section output format specification

### Changed
- Updated `patterns/project_charter/template.md.j2` to use simple content wrapper pattern
- Modified charter wizard form to parse and pre-populate from existing deliverables

### Technical
- Identified and resolved mismatch between AI pattern pipeline (free-form content generation) and variable-substitution template
- Added graceful error handling for charter parsing failures

### Files Modified
- `patterns/project_charter/template.md.j2` - Simplified template structure
- `patterns/project_charter/system.md` - Enhanced with explicit format specification
- Charter wizard - Added form pre-population logic

### Backups Created
- `patterns/project_charter/template.md.j2.backup`
- `patterns/project_charter/system.md.backup`
- `app_v2_5.py.pre_charter_fix`

---

## [2.5.2] - 2025-11-13

### Added
- Chunked document enhancement for large deliverables in DocumentEditor
- `enhance_large_document()` method in CharterAgent for processing documents in ~1000 character chunks
- Session state persistence for deliverable content to prevent reload from disk on every rerun
- Synchronization between text_area widget state and session state for real-time AI enhancements

### Fixed
- AI enhancements not applying to deliverables due to full document being passed to LLM
- Deliverable content being reloaded from disk on every Streamlit rerun, overwriting AI enhancements
- Text area widget state not updating when AI enhancements are applied
- Session state key management for deliverable content across reruns

### Changed
- Temporarily disabled `@st.cache_resource` on `get_services()` to allow dynamic code reloading
- Enhancement buttons now process documents in chunks for better AI output quality

---

## [2.5.1] - 2025-11-12

### Added
- **Visual Project Management System**: Gallery view and project registry
- **Project Registry Service**: Track all projects with metadata in `~/.project_wizard_projects.json`
- **Recent Projects Sidebar**: Quick access to recently used projects
- **Project Gallery Modal**: Visual browse and select interface

### Fixed
- Non-functional recent projects sidebar (introduced ProjectRegistry)

### Files Modified
- `app_v2_5.py` - Added gallery and registry integration
- `app/services/project_registry.py` - New service for project tracking

---

## [2.5.0] - 2025-11-11

### Added
- **Pattern-Based Document Generation System**: 
  - Pattern registry to discover and manage AI patterns
  - Pattern pipeline for draft → critique → enhancement workflow
  - Deliverables tab for automatic pattern discovery
- **Documentation Tab**: View and edit project markdown files
- **Automatic Pattern Discovery**: Scans `patterns/` folder for available patterns

### Changed
- Implemented pattern-based workflow for all document types
- Enhanced UI with tabs for better organization

---

## [2.0.0] - 2025-11-10

### Added
- **AI-Enhanced Charter Creation**: GPT-4o-mini-powered charter generation
- **Anti-Hallucination System**: Structured prompts, rubric-based evaluation
- **Critique System**: AI evaluates documents against rubrics with KPI scores
- **Charter Wizard**: Multi-step form for charter creation
- **Charter Critique Display**: KPI-focused UI with detailed feedback

### Fixed
- AI critique showing 0% scores (fixed mismatched fields)
- OpenAI API key not found error (added dotenv support)
- Hallucinated metrics in generated documents

### Changed
- Moved to structured template-based generation
- Lowered AI temperature for more deterministic outputs (0.3-0.4)
- Implemented rubric-based evaluation system

---

## [0.1.0] - 2025-11-08

### Added
- Initial Project Wizard functionality
- Basic project bootstrapping
- README, CHANGELOG, ISSUES file generation
- Makefile for project management
- Core project structure with patterns folder

### Documentation
- Created initial `README.md`
- Added `PROJECT_PLAN.md` for roadmap
- Created `PROJECT_CHARTER.md` for project definition
- Added `ISSUES.md` for issue tracking

---

## Version Numbering

This project uses Semantic Versioning:
- **Major version (X.0.0)**: Breaking changes, major feature release
- **Minor version (0.X.0)**: New features, non-breaking changes
- **Patch version (0.0.X)**: Bug fixes, minor improvements
