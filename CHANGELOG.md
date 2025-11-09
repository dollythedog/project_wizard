# Changelog

All notable changes to Project Wizard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.1] - 2025-11-09

### Added - Project Management System Overhaul

#### Visual Project Gallery
- **Project Registry Service** (`app/services/project_registry.py`) - Persistent project metadata tracking
- **Project Gallery UI** - Visual grid display with project cards (3-column layout)
  - Project icon selection (20 emoji options)
  - Project metadata: name, type, description, dates
  - Quick actions: Open project, Remove from list
- **Recent Projects sidebar** - Shows 5 most recently accessed projects with one-click loading

#### New Project Creation Wizard
- **Guided project creation flow** - Step-by-step dialog for new projects
  - Project name with automatic folder sanitization
  - Icon picker with visual emoji selection
  - Project type dropdown (Software Development, Process Improvement, Clinical Initiative, Research, Infrastructure, Other)
  - Optional description field
  - Configurable base directory (defaults to `~/Projects`)
  - Live preview of project path before creation
- **Automatic directory creation** - Creates proper project folder structure on initialization
- **Project registration** - Automatically tracks new projects in registry

#### Enhanced Project Navigation
- **Welcome screen** - Shows when no project loaded with clear CTAs
- **My Projects button** (📚) - Opens visual project gallery
- **New Project button** (➕) - Launches creation wizard
- **Current project indicator** - Sidebar displays active project with icon and name
- **Project persistence** - Registry stored in `~/.project_wizard_projects.json`

### Changed

#### Project Workflow Improvements
- **Projects directory structure** - Created `~/Projects/` to match Windows workflow (`C:\Projects`)
- **Hermes project migrated** - Moved from app root to `/home/ivesjl/Projects/Hermes/`
- **Project loading** - Charter files now stay in project directories, properly load on project switch
- **Last accessed tracking** - Projects automatically update access time for recent list sorting

#### Code Organization
- **Decluttered root directory**:
  - Moved old docs to `docs/archive/`
  - Moved version-specific READMEs to `docs/version_docs/`
  - Moved guides to `docs/`
  - Moved backup/deprecated Python files to `docs/archive/`
- **Removed legacy system** - Deleted old `.project_wizard_recent.json` in favor of new registry

### Fixed
- **Non-functional Recent Projects** - Replaced broken sidebar list that showed app directory
- **Clickable project links** - All project navigation now properly loads project context
- **Project confusion** - Clear visual indicators of current project throughout UI
- **Charter location issues** - Charter files now properly saved to project directories

### Technical Improvements
- **ProjectRegistry class** with methods:
  - `register_project()` - Add new project with metadata
  - `update_project()` - Modify project attributes
  - `touch_project()` - Update last accessed timestamp
  - `get_project()` - Retrieve project metadata
  - `list_projects()` - Get all projects with sorting (by name, created_date, last_accessed)
  - `remove_project()` - Unregister project (doesn't delete files)
  - `project_exists()` - Check registration status


## [2.5.0] - 2025-11-08

### Added - Major Pattern System Integration

#### Pattern-Based Document Generation
- **PatternRegistry service** - Dynamic pattern discovery and loading from `patterns/` directory
- **ProjectContext service** - Automatic injection of project documentation (charter, README, issues, changelog) into AI prompts
- **PatternPipeline service** - Unix-style agent orchestration (Draft → Edit → Critique → Output)
- **5W1H Analysis pattern** - Complete LEAN problem definition template with quality rubric

#### Specialized AI Agents
- **DraftAgent** - Initial document generation (temperature: 0.3)
- **EditorAgent** - Polishing without hallucination (temperature: 0.2) with anti-fabrication constraints
- **Enhanced CriticAgent integration** - Pattern-specific quality rubrics

#### Integrated Workflow UI (v2.5)
- **Unified 4-tab interface** replacing separate v2/v3 apps:
  - Tab 1: Project Initiation (enhanced form validation)
  - Tab 2: Business Case (improved help text)
  - Tab 3: Charter - Living document with integrated quality KPIs, enhancement options, save/download
  - Tab 4: Project Home - Activity hub with radio selector for LEAN tools

#### Project Management
- **Sidebar project selector** with recent projects (last 5)
- **Load existing projects** - Automatically parses and loads existing `PROJECT_CHARTER.md`
- **Save to project** - Writes charter to project directory and tracks in recent list
- **Recent projects persistence** - Saved to `~/.project_wizard_recent.json`

#### Dynamic Form System
- **Auto-generated forms** from pattern `variables.json`
- **Template preview** - Shows required fields before starting activity
- **Field validation** - Required field checking with user feedback
- **Contextual help** - Inline help text and placeholders for all fields

### Changed

#### Architecture Improvements
- Refactored charter generation into unified v2.5 app (consolidating v2.0 and v3.0 approaches)
- Implemented Fabric-inspired pattern system (self-contained, reusable document templates)
- Added project context to all AI calls for strategic alignment
- Replaced hard-coded document logic with data-driven patterns

#### User Experience
- **Progressive workflow** - Clear tab progression (Initiation → Business Case → Charter → Home)
- **Charter as living document** - Generate once, iterate with enhancements
- **Activity status indicators** - "✓ Done" or "Create" button for each LEAN tool
- **Quality KPIs at-a-glance** - Scores displayed prominently in Charter tab

### Fixed
- Import errors in UI module exports
- Port configuration for v2.5 (now on 8504)
- Session state persistence across tab navigation
- Form data retention when switching between projects

### Technical Details

#### New Files (v2.5)
```
app/services/
├── pattern_registry.py      (6.2 KB) - Pattern loader
├── project_context.py        (3.5 KB) - Context injection
├── pattern_pipeline.py       (7.4 KB) - Agent orchestrator
└── ai_agents/
    ├── draft_agent.py        (2.4 KB) - Draft generation
    └── editor_agent.py       (4.1 KB) - Polishing

app/ui/
├── __init__.py
├── project_selector.py       (3.7 KB) - Sidebar component
└── pattern_form.py           (4.2 KB) - Dynamic forms

patterns/5w1h_analysis/
├── system.md                 (5.3 KB) - AI instructions
├── user.md                   (0.9 KB) - Context template
├── variables.json            (2.3 KB) - UI fields
├── rubric.json               (1.2 KB) - Quality criteria
└── template.md.j2            (0.8 KB) - Output format

app_v2_5.py                   (Large) - Integrated app
run_v2_5.sh                   - Launch script
```

#### Dependencies
- No new Python dependencies required
- Uses existing: streamlit, openai, jinja2, pathlib

#### Performance
- Pattern loading cached with `@st.cache_resource`
- Project context loaded on-demand
- Minimal API calls (only on user action)

### Deployment

#### Ports
- **v1.0**: 8501 (legacy)
- **v2.0**: 8502 (charter only)
- **v2.5**: 8504 (integrated) ← **Use this**
- v3.0: 8503 (standalone patterns - deprecated)

#### Launch
```bash
./run_v2_5.sh
# or
streamlit run app_v2_5.py --server.port 8504
```

#### Access
- Local: http://localhost:8504
- Network: http://10.69.1.86:8504

### Migration from v2.0

**Automatic** - v2.5 includes all v2.0 functionality plus:
- Pattern system for additional document types
- Project loading/saving
- Enhanced UI with living charter
- Activity hub for LEAN tools

**No breaking changes** - Existing workflows preserved in Tabs 1-3

### Future Roadmap (v3.0+)

#### Planned Features
- Additional patterns: SIPOC, Fishbone, VOC, Process Map
- Pattern cross-referencing (use SIPOC in VSM generation)
- Project scaffolding (auto-create folder structure)
- Core document templates (README.md.j2, ISSUES.md.j2)
- Enhanced AI editing options (multiple tone/style choices)
- OpenProject API integration for task upload

#### Known Limitations
- Charter parsing is simple (may miss complex formatting)
- Enhancement buttons in Charter tab are placeholders
- No visual diagram generation yet (Mermaid planned for v3.1)

### Contributors
- dollythedog (architecture, implementation)

### References
- [Fabric Project](https://github.com/danielmiessler/fabric) - Pattern system inspiration
- [LEAN Six Sigma](https://www.lean.org/) - Methodology standards
- Project guidelines: `docs/PROJECT_GUIDELINES.md`

---

## [2.0.0] - 2024-11-06

### Added
- Structured PM methodology workflow
- AI text enhancement with anti-hallucination design
- Quality critique with 6 weighted criteria
- Streamlit web interface on port 8502

### Changed
- Moved from v1.0 simple form to structured 6-tab workflow

---

## [1.0.0] - Initial Release

### Added
- Basic project charter generation
- OpenAI API integration
- Simple web form

---

**Note**: Version 2.5.0 represents a major architectural shift to pattern-based generation while maintaining full backward compatibility with v2.0 workflows.
