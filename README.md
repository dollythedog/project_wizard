# Project Wizard 🧙‍♂️

AI-powered, web-based document generation for analysis, proposals, and white papers.

Project Wizard turns your notes and inputs into concise, high-quality documents using step-back prompting, suggested outlines, and unified skeleton generation to guarantee a cohesive voice without repetition.

## 🎯 Core Features

- Web UI (FastAPI + HTMX) — no CLI required
- Step-Back Clarification — the AI asks smart questions before drafting
- Suggested Outline — preview and adjust structure prior to generation
- **Section-by-Section Generation** — generates each section with word count enforcement, prevents hallucinations
- Context Passing — each section receives summary of previous sections for coherence
- Multiple Blueprints — Data Analysis, White Paper, Data Analysis Brief, Clinical Services Proposal
- Quality Review + Guided Refinement — critique the draft and apply targeted edits
- SQLite-backed projects — projects, notes, and runs are persisted

## 🚀 Quick Start

1) Install and set up

```powershell
# In repository root
make venv
make install

# Configure your AI key in .env (OpenAI or Anthropic)
notepad .env
```

2) Start the web server

```powershell
# Starts (and first kills) any stray python, then launches the app
make restart-web
# Open http://localhost:8000 (or your LAN IP: http://<your-ip>:8000)
```

Tip: Use your LAN IP if you want to open the UI from your phone or other devices on your network.

## 🧭 How it Works (Web Workflow)

1) Create a project and add notes (copy/paste text, tables, metrics)
2) Generate a document → pick a blueprint (e.g., White Paper, Data Analysis)
3) Fill the input form (title, audience, core argument, constraints, etc.)
4) Clarification step:
   - You see a Suggested Document Outline based on your inputs
   - Answer 5–7 step-back questions to lock the focus and tone
5) Draft generation:
   - The SectionAgentController generates each section sequentially with word count targets
   - Each section receives context from previous sections to maintain voice consistency
   - Automatic hallucination detection (invented names, false credentials)
   - Automatic regeneration if sections exceed word count limits
   - Progress shown in real-time with emoji indicators (🔄 generating, 📝 writing, ✓ valid, ⚠️ regenerating)
6) Review & refine:
   - Run Quality Review to see a critique and improvement suggestions
   - Use Guided Refinement to apply targeted, instruction-based edits

## 📘 Blueprints (Templates)

Blueprints live under `patterns/<name>/` and define inputs, sections, prompts, and limits.

- White Paper (`patterns/white_paper/`)
  - Purpose: reusable across business/research/technical topics
  - Sections: Executive Summary, Background & Context, Key Findings & Analysis, Implications & Recommendations
  - Features: step-back questions, suggested outline, unified skeleton, tight expansion limits (~2–3 pages)

- Data Analysis (`patterns/data_analysis/`)
  - Purpose: 2–3 page analytical report emphasizing tables/bullets
  - Sections: Executive Summary, Trends & Metrics, Key Findings, Conclusions
  - Features: unified skeleton, strict section token limits, redundancy controls

- Data Analysis Brief (`patterns/data_analysis_brief/`)
  - Purpose: 1-page visual brief for executives
  - Sections: Data Summary (table), Key Findings (bullets)
  - Features: visual-first guidance, one-page enforcement

Each blueprint consists of:
- `blueprint.json` — inputs, sections, verification questions, rubric
- `prompts.json` — step_back_prompts, outline_generation, unified_skeleton config
- `template.j2` — final rendering into markdown

## 🧠 Agents (Under the Hood)

- StepBackAgent — generates clarifying questions and a suggested outline
- **SectionAgentController** — generates each document section sequentially with:
  - Target word counts per section (e.g., Executive Summary 150 words)
  - Context passing from previous sections (prevents repetition)
  - Hallucination detection (rejects invented names/credentials)
  - Automatic regeneration with stricter constraints if over-length
- SelfRefineAgent — polishes executive summaries using self-reflection
- VerifierAgent (optional) — runs rubric/verification checks

## 🛠 Makefile Commands

```powershell
make restart-web   # Kill stray python.exe and start the web server in background
make run           # Run CLI entry points if needed (legacy)
make lint          # Ruff linter
make lint-fix      # Ruff with --fix
make test          # Run tests (if configured)
make git-push MSG="feat: update"
```

Note: The restart target is PowerShell-safe (uses `2>$null`) and avoids pager issues.

## 🧩 Troubleshooting

- Internal Server Error after template selection:
  - Check blueprint validation errors. For verification question categories use only: `factual`, `logical`, `completeness`, `alignment`.
- "AttributeError: 'list' object has no attribute 'get'" in step_back_agent:
  - Ensure `step_back_prompts` in prompts.json is an object with a `questions` array, not a top-level array.
- Port/startup issues:
  - Use `make restart-web` to kill existing python processes and start cleanly.

## 📂 Project Structure (repo)

```
project_wizard/
├── app/                      # FastAPI app, agents, services
├── patterns/                 # Blueprints (white_paper, data_analysis, ...)
├── web/                      # Routes and Jinja templates
├── Makefile                  # Developer convenience tasks
├── run_web.py                # App entrypoint
└── README.md
```

## ✍️ Author

Jonathan Ives  
Texas Pulmonary & Critical Care Consultants

---

Project Wizard — generate concise, auditable documents from real context.
