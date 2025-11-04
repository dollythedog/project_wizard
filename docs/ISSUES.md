# Project Issues & Tasks

**Project:** Project Wizard  
**Status:** Phase 2 Complete - Active Development  
**Last Updated:** 2025-11-04  
**Version:** 0.3.0  
**GitHub Repo:** https://github.com/dollythedog/project_wizard

---

## Active Issues

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
