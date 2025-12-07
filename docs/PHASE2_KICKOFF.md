# Phase 2: FastAPI Foundation & Database - Kickoff

**Date:** 2025-12-01  
**Status:** Phase 1 Complete ✅ | Phase 2 Starting  
**Goal for Today:** Generate a project charter through web UI

---

## Current State

### ✅ Phase 1 Complete (2025-11-30)
- Blueprint system fully operational (3 templates: project_charter, work_plan, proposal)
- Blueprint registry service with caching
- CLI template management commands
- 14/14 integration tests passing
- Comprehensive documentation (BLUEPRINT_SCHEMA.md, PHASE1_COMPLETION.md)

**Key Achievement:** Infrastructure ready for AI agents to USE blueprints and prompts

---

## Phase 2 Overview

### Strategic Direction Change

**Original Plan (v0.3.0):** CLI-first with optional web UI later  
**New Plan (v3.0.0):** **Web-first** with FastAPI + HTMX as primary interface

**Rationale:**
The v3.0 AI agent workflow is inherently conversational:
- Step-back prompting: AI asks clarifying questions → user answers
- Draft generation: Show progress, allow inline editing
- Verification: Present questions, collect feedback, show improvements
- Memory: Display lessons learned, apply to new generations

This workflow is **much better in a web browser** than in a CLI.

---

## Phase 2 Architecture

### Technology Stack
- **Backend:** FastAPI (Python)
- **Frontend:** HTMX + Jinja2 templates (server-rendered, minimal JS)
- **Database:** SQLite with SQLModel ORM
- **AI:** OpenAI API (GPT-4)
- **Migrations:** Alembic

### System Components

```
FastAPI Web App (http://localhost:8000)
    ├── Routes
    │   ├── /projects (list, create, detail)
    │   ├── /generate (template selection, document workflow)
    │   └── /api (HTMX endpoints)
    ├── Services
    │   ├── BlueprintRegistry (already built ✅)
    │   ├── ProjectRegistry (new - SQLModel)
    │   ├── ContextBuilder (new - aggregate project context)
    │   ├── LLMClient (new - OpenAI integration)
    │   └── AI Agents
    │       ├── StepBackAgent
    │       ├── DraftAgent
    │       ├── VerifierAgent
    │       └── MemoryAgent
    └── Database (SQLite)
        ├── projects
        ├── project_notes
        ├── supporting_files
        ├── document_runs
        └── memory_entries
```

---

## Phase 2 Sprint Breakdown

### Sprint 2.1: FastAPI Application Setup (3-4 days) ⬅️ **WE ARE HERE**
**Goal:** Get basic web app running with project management

**Tasks:**
1. **FastAPI structure** (2-3 hours)
   - `web/` directory with `app.py`, `routes/`, `static/`, `templates/`
   - HTMX integration setup
   - Jinja2 configuration
   - Base HTML layout

2. **Database setup** (2-3 hours)
   - SQLModel schema design
   - Database initialization
   - Basic CRUD operations

3. **Project management UI** (3-4 hours)
   - Project list page
   - Create project form
   - Project detail view
   - Notes/files management

4. **Basic styling** (1-2 hours)
   - Simple, clean CSS
   - Responsive layout
   - HTMX loading states

**Success Criteria:**
- [ ] Web app runs at http://localhost:8000
- [ ] Can create projects via UI
- [ ] Can add notes and files to projects
- [ ] Projects stored in SQLite database

---

### Sprint 2.2: AI Agent Services Foundation (4-5 days)
**Goal:** Build core AI services

**Tasks:**
1. **LLMClient service** - OpenAI API integration
2. **ContextBuilder service** - Aggregate project context
3. **StepBackAgent** - Generate clarifying questions
4. **DraftAgent (basic)** - Section-by-section generation

**Success Criteria:**
- [ ] Can call OpenAI API successfully
- [ ] Can build context from project data
- [ ] StepBackAgent generates questions
- [ ] DraftAgent generates basic charter sections

---

### Sprint 2.3: Document Generation UI (4-5 days)
**Goal:** Complete document generation workflow

**Tasks:**
1. **Template selector page**
2. **Step-back prompting interface** (chat-like)
3. **Draft display** (markdown rendering)
4. **Input collection** (dynamic forms from blueprint)

**Success Criteria:**
- [ ] Can select project_charter template
- [ ] Can answer step-back questions in UI
- [ ] Can generate draft charter
- [ ] Draft displays nicely with markdown

---

### Sprint 2.4: Verification & Refinement (4-5 days)
**Goal:** Complete the verification loop

**Tasks:**
1. **VerifierAgent** - Generate verification questions
2. **Verification UI** - Display questions, collect answers
3. **Refinement workflow** - Show before/after comparison
4. **Document export** - Download final markdown

**Success Criteria:**
- [ ] Verifier identifies gaps in draft
- [ ] User can answer verification questions
- [ ] Refined draft shows improvements
- [ ] Can download PROJECT_CHARTER.md

---

## Today's Goal: Sprint 2.1 Foundation

**Objective:** By end of session, have:
1. FastAPI app structure created
2. Basic database schema defined
3. Simple project list/create UI working
4. Database initialized with SQLite

**Why This Matters:**
Once we have the web foundation, everything else (AI agents, document generation, verification) can be built incrementally on top of it.

---

## File Structure (After Sprint 2.1)

```
project_wizard/
├── web/                          # NEW
│   ├── app.py                    # FastAPI application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── projects.py           # Project CRUD routes
│   │   └── generate.py           # Document generation routes (later)
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── projects/
│   │   │   ├── list.html
│   │   │   ├── create.html
│   │   │   └── detail.html
│   │   └── partials/             # HTMX partial templates
│   └── static/
│       ├── css/
│       │   └── main.css
│       └── js/
│           └── htmx.min.js       # Downloaded from CDN
├── app/
│   ├── models/
│   │   ├── blueprint.py          # Existing ✅
│   │   └── database.py           # NEW - SQLModel models
│   ├── services/
│   │   ├── blueprint_registry.py # Existing ✅
│   │   ├── project_registry.py   # NEW - Database operations
│   │   ├── context_builder.py    # NEW (Sprint 2.2)
│   │   ├── llm_client.py         # NEW (Sprint 2.2)
│   │   └── ai_agents/            # NEW (Sprint 2.2+)
│   └── ...
├── data/
│   └── project_wizard.db         # NEW - SQLite database
├── patterns/                      # Existing ✅
│   ├── project_charter/
│   ├── work_plan/
│   └── proposal/
├── tests/
│   └── test_web/                 # NEW - Web app tests
└── requirements.txt               # Update with FastAPI, etc.
```

---

## Immediate Next Steps

1. **Review and confirm understanding** ✅ (this document)
2. **Create FastAPI app structure**
3. **Design SQLModel schema**
4. **Build project list/create UI**
5. **Test end-to-end: create project via web UI**

---

## Questions to Answer Today

1. **Database Schema:** Which tables/fields do we need for Sprint 2.1?
   - `projects` table: what fields?
   - `project_notes` table: what fields?
   - `supporting_files` table: store file path or blob?

2. **UI Framework:** Keep it minimal or add a CSS framework?
   - Option A: Vanilla CSS (full control, more work)
   - Option B: Pico.css or similar (classless, minimal)
   - Option C: Tailwind/Bootstrap (more features, more complexity)

3. **HTMX Patterns:** Which interactions should use HTMX?
   - Form submissions (definitely)
   - Inline note editing (yes)
   - File upload (yes)
   - Navigation (maybe, depends on preference)

---

## Success Metric for Today

**Can create a new project through the web UI and see it in the database.**

That's it. Everything else builds on this foundation.

---

**Next Session:** Sprint 2.2 - Build AI agent services (LLMClient, ContextBuilder, StepBackAgent)
