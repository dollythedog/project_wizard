# Project Plan - Project Wizard

**Version:** 0.1.0  
**Last Updated:** 2025-11-03  
**Status:** Phase 1 Complete

---

## Executive Summary

Project Wizard is a CLI tool that automates project initiation by guiding users through charter creation and generating professional documentation. Phase 1 (charter wizard) is complete. Phases 2-4 will add planning, OpenProject integration, and deployment capabilities.

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

### ⏳ Phase 2: Planning (Week of Nov 4)

**Goal:** Work breakdown and PROJECT_PLAN.md generation

**Tasks:**
1. Design planning wizard interface
2. Create work breakdown structure (WBS) model
3. Implement milestone templates from Prompt 3
4. Generate PROJECT_PLAN.md
5. Generate ISSUES.md with task list
6. Add project type templates (YAML)

**Deliverables:**
- [ ] Planning wizard (`project-wizard plan`)
- [ ] PROJECT_PLAN.md template
- [ ] ISSUES.md template
- [ ] YAML project type configs
- [ ] Milestone/task models

**Estimated Effort:** 12-16 hours

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

1. Test Phase 1 with real project
2. Design Phase 2 planning wizard interface
3. Create milestone template structure
4. Begin OpenProject client integration

---

*Last updated: 2025-11-03*
