# Proposal Type Selector - Integration Guide

**Purpose:** Enable users to choose proposal type when generating a proposal (Clinical Services vs. Generic Business Proposal)

**Status:** Implementation-Ready

---

## User Experience

### Current Flow (Single Proposal Type)
```
User: "Generate proposal"
  ↓
  → Uses: patterns/proposal/
  → Output: Generic business proposal (5–7 pages)
```

### New Flow (Type Selector)
```
User: "Generate proposal"
  ↓
  → Question: "What type of proposal?"
     - [ ] Clinical Services Proposal (healthcare staffing/coverage)
     - [ ] Generic Business Proposal (any business service)
     - [ ] Programmatic Proposal (programs like PERT, ELSO) [coming soon]
  ↓
  → User selects: "Clinical Services Proposal"
  ↓
  → Uses: patterns/clinical_services_proposal/
  → Output: Structured clinical proposal with baseline/target metrics, staffing table (5–7 pages)
```

---

## Implementation Steps

### 1. Add Proposal Type Input to Blueprint Selection

In your proposal generation flow (likely in `generate.py` route or form handler), add a type selector **before** asking for inputs:

```python
# Pseudo-code
proposal_type = ask_user(
    "What type of proposal would you like to generate?",
    options=[
        ("clinical_services", "🩺 Clinical Services Proposal (staffing/coverage for hospitals)"),
        ("generic_business", "💼 Generic Business Proposal (any business service)"),
        # ("programmatic", "⚙️ Programmatic Proposal (PERT, ELSO, rapid response teams)") # Coming soon
    ]
)

# Set blueprint name based on selection
blueprint_name = {
    "clinical_services": "clinical_services_proposal",
    "generic_business": "proposal",
    "programmatic": "programmatic_proposal",
}[proposal_type]

# Load appropriate blueprint and continue with generation
```

### 2. Update DocumentGenerator to Handle Type Routing

When calling `DocumentGenerator.generate_from_blueprint()`, pass the selected blueprint name:

```python
# Load correct blueprint
blueprint_registry = get_registry()
blueprint = blueprint_registry.load_blueprint(blueprint_name)

# Generate document using appropriate blueprint
result = document_generator.generate_from_blueprint(
    blueprint_name=blueprint_name,
    context=user_inputs,
    output_path=output_file
)
```

### 3. Update Step-Back Agent Questions

The StepBackAgent should ask **type-specific questions** based on selection:

```python
# In step_back_agent.py or route handler
step_back_prompts = blueprint_registry.load_prompts(blueprint_name)
step_back_config = step_back_prompts.get("step_back_prompts", {})

# Ask type-specific clarifying questions
questions = step_back_config.get("questions", [])
# For clinical: asks about baseline metrics, staffing model, etc.
# For generic: asks about client, problem, solution, team, etc.
```

---

## Directory Structure

After implementation:

```
patterns/
├── proposal/                          # Original generic proposal
│   ├── blueprint.json
│   ├── template.j2
│   ├── prompts.json
│   ├── README.md
│   ├── PROPOSAL_QUALITY_GUIDE.md
│   └── IMPROVEMENTS_2025-12-03.md
│
├── clinical_services_proposal/        # NEW: Clinical/staffing proposals
│   ├── blueprint.json
│   ├── template.j2
│   ├── prompts.json
│   └── README.md
│
├── programmatic_proposal/             # FUTURE: Program development proposals
│   ├── blueprint.json
│   ├── template.j2
│   ├── prompts.json
│   └── README.md
│
└── PROPOSAL_TYPE_SELECTOR.md          # This file
```

---

## Key Benefits of This Approach

| Benefit | Why |
|---------|-----|
| **Clean separation** | Each proposal type lives in its own directory; no clutter |
| **Type-specific inputs** | Clinical proposals ask about baseline metrics; generic proposals ask about client pain points |
| **Type-specific prompts** | AI agents have specialized instructions for each proposal type |
| **Maintainability** | Easy to add new proposal types without affecting existing ones |
| **User clarity** | Users understand what type of proposal they're generating upfront |

---

## Testing Checklist

Before deploying proposal type selector:

- [ ] **Type Selector Display** - UI correctly shows proposal type options
- [ ] **Clinical Services Proposal** - Generate complete clinical proposal; verify:
  - 8 sections present (Executive Summary → Conclusion)
  - Baseline and target metrics populated in table format
  - Staffing model includes specific counts and schedule
  - Financial proposal shows pricing table
  - Total length 5–7 pages
  - Zero hallucinations (no invented team names)
- [ ] **Generic Business Proposal** - Generate standard proposal; verify existing functionality still works
- [ ] **Form Routing** - Correct blueprint is selected and loaded based on user choice
- [ ] **Prompts Routing** - Step-back agent asks type-appropriate questions

---

## Future Expansion

### Programmatic Proposal (Phase 2)

Create `patterns/programmatic_proposal/` for program development proposals:
- PERT (Pulmonary Embolism Response Team)
- ELSO (rapid response for extracorporeal life support)
- Rapid response team formalization
- Multidisciplinary program establishment

**Sections:** Executive Summary → Rationale → Program Structure → Governance → Deliverables → KPIs → Resources → Reporting → Next Steps

**Key Differences from Clinical Services Proposal:**
- Focus on program development, not staffing
- Governance structure more emphasized
- KPIs are program-specific (activation time, intervention rate, etc.)
- Funding model is shared cost (hospital + provider org)

---

## File Changes Needed

### To Implement Type Selector

1. **Update proposal generation route** (likely `web/routes/generate.py`)
   - Add type selector question before blueprint inputs
   - Route to correct blueprint based on selection

2. **No changes needed to:**
   - `patterns/proposal/` (existing generic proposal)
   - `app/services/document_generator.py` (already supports blueprint routing)
   - `app/services/ai_agents/` (agents already use loaded blueprint/prompts)

3. **New files added:**
   - `patterns/clinical_services_proposal/blueprint.json`
   - `patterns/clinical_services_proposal/template.j2`
   - `patterns/clinical_services_proposal/prompts.json`
   - `patterns/clinical_services_proposal/README.md`
   - `patterns/PROPOSAL_TYPE_SELECTOR.md` (this file)

---

## Example: Clinical Services Proposal Generation Flow

```
User clicks "Generate Proposal"
  ↓
UI asks: "Proposal Type?"
  - [ ] Clinical Services (🩺)
  - [ ] Generic Business (💼)
User selects: Clinical Services
  ↓
Backend sets: blueprint_name = "clinical_services_proposal"
  ↓
StepBackAgent loads prompts from clinical_services_proposal/prompts.json
  ↓
StepBackAgent asks:
  "What is the specialty/service line?"
  "What is the current baseline for ICU LOS, mortality, consult turnaround?"
  "What is your proposed staffing model?"
  [etc.]
  ↓
User provides inputs
  ↓
DraftAgent loads clinical_services_proposal/blueprint.json
  ↓
DraftAgent generates proposal using skeleton-of-thought strategy
  ↓
Proposal includes:
  - Section 1: Executive Summary (150–200 words)
  - Section 2: Background with baseline metrics
  - Section 3: Coverage Model with staffing table
  - Section 4: Metrics table (baseline → target)
  - Section 5: Financial table
  - Section 6-8: Governance, Compliance, Conclusion
  ↓
VerifierAgent checks:
  ✓ All metrics from provided data (no estimates)
  ✓ Staffing clearly specified
  ✓ No invented names/credentials
  ✓ All sections unique purpose
  ✓ Document 5–7 pages
  ↓
Output: Professional 5–7 page clinical proposal
```

---

## Implementation Priority

**Phase 1 (DONE):**
- Create clinical_services_proposal blueprint, template, prompts
- Document in README and quality guide

**Phase 2 (NEXT):**
- Add type selector UI to proposal generation flow
- Update route handler to route based on selection
- Test end-to-end generation for both types

**Phase 3 (FUTURE):**
- Create programmatic_proposal blueprint
- Add type selector option for it
- Test all three proposal types

---

## Questions for Implementation

1. **Where is the proposal generation form?** (which file/route?)
2. **How is the form presented to users?** (web form, CLI, API?)
3. **Should type selector be mandatory, or default to generic?** (recommended: mandatory, shows options)
4. **Any other proposal types you anticipate needing?**

---

**Status:** Ready to implement  
**Effort:** 2–4 hours (mostly UI routing, logic already exists)  
**Risk:** Low (additive change, doesn't break existing proposal flow)

---

*Last Updated: 2025-12-03*
