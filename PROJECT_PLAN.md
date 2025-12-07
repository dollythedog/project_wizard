# Project Plan - Project Wizard

**Version:** 3.0.0  
**Last Updated:** 2025-12-07  
**Status:** ✅ PRODUCTION READY | Web UI Complete | Ready for Server Deployment

---

## 🚀 Quick Start - Get Running in 5 Minutes

**1. Configure Your API Key**
```powershell
# Copy the example config
cp .env.example .env

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-key-here
# Or use Anthropic:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**2. Start the Web Server**
```powershell
python run_web.py
```

**3. Navigate to http://localhost:8000**

**4. Try the Full Workflow**
- Create a new project (e.g., "Healthcare Monitoring MVP")
- Add 2-3 notes with project context/ideas
- Click "Generate Document" → select "Project Charter"
- Answer the AI-generated clarifying questions
- Review your beautiful draft document!
- Try "Proposal" next for the same project

**That's it!** You now have an AI-powered document generation system. 🎉

---

## Executive Summary

Project Wizard is evolving from a CLI-based project charter creation tool into a comprehensive **AI Project Operating System**. This evolution transforms it from a document generator into a **project-centric context repository** where projects become first-class containers for all project knowledge, and AI-powered document generation uses full project context to produce consistently high-quality outputs.

**Current State (v3.0 - 2025-12-07):**
- ✅ Web-based project management UI (FastAPI + HTMX)
- ✅ SQLite database with rich project context (notes, files, history)
- ✅ AI-powered document generation (GPT-4, Claude)
- ✅ Step-back prompting with suggested outlines
- ✅ 10 production blueprints (white_paper, data_analysis, project_charter, proposal, etc.)
- ✅ Section-by-section generation with word count enforcement
- ✅ Hallucination detection and auto-regeneration
- ✅ Beautiful markdown rendering and export
- ✅ Context-aware AI agents
- ✅ Quality review and guided refinement

**Production Status (v3.0):**
- ✅ **Context-Rich Project Containers** - Projects store notes, files, complete history
- ✅ **Agentic Document Pipeline** - Step-back → outline → section-by-section generation
- ✅ **Multi-Document Generation** - 10 production blueprints ready
- ✅ **Web Interface** - Full FastAPI + HTMX UI operational
- ✅ **Quality Controls** - Hallucination detection, word count enforcement, auto-regeneration
- ✅ **Refinement Tools** - Quality review and guided refinement working

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

### Phase 1: Blueprint System Foundation ✅ **COMPLETED 2025-11-30**
**Duration:** 2 weeks (2025-11-15 to 2025-11-30)  
**Goal:** Create infrastructure for template blueprints

#### What Was Built:
- ✅ `patterns/` directory with 3 blueprints: project_charter, work_plan, proposal
- ✅ Complete blueprint.json schema with sections, inputs, prompts
- ✅ Pydantic models: BlueprintSpec, TemplateInput, TemplateSection
- ✅ BlueprintRegistry service with load/validate/list methods
- ✅ Blueprint-specific prompts in prompts.json files
- ✅ Comprehensive test suite (14/14 tests passing)
- ✅ CLI commands: `templates list`, `templates info <name>`

**Phase 1 Success Criteria:** ALL MET ✅
- ✅ All existing templates converted to blueprint format
- ✅ BlueprintRegistry loads and validates blueprints
- ✅ Existing document generation works with new system
- ✅ Zero breaking changes to current CLI commands

**See:** `docs/PHASE1_COMPLETION.md` for detailed sprint notes

---

### Phase 2: AI-Powered Web Application ✅ **COMPLETED 2025-12-01**
**Duration:** Single intensive session (~4 hours)
**Goal:** Build complete web interface with AI document generation

**Key Decision:** Phase 2 prioritized **web interface over CLI** because conversational AI workflows (step-back prompting, verification, iterative refinement) work much better in a browser than a terminal.

#### Sprint 2.1: FastAPI Foundation & Database ✅
- ✅ SQLModel schema: Project, ProjectNote, SupportingFile, DocumentRun, MemoryEntry
- ✅ Database utilities with session management (app/services/database.py)
- ✅ ProjectRegistry service with full CRUD operations (246 lines)
- ✅ FastAPI app with Jinja2 templates and HTMX integration
- ✅ Web UI: base layout, index, project list/create/detail pages
- ✅ Responsive CSS styling (467 lines)
- ✅ SQLite database initialized at data/project_wizard.db

#### Sprint 2.2: AI Agent Services ✅
- ✅ LLMClient service with OpenAI and Anthropic support (208 lines)
- ✅ Retry logic, token tracking, configurable models
- ✅ ContextBuilder service aggregates project data (259 lines)
- ✅ StepBackAgent generates clarifying questions (196 lines)
- ✅ DraftAgent creates documents from context (212 lines)
- ✅ Configuration management with .env support (app/config.py)

#### Sprint 2.3: Document Generation UI ✅
- ✅ Complete web workflow: template selection → questions → draft
- ✅ Template selector with grid layout (select_template.html)
- ✅ Questions page with loading spinner (questions.html, 172 lines)
- ✅ Draft display with dual view: rendered HTML + markdown source (draft.html, 279 lines)
- ✅ Marked.js integration for beautiful markdown rendering
- ✅ Copy to clipboard and download functionality
- ✅ Error handling pages (no_api_key.html, error.html)
- ✅ Generate routes (web/routes/generate.py, 215 lines)

**Phase 2 Success Criteria:** ALL MET ✅
- ✅ Web app runs at http://localhost:8000
- ✅ Can create projects and add notes/context via UI
- ✅ Projects stored in SQLite database
- ✅ AI agents (StepBackAgent, DraftAgent) operational
- ✅ Complete document generation workflow functional
- ✅ Beautiful markdown rendering and export

**Files Created:** 25+ files, ~3800 lines of code
**See:** `docs/SPRINT_2.1_COMPLETE.md`, `docs/SPRINT_2.2_COMPLETE.md`, `docs/SPRINT_2.3_COMPLETE.md`

---

## 🎯 What's Next? MVP → Production

**Current Status:** You have a working MVP! 🎉 The system generates documents with AI step-back prompting.

### Immediate Next Steps (Getting Started)

**1. Configure API Key** (5 minutes)
```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-key-here
# Or use Anthropic:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**2. Start the Web Server**
```bash
python run_web.py
# Navigate to http://localhost:8000
```

**3. Test End-to-End Workflow**
- Create a new project
- Add 2-3 notes with project context
- Click "Generate Document" → select "Project Charter"
- Answer the step-back questions
- Review the generated draft
- Try generating a "Proposal" next

### Phase 3: Polish & Enhancement (Optional - Future Work)

#### High-Value Additions
**A. VerifierAgent - Chain of Verification** (3-5 days)
- [ ] Create `app/services/ai_agents/verifier_agent.py`
- [ ] Generate verification questions from blueprint rubric
- [ ] Compare draft against context and identify gaps
- [ ] Iterative refinement loop
- **Value:** Catches errors, improves document quality by 30-50%

**B. File Upload & Processing** (2-3 days)
- [ ] Add file upload to project detail page
- [ ] PDF/DOCX text extraction (PyPDF2, python-docx)
- [ ] AI summarization of uploaded files
- [ ] Include file content in ContextBuilder
- **Value:** Leverage existing documents as project context

**C. Memory System** (4-5 days)
- [ ] Create `app/services/ai_agents/memory_agent.py`
- [ ] Extract lessons learned from DocumentRun
- [ ] Build best practices library (global + template-specific)
- [ ] Inject relevant memories into DraftAgent prompts
- **Value:** System learns and improves over time

**D. Additional Templates** (2-3 days each)
- [ ] White paper blueprint + prompts
- [ ] Executive brief blueprint + prompts
- [ ] Engineering report blueprint + prompts
- [ ] Policy recommendation blueprint + prompts
- **Value:** Expand use cases beyond charter/plan/proposal

#### Quality of Life Improvements
**E. File Upload UI** (1-2 days)
- [ ] Drag-and-drop file upload on project detail page
- [ ] Display uploaded files with summaries
- [ ] Delete/rename file functionality

**F. Document History** (2-3 days)
- [ ] Show all DocumentRuns for a project
- [ ] Compare versions side-by-side
- [ ] Re-download previous drafts

**G. Better Error Handling** (1 day)
- [ ] Graceful API timeout handling
- [ ] Token limit warnings
- [ ] More informative error messages

**H. Export Formats** (1-2 days)
- [ ] PDF export (markdown → HTML → PDF)
- [ ] DOCX export (python-docx)
- [ ] Custom styling/branding

### Phase 4: Production Deployment (Optional)

#### Production Readiness
**A. Docker Containerization** (2-3 days)
- [ ] Create Dockerfile
- [ ] Docker Compose for easy deployment
- [ ] Volume mounts for data/ directory
- **Value:** Deploy to any server easily

**B. Authentication** (3-4 days)
- [ ] Simple username/password login
- [ ] Session management
- [ ] Multi-user support (optional)
- **Value:** Secure if exposing to network

**C. PostgreSQL Migration** (2-3 days)
- [ ] Switch from SQLite to PostgreSQL
- [ ] Alembic migrations
- [ ] Connection pooling
- **Value:** Better performance at scale

**D. Backup & Recovery** (1-2 days)
- [ ] Automated database backups
- [ ] Export all projects as JSON
- [ ] Restore from backup functionality
- **Value:** Don't lose your work!

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
