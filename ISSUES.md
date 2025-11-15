# Issues & Enhancements

Track issues for both **Project Wizard** (this tool) and **projects created by it**.

**Current Version:** 2.7.0  
**Last Updated:** 2025-11-15

---

## 🎯 Active Issues

### Medium Priority

**#3: Inconsistent Entry Point**  
**Status:** 🟡 Ready to Fix  
**Priority:** Medium  
**Component:** Configuration

**Description:**  
- Main app is now `app.py` but some documentation may reference old files
- Ensure all references are consistent

**Solution:**
- Audit all documentation for old app references
- Update any remaining inconsistencies

---

### Low Priority

**#4: Pattern Content Library Not Fully Integrated**  
**Status:** 🔵 Planned  
**Priority:** Low  
**Component:** Patterns

**Description:**  
The `proposal` pattern has a `content_library.json` for reusable input snippets, but this isn't exposed in the UI or extended to other patterns.

**Potential Enhancement:**
- Add "Input Library" tab to manage reusable content across patterns
- Allow users to save common inputs (e.g., boilerplate problem statements)
- Share library across all patterns

---

## ✅ Recently Resolved Issues

### v2.7.0 (2025-11-15)

✅ **OpenProject Integration (High Priority)**  
**Resolved:** 2025-11-15  
**Component:** Integration / Deliverables

**Description:**  
Added seamless integration with OpenProject to export WORK_PLAN.md files as structured work packages.

**Implementation:**
- Created `OpenProjectExporter` service with RESTful API integration
- Added one-click export button in Deliverables tab
- Parses work plan structure (phases, tasks, metadata)
- Creates hierarchical work packages (phases as parents, tasks as children)
- Converts durations to estimated hours
- Secure credential management via environment variables

**Files:**
- Added: `app/services/openproject_exporter.py`
- Modified: `app/ui/tabs/deliverables_tab.py`
- Documentation: `docs/OPENPROJECT_INTEGRATION.md`, `.env.example`

---

✅ **Kanban Board View for Issues (Critical)**  
- **Fixed in:** v2.7.0 - Phase 1 Complete
- **Solution:** Implemented full Kanban board with:
  - Visual columns: Backlog, In Progress, Review, Done
  - Issue parser to read ISSUES.md
  - Issue manager service
  - Project filter dropdown
  - Priority and status indicators
  - Expandable issue details
- **Files Created:**
  - `app/models/issue.py` - Issue data model
  - `app/parsers/issues_parser.py` - ISSUES.md parser
  - `app/services/issue_manager.py` - Issue management service
  - `app/ui/tabs/issues_tab.py` - Kanban board UI
- **Impact:** Issues are now visually trackable in the app!

✅ **Repository Clutter - Too Many Loose Files**  
- **Fixed in:** v2.7.0
- **Solution:** 
  - Moved feature completion docs to `docs/archive/completed_features/`
  - Moved backup files to `docs/archive/backups/`
  - Updated Makefile to use `app.py`
  - Cleaned root directory to only essential docs
- **Result:** Clean, organized repository structure

### v2.6.0 (2025-11-14)

✅ **Monolithic Codebase Hard to Maintain**  
- **Fixed in:** v2.6.0
- **Solution:** Refactored into modular architecture with tabs, components, services
- **Impact:** Much easier to add features and maintain code

✅ **Difficult to Track Multiple Projects**  
- **Fixed in:** v2.5.1
- **Solution:** Added ProjectRegistry and visual gallery
- **Files:** `app/services/project_registry.py`

### v2.5.3 (2025-11-14)

✅ **Project Charter Generated Without User Inputs (Critical)**  
- **Fixed in:** v2.5.3
- **Root Cause:** Template expected variable substitution but AI pipeline provided free-form content
- **Solution:** Simplified `patterns/project_charter/template.md.j2` to wrap `{{ content }}`
- **Files Modified:**
  - `patterns/project_charter/template.md.j2`
  - `patterns/project_charter/system.md`

✅ **Cannot Recreate Existing Charter - Wizard Shows Empty Fields**  
- **Fixed in:** v2.5.3
- **Root Cause:** Wizard didn't pre-populate from existing charter
- **Solution:** Added `parse_charter_to_form_data()` logic

### v2.5.2 (2025-11-13)

✅ **AI Enhancements Not Applying to Deliverables**  
- **Fixed in:** v2.5.2
- **Root Cause:** Full documents sent to LLM, session state reloaded from disk
- **Solution:** Chunked processing (~1000 chars), session state persistence
- **Files Modified:**
  - `app/services/ai_agents/charter_agent.py` - Added `enhance_large_document()`
  - `app/components/document_editor.py` - Session state sync

✅ **Charter Critique Results Not Displaying**  
- **Fixed in:** v2.5.2
- **Solution:** Improved error handling and UI feedback

### v2.5.1 (2025-11-12)

✅ **Non-Functional Recent Projects Sidebar**  
- **Fixed in:** v2.5.1
- **Solution:** Introduced ProjectRegistry service

### v2.0.0 (2025-11-10)

✅ **AI Critique Showing 0% Score**  
- **Fixed in:** v2.0.0
- **Root Cause:** Mismatched field names between critique and rubric

✅ **OpenAI API Key Not Found Error**  
- **Fixed in:** v2.0.0
- **Solution:** Added `dotenv` support, load `.env` file at startup

✅ **AI Hallucinating Metrics in Generated Documents**  
- **Fixed in:** v2.0.0
- **Solution:** Structured prompts, lower temperature, template-based generation

---

## 🚀 Enhancement Backlog

### Planned for v2.7.1

1. **Issue Management** - Create, edit, delete issues from UI
2. **Status Updates** - Move issues between columns
3. **README Tab** - Display project README on welcome screen

### Future Enhancements (v2.8.0+)

4. **GitHub Integration**
   - Auto-sync ISSUES.md with GitHub Issues
   - Create GitHub repo from Project Wizard

5. **Custom Pattern Creation UI**
   - Visual editor for creating new patterns

6. **Session Persistence**
   - Save/resume work sessions

7. **Drag-and-Drop Status Updates**
   - Move issues between columns with drag-and-drop

8. **Multi-Project Issue Tracking**
   - Track issues across all created projects

---

## 📋 Known Limitations

### Current Version (2.7.0)

- **L1: Read-Only Issues** - Can view but not edit issues yet (v2.7.1)
- **L2: No Session Persistence** - Work lost on browser refresh (v2.8.0)
- **L3: Single User Only** - No multi-user support yet (v2.8.0)
- **L4: No Git Integration** - Must use command line for version control

---

## 📊 Issue Statistics

**Total Issues:** 2 active, 12 resolved  
**By Priority:** 0 High, 1 Medium, 1 Low  
**By Status:** 0 Planned, 0 In Progress, 1 Ready to Fix, 1 Future  

**Resolution Rate:** 86% (12 resolved / 14 total)  
**Recent Velocity:** 2 issues resolved in v2.7.0

---

**Legend:**
- 🔵 Planned - Scheduled for implementation
- 🟢 In Progress - Actively being worked on
- 🟡 Ready to Fix - Understood, ready for implementation
- 🔴 Blocked - Waiting on dependencies
- ✅ Resolved - Fixed and deployed
