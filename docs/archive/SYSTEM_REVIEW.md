# Project Wizard Document Generation System - Architecture Review

## Overview
The system enables users to generate AI-powered documents by combining project charter data with user-uploaded notes. The workflow flows through multiple stages: template selection → note selection → user inputs → step-back questions → document draft → verification & refinement.

---

## 1. DATA COLLECTION LAYER

### Project Structure (Database)
- **Projects**: Main container (title, project_type, description, status)
- **ProjectNote**: User-created notes attached to projects
  - Fields: title, content, note_type (general/technical/decision/lesson), tags
  - Can create multiple notes and select specific ones for context
  
- **SupportingFile**: Uploaded files (PDFs, DOCX, etc.)
  - Includes: filename, file_type, summary, extracted_text
  
- **DocumentRun**: Records each generation workflow
  - Stores: user_inputs (JSON), step_back_summary, initial_draft, refined_draft, executive_summary

### Note System
- Users navigate to a project and upload notes via POST `/projects/{project_id}/notes`
- Notes are stored with metadata (type, tags) for filtering/organization
- Each note is independent but can be selected/deselected during document generation

---

## 2. CONTEXT BUILDING LAYER

### ContextBuilder Service
Location: `app/services/ai_agents/context_builder.py`

**Flow:**
```
build_context(project_id, note_ids=[selected_only])
├── _build_notes_context()        → Aggregates selected notes grouped by type
├── _build_files_context()        → Adds file summaries
├── _load_charter_from_document_runs() → Extracts charter from previous generation
└── _format_full_context()        → Creates unified AI-consumable text
```

**Key Features:**
- **Selective Note Inclusion**: When `note_ids` parameter is provided, ONLY those notes are included
  - Line 146-147 in context_builder.py: `if note_ids is not None: notes = [n for n in notes if n.id in note_ids]`
- **Note Grouping**: Notes organized by type (GENERAL, TECHNICAL, DECISION, etc.)
- **Full Content Preservation**: No truncation—AI receives complete note text
- **Charter Extraction**: Attempts to load charter from DocumentRun records, falls back to legacy charter_data
- **Token Estimation**: Rough estimate (~4 chars per token) for tracking context size

**Output: ProjectContext Dataclass**
```python
- project_id, title, type, description, status
- notes_summary, notes_count, files_summary, files_count
- charter_data (dict)
- full_context_text (formatted for AI)
- token_estimate
```

---

## 3. TEMPLATE & BLUEPRINT LAYER

### Blueprint System
Location: `app/services/blueprint_registry.py`

Each blueprint (e.g., `data_analysis`, `project_charter_lite`) contains:

```
patterns/{blueprint_name}/
├── blueprint.json      → Defines inputs, sections, verification questions, rubric
├── template.j2         → Jinja2 template for final document
└── prompts.json        → AI prompts for section-by-section generation
```

**Blueprint.json Structure:**
- **Inputs**: Form fields (text, textarea, select, multiselect)
  - Each input has: id, label, type, validation, required flag
  - Examples: "analysis_title", "dataset_description", "key_question", "metrics_of_interest"
  
- **Sections**: Document structure
  - Each section: id, title, description, order, required flag
  - Example sections: "executive_summary", "trend_analysis", "key_findings", "conclusions"
  
- **Verification Questions**: Quality checks
  - Each question: id, question_text, category, priority, expected_answer, remediation_hint
  
- **Rubric**: Scoring criteria with weights
  - Example criteria: conciseness (40%), accuracy (25%), clarity (15%), relevance (15%), completeness (5%)

**BlueprintRegistry Features:**
- Loads blueprints from disk on first access, caches in memory
- Lists available blueprints: `list_blueprints()` → returns sorted names
- Validates user inputs against blueprint requirements
- Loads prompts.json for AI generation
- Provides template path for Jinja2 rendering

---

## 4. VARIABLE COLLECTION LAYER

### Route: `/generate/{project_id}/{template_name}/inputs`
Location: `web/routes/generate.py`, lines 117-153

**Workflow:**
1. User selects template → system loads blueprint
2. System renders form with blueprint.inputs
3. User fills form with project-specific context
4. Selected note IDs passed forward (from previous step)

**Data Passed Through:**
- `selected_note_ids`: List of note IDs chosen for context
- `user_inputs`: Form data keyed by input.id
  - Example: {"analysis_title": "...", "key_question": "...", "metrics_of_interest": "..."}

**Note Handling:**
- POST request from note selection step includes `selected_notes` form array
- Line 137-138: `selected_note_ids = [int(id) for id in form_data.getlist("selected_notes")]`
- These IDs are embedded in hidden form fields and passed through each step

---

## 5. DOCUMENT GENERATION LAYER

### Route: POST `/generate/{project_id}/{template_name}/submit-inputs`
Location: `web/routes/generate.py`, lines 156-259

**Multi-Stage Process:**

**Stage 1: Input Processing**
- Separates form data into:
  - `selected_note_ids`: Which notes to include in context
  - `user_inputs`: Template-specific inputs from form
  - (Later) `responses`: Answers to clarifying questions

**Stage 2: Context Building**
```python
context_builder = ContextBuilder(registry)
context = context_builder.build_context(
    project_id, 
    note_ids=selected_note_ids if selected_note_ids else None  # FILTERED!
)
```
- Only selected notes are included in context
- If no notes selected, uses `None` → defaults to all notes

**Stage 3: Step-Back Agent (LLM)**
```python
step_back_agent = StepBackAgent(llm_client)
questions = step_back_agent.generate_questions(
    template_name,
    user_inputs=user_inputs,
    project_context=context
)
```
- Generates clarifying questions based on:
  - Blueprint for the template
  - User inputs
  - Project context (charter + selected notes)

**Stage 4: Optional Outline Preview**
- Generates suggested outline based on user inputs
- User can view/edit before proceeding

### Route: POST `/generate/{project_id}/{template_name}/submit-inputs` → `/review-outline`
Location: `web/routes/generate.py`, lines 262-335

- User answers step-back questions
- System generates refined outline using question responses
- User can edit outline before final generation

### Route: POST `/generate` (generate_draft)
Location: `web/routes/generate.py`, lines 338-504

**Final Document Generation:**

1. **Form Parsing** (lines 346-375):
   - Extract `selected_note_ids`
   - Extract `user_inputs` (prefixed with "input_")
   - Extract `responses` (prefixed with "question_")
   - Optional `refined_outline` (user-edited)

2. **Context Building** (line 386):
   ```python
   context = context_builder.build_context(
       project_id, 
       note_ids=selected_note_ids if selected_note_ids else None
   )
   ```

3. **Charter Extraction** (lines 408-416):
   - Looks for charter fields in user_inputs:
     - project_goal, success_criteria, scope_out
   - Builds charter_dict for use by section agent

4. **Section-by-Section Generation** (lines 419-426):
   ```python
   section_controller = SectionAgentController(llm_client, blueprint, pattern_name=template_name)
   sections = section_controller.generate_all_sections(
       user_inputs=user_inputs,
       prompts=prompts,
       project_context=context,
       max_regenerations=2,
       charter=charter_dict
   )
   ```
   - Generates each blueprint section independently
   - Applies constraints (max_regenerations, charter scope)
   - Uses prompts from blueprint

5. **Assembly & Storage** (lines 429-477):
   - Assembles sections into final markdown document
   - Stores in DocumentRun table:
     - user_inputs (JSON)
     - step_back_summary
     - initial_draft
     - executive_summary (refined by self-refine agent)
   - Returns draft for display

---

## 6. POST-GENERATION LAYER

### Review & Refinement Routes

**Route: GET `/document/{document_run_id}/review`**
- Verifier agent analyzes document
- Returns issues, recommendations, verification questions
- User can see what needs improvement

**Route: POST `/document/{document_run_id}/apply-refinement`**
- User can apply guided refinements
- Refinement agent processes improvement instructions
- Returns refined draft

**Route: POST `/document/{document_run_id}/condense`**
- Condenses document 40-50% by removing repetition
- Uses verification feedback to prioritize fixes
- Stores as refined_draft

---

## DATA FLOW SUMMARY

```
User Creates Project
    ↓
User Uploads Notes (multiple, tagged, typed)
    ↓
User Selects Document Template
    ↓
User Selects SPECIFIC NOTES to include → (key step!)
    ↓
User Fills Template Input Form
    ↓
System Builds Context: ONLY selected notes + charter + files
    ↓
AI Generates Clarifying Questions
    ↓
User Answers Questions (optional outline review/edit)
    ↓
System generates DRAFT
    └─→ Inputs all three data sources to section agent:
        - user_inputs (from form)
        - project_context (selected notes + charter + files)
        - prompts (from blueprint)
    ↓
Document Stored in DocumentRun table
    ↓
User can Review, Refine, Condense, Download
```

---

## KEY INSIGHTS

1. **Selective Context**: Notes are NOT all included automatically—user selects which ones via checkboxes
   - This controls information quality and token usage
   - Selection is passed through all generation stages

2. **Multi-Source Template Inputs**: User inputs vary by blueprint
   - Some templates expect charter fields (project_goal, success_criteria)
   - Others expect domain-specific fields (analysis_title, dataset_description)
   - Blueprint.json defines all valid input ids

3. **Charter as Primary Context**: The completed project charter is loaded from a previous DocumentRun
   - Serves as background/baseline context
   - Can be enriched with additional notes
   - Extracted via `_load_charter_from_document_runs()`

4. **Section-Based Generation**: Rather than generating one monolithic document, system:
   - Generates each section independently via prompts.json
   - Uses blueprint.sections to define structure
   - Allows regeneration of individual sections (max_regenerations=2)

5. **Verification & Quality**: Rubric-based scoring embedded in blueprint
   - Verifier agent checks against verification_questions
   - Rubric has weighted criteria and passing_score
   - User can request condense/refine based on feedback

---

## Questions for Requirements Discussion

Now that you understand the system, I'm ready to discuss improvements. What enhancements are you considering?

