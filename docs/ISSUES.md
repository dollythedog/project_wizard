# Project Issues & Tasks

**Project:** Project Wizard  
**Status:** Phase 2 Complete - Active Development  
**Last Updated:** 2025-11-04  
**Version:** 0.4.0  
**GitHub Repo:** https://github.com/dollythedog/project_wizard

---

## Active Issues

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
