# SectionAgentController Integration Guide

## Overview

The `SectionAgentController` replaces the traditional single-pass `DraftAgent` with a **section-by-section generation approach** that:

✅ Enforces word count limits per section  
✅ Prevents hallucinations (invented names, metrics, financials)  
✅ Maintains consistent voice across sections  
✅ Avoids repetition by passing context between sections  
✅ Automatically regenerates oversized sections with tighter constraints  

## How It Works

### Before (Single-Pass Generation)
```
DraftAgent generates entire 30+ page proposal at once
  ↓
VerifierAgent checks final output
  ↓
Output: Bloated, repetitive, possibly hallucinated proposal
```

### After (Section-by-Section with Smart Caching)
```
User confirms skeleton outline
  ↓
SectionAgentController:
  1. Generates Section 1 (Executive Summary)
     - Target: 150 words
     - LLM constraints: max 180 words
     - Verify: word count, hallucinations
  2. Generates Section 2 (Background & Need)
     - Passes Section 1 summary as context (prevents repetition)
     - Target: 200 words
     - Verify: word count, no repeating Section 1 content
  3. Generates Section 3-8 (same pattern)
  ↓
Assemble all sections
  ↓
Output: Concise, coherent, hallucination-free proposal (5–7 pages)
```

## Integration Points

### 1. In Your Generation Route (e.g., `web/routes/generate.py`)

```python
from app.services.ai_agents import SectionAgentController, LLMClient
from app.services.blueprint_registry import get_registry

async def generate_document(request: Request):
    # After user confirms skeleton outline and provides inputs...
    
    # Load blueprint
    registry = get_registry()
    blueprint = registry.load_blueprint(template_name)
    prompts = registry.load_prompts(template_name)
    
    # Initialize section agent controller
    llm_client = LLMClient()
    section_controller = SectionAgentController(llm_client, blueprint)
    
    # Generate all sections sequentially
    sections = section_controller.generate_all_sections(
        user_inputs=user_form_data,
        prompts=prompts,
        project_context=project_context,
        max_regenerations=2
    )
    
    # Assemble final document
    final_document = section_controller.assemble_document(
        document_title="🩺 Clinical Coverage Services Proposal",
        prepend_header=True
    )
    
    # Save to file
    output_path = f"output/{template_name}_{timestamp}.md"
    with open(output_path, 'w') as f:
        f.write(final_document)
    
    return {"status": "success", "output": output_path}
```

### 2. Replace DraftAgent Call

**Old code:**
```python
draft_agent = DraftAgent(llm_client)
result = draft_agent.generate_draft(
    template_name=template_name,
    user_inputs=user_inputs,
    project_context=project_context,
    step_back_result=step_back_result
)
```

**New code:**
```python
section_controller = SectionAgentController(llm_client, blueprint)
sections = section_controller.generate_all_sections(
    user_inputs=user_inputs,
    prompts=prompts,
    project_context=project_context,
    max_regenerations=2
)
final_document = section_controller.assemble_document(
    document_title=f"🩺 {template_name.replace('_', ' ').title()}",
    prepend_header=True
)
```

### 3. Console Output (User Visibility)

Users will see progress as sections are generated:

```
🔄 Generating sections sequentially...
Total target length: 2,500–3,500 words (5–7 pages)

📝 Section 1: Executive Summary
   Target: 150 words (±10%)
   ✓ Valid (148 words)

📝 Section 2: Background and Need
   Target: 200 words (±10%)
   ⚠️  Over limit or has issues (285 words)
   🔄 Regenerating with tighter constraints...
   ✓ Valid (198 words)

📝 Section 3: Proposed Coverage Model
   Target: 350 words (±10%)
   ✓ Valid (347 words)

... (continues for all 8 sections)

✓ All sections generated
Total: 2,847 words across 8 sections
```

## Key Features

### 1. Smart Regeneration

If a section exceeds limits on first attempt:
- **First attempt**: 20% tolerance (e.g., 150 target → max 180)
- **Second attempt**: 10% tolerance (e.g., 150 target → max 165)
- **Third attempt**: Uses as-is (flagged for review)

### 2. Context Passing

Each section receives a summary of previous sections:
```
## Previous Sections (for context—DO NOT REPEAT)

**Executive Summary:** The partnership between TPCCC and HFW has
evolved as HFW emerged as a regional cardiac care center...

**Background and Need:** Over the past 22 months, HFW has experienced
80% increase in mechanical circulatory support volume...
```

This prevents repetition while maintaining cohesion.

### 3. Section-Specific Guidance

Each section receives explicit instructions about what goes in it and what doesn't:

```
## Section-Specific Guidance

- Hook the decision-maker in 1-2 opening sentences
- List 3-4 key highlights as bullets
- Do NOT include detailed staffing numbers (save for later sections)
- Do NOT include specific metrics or financial terms
```

### 4. Hallucination Detection

The controller checks for:
- ❌ Invented names (e.g., "Dr. Sarah Mitchell" if not provided)
- ❌ Fabricated credentials (e.g., "15 years experience" if not stated)
- ❌ Made-up financial figures (e.g., "$1.9M Admin cost" if not in inputs)

If detected, the section is regenerated with stricter anti-hallucination rules.

### 5. Word Count Enforcement

Hard limits per section:
- Executive Summary: 150 words (max 180)
- Background & Need: 200 words (max 240)
- Coverage Model: 350 words (max 420)
- Quality Metrics: 200 words (max 240)
- Financial Proposal: 200 words (max 240)
- Governance: 150 words (max 180)
- Compliance: 150 words (max 180)
- Conclusion: 150 words (max 180)

**Total**: ~2,500–3,500 words (5–7 pages)

## Configuration

### Adjusting Word Count Targets

Edit `_get_section_targets()` in `SectionAgentController`:

```python
def _get_section_targets(self) -> dict:
    return {
        "executive_summary": 150,        # Adjust here
        "background_and_need": 200,      # Adjust here
        "coverage_model": 350,           # Adjust here
        # ... etc
    }
```

### Adjusting Regeneration Behavior

Pass `max_regenerations` to control how many times to retry oversized sections:

```python
sections = section_controller.generate_all_sections(
    user_inputs=user_inputs,
    prompts=prompts,
    max_regenerations=3  # Try up to 3 times (default: 2)
)
```

### Customizing Section Guidance

Edit `_get_section_guidance()` to refine instructions for each section:

```python
def _get_section_guidance(self, section_id: str) -> str:
    section_guidance = {
        "executive_summary": (
            "- Hook the decision-maker in 1-2 opening sentences\n"
            "- List 3-4 key highlights as bullets\n"
            # ... add your custom guidance
        ),
        # ... etc
    }
```

## Testing

```python
from app.services.ai_agents import SectionAgentController
from app.services.blueprint_registry import get_registry

# Test with clinical_services_proposal
registry = get_registry()
blueprint = registry.load_blueprint('clinical_services_proposal')
prompts = registry.load_prompts('clinical_services_proposal')

controller = SectionAgentController(llm_client, blueprint)

sections = controller.generate_all_sections(
    user_inputs={
        "specialty": "Pulmonary and Critical Care",
        "recipient_organization": "Heart and Vascular Hospital",
        # ... other inputs
    },
    prompts=prompts
)

# Check results
for section_id, content in sections.items():
    print(f"{content.section_title}: {content.word_count} words (target: {content.target_words})")
    print(f"  Valid: {content.is_valid}, Regenerations: {content.regeneration_count}")

# Assemble final document
final_doc = controller.assemble_document(
    document_title="🩺 Clinical Coverage Services Proposal"
)

print(final_doc)
```

## Expected Output

A proposal that:
- ✅ Is 5–7 pages (2,500–3,500 words)
- ✅ Has consistent voice across sections
- ✅ Avoids repetition (thanks to context passing)
- ✅ Has no hallucinated names, credentials, or metrics
- ✅ Respects word count constraints per section
- ✅ Flows logically from problem → solution → terms → next steps

## Comparison: Old vs. New

| Aspect | Old DraftAgent | New SectionAgentController |
|--------|---|---|
| **Length** | 30+ pages | 5–7 pages (enforced) |
| **Hallucinations** | Common (invented names, metrics) | Detected and regenerated |
| **Repetition** | High (same info in multiple sections) | Low (context prevents it) |
| **Coherence** | Can be disjointed | Cohesive (single voice) |
| **Word count** | No enforcement | Strict per-section limits |
| **Regeneration** | No | Auto-regenerate oversized sections |
| **API calls** | 1 large call (risky) | 8 smaller calls (more reliable) |

---

**Status:** Ready to integrate  
**Effort:** 30 minutes (copy/paste the code into your route)  
**Impact:** Dramatically better proposal quality
