# Project Issues & Tasks

**Project:** Project Wizard  
**Status:** Active Development  
**Last Updated:** 2025-11-03

---

## Active Issues

### Phase 2: Planning Wizard

**Issue #1: Design Planning Wizard Interface**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Create interactive wizard for Phase 2 (work breakdown)
- **Tasks:**
  - [ ] Design questionary prompts for milestone entry
  - [ ] Create WBS data model
  - [ ] Add task dependency tracking
  - [ ] Implement duration estimation

**Issue #2: Generate PROJECT_PLAN.md**
- **Status:** Open
- **Priority:** High  
- **Assignee:** Jonathan Ives
- **Description:** Create Jinja2 template for project plan generation
- **Tasks:**
  - [ ] Design PROJECT_PLAN.md template
  - [ ] Add work breakdown section
  - [ ] Include Gantt chart data
  - [ ] Add resource allocation

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

**Issue #5: Port OpenProject Client**
- **Status:** Open
- **Priority:** High
- **Assignee:** Jonathan Ives
- **Description:** Adapt patio-drainage import script into reusable service
- **Tasks:**
  - [ ] Copy OpenProjectImporter class
  - [ ] Refactor into app/services/openproject_client.py
  - [ ] Add error handling
  - [ ] Add retry logic

**Issue #6: Implement Sync Command**
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
