# Project Plan - Project Wizard

**Version:** 3.0.0  
**Last Updated:** 2025-11-28  
**Status:** v0.3.0 CLI Complete ✅ | Planning v3.0: AI Project OS Evolution

---

## Executive Summary

Project Wizard is evolving from a CLI-based project charter creation tool into a comprehensive **AI Project Operating System**. This evolution transforms it from a document generator into a **project-centric context repository** where projects become first-class containers for all project knowledge, and AI-powered document generation uses full project context to produce consistently high-quality outputs.

**Current State (v0.3.0):**
- ✅ CLI-based charter creation wizard (20+ structured prompts)
- ✅ Repository scaffolding with standardized folder architecture
- ✅ Planning wizard with AI-assisted work breakdown
- ✅ RPG-style progress tracking
- ✅ Document generation (charter, plan, issues, contributing, etc.)

**Target State (v3.0.0):**
- 🎯 **Context-Rich Project Containers** - Projects store charters, notes, files, stakeholders, lessons learned
- 🎯 **Agentic Document Pipeline** - Step-back prompting → draft → chain-of-verification → refinement → memory logging
- 🎯 **Multi-Document Generation** - Charters, proposals, white papers, briefs, reports, protocols
- 🎯 **Learning System** - Memory-of-thought captures improvements, builds best practices library
- 🎯 **Web Interface** - FastAPI + HTMX for richer interactions (optional, CLI remains)

---

## Vision: From Document Generator to AI Project OS

### Philosophy Shift

**Before (v0.3.0):**
```
User Input → Charter Wizard → Jinja2 Template → Document
```

**After (v3.0.0):**
```
Project Context Container (charter + notes + files + history + memory)
    ↓
Step-Back Prompting (clarify the true problem)
    ↓
Section-by-Section Draft Generation (Jinja2 + context injection)
    ↓
Chain of Verification (4-step validation)
    ↓
User Feedback Loop
    ↓
Refined Draft
    ↓
Memory-of-Thought Logging (continuous improvement)
```

### Core Concepts

1. **Projects as Context Repositories**
   - Not just charters—store ALL project knowledge
   - Notes, files, stakeholder info, meeting notes, lessons learned
   - Context automatically informs every document generated

2. **Blueprint-Driven Templates**
   - Each document type (charter, proposal, white paper, etc.) has a blueprint
   - Blueprints define: inputs, sections, verification questions, rubrics
   - Templates rendered with full project context

3. **Agentic Techniques Built-In**
   - **Step-Back Prompting**: Clarify problem before drafting
   - **Chain of Verification**: Generate → verify → refine loop
   - **Memory of Thought**: Learn from each generation to improve future outputs

4. **Second Brain Integration**
   - Projects → Areas (project types) → Resources (templates) → Archives
   - Following Tiago Forte's PARA methodology
   - Everything in one place for AI context richness

---

## Technical Architecture

### v3.0 System Components

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface Layer                   │
│  ┌──────────────┐         ┌──────────────────────────┐  │
│  │  CLI (Click) │         │ Web UI (FastAPI + HTMX) │  │
│  │   v0.3.0     │         │     v3.1+ (optional)     │  │
│  └──────┬───────┘         └────────────┬─────────────┘  │
└─────────┼──────────────────────────────┼────────────────┘
          │                              │
┌─────────┴──────────────────────────────┴────────────────┐
│                  Service Layer                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ProjectRegistry (SQLModel)                     │    │
│  │  - Projects, Notes, Files, Memory               │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  BlueprintRegistry                              │    │
│  │  - Load/validate template blueprints            │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ContextBuilder                                 │    │
│  │  - Aggregate project context for AI             │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  DocumentPipeline                               │    │
│  │  - Orchestrate agentic workflow                 │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
          │
┌─────────┴────────────────────────────────────────────────┐
│                  AI Agent Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ StepBackAgent│  │  DraftAgent  │  │VerifierAgent│   │
│  │              │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ MemoryAgent  │  │  LLMClient   │                     │
│  │              │  │ (OpenAI/     │                     │
│  └──────────────┘  │  Anthropic)  │                     │
│                    └──────────────┘                     │
└──────────────────────────────────────────────────────────┘
          │
┌─────────┴────────────────────────────────────────────────┐
│                  Data Layer                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │  SQLite Database (via SQLModel)                 │    │
│  │  - projects, notes, files, document_runs        │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Blueprints (JSON)                              │    │
│  │  - patterns/<type>/blueprint.json               │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Templates (Jinja2)                             │    │
│  │  - patterns/<type>/template.j2                  │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### Data Models (v3.0)

```python
# Enhanced Project Model
class Project(SQLModel, table=True):
    id: int (primary key)
    title: str
    type: str  # software_mvp, clinical_workflow, etc.
    
    # Charter data (embedded or foreign key)
    charter: CharterData
    
    # Context-rich additions
    notes: list[ProjectNote]
    files: list[SupportingFile]
    stakeholders: list[Stakeholder]
    meeting_notes: list[MeetingNote]
    best_practices: list[BestPractice]
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    status: str  # initiating, planning, executing, closing

class ProjectNote(SQLModel, table=True):
    id: int
    project_id: int (foreign key)
    title: str
    content: str (markdown)
    tags: list[str]
    note_type: str  # general, technical, decision, lesson
    created_at: datetime

class SupportingFile(SQLModel, table=True):
    id: int
    project_id: int (foreign key)
    filename: str
    filepath: Path
    file_type: str  # pdf, docx, txt, markdown
    summary: str  # AI-generated
    extracted_text: str  # for searchability
    uploaded_at: datetime

class DocumentRun(SQLModel, table=True):
    id: int
    project_id: int (foreign key)
    template_name: str  # charter, white_paper, proposal, etc.
    
    # Agentic pipeline stages
    user_inputs: dict (JSON)
    step_back_summary: str
    initial_draft: str (markdown)
    verification_questions: str
    verification_answers: str  # user provides
    refined_draft: str (markdown)
    executive_summary: str
    
    # Memory system
    memory_log: str
    improvements_applied: list[str]
    
    created_at: datetime

class MemoryEntry(SQLModel, table=True):
    id: int
    template_name: str | None  # global or template-specific
    category: str  # best_practice, lesson_learned, pattern
    content: str
    source_document_run_id: int | None
    times_applied: int
    effectiveness_score: float
    created_at: datetime
```

---

## Implementation Roadmap

### Phase 1: Blueprint System Foundation ✨ **CURRENT PRIORITY**
**Duration:** 1-2 weeks  
**Goal:** Create infrastructure for template blueprints

#### Sprint 1.1: Blueprint Schema Design (2-3 days)
- [ ] **Task 1.1.1:** Design `blueprint.json` schema specification
  - Define JSON structure for inputs, sections, prompts, verification, rubrics
  - Create JSON Schema validation file
  - Document blueprint format with examples
  
- [ ] **Task 1.1.2:** Create Blueprint Pydantic models
  - `BlueprintSpec` model for validation
  - `TemplateInput`, `TemplateSection`, `VerificationQuestion` models
  - `Rubric` model with weighted criteria
  
- [ ] **Task 1.1.3:** Write blueprint validation tests
  - Test valid blueprint loading
  - Test invalid blueprint rejection
  - Test schema compliance

#### Sprint 1.2: Convert Existing Templates (3-4 days)
- [ ] **Task 1.2.1:** Create `patterns/` directory structure
  ```
  patterns/
  ├── project_charter/
  │   ├── blueprint.json
  │   ├── template.j2
  │   └── prompts.json
  ├── work_plan/
  │   ├── blueprint.json
  │   ├── template.j2
  │   └── prompts.json
  └── proposal/
      ├── blueprint.json
      ├── template.j2
      └── prompts.json
  ```
  
- [ ] **Task 1.2.2:** Migrate PROJECT_CHARTER.md.j2 to blueprint format
  - Extract inputs from phase1_initiation.py wizard
  - Define section structure
  - Create verification questions
  - Define quality rubric
  
- [ ] **Task 1.2.3:** Migrate PROJECT_PLAN.md.j2 to blueprint format
  - Extract inputs from phase2_planning.py
  - Define sections (milestones, tasks, dependencies)
  - Create verification questions
  
- [ ] **Task 1.2.4:** Create proposal blueprint (new)
  - Design input fields
  - Define standard proposal sections
  - Create verification checklist

#### Sprint 1.3: BlueprintRegistry Service (2-3 days)
- [ ] **Task 1.3.1:** Create `app/services/blueprint_registry.py`
  - `BlueprintRegistry` class
  - `load_blueprint(template_name)` method
  - `list_blueprints()` method
  - `validate_blueprint(blueprint)` method
  
- [ ] **Task 1.3.2:** Implement blueprint caching
  - Load blueprints once at startup
  - Hot-reload on file change (dev mode)
  
- [ ] **Task 1.3.3:** Create CLI command: `project-wizard templates`
  - List available templates
  - Show template details
  - Validate template directory

#### Sprint 1.4: Integration & Testing (1-2 days)
- [ ] **Task 1.4.1:** Update DocumentGenerator to use blueprints
  - Read blueprint instead of hardcoded logic
  - Pass blueprint metadata to templates
  
- [ ] **Task 1.4.2:** Create integration tests
  - End-to-end blueprint → document generation
  - Test all existing templates
  
- [ ] **Task 1.4.3:** Update documentation
  - BLUEPRINT_GUIDE.md (how to create blueprints)
  - Update README with blueprint architecture

**Phase 1 Success Criteria:**
- ✅ All existing templates converted to blueprint format
- ✅ BlueprintRegistry loads and validates blueprints
- ✅ Existing document generation works with new system
- ✅ Zero breaking changes to current CLI commands

---

### Phase 2: Database Migration & Enhanced Project Model
**Duration:** 2-3 weeks  
**Goal:** Move from JSON to SQLite, expand Project model

#### Sprint 2.1: Database Setup (3-4 days)
- [ ] Design SQLModel schema
- [ ] Create migration script from JSON → SQLite
- [ ] Set up Alembic for future migrations
- [ ] Create database initialization script

#### Sprint 2.2: Enhanced Project Model (4-5 days)
- [ ] Implement `ProjectNote` model and CRUD
- [ ] Implement `SupportingFile` model and CRUD
- [ ] Implement `DocumentRun` model
- [ ] Update ProjectRegistry to use SQLModel

#### Sprint 2.3: CLI Commands for Context Management (3-4 days)
- [ ] `project-wizard note add` - Add note to project
- [ ] `project-wizard note list` - List project notes
- [ ] `project-wizard file upload` - Upload supporting file
- [ ] `project-wizard context show` - Show project context summary

#### Sprint 2.4: File Processing (3-4 days)
- [ ] PDF text extraction (PyPDF2 or pdfplumber)
- [ ] DOCX text extraction (python-docx)
- [ ] AI summarization of uploaded files
- [ ] Full-text search across notes and files

**Phase 2 Success Criteria:**
- ✅ All projects stored in SQLite database
- ✅ Notes and files can be added to projects
- ✅ Context can be viewed via CLI
- ✅ Backward compatibility with v0.3.0 maintained

---

### Phase 3: Agentic Pipeline Components
**Duration:** 3-4 weeks  
**Goal:** Build AI agent system with step-back, verification, memory

#### Sprint 3.1: ContextBuilder Service (3-4 days)
- [ ] Create `app/services/context_builder.py`
- [ ] Implement context aggregation from all project sources
- [ ] Context summarization for AI consumption
- [ ] Context relevance filtering

#### Sprint 3.2: StepBackAgent (4-5 days)
- [ ] Create `app/services/ai_agents/step_back_agent.py`
- [ ] Implement problem restatement
- [ ] Generate clarifying questions
- [ ] Integrate with blueprint system

#### Sprint 3.3: DraftAgent Enhancement (4-5 days)
- [ ] Enhance existing CharterAgent → DraftAgent
- [ ] Section-by-section generation
- [ ] Context injection into prompts
- [ ] Internal monologue/reasoning capture

#### Sprint 3.4: VerifierAgent (Chain of Verification) (5-6 days)
- [ ] Create `app/services/ai_agents/verifier_agent.py`
- [ ] Generate verification questions from blueprint
- [ ] Compare draft against context/charter
- [ ] Identify gaps and inconsistencies
- [ ] Generate executive summary

#### Sprint 3.5: MemoryAgent (4-5 days)
- [ ] Create `app/services/ai_agents/memory_agent.py`
- [ ] Implement `MemoryEntry` model
- [ ] Extract lessons learned from document runs
- [ ] Build best practices library (global + template-specific)
- [ ] Implement memory retrieval based on relevance

**Phase 3 Success Criteria:**
- ✅ Full agentic pipeline operational
- ✅ Step-back prompting improves document quality
- ✅ Verification catches errors and inconsistencies
- ✅ Memory system learns from each generation

---

### Phase 4: DocumentPipeline Orchestration
**Duration:** 2-3 weeks  
**Goal:** Wire all agents together into cohesive workflow

#### Sprint 4.1: Pipeline Core (4-5 days)
- [ ] Create `app/services/document_pipeline.py`
- [ ] Orchestrate: context → step-back → draft → verify → refine
- [ ] Handle user feedback loop
- [ ] Store DocumentRun with all intermediate outputs

#### Sprint 4.2: CLI Integration (3-4 days)
- [ ] Update `project-wizard generate <template>` command
- [ ] Interactive verification question interface
- [ ] Show draft comparison (initial vs refined)
- [ ] Memory insights display

#### Sprint 4.3: Template Expansion (5-6 days)
- [ ] White paper blueprint + template
- [ ] Executive brief blueprint + template
- [ ] Engineering report blueprint + template
- [ ] Policy recommendation blueprint + template

**Phase 4 Success Criteria:**
- ✅ End-to-end pipeline: user input → refined document
- ✅ CLI provides rich interaction for verification
- ✅ 6+ document templates operational
- ✅ Memory system visibly improving outputs

---

### Phase 5: Web Interface (Optional - FastAPI + HTMX)
**Duration:** 4-6 weeks  
**Goal:** Rich web UI for better UX

#### Sprint 5.1: FastAPI Foundation (5-6 days)
- [ ] Set up FastAPI application structure
- [ ] HTMX integration
- [ ] Jinja2 HTML templates
- [ ] Authentication (optional for personal use)

#### Sprint 5.2: Project Management UI (6-8 days)
- [ ] Project list/dashboard
- [ ] Project detail view
- [ ] Notes CRUD interface
- [ ] File upload interface

#### Sprint 5.3: Document Generation UI (6-8 days)
- [ ] Template selector
- [ ] Dynamic form generation from blueprint
- [ ] Step-back prompting interface
- [ ] Verification questions interface
- [ ] Draft comparison view

#### Sprint 5.4: Memory Bank UI (4-5 days)
- [ ] Best practices library browser
- [ ] Lessons learned viewer
- [ ] Memory search interface

**Phase 5 Success Criteria:**
- ✅ Web UI accessible at http://localhost:8000
- ✅ Full feature parity with CLI
- ✅ Richer interactions (inline editing, drag-drop files)
- ✅ Mobile-responsive design

---

## Technology Stack

### Current (v0.3.0)
- **CLI:** Click framework
- **Prompts:** questionary + rich
- **Templates:** Jinja2
- **Validation:** Pydantic v2
- **Git Operations:** GitPython
- **Storage:** JSON files

### v3.0 Additions
- **Database:** SQLite + SQLModel (ORM)
- **Migrations:** Alembic
- **AI Client:** OpenAI API / Anthropic API
- **File Processing:** PyPDF2, python-docx
- **Web Framework:** FastAPI (optional)
- **Frontend:** HTMX + Jinja2 templates (optional)

---

## Success Metrics

### v3.0 Success Criteria
- [ ] Projects store 5+ types of context (notes, files, stakeholders, etc.)
- [ ] Blueprint system supports 8+ document templates
- [ ] Agentic pipeline reduces document errors by 50%
- [ ] Memory system provides 3+ relevant best practices per generation
- [ ] Document generation time < 5 minutes for complex documents
- [ ] User satisfaction: 90%+ of documents require minimal manual editing

### Performance Targets
- Database queries: < 100ms
- Document generation: < 2 minutes (excluding LLM API time)
- Context aggregation: < 5 seconds
- Memory retrieval: < 500ms

---

## Development Practices

### Version Control
- **Branch Strategy:** `main`, `develop`, `feature/*`, `bugfix/*`
- **Commit Convention:** Conventional Commits (feat:, fix:, docs:, refactor:, test:)
- **PR Process:** Self-review, test locally, update CHANGELOG.md
- **Tagging:** Semantic versioning (v3.0.0, v3.1.0, etc.)

### Testing Strategy
- **Unit Tests:** pytest for all services and models
- **Integration Tests:** End-to-end document generation workflows
- **Blueprint Tests:** Validate all blueprint.json files
- **Regression Tests:** Ensure v0.3.0 CLI commands still work

### Code Quality
- **Style:** PEP 8 (enforced via ruff)
- **Linting:** `make lint` before commits
- **Complexity:** Max cyclomatic complexity 10
- **Coverage:** Target 80%+ test coverage
- **Documentation:** Docstrings for all public functions

### Deployment
- **CLI:** pip install -e . (editable mode for dev)
- **Web:** uvicorn for local development
- **Production:** Docker container (future)
- **Database:** SQLite for simplicity, PostgreSQL for scale (future)

---

## Risk Management

### Technical Risks

**R1: Blueprint Complexity**
- **Impact:** High - If blueprints become too complex, template authors struggle
- **Mitigation:** Keep schema simple, provide generator tool, excellent docs
- **Contingency:** Fall back to hardcoded templates for complex cases

**R2: AI API Costs**
- **Impact:** Medium - OpenAI costs could escalate with heavy usage
- **Probability:** Low (personal use, conservative prompting)
- **Mitigation:** Token usage monitoring, caching, local LLM fallback
- **Contingency:** Ollama integration for local inference

**R3: Database Migration Issues**
- **Impact:** High - Data loss from JSON → SQLite migration
- **Probability:** Low (careful migration script)
- **Mitigation:** Backup JSON files, dry-run testing, rollback capability
- **Contingency:** Keep JSON files as backup, manual restore

**R4: Breaking Changes**
- **Impact:** High - Existing v0.3.0 users can't upgrade
- **Probability:** Medium
- **Mitigation:** Maintain backward compatibility, gradual migration path
- **Contingency:** Support both v0.3.0 and v3.0 in parallel branches

### Product Risks

**R5: Scope Creep**
- **Impact:** High - Project never reaches usable v3.0
- **Probability:** High (ADHD developer, exciting new features)
- **Mitigation:** Strict MVP definition per phase, time-boxing
- **Contingency:** Defer features to v3.1, v3.2, etc.

**R6: Over-Engineering**
- **Impact:** Medium - System becomes too complex for personal use
- **Probability:** Medium
- **Mitigation:** YAGNI principle, build only what's needed
- **Contingency:** Simplify architecture if complexity hinders productivity

**R7: AI Quality Issues**
- **Impact:** High - Generated documents contain errors or hallucinations
- **Probability:** Low (using chain-of-verification)
- **Mitigation:** User review at every stage, anti-hallucination prompts
- **Contingency:** Manual editing always available, AI optional

---

## Resource Requirements

### Development Time
- **Phase 1 (Blueprint System):** 40-60 hours (2-3 weeks part-time)
- **Phase 2 (Database Migration):** 60-80 hours (3-4 weeks part-time)
- **Phase 3 (Agentic Pipeline):** 80-100 hours (4-5 weeks part-time)
- **Phase 4 (Pipeline Orchestration):** 60-80 hours (3-4 weeks part-time)
- **Phase 5 (Web Interface):** 100-120 hours (5-6 weeks part-time) - Optional
- **Total v3.0 (CLI only):** 240-320 hours (~12-16 weeks part-time)
- **Total v3.0 (with Web UI):** 340-440 hours (~17-22 weeks part-time)

### Infrastructure
- **Development:** Local machine (Windows + WSL or Ubuntu VM)
- **Database:** SQLite (local file)
- **AI API:** OpenAI or Anthropic account ($10-50/month estimated)
- **Web Hosting (optional):** Local MiniPC at 10.69.1.86 or cloud (Railway, Fly.io)

### Costs
- **Current (v0.3.0):** $0/month (no external dependencies)
- **v3.0 (CLI):** ~$10-20/month (AI API usage for personal projects)
- **v3.0 (Web):** ~$20-50/month (AI + potential hosting)

---

## Dependencies

### External Systems
- **OpenAI API** - GPT-4 for high-quality document generation (v3.0+)
- **Anthropic API** - Claude as alternative (v3.0+)
- **Ollama** - Local LLM fallback (v3.1+)

### Python Packages (v3.0)
**Existing:**
- click (CLI framework)
- jinja2 (template engine)
- pydantic (data validation)
- rich (console formatting)
- questionary (interactive prompts)
- gitpython (git operations)

**New:**
- sqlmodel (ORM + Pydantic integration)
- alembic (database migrations)
- openai (OpenAI API client)
- anthropic (Anthropic API client)
- pypdf2 or pdfplumber (PDF extraction)
- python-docx (Word document extraction)
- fastapi (web framework - optional)
- uvicorn (ASGI server - optional)
- htmx (via CDN - optional)

---

## Lessons Learned

### What Worked Well (v0.1.0 - v0.3.0)
1. **Structured wizard approach** - Users appreciate step-by-step guidance
2. **Jinja2 templates** - Flexible, maintainable, version-controllable
3. **Pydantic validation** - Catches errors early, self-documenting
4. **Standardized folder structure** - Consistency across all projects
5. **RPG framework** - Gamification increases engagement

### What Didn't Work
1. **Hardcoded wizard logic** - Difficult to add new templates, not scalable
2. **JSON storage** - Limited querying, no relationships, manual management
3. **No context awareness** - Each document generated in isolation
4. **Manual AI integration** - Copy-paste workflow prone to errors

### What to Try in v3.0
1. **Blueprint system** - Data-driven template definitions
2. **Database storage** - Better querying, relationships, integrity
3. **Context-rich generation** - Use all project knowledge automatically
4. **Agentic workflows** - Step-back, verify, learn from mistakes
5. **Memory system** - Continuous improvement across documents

---

## Appendices

### A. Blueprint JSON Schema

See `docs/BLUEPRINT_SCHEMA.md` for detailed specification.

Example structure:
```json
{
  "name": "white_paper",
  "version": "1.0.0",
  "description": "Professional white paper with evidence-based analysis",
  "inputs": [ ... ],
  "sections": [ ... ],
  "step_back_prompts": { ... },
  "verification_questions": [ ... ],
  "rubric": { ... }
}
```

### B. Agentic Pipeline Flow

Detailed flow diagram in `docs/AGENTIC_PIPELINE.md`.

```
User Request
    ↓
[ContextBuilder] → Aggregate project context
    ↓
[StepBackAgent] → Clarify problem, ask questions
    ↓
[DraftAgent] → Generate section-by-section draft
    ↓
[VerifierAgent] → Generate verification questions
    ↓
User Provides Answers
    ↓
[DraftAgent] → Refine draft based on feedback
    ↓
[VerifierAgent] → Generate executive summary
    ↓
[MemoryAgent] → Extract lessons, update best practices
    ↓
[DocumentRun] → Save complete record
```

### C. Migration Path from v0.3.0 → v3.0

**For Users:**
1. Run `project-wizard migrate` command
2. All JSON projects converted to SQLite
3. Existing CLI commands work unchanged
4. New commands available for context management

**For Developers:**
1. Phase 1 (Blueprint) is backward compatible
2. Phase 2 (Database) requires migration script
3. Phase 3+ (Agentic) are additive features
4. v0.3.0 branch maintained for legacy support

---

## Next Steps (Immediate Actions)

### Week 1-2: Blueprint System (Phase 1)
1. [x] Design blueprint.json schema
2. [ ] Create Pydantic models for blueprints
3. [ ] Convert PROJECT_CHARTER.md.j2 to blueprint format
4. [ ] Convert PROJECT_PLAN.md.j2 to blueprint format
5. [ ] Create BlueprintRegistry service
6. [ ] Add `project-wizard templates` CLI command
7. [ ] Integration testing
8. [ ] Documentation

### Week 3-4: Database Foundation (Phase 2 Start)
1. [ ] Design SQLModel schema
2. [ ] Create migration script
3. [ ] Test migration with real projects
4. [ ] Update ProjectRegistry

---

**Document Version:** 3.0.0-draft  
**Last Updated:** 2025-11-28  
**Next Review:** End of Phase 1 (Blueprint System)  
**Owner:** Jonathan Ives (dollythedog)

**References:**
- `README.md` - Current features and quick start
- `WARP.md` - Development guidelines
- `docs/PROJECT_GUIDELINES.md` - PM methodology
- `docs/BLUEPRINT_SCHEMA.md` - Blueprint specification (to be created)
- `docs/AGENTIC_PIPELINE.md` - Pipeline architecture (to be created)
