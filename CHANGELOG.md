# Changelog

All notable changes to the Project Wizard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-11-06

### Added
- **Complete v2.0 Web Application** with 6-tab workflow following formal PM methodology
- **Tab 1: Project Initiation Request** - Structured data collection for business need, outcomes, success criteria
- **Tab 2: Business Case** - Strategic alignment, solution analysis, requirements, resources
- **Tab 3: AI Enhancement** - Per-section enhancement with Accept/Reject/Edit controls
- **Tab 4: Generate Charter** - Template-based charter generation from user data
- **Tab 5: Quality Review** - AI critique against 6-criteria PM rubric with detailed feedback
- **Tab 6: Create Project** - Placeholder for project scaffolding and OpenProject integration
- **Anti-Hallucination System** - Structured prompt library (`configs/enhancement_prompts.json`) with explicit constraints
- **Editable Manual Editing** - Full text area editing with save functionality
- **Quality Critique Display** - Proper transformation of critic_agent output (weighted_score, approved, scores array)
- **Environment Variable Loading** - `load_dotenv()` for OpenAI API key management
- **Comprehensive Documentation** - V2_IMPLEMENTATION_COMPLETE.md, CRITIQUE_FIX.md, QUICK_START.md

### Changed
- **Charter Generation Strategy** - Moved from AI-generated to template-based (eliminates hallucination)
- **Enhancement Approach** - AI now only polishes text structure, never adds facts or metrics
- **Temperature Settings** - Reduced to 0.3 for enhancement (was 0.4) for maximum consistency
- **Scoring Display** - Convert weighted_score (0.0-1.0) to percentage (0-100%) for user clarity
- **Critique Format** - Display strengths, weaknesses, and improvements per criterion
- **Session Management** - Separate state dictionaries for form_data, enhanced_data, manual_edits

### Fixed
- **API Key Loading** - Added `from dotenv import load_dotenv` to v2.0 app (was missing)
- **Critique Display Bug** - Fixed data structure mismatch between critic_agent output and display code
  - Was expecting `overall_score`, `passed`, `criteria_scores` (dict), `summary`
  - Now correctly uses `weighted_score`, `approved`, `scores` (array), `overall_assessment`
- **Zero Score Issue** - Critique now displays actual percentages (e.g., 82%) instead of 0%
- **Edit Manually Button** - Now actually editable with working save functionality

### Documentation
- Updated README.md with v2.0 features, architecture, and complete usage guide
- Created CRITIQUE_FIX.md documenting data structure mismatch resolution
- Updated V2_IMPLEMENTATION_COMPLETE.md with final implementation status
- Enhanced QUICK_START.md with step-by-step workflow examples

### Technical Debt
- Backup file created: `app_streamlit_v2.py.backup` (can be removed after validation)
- v1.0 app still running on port 8501 (consider deprecation timeline)
- Tab 6 (Create Project) not yet implemented - planned for v2.1

---

## [1.0.0] - 2024-11-06

### Added
- **Initial Web Interface** (v1.0) with Streamlit
- **AI-Powered Charter Drafting** - Single-form charter generation with AI agents
- **CharterAgent** - Drafts charter sections from project brief
- **CriticAgent** - Reviews charters against quality rubric
- **LLMClient** - OpenAI API wrapper with retry logic and error handling
- **Configuration System** - YAML-based AI configuration (`ai_config.yaml`)
- **Quality Rubric** - 6-criteria JSON rubric (`rubric_charter.json`) with 75% threshold
- **Systemd Service** - Production deployment as `project-wizard-web.service`
- **UFW Firewall Rules** - LAN access on ports 8501, 8502
- **Logging System** - Structured logging with file output

### Technical
- Python 3.12 support
- OpenAI gpt-4o-mini integration
- Streamlit 1.31.0 web framework
- Virtual environment setup
- .env file for secrets management

---

## [0.2.0] - 2024-11-03

### Added
- CLI-based interactive charter wizard (`project-wizard init`)
- Automatic folder structure generation (configs/, data/, scripts/, docs/)
- PROJECT_CHARTER.md template generation
- README.md auto-generation
- Git repository initialization
- setup.py for package installation

### Features
- Interactive prompts for charter components
- Business case and strategic alignment questions
- Success criteria definition
- Risk and mitigation identification
- Timeline and collaboration needs

---

## [0.1.0] - 2024-11-01

### Added
- Initial project structure
- Basic CLI framework
- Development documentation
- Project planning documents (PROJECT_CHARTER.md, PROJECT_PLAN.md)

---

## Upcoming Releases

### [2.1.0] - Planned
**Focus: Project Scaffolding & OpenProject Integration**

#### Planned Features
- [ ] Tab 6 Implementation: Project scaffolding
- [ ] Folder structure generation (src/, tests/, docs/, configs/)
- [ ] File generation (README.md, CHANGELOG.md, LICENSE.md, .gitignore)
- [ ] Git repository initialization with initial commit
- [ ] OpenProject API integration
- [ ] Automated task creation from charter sections
- [ ] Work package hierarchy setup
- [ ] Project board configuration
- [ ] Template library (software_mvp, research_study, clinical_trial)

#### Technical Improvements
- [ ] Session persistence across days
- [ ] Progress indicators
- [ ] Estimated time to completion
- [ ] Undo/redo functionality
- [ ] Auto-save drafts

### [2.2.0] - Planned
**Focus: Collaboration & Quality**

#### Planned Features
- [ ] Multi-user support with authentication
- [ ] Charter version history and comparison
- [ ] Custom rubric editor for different project types
- [ ] Export to PDF and DOCX formats
- [ ] GitHub Projects integration
- [ ] NTFY notifications for charter reviews

#### Quality Improvements
- [ ] Enhanced error handling and recovery
- [ ] Offline mode support
- [ ] Mobile-responsive design improvements
- [ ] Accessibility (WCAG 2.1 AA compliance)

### [3.0.0] - Vision
**Focus: Full Project Lifecycle Management**

#### Planned Features
- [ ] Phase 2: Project Planning (WBS, Gantt charts, resource allocation)
- [ ] Phase 3: Execution Tracking (task progress, time tracking, status reports)
- [ ] Phase 4: Closure & Lessons Learned (retrospectives, documentation, archival)
- [ ] Dashboard with project portfolio view
- [ ] Analytics and reporting
- [ ] Integration with JIRA, Asana, Trello
- [ ] AI-powered project health monitoring

---

## Version History Summary

| Version | Date | Status | Key Feature |
|---------|------|--------|-------------|
| 2.0.0 | 2024-11-06 | ✅ Current | AI-enhanced structured workflow |
| 1.0.0 | 2024-11-06 | ⚠️ Legacy | Initial web interface |
| 0.2.0 | 2024-11-03 | 🗄️ Archived | CLI wizard |
| 0.1.0 | 2024-11-01 | 🗄️ Archived | Initial framework |

---

## Migration Notes

### Upgrading from v1.0 to v2.0
**Breaking Changes:**
- New multi-tab interface replaces single-form design
- Charter generation now template-based (not AI-generated)
- Different data collection workflow (2 tabs vs 1 form)

**Data Migration:**
- No automatic migration available
- Manually re-enter charter data through new workflow
- Export v1.0 charters before upgrading

**Benefits:**
- Elimination of AI hallucination
- Full manual control at every step
- Better PM methodology alignment
- Enhanced quality critique
- Professional output quality

### Running Both Versions
Both v1.0 and v2.0 can run simultaneously:
- v1.0: http://10.69.1.86:8501
- v2.0: http://10.69.1.86:8502

Recommendation: Use v2.0 for new projects, v1.0 for reference only.

---

## Deprecation Notices

### v1.0 (app_streamlit.py)
- **Status:** Maintained but not actively developed
- **Deprecation Date:** TBD (after v2.1 release)
- **End of Life:** Estimated Q1 2025
- **Migration Path:** Re-create charters in v2.0

### CLI Mode (0.2.0)
- **Status:** Archived, not maintained
- **Replacement:** Web interface (v1.0, v2.0)
- **Access:** Code available in git history

---

## Contributors

- **dollythedog** - Primary developer and product owner

## Changelog Conventions

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Vulnerability fixes
- **Technical Debt** - Known issues or cleanup needed
