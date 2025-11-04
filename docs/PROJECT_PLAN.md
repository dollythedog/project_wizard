# Project Plan - Project Wizard

**Version:** 0.3.0  
**Last Updated:** 2025-11-04  
**Status:** Phase 2 Complete + Best Practices Integration

---

## Executive Summary

Project Wizard is a CLI tool that automates project initiation by guiding users through charter creation and generating professional documentation. 

**Current Status:** Phase 2 complete + Best practices integration! Planning wizard functional with AI-assisted workflow. Projects now include industry-standard documentation and code quality tools. Ready for Phase 3 (OpenProject Integration).

**Latest Updates (v0.3.0):**
- ✅ **Best Practices Integration complete**
- ✅ CONTRIBUTING.md, CODE_OF_CONDUCT.md, LICENSE.md auto-generated
- ✅ Centralized logging (data/logs/) with proper .gitignore
- ✅ Code quality enforcement (pyproject.toml with ruff config)
- ✅ PEP-8 compliance, complexity limits, and testing setup

---

## Technical Architecture

### Components

1. **CLI Interface** (`app/main.py`)
   - Click framework for command structure
   - Commands: `init`, `plan`, `sync`

2. **Charter Wizard** (`app/wizard/phase1_initiation.py`)
   - Interactive prompts with questionary
   - Rich console output
   - Captures 12+ charter fields

3. **Data Models** (`app/models/`)
   - Pydantic models for validation
   - CharterData, ProjectMetadata

4. **Document Generator** (`app/services/document_generator.py`)
   - Jinja2 template engine
   - Generates PROJECT_CHARTER.md, README.md

5. **Repository Bootstrapper** (`app/services/repo_bootstrapper.py`)
   - Creates standard folder structure
   - Git initialization

### Dependencies

- Python 3.8+
- click, jinja2, pydantic, requests
- rich, questionary (UI)
- gitpython

---

## Implementation Roadmap

### ✅ Phase 1: Initiation (Complete - Nov 3, 2025)

**Goal:** Interactive charter creation and document generation

**Deliverables:**
- [x] Charter wizard with Prompt 1 + 2 fields
- [x] PROJECT_CHARTER.md template
- [x] README.md generation
- [x] Repository structure creation
- [x] Git initialization
- [x] CLI framework
- [x] Makefile for workflows

**Outcome:** Working `project-wizard init` command

---

### ✅ Phase 2: Planning (Complete - Nov 3, 2025)

**Goal:** Work breakdown and PROJECT_PLAN.md generation

**Deliverables:**
- [x] Planning wizard (`project-wizard plan`)
- [x] PROJECT_PLAN.md template
- [x] ISSUES.md template
- [x] Milestone/task models (Pydantic)
- [x] Robust markdown parser
- [x] AI-assisted workflow

**Outcome:** Working planning wizard that generates actionable work breakdowns from AI-generated plans

**Actual Effort:** ~6 hours

---

### ✅ Phase 2.5: Best Practices Integration (Complete - Nov 4, 2025)

**Goal:** Integrate software development best practices into generated projects

**Deliverables:**
- [x] CONTRIBUTING.md template with PEP-8 and commit conventions
- [x] CODE_OF_CONDUCT.md template (Contributor Covenant v2.0)
- [x] LICENSE.md template (MIT License)
- [x] Centralized logging standards (data/logs/)
- [x] pyproject.toml with ruff configuration
- [x] Documentation standards (Google Style Guide links)
- [x] HIPAA compliance reminders for healthcare projects
- [x] Updated all project documentation

**Outcome:** All generated projects now include professional documentation, coding standards, and quality tooling out-of-the-box

**Actual Effort:** ~4 hours

---

### ⏳ Phase 3: OpenProject Integration (Week of Nov 11)

**Goal:** Sync projects to OpenProject via REST API

**Tasks:**
1. Port OpenProject client from patio-drainage-project
2. Implement `project-wizard sync --create`
3. Create work packages from ISSUES.md
4. Implement `project-wizard sync --update` (bidirectional)
5. Store OpenProject IDs in charter.json
6. Handle project types and work package types

**Deliverables:**
- [ ] OpenProject client service
- [ ] Sync command implementation
- [ ] Bidirectional ISSUES.md sync
- [ ] Error handling and retries

**Estimated Effort:** 10-14 hours

---

### ⏳ Phase 4: Deployment (Week of Nov 18)

**Goal:** Docker deployment alongside OpenProject

**Tasks:**
1. Create Dockerfile
2. Create docker-compose.yml
3. Test on Ubuntu home server
4. Document migration to Windows office server
5. Create deployment guide
6. Set up volume mounts for projects

**Deliverables:**
- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] Deployment documentation
- [ ] Windows deployment guide

**Estimated Effort:** 8-10 hours

---

## Testing Strategy

### Unit Tests
- Model validation (Pydantic)
- Document generation
- Template rendering

### Integration Tests
- End-to-end charter creation
- OpenProject API calls
- Git operations

### Manual Testing
- Create test projects for each type
- Verify generated documents
- Test OpenProject sync

---

## Deployment Plan

### Development Environment
- Local development on Ubuntu server
- `make dev` for development installation
- Manual testing with real projects

### Production Deployment

**Home Server (Ubuntu):**
```bash
cd /srv/project_wizard
docker-compose up -d
```

**Office Server (Windows):**
- Deploy with Docker Desktop
- Same docker-compose.yml
- Mount volumes for persistence

---

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenProject API changes | High | Pin to stable v3 API, monitor changelog |
| Template inflexibility | Medium | Support custom templates via config |
| Performance with large projects | Low | Batch operations, optimize queries |
| Windows Docker compatibility | Medium | Test thoroughly, document differences |

---

## Success Metrics

**Phase 1:**
- ✅ Charter wizard captures all 12+ fields
- ✅ Generates valid PROJECT_CHARTER.md
- ✅ Creates standard repository structure
- ✅ Git initialization successful

**Phase 2:**
- Work breakdown wizard completes in <5 minutes
- PROJECT_PLAN.md generated correctly
- ISSUES.md tracks all tasks

**Phase 3:**
- Successfully creates projects in OpenProject
- Work packages imported with parent-child relationships
- Bidirectional sync working

**Phase 4:**
- Docker container builds successfully
- Deploys on Ubuntu and Windows
- Migration guide clear and tested

---

## Next Actions

### Immediate (Ready to Start)

**Option A: Phase 2 - Planning Wizard** (4-6 hours)
1. Design planning wizard interface (questionary prompts)
2. Create WBS/milestone data model (Pydantic)
3. Implement PROJECT_PLAN.md Jinja2 template
4. Implement ISSUES.md generation
5. Add project type templates (YAML configs)

**Option B: Phase 3 - OpenProject Integration** (3-4 hours)
1. Port OpenProject client from meeting_exporter repo
2. Implement `project-wizard sync --create` command
3. Store OpenProject IDs in charter.json
4. Add basic error handling and retries

**Option C: Testing & Validation** (1-2 hours)
1. Use wizard for real project (Office Server Transition)
2. Add automated tests for Phase 1 functionality
3. Document any UX issues found
4. Fix hardcoded project_template path

### Recommended Next Step

**Start with Option C (Testing)**, then choose between Phase 2 or Phase 3 based on priority:
- Choose Phase 2 if you want complete project planning automation
- Choose Phase 3 if you need OpenProject integration for current projects

---

*Last updated: 2025-11-03*
