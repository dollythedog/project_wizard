# Workflow Redesign - Blueprint Inputs First

**Date:** 2025-12-01  
**Issue:** Step-back questions were asked before collecting structured inputs  
**Solution:** Redesigned workflow to collect blueprint inputs first, then use AI for clarification

---

## Problem Identified by User

The original workflow was backwards:
```
❌ OLD: Project → Notes → Template → Questions → Draft
```

**Issue**: Step-back questions came BEFORE we collected the structured blueprint inputs (project sponsor, goals, scope, etc.). The AI was asking clarifying questions without knowing what the user had already provided.

---

## New Workflow (Correct)

```
✅ NEW: Project → Notes → Template → Input Form → Questions → Draft
```

**3-Step Process:**

### Step 1: Input Form
- Collect all **blueprint inputs** (structured form fields from blueprint.json)
- User fills 20+ fields: project_title, project_sponsor, business_need, scope, etc.
- Dynamic form generation based on input types (text, textarea, date, number, select, multiselect)

### Step 2: Clarification Questions
- AI reviews inputs + project context
- Generates 5-7 **personalized** clarifying questions
- Questions validate and refine what user already provided
- Examples: "You mentioned X, have you considered Y?" or "Can you clarify Z?"

### Step 3: Generate Draft
- DraftAgent receives:
  - Blueprint inputs (structured data)
  - Step-back clarifications (AI refinements)
  - Project context (notes, files)
- Generates complete document with all information integrated

---

## Files Changed

### 1. New Template
**`web/templates/generate/input_form.html`** (174 lines)
- Dynamically renders form fields based on blueprint.inputs
- Supports all input types: text, textarea, date, number, select, multiselect
- Beautiful 3-step progress indicator
- Client-side validation
- Responsive design

### 2. Updated Routes
**`web/routes/generate.py`**

**New routes:**
- `GET /{project_id}/{template_name}/inputs` - Show input form
- `POST /{project_id}/{template_name}/submit-inputs` - Process inputs, show questions

**Updated routes:**
- `POST /generate` - Now receives BOTH inputs + responses
- Separates `input_*` fields (Step 1) from `question_*` fields (Step 2)

### 3. Updated Templates
**`web/templates/generate/select_template.html`**
- Links now point to input form: `/generate/{project_id}/{template_name}/inputs`

**`web/templates/generate/questions.html`**
- Added 3-step progress indicator (checkmark on Step 1, active on Step 2)
- Hidden fields pass `user_inputs` from Step 1 to Step 3
- Updated styling for consistency

### 4. Updated AI Agents
**`app/services/ai_agents/step_back_agent.py`**

**`generate_questions()` method:**
- New parameter: `user_inputs: Optional[dict[str, any]]`
- Personalizes questions based on what user already provided
- Combines inputs + context for better question generation

**`_personalize_questions()` method:**
- Now accepts `user_inputs` parameter
- Formats inputs into context for LLM
- AI generates questions that build on known information

**`app/services/ai_agents/draft_agent.py`**
- Already accepts `user_inputs` parameter (no changes needed)
- Now receives populated inputs from Step 1

---

## Benefits

### 1. Logical Flow
- User provides structured data FIRST
- AI asks clarifying questions SECOND (building on inputs)
- Draft generation has complete information

### 2. Better AI Questions
- Questions are **context-aware** - AI knows what user said
- Questions **validate** inputs - "You said X, did you mean Y?"
- Questions **fill gaps** - focus on missing information

### 3. Higher Quality Documents
- Draft has structured inputs (blueprint fields)
- Draft has AI clarifications (step-back summaries)
- Draft has project context (notes, files)
- All three sources integrated

### 4. Better UX
- Clear 3-step workflow with progress indicator
- User knows exactly where they are
- Each step has a specific purpose
- No redundant information collection

---

## Example: Project Charter Workflow

### Step 1: Input Form (Blueprint Inputs)
User fills 20+ fields:
- Project Title: "Post-Discharge Patient Monitoring"
- Project Sponsor: "Dr. Sarah Johnson"
- Business Need: "Patients discharged from hospital need daily check-ins..."
- Proposed Solution: "SMS-based automated check-in system using Twilio..."
- Success Criteria: "95% patient response rate within 24 hours..."
- Scope: "In scope: SMS delivery, triage engine. Out of scope: EHR integration..."
- Risks: "Risk: Patient non-response. Mitigation: Escalation protocol..."
- *(and 13 more fields)*

### Step 2: Clarification Questions (AI Refines)
AI reviews inputs + context, asks:
1. "You mentioned HIPAA compliance - what specific PHI handling procedures will you implement?"
2. "Your scope excludes EHR integration - how will patient data be imported initially?"
3. "Success criteria mentions 95% response rate - what happens if response rate drops?"
4. "You identified patient non-response as a risk - who exactly gets escalation alerts?"
5. "The timeline shows 90 days - does this include the pilot phase you mentioned?"

### Step 3: Generate Draft
DraftAgent has:
- **Structured inputs**: All 20 blueprint fields filled
- **Clarifications**: User's answers to 5 targeted questions
- **Context**: 3 notes about requirements, tech stack, workflow

Result: Complete, professional project charter with all sections populated.

---

## Testing

To test the new workflow:

```powershell
# Start server
python run_web.py

# Navigate to project → Generate Document → Project Charter
# You'll see:
# 1. Input Form (20+ fields)
# 2. Clarification Questions (5-7 questions)
# 3. Generated Draft
```

**Expected behavior:**
- Step 1 form has all blueprint inputs
- Step 2 questions reference what you entered in Step 1
- Step 3 draft uses inputs + questions + context

---

## Future Enhancements

### Optional: Pre-fill from Context
- If project notes mention "Dr. Smith", pre-fill Project Sponsor field
- If notes mention "90 days", pre-fill estimated duration
- Saves user time, they just verify/edit

### Optional: Smart Defaults
- Auto-set charter_date to today
- Suggest project_title based on project name
- Infer project type from existing project.project_type

### Optional: Save Draft Inputs
- Store user_inputs in database during Step 1
- User can return later and continue
- No need to re-enter 20 fields

---

## Conclusion

This workflow redesign aligns with best practices:
1. **Collect structured data first** (blueprint inputs)
2. **Validate and clarify** (AI step-back questions)
3. **Generate with complete information** (inputs + clarifications + context)

User feedback: "I think it's vital that we are collecting the inputs for the MVP. The step back questions are good because they help refine the inputs before generating things."

**Status**: ✅ Implemented and ready for testing
