# Project Issues & Tasks

**Project:** Project Wizard  
**Status:** Phase 2 Complete - Active Development  
**Last Updated:** 2025-11-04  
**Version:** 0.4.2  
**GitHub Repo:** https://github.com/dollythedog/project_wizard

---

## Active Issues

### Phase 2.8: Planning Wizard UX Improvements

**Issue #35: AI Prompt Generator**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Generate pre-formed AI prompt instead of vague instructions
- **Completed Tasks:**
  - [x] Create _generate_ai_prompt() function
  - [x] Include charter summary automatically
  - [x] Add formatting requirements and examples
  - [x] Add instruction for AI to ask clarifying questions
  - [x] Follow user rule: "answer questions when asked so I understand assumptions"
  - [x] Update wizard flow: show prompt → wait → paste response
  - [x] Test with questionary.press_any_key_to_continue()
  - [x] Update README and CHANGELOG

**Issue #36: Test AI Prompt Generator with Kindred Contract**
- **Status:** Complete (2025-11-04) ✅ 85% PASSING (22/26)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Validate AI prompt generator with real project
- **Test Project:** Kindred Contract (Healthcare LTAC contract negotiation)
- **Test Results:**
  1. **Prompt Generation (7/7 ✅):**
     - [x] Displays charter summary (goal, timeline, deliverables, risks)
     - [x] Shows clear formatting requirements (PHASE/Issue/bullet)
     - [x] Includes instruction: "Ask 3-5 clarifying questions"
     - [x] Includes instruction: "Answer your own questions" (user rule)
     - [x] Provides complete format example
     - [x] Mentions Critical Path and Dependencies sections
     - [x] Prompt is copy-friendly (no Rich markup in text)
  2. **User Workflow (4/4 ✅):**
     - [x] User can easily copy entire prompt
     - [x] "Press any key" pause works correctly
     - [x] Paste area accepts multi-line input
     - [x] Parser handles AI response correctly
  3. **Output Quality (6/6 ✅):**
     - [x] PROJECT_PLAN.md tasks on separate lines (not run together) - **FIXED v0.4.2**
     - [x] Duration fields correctly parsed (or empty if no duration)
     - [x] No parenthetical clarifications extracted as durations
     - [x] Dependencies filtered from task list - **FIXED v0.4.2** (156 tasks vs 162)
     - [x] Critical path items identified (in AI output, not yet extracted to separate section)
     - [x] ISSUES.md properly formatted with checkboxes
  4. **Phase Progression (4/6 ⚠️):**
     - [x] Initiation marked complete
     - [x] RfP gate approved
     - [x] Planning phase started and completed
     - [x] RfE gate approved
     - [ ] Phase state advances to Execution (advances correctly, but...)
     - [ ] Quest map shows correct progress - ❌ Shows 90% (should be ~50%) → Issue #33
  5. **HIPAA Detection (1/2 ⚠️):**
     - [ ] Charter includes HIPAA warning section - ❌ Only runs during init, not retroactive
     - [x] Warning mentions PHI, encryption, BAAs (when present)
- **Success Criteria:** 22/26 criteria met (85% pass rate)
  - Generated plan is professional quality ✅
  - User experience smooth and clear ✅
  - Critical bugs resolved (line breaks, dependency filtering) ✅
- **Test Dates:** 
  - First run: 2025-11-04 (65% pass - 17/26)
  - Second run: 2025-11-04 (85% pass - 22/26)
- **Improvements:**
  - +5 tasks resolved (line breaks, dependency filtering)
  - 20 percentage point improvement
- **Remaining Issues:** See #33 (progress calculation)

---

### Phase 2.7: Planning Parser Quality Fixes (v0.4.2)

**Issue #29: Fix Task Formatting in PROJECT_PLAN.md**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Tasks run together without line breaks making document unreadable
- **Root Cause:** PROJECT_PLAN.md.j2 template missing blank line after each task in loop
- **Solution:** Added blank line after task in Jinja2 template (line 34)
- **Completed Tasks:**
  - [x] Update PROJECT_PLAN.md.j2 template to add blank line between tasks
  - [x] Test with multi-task milestones (Kindred Contract - 7 phases, 156 tasks)
  - [x] Verify GitHub/editor checkbox compatibility

**Issue #30: Fix Duration Parsing Logic**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Parser extracts parenthetical clarifications as task durations
- **Examples:**
  - "Calculate staffing costs (5 days APP, 2 days physician)" → Duration: "5 days APP, 2 days physician"
  - "Evaluate platforms (e.g., Zoom Healthcare)" → Duration: "e.g., Zoom Healthcare"
- **Root Cause:** Regex/parser treats all parentheses content as duration
- **Tasks:**
  - [ ] Review parser logic in phase2_planning.py
  - [ ] Only extract duration if format matches time patterns (e.g., "2 days", "3 hours")
  - [ ] Keep clarifications as part of task description
  - [ ] Add unit tests for duration parsing

**Issue #31: Separate Dependencies from Tasks**
- **Status:** Partially Complete (2025-11-04)
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Dependencies incorrectly parsed as tasks in Phase 7
- **Root Cause:** Parser treated "Phase X depends on Phase Y" statements as tasks
- **Solution:** Added skip keywords to parser: 'depends on', 'requires', 'must complete'
- **Completed Tasks:**
  - [x] Update parser to detect dependency language (phase2_planning.py line 293)
  - [x] Filter dependencies from task count (verified: 156 tasks vs 162 before fix)
  - [ ] Add Dependencies section to PROJECT_PLAN.md.j2 template (future)
  - [ ] Extract dependencies into separate list in data model (future)
  - [ ] Add dependency visualization to plan (future)
- **Impact:** Task count now accurate, but dependencies not yet extracted to separate section

**Issue #32: Add Critical Path Section**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Critical path items from AI output not captured in plan
- **Tasks:**
  - [ ] Add Critical Path section to PROJECT_PLAN.md.j2
  - [ ] Update parser to detect critical path items
  - [ ] Highlight blocking tasks in ISSUES.md
  - [ ] Add visual indicator for critical path in quest map

**Issue #33: Improve Progress Calculation**
- **Status:** Open
- **Priority:** Medium (upgraded from Low)
- **Assignee:** Jonathan Ives
- **Description:** Progress shows 90% when only charter+plan complete (should be ~50%)
- **Current Behavior:** After completing Planning phase, shows 90% progress
- **Expected Behavior:** Should show ~50% (Initiation=25%, Planning=25%, Execution and Closure not started)
- **Current Logic:** Gives partial credit for starting a phase
- **Proposed Fix:** Only credit completed phases, not started ones
- **Test Results:**
  - First test: Showed 70% (incorrect)
  - Second test: Showed 90% (worse - regressed)
  - Should show: ~50%
- **Tasks:**
  - [ ] Review PhaseState.get_progress_percentage() method in app/models/phase_state.py
  - [ ] Remove partial credit for started_at without completed_at
  - [ ] Use formula: (completed_phases / total_phases) * 100
  - [ ] Update tests
- **Priority Upgrade Reason:** Regression from 70% to 90% makes this more critical

**Issue #34: Add Deadline Warning**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** No warning when charter deadline is imminent
- **Example:** User's deadline was 11/5/2025 (1 day away), no warning shown
- **Tasks:**
  - [ ] Parse schedule_overview for deadline dates
  - [ ] Calculate days until deadline
  - [ ] Display warning if < 3 days away
  - [ ] Suggest adjusting timeline in wizard output

---

### Phase 2.6: Post-Release Fixes & Improvements

**Issue #25: Charter Template Field Mapping**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Fix inverted field mappings in charter template
- **Completed Tasks:**
  - [x] Reorganize sections 2-5 for logical flow
  - [x] Remove duplicate strategic_alignment
  - [x] Fix section numbering (now 1-13)
  - [x] Test with real project data

**Issue #26: Missing Documentation Templates**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Create templates for referenced but missing docs
- **Completed Tasks:**
  - [x] Create CHANGELOG.md.j2 template
  - [x] Create QUICKSTART.md.j2 template
  - [x] Add generate_changelog() method
  - [x] Add generate_quickstart() method
  - [x] Update main.py to generate both files
  - [x] Update README template references

**Issue #27: HIPAA Compliance Detection**
- **Status:** Complete (2025-11-04)
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Auto-detect healthcare projects and add HIPAA warnings
- **Completed Tasks:**
  - [x] Add keyword detection in charter template
  - [x] Create HIPAA warning section with checklist
  - [x] Add links to HHS resources
  - [x] Test with healthcare project

**Issue #28: CLI Installation Fix**
- **Status:** Complete (2025-11-04)
- **Priority:** Critical
- **Assignee:** Jonathan Ives
- **Description:** Fix project-wizard command not found error
- **Completed Tasks:**
  - [x] Add [project.scripts] section to pyproject.toml
  - [x] Add dependencies list
  - [x] Update version to 0.4.0
  - [x] Reinstall and verify CLI works

---

### Phase 2.5: RPG Framework Testing & Verification

**Issue #19: Test RPG Framework - New Project Flow**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Verify complete new project initialization with phase tracking
- **Expected Behavior:**
  1. Run `project-wizard init` with test project
  2. Charter wizard completes successfully
  3. Phase state initialized with Initiation phase started
  4. `data/inbox/phase_state.json` created
  5. Quest map displayed showing:
     - Project in Initiation phase
     - Progress: ~12% (started but not complete)
     - RfP gate status: NOT_REACHED
     - Current quest: "The Call to Adventure"
  6. Project files created successfully
- **Tasks:**
  - [ ] Create test project: "RPG Framework Test"
  - [ ] Verify phase_state.json exists and is valid JSON
  - [ ] Verify phase_state.json contains correct project_title
  - [ ] Verify initiation.started_at is set
  - [ ] Verify initiation.artifacts includes charter and README
  - [ ] Verify quest map renders without errors
  - [ ] Screenshot quest map output

**Issue #20: Test RPG Framework - Planning Flow**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Verify planning wizard advances phases correctly
- **Expected Behavior:**
  1. From test project directory, run `project-wizard plan`
  2. Phase state loads successfully
  3. Planning wizard completes
  4. Phase state updated:
     - Initiation phase marked complete
     - RfP gate approved
     - Advanced to Planning phase
     - Planning artifacts added
  5. Updated quest map displayed showing:
     - Checkmark on Initiation
     - Current position: Planning
     - Progress: ~37% (completed Init, started Planning)
     - RfP gate: APPROVED (green diamond)
     - RfE gate: NOT_REACHED
     - Current quest: "The Strategist's Forge"
- **Tasks:**
  - [ ] Run planning wizard on test project
  - [ ] Verify phase_state.json updated correctly
  - [ ] Verify initiation.completed_at is set
  - [ ] Verify rfp_status = APPROVED
  - [ ] Verify rfp_approved_at timestamp
  - [ ] Verify current_phase = planning
  - [ ] Verify planning.started_at is set
  - [ ] Verify planning.artifacts includes plan and issues
  - [ ] Screenshot updated quest map

**Issue #21: Test RPG Framework - Status Command**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Verify status command displays quest map correctly
- **Expected Behavior:**
  1. From test project, run `project-wizard status`
  2. Quest map displays with all components:
     - Header with project name and progress
     - Phase flow with icons and arrows
     - Current position indicator ("YOU ARE HERE")
     - Gate approval diamonds
     - Next steps panel
  3. Run `project-wizard status -d` for detailed view
  4. Chapter Details table displays with all 4 phases
- **Tasks:**
  - [ ] Test status command from project root
  - [ ] Test status command from subdirectory (should work)
  - [ ] Test status -d (detailed) flag
  - [ ] Verify all emojis render correctly
  - [ ] Verify colors display properly
  - [ ] Test status in non-project directory (should error gracefully)
  - [ ] Screenshot standard and detailed views

**Issue #22: Test RPG Framework - Data Persistence**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Verify phase state persists correctly across sessions
- **Expected Behavior:**
  1. Create project, advance through phases
  2. Exit terminal completely
  3. Reopen terminal, cd to project
  4. Run `project-wizard status`
  5. Phase state loads from JSON correctly
  6. All progress, gates, artifacts preserved
- **Tasks:**
  - [ ] Test state persistence after closing terminal
  - [ ] Test state persistence after system reboot
  - [ ] Verify datetime fields parse correctly
  - [ ] Test with corrupted phase_state.json (error handling)
  - [ ] Test with missing phase_state.json (graceful fallback)

**Issue #23: Code Quality - Lint RPG Framework Code**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Run linting on new RPG framework modules
- **Completed Tasks:**
  - [x] Run `make lint` on phase_state.py
  - [x] Run `make lint` on phase_manager.py
  - [x] Run `make lint` on phase_navigator.py
  - [x] Fix all linting errors
  - [x] Verify all code passes PEP-8 checks

**Issue #24: Documentation - Verify RPG Framework Docs**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Review and verify all RPG framework documentation
- **Tasks:**
  - [ ] Review RPG_FRAMEWORK_GUIDE.md for accuracy
  - [ ] Review RPG_IMPLEMENTATION_SUMMARY.md
  - [ ] Verify README.md RPG section
  - [ ] Verify CHANGELOG.md v0.4.0 entries
  - [ ] Check for broken links
  - [ ] Verify code examples work

---

### Phase 1: Foundation Fixes

**Issue #14: Fix Utility Script Copying**
- **Status:** Complete (2025-11-03)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Copy standard utility modules from project_template to generated projects
- **Completed Tasks:**
  - [x] Add shutil import to repo_bootstrapper
  - [x] Create _copy_utility_scripts method
  - [x] Copy config_loader.py, db_utils.py, email_utils.py, log_utils.py, time_utils.py
  - [x] Add console feedback for copied utilities

**Issue #15: Fix Windows UTF-8 Encoding**
- **Status:** Complete (2025-11-03)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Fix charmap codec errors when generating documents with emojis on Windows
- **Completed Tasks:**
  - [x] Add encoding='utf-8' to document_generator.py (lines 34, 83)
  - [x] Add encoding='utf-8' to main.py charter JSON write (line 107)
  - [x] Test with emoji characters in templates

**Issue #16: Improve Charter Template**
- **Status:** Complete (2025-11-03)
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Fix template field mappings and section numbering issues
- **Completed Tasks:**
  - [x] Fix selection criteria 'done' value filtering
  - [x] Correct section numbering (9-12)
  - [x] Move Major Obstacles into Risks section
  - [x] Reorganize Collaboration Needs placement

**Issue #17: Add Code Linting and Quality Checks**
- **Status:** Complete (2025-11-03)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Implement automated code quality checking with ruff linter
- **Completed Tasks:**
  - [x] Run ruff check and identify 17 errors
  - [x] Auto-fix 15 errors (unused imports, unnecessary f-strings)
  - [x] Manually fix 2 bare except clauses
  - [x] Add make lint and make lint-fix commands
  - [x] Verify all checks pass

**Issue #18: Integrate Software Development Best Practices**
- **Status:** Complete (2025-11-04)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Incorporate industry-standard best practices into project generation
- **Completed Tasks:**
  - [x] Create CONTRIBUTING.md template with PEP-8 and commit conventions
  - [x] Create CODE_OF_CONDUCT.md template (Contributor Covenant)
  - [x] Create LICENSE.md template (MIT License)
  - [x] Add data/logs/ folder to project structure
  - [x] Update .gitignore for centralized logging
  - [x] Add pyproject.toml with ruff configuration and complexity limits
  - [x] Update DocumentGenerator to generate new files
  - [x] Update main.py to call new generators during init
  - [x] Update README template with links to new docs
  - [x] Update CHANGELOG, ISSUES, README, WARP documentation

---

### Phase 2: Planning Wizard ✅

**Issue #1: Design Planning Wizard Interface** ([GitHub #1](https://github.com/dollythedog/project_wizard/issues/1))
- **Status:** Complete (2025-11-03)
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Create interactive wizard for Phase 2 (work breakdown)
- **Completed Tasks:**
  - [x] Create AI-assisted paste workflow
  - [x] Create WBS data model (Pydantic)
  - [x] Implement robust markdown parser
  - [x] Add error handling and validation

**Issue #2: Generate PROJECT_PLAN.md** ([GitHub #2](https://github.com/dollythedog/project_wizard/issues/2))
- **Status:** Complete (2025-11-03)
- **Priority:** High  
- **Assignee:** Jonathan Ives
- **Description:** Create Jinja2 template for project plan generation
- **Completed Tasks:**
  - [x] Design PROJECT_PLAN.md template
  - [x] Add work breakdown section with phases/milestones
  - [x] Include task lists with durations
  - [x] Add ISSUES.md template for task tracking

**Issue #3: Generate ISSUES.md Template**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Auto-generate ISSUES.md from milestone data
- **Tasks:**
  - [ ] Create ISSUES.md Jinja2 template
  - [ ] Map milestones to GitHub-style issues
  - [ ] Add status tracking
  - [ ] Include OpenProject ID field

**Issue #4: Create Project Type Templates**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** YAML configs for common project types
- **Tasks:**
  - [ ] software_mvp.yaml
  - [ ] clinical_workflow.yaml
  - [ ] infrastructure.yaml
  - [ ] landscaping.yaml

---

### Phase 3: OpenProject Integration

**Issue #5: Port OpenProject Client** ([GitHub #3](https://github.com/dollythedog/project_wizard/issues/3))
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Adapt patio-drainage import script into reusable service
- **Tasks:**
  - [ ] Copy OpenProjectImporter class
  - [ ] Refactor into app/services/openproject_client.py
  - [ ] Add error handling
  - [ ] Add retry logic

**Issue #6: Implement Sync Command** ([GitHub #4](https://github.com/dollythedog/project_wizard/issues/4))
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Create `project-wizard sync` command
- **Tasks:**
  - [ ] Implement `sync --create` (local → OpenProject)
  - [ ] Implement `sync --update` (bidirectional)
  - [ ] Store OpenProject IDs in charter.json
  - [ ] Handle conflicts

**Issue #7: ISSUES.md ↔ OpenProject Sync**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Bidirectional sync between local markdown and OpenProject
- **Tasks:**
  - [ ] Parse ISSUES.md into work packages
  - [ ] Fetch OpenProject work package status
  - [ ] Update ISSUES.md with status changes
  - [ ] Handle additions/deletions

---

### Phase 4: Deployment

**Issue #8: Docker Containerization**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Create Docker deployment
- **Tasks:**
  - [ ] Write Dockerfile (Python 3.12 base)
  - [ ] Create docker-compose.yml
  - [ ] Configure volume mounts
  - [ ] Test on Ubuntu

**Issue #9: Windows Deployment**
- **Status:** Open
- **Priority:** Medium
- **Assignee:** Jonathan Ives
- **Description:** Deploy on office Windows server
- **Tasks:**
  - [ ] Test Docker Desktop for Windows
  - [ ] Document Windows-specific config
  - [ ] Test migration process
  - [ ] Create deployment guide

---

## Completed Issues

### Phase 1: Initiation ✅

**Issue #10: Charter Wizard Implementation** ✅
- **Status:** Complete (2025-11-03)
- **Assignee:** Jonathan Ives
- **Description:** Interactive CLI for charter creation
- **Completed Tasks:**
  - [x] Implement questionary-based wizard
  - [x] Capture Prompt 1 + 2 fields
  - [x] Add Pydantic validation
  - [x] Rich console output

**Issue #11: Document Generation** ✅
- **Status:** Complete (2025-11-03)
- **Assignee:** Jonathan Ives
- **Description:** Generate PROJECT_CHARTER.md and README.md
- **Completed Tasks:**
  - [x] Create Jinja2 templates
  - [x] Implement DocumentGenerator service
  - [x] Generate PROJECT_CHARTER.md
  - [x] Generate README.md

**Issue #12: Repository Bootstrapping** ✅
- **Status:** Complete (2025-11-03)
- **Assignee:** Jonathan Ives
- **Description:** Create standard project structure
- **Completed Tasks:**
  - [x] Implement RepoBootstrapper
  - [x] Create folder structure (configs, data, scripts, docs)
  - [x] Generate .gitignore
  - [x] Initialize git repository

**Issue #13: CLI Framework** ✅
- **Status:** Complete (2025-11-03)
- **Assignee:** Jonathan Ives
- **Description:** CLI with Click
- **Completed Tasks:**
  - [x] Implement `project-wizard init`
  - [x] Add stub commands (plan, sync)
  - [x] Create setup.py
  - [x] Add Makefile

---

## Issue Labels

- **Priority:** High, Medium, Low
- **Type:** Feature, Bug, Enhancement, Documentation
- **Phase:** Phase-1, Phase-2, Phase-3, Phase-4
- **Status:** Open, In Progress, Complete, Blocked

---

## GitHub Integration (Future)

Once pushed to GitHub, sync these issues using:
```bash
gh issue create --title "Issue Title" --body "Description" --label "Phase-2"
```

Or use GitHub CLI to import from this file.

---

*This file will be kept in sync with OpenProject once Phase 3 is complete*
