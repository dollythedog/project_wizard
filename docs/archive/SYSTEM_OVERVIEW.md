# Project Wizard: Refine Agent System Overview

## 🎯 Core Purpose

Project Wizard is an **AI-powered document generation system** that transforms raw project inputs into high-quality professional documents through a multi-stage agentic pipeline. The system is designed to:

1. **Capture project context** (notes, files, charter data)
2. **Clarify requirements** through step-back prompting
3. **Generate high-quality drafts** using skeleton-of-thought or field-enrichment strategies
4. **Refine outputs** through iterative improvement
5. **Verify quality** through rubric-based assessment

---

## 📐 System Architecture

### High-Level Flow

```
Project Context (Charter + Notes + Files)
    ↓
[User fills blueprint form with specific project details]
    ↓
[Step-Back Agent] → Generates clarifying questions
    ↓
[User answers clarifying questions]
    ↓
[Step-Back Agent] → Synthesizes responses into summary
    ↓
[Draft Agent] → Generates complete document
    ↓
[Self-Refine Agent] → Iteratively improves summary
    ↓
[Verifier Agent] → Quality assessment (optional)
    ↓
[Final Document Output] → Display, download, or edit
```

---

## 🔧 Core Components

### 1. **LLMClient** (`app/services/ai_agents/llm_client.py`)

**Purpose:** Unified interface to OpenAI or Anthropic APIs

**Key Features:**
- Auto-detects AI provider based on `.env` keys
- Supports both OpenAI (GPT-4) and Anthropic (Claude)
- Retry logic with exponential backoff
- Token counting and latency tracking
- Configurable temperature and max_tokens

**Usage:**
```python
llm_client = LLMClient()  # Auto-detects provider
response = llm_client.generate(
    prompt="Your prompt here",
    system_message="You are...",
    temperature=0.7,
    max_tokens=4000
)
# Returns: LLMResponse(content, model, tokens_used, finish_reason, latency_ms)
```

**Configuration:**
- `.env` file sets `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Models: GPT-4 (OpenAI) or Claude 3 (Anthropic)

---

### 2. **ContextBuilder** (`app/services/ai_agents/context_builder.py`)

**Purpose:** Aggregates all project information into a single context for AI consumption

**What it includes:**
- **Project metadata:** Title, type, status, description
- **Notes:** All project notes (general, technical, decision, lesson)
- **Files:** Supporting documents with summaries
- **Charter data:** From most recent completed project charter
- **Charter markdown:** Full completed charter document (for rich context)

**Process:**
1. Queries database for all project-related information
2. Formats into readable markdown text
3. Estimates token count
4. Returns `ProjectContext` object with full formatted text

**Usage:**
```python
context_builder = ContextBuilder(registry)
context = context_builder.build_context(
    project_id=1,
    include_notes=True,
    include_files=True,
    include_charter=True,
    note_ids=[1, 3, 5]  # Optional: specific notes only
)
# Returns: ProjectContext with full_context_text, token_estimate, etc.
```

**Key Design:**
- Includes ALL project context (not truncated) so AI has complete information
- Groups notes by type for better organization
- Includes completed charter markdown as background context
- Token estimate helps manage API costs

---

### 3. **StepBackAgent** (`app/services/ai_agents/step_back_agent.py`)

**Purpose:** Uses step-back prompting to clarify project requirements BEFORE document generation

**Two-Phase Process:**

#### Phase 1: Generate Questions
```python
questions = step_back_agent.generate_questions(
    template_name="project_charter",
    user_inputs=form_data,  # What user entered in form
    project_context=context  # Project background
)
# Returns: list of 5-7 personalized clarifying questions
```

- Loads default questions from blueprint
- If context exists, personalizes questions to the specific project
- Uses LLM to adapt questions based on project type and existing inputs

#### Phase 2: Process Responses
```python
step_back_result = step_back_agent.process_responses(
    template_name="project_charter",
    responses={
        "Why is this project strategic?": "Because...",
        "What are key success metrics?": "..."
    },
    project_context=context
)
# Returns: StepBackResult(questions, summary, context_used)
```

- Takes user's answers to clarifying questions
- Synthesizes into a strategic summary (2-3 paragraphs)
- This summary becomes the "true problem statement" for document generation

**Why This Matters:**
- Users often provide incomplete or unclear initial inputs
- Step-back prompting forces explicit thinking about requirements
- The synthesized summary ensures AI drafts address real needs
- Reduces hallucinations and off-target content

---

### 4. **DraftAgent** (`app/services/ai_agents/draft_agent.py`)

**Purpose:** Generates high-quality document drafts using AI

**Two Generation Strategies:**

#### Strategy A: Field Enrichment (Default)
```
User Input → AI Enrichment → Template Rendering → Markdown Output
```

1. **Enrich user inputs:** AI expands brief answers into 2-3 paragraph detailed content
   - Uses project context and step-back summary for detail
   - Preserves arrays/lists (from multiselect fields) as-is
   - Avoids hallucination through "factual grounding" constraints

2. **Render template:** Jinja2 template populated with enriched values

3. **Output:** Formatted markdown document

**Example:** User provides "We need to improve patient outcomes" → AI enriches to full paragraph with specific metrics

#### Strategy B: Skeleton-of-Thought (For Complex Documents)
```
1. Generate Skeleton
   ├─ Section title
   ├─ 3-5 key points per section
   └─ Data to include

2. Expand Each Section
   ├─ Take skeleton key points
   ├─ Generate 2-3 paragraphs per point
   └─ Include tables, metrics, formatting

3. Assemble Document
   └─ Combine expanded sections with headers
```

**Anti-Hallucination Safeguards:**
- "FACTUAL GROUNDING" section lists ONLY data from user inputs
- AI must cite from factual grounding or use generic language
- Verification checklist: Is this name/number/date/program in FACTUAL GROUNDING?
- Critical Rules enforce: NO invented names, numbers, dates, programs

**Usage:**
```python
draft_result = draft_agent.generate_draft(
    template_name="project_charter",
    user_inputs=enriched_form_data,
    project_context=context,
    step_back_result=step_back_result
)
# Returns: DraftResult(content, model_used, tokens_used, sections_generated)
```

---

### 5. **SelfRefineAgent** (`app/services/ai_agents/self_refine_agent.py`)

**Purpose:** Iteratively refines analytical summaries through self-critique

**Three-Step Process:**

1. **Initial Distillation** (Iteration 1)
   - Takes full analytical summary (e.g., step-back result)
   - Distills to 4-6 high-yield sentences
   - Focuses on: core problem, key decisions, critical risks

2. **Evaluate** (Iterations 2+)
   - LLM evaluates current summary against original
   - Questions: What's missing? What's incorrect? What can improve?
   - Scores `needs_improvement` flag

3. **Refine** (If needed)
   - Based on evaluation feedback, improve the summary
   - Maintain 4-6 sentence constraint
   - Repeat until quality threshold met (max 3 iterations)

**Usage:**
```python
refinement_result = self_refine_agent.refine_summary(
    original_summary=step_back_result.summary,
    context=context.full_context_text
)
# Returns: RefinementResult(refined_summary, iterations_performed, improvements_made)
```

**Result:** Ultra-concise executive summary for decision-makers

---

### 6. **VerifierAgent** (`app/services/ai_agents/verifier_agent.py`)

**Purpose:** Quality assessment against blueprint rubrics

**Process:**
1. Load rubric from blueprint (criteria, weights, descriptions)
2. Score document on each criterion (1-5 scale)
3. Calculate weighted overall score
4. Identify strengths and weaknesses
5. Generate specific improvement suggestions

**Rubric Example:**
```json
{
  "criteria": [
    {"id": "clarity", "name": "Clarity", "weight": 0.25, "description": "..."},
    {"id": "completeness", "name": "Completeness", "weight": 0.25, "description": "..."},
    {"id": "alignment", "name": "Strategic Alignment", "weight": 0.25, "description": "..."},
    {"id": "feasibility", "name": "Feasibility", "weight": 0.25, "description": "..."}
  ]
}
```

**Usage:**
```python
verification = verifier_agent.verify_document(
    template_name="project_charter",
    document_content=draft_result.content,
    project_context=context,
    user_inputs=user_inputs
)
# Returns: VerificationResult with overall_score (1.0-5.0), 
#          detailed scores, strengths, weaknesses, improvements
```

**Output:** JSON structure with scores and actionable feedback

---

## 📊 Blueprint System

Blueprints define document types and govern the generation process.

### Blueprint Structure

```json
{
  "name": "project_charter",
  "version": "1.0.0",
  "description": "Professional project charter with business case and approach",
  
  "inputs": [
    {"id": "goal", "type": "textarea", "label": "Project Goal", "required": true},
    {"id": "problem", "type": "textarea", "label": "Problem/Opportunity"},
    {"id": "approach", "type": "textarea", "label": "Proposed Approach"}
  ],
  
  "sections": [
    {
      "id": "executive_summary",
      "title": "Executive Summary",
      "order": 1,
      "description": "High-level overview for decision-makers"
    },
    {
      "id": "business_case",
      "title": "Business Case",
      "order": 2,
      "subsections": [...]
    }
  ],
  
  "generation_strategy": "field_enrichment",  // or "skeleton_of_thought"
  
  "rubric": {
    "criteria": [...]
  }
}
```

### Prompts Configuration

Each blueprint has a `prompts.json` file:

```json
{
  "step_back_prompts": {
    "identity": "You are a project clarification specialist...",
    "questions": ["Q1", "Q2", ...],
    "output_instructions": "Synthesize responses into a clear summary..."
  },
  
  "draft_generation": {
    "identity": "You are a professional PM document writer...",
    "goals": ["Create professional-grade documents..."],
    "quality_standards": {"clarity": "...", "completeness": "..."},
    "rules": {"do": [...], "do_not": [...]},
    "tone_and_style": {"style": "professional", "audience": "executives"}
  },
  
  "skeleton_generation": {
    "identity": "You are a document architect..."
  }
}
```

---

## 🌐 Web Interface Workflow

### Route: `/generate`

#### Step 1: Select Template
```
GET /generate?project_id=1
→ select_template.html
→ Shows grid of available templates (charter, proposal, work_plan, etc.)
```

#### Step 2: Select Context Notes
```
GET /generate/{project_id}/{template_name}/select-notes
→ select_notes.html
→ Checkbox list of all project notes
→ User selects which notes to include in context
```

#### Step 3: Fill Blueprint Input Form
```
GET /generate/{project_id}/{template_name}/inputs
→ input_form.html
→ Dynamic form based on blueprint.inputs
→ Text fields, textareas, multiselect, etc.
→ User provides initial project information
```

#### Step 4: Generate Step-Back Questions
```
POST /generate/{project_id}/{template_name}/submit-inputs
→ Runs StepBackAgent.generate_questions()
→ questions.html
→ Displays 5-7 clarifying questions
→ User answers each question
```

#### Step 5: Generate Draft
```
POST /generate/generate
→ Runs full pipeline:
   1. StepBackAgent.process_responses() → step_back_summary
   2. DraftAgent.generate_draft() → draft_content
   3. SelfRefineAgent.refine_summary() → executive_summary
→ Saves DocumentRun to database
→ draft.html
→ Displays final document with rendering + markdown view
```

#### Step 6 (Optional): Review & Refine
```
GET /generate/document/{document_run_id}/review
→ Runs VerifierAgent.verify_document()
→ review.html
→ Shows scores, strengths, weaknesses, improvements

POST /generate/document/{document_run_id}/condense
→ Uses VerifierAgent feedback
→ Condenses document by 40-50%
→ Removes repetition, tightens paragraphs
```

#### Step 7: Download
```
GET /generate/download/{document_run_id}
→ Returns markdown file download
→ Filename: {project_title}_{template_name}_{date}.md
```

---

## 📦 Database Schema (SQLModel)

### Project
```python
- id: int (PK)
- title: str
- project_type: str  # software_mvp, clinical_workflow, etc.
- description: str
- status: str  # initiating, planning, executing, closing
- charter_data: str (JSON)  # Legacy field
- created_at: datetime
- updated_at: datetime
- notes: list[ProjectNote]  # Relationship
- document_runs: list[DocumentRun]  # Relationship
```

### ProjectNote
```python
- id: int (PK)
- project_id: int (FK)
- title: str
- content: str (markdown)
- note_type: str  # general, technical, decision, lesson
- created_at: datetime
```

### DocumentRun
```python
- id: int (PK)
- project_id: int (FK)
- template_name: str  # project_charter, proposal, etc.
- user_inputs: str (JSON)  # Original form inputs
- step_back_summary: str  # From StepBackAgent
- initial_draft: str (markdown)  # From DraftAgent
- executive_summary: str  # From SelfRefineAgent
- refined_draft: str (markdown)  # Optional: condensed version
- status: str  # pending, in_progress, completed
- created_at: datetime
- completed_at: datetime
```

---

## 🎯 Key Design Decisions

### 1. **Three-Layer Pipeline**

```
INPUT CLARIFICATION          DRAFT GENERATION         REFINEMENT
      ↓                             ↓                      ↓
Step-Back Questions    Field Enrichment/Skeleton   Self-Critique Loop
      ↓                   + Template Rendering            ↓
User Answers              + Context Injection        4-6 Sentence Summary
      ↓                             ↓                      ↓
Strategic Summary      Full Document Draft        High-Yield Summary
```

### 2. **Context-Rich Generation**

- ALL project context (notes, charter, files) included in every AI call
- No truncation of notes - AI gets complete information
- Full charter markdown available for background context
- Users select which notes to include for each generation

### 3. **Anti-Hallucination Strategy**

- **Factual Grounding:** AI only uses data from user inputs
- **Verification Checklist:** Every name, number, date must be in FACTUAL GROUNDING
- **Generic Language Fallback:** "significant" instead of invented percentage
- **Explicit Rules:** DO/DO NOT instructions in system message
- **Temperature Control:** Lower temp (0.3-0.5) for factual tasks

### 4. **Agentic Techniques**

- **Step-Back Prompting:** Clarify before drafting
- **Skeleton-of-Thought:** Complex documents broken into outlines then expanded
- **Self-Critique:** Iterative improvement through evaluation
- **Chain of Verification:** Quality scoring against rubrics

### 5. **Separation of Concerns**

- **Agents:** Specialized AI roles (step-back, draft, verify, refine)
- **Blueprints:** Template definitions + prompts separate from code
- **Registry:** Blueprint and project lookups centralized
- **Routes:** Web interface separate from business logic

---

## 🔄 Quality Assurance Workflow

### Automatic (Every Generation):
1. ✅ Field validation in blueprint inputs
2. ✅ Step-back prompting for requirement clarification
3. ✅ AI enrichment of user inputs with context
4. ✅ Template rendering with validation
5. ✅ Self-refinement of summary (3 iterations max)

### Optional (User-Initiated):
1. ✅ VerifierAgent quality scoring (against rubric)
2. ✅ Document condensation (remove 40-50% of content)
3. ✅ Manual editing in web UI

---

## 📈 Token Management

### Estimation
- ~4 characters per token (rough estimate)
- ProjectContext includes token_estimate
- Each LLMResponse includes tokens_used

### Cost Optimization
- Step-back questions: ~500-1000 tokens
- Input enrichment: ~4000-6000 tokens
- Skeleton generation: ~8000-16000 tokens (can truncate if needed)
- Section expansion: ~2000-3000 tokens per section
- Verification: ~10000-20000 tokens (depends on doc size)

### Retry Logic
- Automatic retries (3x) with exponential backoff
- Handles rate limits and transient errors
- Logs attempt number for debugging

---

## 🚀 Extending the System

### Adding a New Template

1. **Create blueprint:** `patterns/my_template/blueprint.json`
2. **Create prompts:** `patterns/my_template/prompts.json`
3. **Create template:** `patterns/my_template/template.j2` (Jinja2)
4. **Register:** Automatically loaded by BlueprintRegistry
5. **Test:** Via web UI or CLI

### Adding a New Agent

1. Create file: `app/services/ai_agents/new_agent.py`
2. Inherit base patterns (LLMClient, dataclass results)
3. Use StepBackAgent/DraftAgent as reference
4. Import in routes and add to pipeline

### Adding Quality Criteria

1. Update blueprint rubric
2. VerifierAgent automatically scores new criteria
3. Add to verification_result output

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `app/services/ai_agents/llm_client.py` | LLM API wrapper |
| `app/services/ai_agents/context_builder.py` | Project context aggregation |
| `app/services/ai_agents/step_back_agent.py` | Requirement clarification |
| `app/services/ai_agents/draft_agent.py` | Document generation |
| `app/services/ai_agents/self_refine_agent.py` | Summary refinement |
| `app/services/ai_agents/verifier_agent.py` | Quality verification |
| `web/routes/generate.py` | Web interface orchestration |
| `patterns/*/blueprint.json` | Template definitions |
| `patterns/*/prompts.json` | AI system messages |
| `patterns/*/template.j2` | Document templates |

---

## 📝 Example: Full Workflow

### User Flow

```
1. User creates project "Healthcare MVP"
2. User adds 3 notes: problem statement, user stories, technical constraints
3. User navigates to: /generate?project_id=1
4. Selects template: "Project Charter"
5. Selects all 3 notes for context
6. Fills form:
   - Goal: "Improve patient engagement post-discharge"
   - Problem: "45% readmissions within 30 days"
   - Approach: "SMS-based monitoring system"
7. System generates 7 clarifying questions
8. User answers: specific metrics, timeline, stakeholders, success criteria
9. System generates charter:
   - StepBackAgent synthesizes answers into strategic summary
   - DraftAgent enriches inputs + synthesizes into full charter
   - SelfRefineAgent creates 4-6 sentence executive summary
   - Renders final markdown
10. User sees: rendered HTML + raw markdown
11. User can: download, edit, review quality, condense, or regenerate
```

### Backend Processing

```
Step 1: ContextBuilder
├─ Query Project #1
├─ Get 3 selected notes
├─ Load charter data (if exists)
├─ Format into 2000 tokens of context text
└─ Return ProjectContext

Step 2: StepBackAgent.generate_questions()
├─ Load blueprint + prompts
├─ Call LLM with default questions + context
├─ Return 7 personalized questions

Step 3: StepBackAgent.process_responses()
├─ Take user's answers to 7 questions
├─ Call LLM to synthesize into 2-3 paragraph summary
├─ Return StepBackResult

Step 4: DraftAgent.generate_draft()
├─ Branch: Field Enrichment
│  ├─ Call LLM to enrich each input (text, textarea fields)
│  ├─ Preserve arrays (multiselect)
│  └─ Render Jinja2 template with enriched values
├─ Or Branch: Skeleton-of-Thought
│  ├─ Generate skeleton (outline)
│  ├─ Expand each section
│  └─ Assemble document
└─ Return DraftResult (full markdown)

Step 5: SelfRefineAgent.refine_summary()
├─ Take StepBackAgent summary
├─ Iteration 1: Distill to 4-6 sentences
├─ Iterations 2+: Evaluate + refine
└─ Return 4-6 sentence executive summary

Step 6: Save DocumentRun
├─ Create document_runs record
├─ Store user_inputs, step_back_summary, initial_draft, etc.
└─ Return for display

Step 7: Display
├─ Show rendered HTML + raw markdown
├─ Show summary + model used + tokens
└─ Offer download, edit, review, condense options
```

---

## 🔐 Security Considerations

### PHI/Data Protection
- **No AI Logging:** LLM payloads not logged to disk
- **FACTUAL GROUNDING:** Only data in user inputs sent to AI
- **No Data Leakage:** Project notes can contain sensitive info, but control what's included
- **Environment Variables:** API keys in .env (never in code)

### API Safety
- **Rate Limiting:** Retry logic with exponential backoff
- **Error Handling:** Graceful degradation if API unavailable
- **Token Limits:** Per-document token estimates prevent runaway costs

---

## 📊 Quality Metrics

### Output Scoring
- **Overall Score:** Weighted average of 4 criteria (1.0-5.0)
- **Ready for Approval:** Score ≥ 4.0
- **Specific Feedback:** For each criterion

### Generation Efficiency
- **Tokens/Document:** Tracked and reported
- **Latency:** API response time measured
- **Iterations:** Self-refine iterations to reach quality threshold

---

This system represents a sophisticated AI pipeline optimized for professional document generation with built-in quality assurance, anti-hallucination safeguards, and context-aware personalization.
