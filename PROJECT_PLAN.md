# Project Plan - Project Wizard

**Version:** 2.0.0  
**Last Updated:** 2024-11-06  
**Status:** v2.0 MVP Complete ✅ | Next: v2.1 Development

---

## Executive Summary

Project Wizard is an AI-powered web application that automates project charter creation following formal project management methodology. Designed for developers with ADHD, it eliminates "setup paralysis" by providing structured, guided workflows with optional AI assistance that enhances without hallucinating.

**Current State:**
- ✅ v2.0 MVP deployed and production-ready
- ✅ 6-tab structured workflow operational
- ✅ AI enhancement with anti-hallucination safeguards
- ✅ Quality critique against PM best practices
- ⏳ OpenProject integration planned for v2.1

---

## Technical Architecture

### v2.0 Stack

**Frontend:**
- Streamlit 1.31.0 (Python web framework)
- Multi-tab interface with session state management
- Real-time form validation
- Markdown rendering for preview

**Backend:**
- Python 3.12
- FastAPI-style service architecture
- Modular AI agent system

**AI Engine:**
- OpenAI GPT-4o-mini API
- Structured prompt library (JSON)
- Conservative temperature settings (0.3-0.4)
- Retry logic with exponential backoff

**Configuration:**
- YAML: `ai_config.yaml` (AI settings, feature flags)
- JSON: `enhancement_prompts.json` (anti-hallucination prompts)
- JSON: `rubric_charter.json` (quality criteria with weights)
- ENV: `.env` file for API keys

**Storage:**
- Session state for active data
- File system for charter exports
- No database (yet - planned for v2.2)

### Component Architecture

```
┌─────────────────────────────────────────┐
│     app_streamlit_v2.py (Frontend)      │
│  ┌──────────┬──────────┬──────────┐     │
│  │  Tab 1   │  Tab 2   │  Tab 3   │     │
│  │Initiation│ Business │Enhancement│     │
│  │          │   Case   │          │     │
│  └────┬─────┴────┬─────┴────┬─────┘     │
│       │          │          │           │
│       └──────────┴──────────┘           │
│               │                         │
│      session_state management           │
└───────────────┼─────────────────────────┘
                │
        ┌───────┴────────┐
        │  AI Agents     │
        │  (Backend)     │
        ├────────────────┤
        │ CharterAgent   │──→ enhancement_prompts.json
        │                │
        │ CriticAgent    │──→ rubric_charter.json
        │                │
        │ LLMClient      │──→ OpenAI API
        └────────────────┘
```

### Data Flow

```
User Input (Tabs 1-2)
    ↓
session_state.form_data
    ↓
AI Enhancement (Tab 3) ──→ CharterAgent ──→ OpenAI API
    ↓                           ↓
Accept/Reject/Edit      enhanced_data
    ↓                           ↓
manual_edits ←────────────────┘
    ↓
Updated form_data
    ↓
Charter Generation (Tab 4) ──→ Template-based (NO AI)
    ↓
charter_text (markdown)
    ↓
Quality Critique (Tab 5) ──→ CriticAgent ──→ OpenAI API
    ↓                           ↓
critique results         scores, feedback, gaps
    ↓
Display & Download
```

### File Structure

```
project_wizard/
├── app/
│   ├── __init__.py
│   └── services/
│       └── ai_agents/
│           ├── __init__.py
│           ├── charter_agent.py          # Enhancement logic
│           ├── critic_agent.py           # Quality review
│           └── llm_client.py             # OpenAI wrapper
├── configs/
│   ├── ai_config.yaml                    # AI model settings
│   ├── enhancement_prompts.json          # Structured prompts
│   └── rubric_charter.json               # Quality criteria
├── logs/
│   └── ai_agents.log                     # Application logs
├── reference_docs/
│   └── PROJECT_GUIDELINES.md             # PM methodology reference
├── tests/
│   └── test_ai_agents.py                 # Unit tests
├── app_streamlit_v2.py                   # v2.0 main application
├── app_streamlit.py                      # v1.0 legacy application
├── .env                                  # OpenAI API key (secret)
├── .gitignore
├── requirements.txt
├── setup.py
├── README.md
├── CHANGELOG.md
├── ISSUES.md
├── PROJECT_CHARTER.md
├── PROJECT_PLAN.md                       # This document
├── QUICK_START.md
├── V2_IMPLEMENTATION_COMPLETE.md
└── CRITIQUE_FIX.md
```

---

## Implementation Roadmap

### ✅ Phase 1: CLI Wizard (Complete - Nov 3, 2024)

**Goal:** Basic command-line charter creation

**Deliverables:**
- [x] Interactive CLI with questionary
- [x] Charter template generation
- [x] Basic folder structure creation
- [x] Git initialization
- [x] `project-wizard init` command

**Status:** Archived - Replaced by web interface

---

### ✅ Phase 2: v1.0 Web Interface (Complete - Nov 6, 2024)

**Goal:** Web-based charter creation with AI assistance

**Deliverables:**
- [x] Streamlit web application
- [x] Single-form charter input
- [x] AI-powered charter drafting
- [x] Quality critique with rubric
- [x] OpenAI integration
- [x] Production deployment on port 8501

**Issues Identified:**
- AI hallucination problem
- Limited user control
- All-or-nothing AI generation

**Status:** Operational but deprecated in favor of v2.0

---

### ✅ Phase 3: v2.0 MVP (Complete - Nov 6, 2024)

**Goal:** Eliminate AI hallucination, add structured workflow, full user control

**Sprint 1: Foundation (Completed Nov 6)**
- [x] Design 6-tab workflow architecture
- [x] Implement Tab 1: Project Initiation Request
- [x] Implement Tab 2: Business Case
- [x] Create structured data collection forms
- [x] Session state management system

**Sprint 2: AI Enhancement (Completed Nov 6)**
- [x] Design anti-hallucination system
- [x] Create structured prompt library (enhancement_prompts.json)
- [x] Update CharterAgent with structured prompts
- [x] Implement Tab 3: AI Enhancement
- [x] Add Accept/Reject/Edit controls
- [x] Implement editable manual editing

**Sprint 3: Generation & Review (Completed Nov 6)**
- [x] Implement Tab 4: Charter Generation (template-based)
- [x] Fix CriticAgent data structure mismatch
- [x] Implement Tab 5: Quality Review display
- [x] Add strengths/weaknesses/improvements display
- [x] Markdown export functionality

**Sprint 4: Bug Fixes & Polish (Completed Nov 6)**
- [x] Fix: OpenAI API key loading (load_dotenv)
- [x] Fix: Critique display showing 0% score
- [x] Fix: Edit Manually button not editable
- [x] Fix: AI hallucination prevention
- [x] Update all documentation

**Deliverables:**
- [x] Complete 6-tab web application
- [x] Anti-hallucination AI system
- [x] Quality critique with detailed feedback
- [x] Production deployment on port 8502
- [x] Comprehensive documentation

**Outcome:** ✅ v2.0 MVP production-ready and deployed

---

### ⏳ Phase 4: v2.1 - Project Scaffolding (Planned - Dec 2024)

**Goal:** Complete Tab 6, add project structure generation and OpenProject integration

**Sprint 1: Project Scaffolding (Week 1-2)**
- [ ] Design folder structure templates
- [ ] Implement directory creation logic
- [ ] Generate README.md from charter data
- [ ] Generate CHANGELOG.md with v0.1.0 entry
- [ ] Generate LICENSE.md (MIT template)
- [ ] Create .gitignore (project-type specific)
- [ ] Git repository initialization
- [ ] Initial commit with proper message

**Sprint 2: OpenProject API Integration (Week 3-4)**
- [ ] Review user's existing OpenProject API code
- [ ] Design task breakdown from charter sections
- [ ] Implement OpenProject API client
- [ ] Map charter sections to work packages
- [ ] Create project in OpenProject
- [ ] Generate tasks with descriptions
- [ ] Set up task dependencies
- [ ] Configure project board

**Sprint 3: Template Library (Week 5)**
- [ ] Software MVP template (web app, API, CLI)
- [ ] Research study template (hypothesis, data collection, analysis)
- [ ] Clinical trial template (HIPAA-compliant, regulatory)
- [ ] Data pipeline template (ETL, validation, reporting)
- [ ] Template selection UI in Tab 1
- [ ] Pre-populated field examples per template

**Sprint 4: UX Improvements (Week 6)**
- [ ] Progress indicators across tabs
- [ ] Estimated time to completion
- [ ] Auto-save to localStorage
- [ ] Draft save/load functionality
- [ ] "Quick start" wizard mode
- [ ] Keyboard shortcuts
- [ ] Mobile-responsive improvements

**Deliverables:**
- [ ] Fully functional Tab 6
- [ ] OpenProject integration
- [ ] 5+ project templates
- [ ] Enhanced user experience
- [ ] v2.1.0 release

**Success Criteria:**
- User can generate charter and complete project in <15 minutes
- OpenProject tasks automatically created
- Template accelerates charter creation by 50%
- Zero manual file/folder creation needed

---

### 🔮 Phase 5: v2.2 - Collaboration & Multi-User (Planned - Q1 2025)

**Goal:** Support teams, add authentication, improve quality

**Features:**
- [ ] User authentication (OAuth, username/password)
- [ ] Multi-user session isolation
- [ ] Charter ownership and permissions
- [ ] Charter version history
- [ ] Side-by-side version comparison
- [ ] Comments and approvals
- [ ] Custom rubric editor
- [ ] Export to PDF/DOCX
- [ ] GitHub Projects integration
- [ ] NTFY notifications
- [ ] PostgreSQL database backend
- [ ] RESTful API for programmatic access

**Technical Improvements:**
- [ ] Database schema design
- [ ] Authentication middleware
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] Horizontal scaling support
- [ ] CI/CD pipeline
- [ ] Automated testing (90%+ coverage)
- [ ] Performance monitoring

---

### 🌟 Phase 6: v3.0 - Full Lifecycle Management (Planned - Q2 2025)

**Goal:** Extend beyond charter creation to full project lifecycle

**Phase 2: Project Planning**
- [ ] Work Breakdown Structure (WBS) editor
- [ ] Gantt chart visualization
- [ ] Resource allocation planning
- [ ] Budget tracking
- [ ] Risk register management
- [ ] Communications plan

**Phase 3: Execution & Tracking**
- [ ] Task progress tracking
- [ ] Time logging
- [ ] Status report generation
- [ ] Burndown charts
- [ ] Team velocity metrics
- [ ] Blocker identification

**Phase 4: Closure & Lessons Learned**
- [ ] Project retrospectives
- [ ] Lessons learned capture
- [ ] Final documentation generation
- [ ] Archival and handoff
- [ ] Success metrics analysis

**Dashboard & Analytics:**
- [ ] Portfolio view (all projects)
- [ ] Health indicators
- [ ] Predictive analytics (AI-powered)
- [ ] Custom reporting
- [ ] Executive summaries

---

## Development Practices

### Version Control
- **Branch Strategy:** feature/*, bugfix/*, release/*
- **Commit Convention:** Conventional Commits (feat:, fix:, docs:, etc.)
- **PR Process:** Self-review, test locally, descriptive PR description
- **Tagging:** Semantic versioning (v2.0.0, v2.1.0, etc.)

### Testing Strategy
- **Unit Tests:** pytest for agent logic, utilities
- **Integration Tests:** Streamlit app testing with selenium
- **Manual Testing:** User acceptance testing with real charters
- **Regression Testing:** Test previous bugs don't reappear

### Code Quality
- **Style:** PEP 8 (Python)
- **Linting:** ruff, mypy for type checking
- **Documentation:** Docstrings for all functions, README updates
- **Complexity:** Keep functions under 50 lines, classes focused

### Deployment
- **Environment:** Ubuntu server (10.69.1.86)
- **Process:** Manual deployment (for now)
- **Monitoring:** Log files, ps aux checks
- **Rollback:** Keep previous version running on different port

---

## Risk Management

### Technical Risks

**R1: OpenAI API Outage**
- **Impact:** High - AI features unavailable
- **Probability:** Low
- **Mitigation:** Graceful degradation, show user's original text, cache responses
- **Contingency:** Fallback to local LLM (Ollama) in future

**R2: API Cost Overrun**
- **Impact:** Medium - Monthly costs exceed budget
- **Probability:** Low (current: $0.08/month for 20 charters)
- **Mitigation:** Rate limiting, usage monitoring, cost alerts
- **Contingency:** Switch to cheaper model or local LLM

**R3: Session State Loss**
- **Impact:** Medium - Users lose in-progress work
- **Probability:** Medium (service restart, browser close)
- **Mitigation:** Auto-save to localStorage (v2.1)
- **Contingency:** User education, copy-paste to external doc

**R4: Single Point of Failure (One Server)**
- **Impact:** High - Service completely unavailable
- **Probability:** Medium
- **Mitigation:** Backup server, docker deployment
- **Contingency:** Cloud deployment (Streamlit Cloud, Railway, Fly.io)

### Product Risks

**R5: User Adoption - Too Complex**
- **Impact:** High - Users abandon tool
- **Probability:** Low (designed for simplicity)
- **Mitigation:** Quick start guide, templates, examples
- **Contingency:** Simplify workflow, add wizard mode

**R6: Output Quality Issues**
- **Impact:** High - Users don't trust AI output
- **Probability:** Low (anti-hallucination system)
- **Mitigation:** User control, transparency, clear disclaimers
- **Contingency:** Make AI optional, manual-only mode

**R7: Scope Creep**
- **Impact:** Medium - Delays v2.1 release
- **Probability:** High (ADHD developer)
- **Mitigation:** Strict MVP scope, issue prioritization
- **Contingency:** Time-box features, defer to later versions

---

## Success Metrics

### v2.0 Success Criteria (✅ Achieved)
- [x] Zero AI hallucination in production charters
- [x] Users can edit every field manually
- [x] Quality critique provides actionable feedback
- [x] Charter generation takes <20 minutes
- [x] Cost per charter under $0.01

### v2.1 Success Criteria (Target)
- [ ] Project scaffolding completes in <2 minutes
- [ ] OpenProject tasks created automatically
- [ ] Template reduces input time by 50%
- [ ] 90% of users complete full workflow
- [ ] Zero blockers from setup paralysis

### v3.0 Success Criteria (Vision)
- [ ] Full project lifecycle in one tool
- [ ] 80% reduction in PM admin time
- [ ] Predictive project health alerts
- [ ] Portfolio management for 20+ projects
- [ ] Team adoption (5+ users)

---

## Resource Requirements

### Development Time
- **v2.1:** 40-60 hours (6-8 weeks part-time)
- **v2.2:** 60-80 hours (10-12 weeks part-time)
- **v3.0:** 120-160 hours (20-24 weeks part-time)

### Infrastructure
- **Current:** Single Ubuntu server, adequate for personal use
- **v2.1:** Same server, consider backup
- **v2.2:** Database server (PostgreSQL), possible cloud migration
- **v3.0:** Multi-server deployment, load balancer, Redis cache

### Costs
- **Current:** ~$0.08/month (OpenAI API only)
- **v2.1:** ~$0.50/month (increased usage)
- **v2.2:** ~$5-10/month (database hosting, cloud infra)
- **v3.0:** ~$20-50/month (full stack deployment)

---

## Dependencies

### External Systems
- **OpenAI API** - Required for AI features (v2.0+)
- **OpenProject** - Optional integration (v2.1+)
- **GitHub** - Optional integration (v2.2+)
- **Ollama** - Future fallback for local LLM (v2.3+)

### Python Packages
- streamlit (1.31.0) - Web framework
- openai (1.3.0) - API client
- python-dotenv (1.0.0) - Environment management
- pyyaml (6.0) - Configuration files
- pydantic (2.0+) - Data validation

---

## Lessons Learned

### What Worked Well
1. **Structured prompts prevent hallucination** - Meta-constraints + forbidden actions effective
2. **Template-based generation over AI** - User data is truth, AI only enhances
3. **Conservative temperature (0.3)** - Consistency over creativity
4. **Multi-tab workflow** - Users appreciate step-by-step guidance
5. **Accept/Reject/Edit pattern** - Full control increases trust

### What Didn't Work
1. **All-or-nothing AI generation (v1.0)** - Too risky, users want control
2. **Generic prompts** - Led to hallucination, needed structure
3. **Single-form input** - Overwhelming, multi-tab better
4. **High temperature (0.7)** - Too creative, added unwanted content

### What to Try Next
1. **Template library** - Accelerate charter creation with pre-fills
2. **Auto-save** - Prevent data loss from session issues
3. **Progress indicators** - Show completion percentage
4. **Quick start mode** - Skip AI, use defaults, fill required only
5. **Keyboard shortcuts** - Power user efficiency

---

## Appendices

### A. Technology Evaluation

**Why Streamlit?**
- Rapid prototyping (MVP in days)
- Python-native (no separate frontend/backend)
- Built-in session management
- Great for internal tools

**Limitations:**
- Not ideal for multi-user (v2.2 may require migration)
- Limited customization vs React
- Session state tied to server

**Alternatives Considered:**
- **Flask + React** - Too much boilerplate for MVP
- **FastAPI + Vue** - Modern but overkill for personal tool
- **Django** - Too heavyweight for charter generation

**Future Migration Path:**
- v2.0-2.1: Stay with Streamlit
- v2.2: Evaluate FastAPI + React if multi-user becomes priority
- v3.0: Consider full rewrite if scaling needed

### B. PM Methodology References

Based on formal project management principles from:
- PROJECT_GUIDELINES.md (user's reference document)
- PROJECT_STEP_BY_STEP.md (4-step process)
- PMI PMBOK guidelines (adapted)
- Agile/Scrum practices (where applicable)

### C. ADHD-Friendly Design Principles

1. **Eliminate Decision Fatigue** - Guided workflow, clear next steps
2. **Instant Gratification** - See progress immediately, working charter fast
3. **No Blank Page Paralysis** - Examples, templates, prompts
4. **Error Forgiveness** - Can go back, edit anything, undo
5. **External Memory** - Tool remembers, user doesn't have to
6. **Discrete Tasks** - One thing at a time, not overwhelming
7. **Visual Progress** - Tab numbers, completion indicators
8. **Time Awareness** - Show estimated time remaining

---

**Document Version:** 2.0.0  
**Last Updated:** 2024-11-06  
**Next Review:** Start of v2.1 development  
**Owner:** dollythedog
