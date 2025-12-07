# SectionAgentController - Template-Agnostic Section Mapping Fix

**Date:** 2025-12-05  
**Status:** ✅ Fixed and Tested  
**Issue:** KeyError `'facility'` when generating productivity_pulse documents

---

## Problem

When attempting to generate a `productivity_pulse` document, the system failed with a KeyError on the variable `'facility'`. This occurred in `SectionAgentController._get_relevant_inputs()` when processing productivity_pulse section IDs.

### Root Cause

The `SectionAgentController` class contains a hardcoded `relevance_map` dictionary that maps section IDs to relevant input field names. This map was designed for the `clinical_services_proposal` template and contained section IDs like:

```python
relevance_map = {
    "executive_summary": ["specialty", "recipient_organization", "your_company_name"],
    "background_and_need": ["current_challenges", "clinical_impact", ...],
    # ... etc for 8 sections
}
```

When processing `productivity_pulse` sections (`subject_line`, `opening_paragraph`, `metrics_highlights`, `closing_paragraph`), these section IDs were **not** in the hardcoded map. The original code returned an empty dict for unknown section IDs:

```python
relevant_keys = relevance_map.get(section_id, [])  # Returns [] for unknown IDs
return {k: v for k, v in user_inputs.items() if k in relevant_keys}  # Returns {}
```

An empty dict meant **no user inputs were provided to the LLM** when generating sections. This led to template rendering failures and KeyError exceptions when the LLM tried to reference variables like `'facility'` that weren't available.

---

## Solution

### 1. Made `_get_relevant_inputs()` Template-Agnostic

Changed the logic to return **all user inputs** for unknown section IDs, while maintaining precise filtering for known section IDs:

```python
def _get_relevant_inputs(self, section_id: str, user_inputs: dict) -> dict:
    """Get relevant inputs for a section.
    
    Returns relevant inputs based on the section_id if known.
    For unknown section IDs (e.g., productivity_pulse sections), returns all inputs.
    This ensures compatibility with multiple template types.
    """
    # If section_id is in the map, use specific keys
    if section_id in relevance_map:
        relevant_keys = relevance_map[section_id]
        return {k: v for k, v in user_inputs.items() if k in relevant_keys}
    else:
        # For unknown section IDs (e.g., productivity_pulse), return all inputs
        # This allows templates to reference any input they need
        return user_inputs
```

### 2. Added Productivity_Pulse Section Guidance

Extended `_get_section_guidance()` with guidance for all 4 productivity_pulse sections:

```python
"subject_line": (
    "- Keep it concise (5-8 words max)\n"
    "- Signal this is a data/productivity report\n"
    "- Include month/period reference\n"
    "- Do NOT use sales language"
),
"opening_paragraph": (
    "- Professional greeting\n"
    "- State the reporting month/period clearly\n"
    "- Remind reader this is factual, partnership-focused reporting\n"
    "- 2-3 sentences max"
),
"metrics_highlights": (
    "- Extract 2-3 key findings from the JSON data\n"
    "- Organize by service line (ICU, Floor, Clinic, etc.)\n"
    "- Use specific numbers: visits/shift, wRVU/shift, procedures/shift\n"
    "- Use neutral language (no facility comparisons or rankings)\n"
    "- Reference the comparison_metrics user provided"
),
"closing_paragraph": (
    "- Summarize what the metrics mean for staffing planning\n"
    "- Invite questions or discussion\n"
    "- Include next steps or follow-up meeting mention\n"
    "- Close professionally and collaboratively"
),
```

### 3. Added Target Word Counts for Productivity_Pulse

Extended `_get_section_targets()` to include targets for all 4 productivity_pulse sections:

```python
"subject_line": 10,           # Very short (just the subject)
"opening_paragraph": 60,      # Context-setting intro
"metrics_highlights": 100,    # Main content with data points
"closing_paragraph": 40,      # Call to action
# Total: ~210 words (exactly 3 paragraphs as designed)
```

---

## Backward Compatibility

The fix maintains **full backward compatibility** with existing templates like `clinical_services_proposal`:

- Section IDs that exist in `relevance_map` continue to use precise filtering
- Only section IDs **not** in the map get all inputs
- Clinical proposal sections still receive only their specified inputs

### Before vs. After

| Template | Section | Before | After |
|----------|---------|--------|-------|
| clinical_services_proposal | executive_summary | 3 inputs (precise) | 3 inputs (precise) ✅ |
| clinical_services_proposal | coverage_model | 4 inputs (precise) | 4 inputs (precise) ✅ |
| productivity_pulse | subject_line | {} empty dict ❌ | 6 inputs (all) ✅ |
| productivity_pulse | metrics_highlights | {} empty dict ❌ | 6 inputs (all) ✅ |

---

## Files Modified

### `app/services/ai_agents/section_agent.py`

**Method: `_get_section_targets()`** (lines 329-352)
- Added 4 productivity_pulse section targets
- Updated docstring with usage breakdown

**Method: `_get_section_guidance()`** (lines 342-420)
- Added 4 productivity_pulse section guidance entries
- Maintained existing clinical_services_proposal guidance

**Method: `_get_relevant_inputs()`** (lines 422-463)
- Changed logic to return all inputs for unknown section IDs
- Updated docstring explaining the template-agnostic approach
- Backward compatible with existing templates

---

## Testing

Two test scripts were created to verify the fix:

### 1. `test_productivity_pulse.py` (Verified ✅)
Tests that productivity_pulse sections receive all user inputs:
- ✅ Each section receives all 6 user inputs
- ✅ Section guidance available for all 4 sections
- ✅ No KeyError exceptions

### 2. `test_clinical_proposal.py` (Verified ✅)
Tests that clinical_services_proposal maintains precise filtering:
- ✅ executive_summary receives 3 inputs (not all 17)
- ✅ coverage_model receives 4 inputs (not all 17)
- ✅ Each section receives exactly the expected count
- ✅ Backward compatibility maintained

---

## How to Test Manually

### Generate a Productivity Pulse Document

1. **Create a project** via the web UI or CLI
2. **Add some notes** (or use existing project context)
3. **Navigate to:** `/generate/` and select `productivity_pulse` template
4. **Fill form with:**
   - `json_data`: Paste service line breakdown JSON
   - `reporting_month`: e.g., "December 2025"
   - `high_profile_service_lines`: e.g., "ICU, Floor"
   - `comparison_metrics`: e.g., "avg_visits_per_shift, wrvu_per_shift"
5. **Answer step-back questions** about trends, audience, framing
6. **Generate document** → Should produce 3-4 paragraph email without errors

### Expected Output

A professional 3-paragraph productivity report:
1. **Subject line** (subject_line section)
2. **Professional greeting + context** (opening_paragraph section)
3. **Data metrics + insights** (metrics_highlights section)
4. **Call to action + close** (closing_paragraph section)

Total: ~200-300 words, no KeyError exceptions, no empty template variables.

---

## Why This Approach?

### Flexibility Over Rigidity
- ✅ Supports templates with unknown section IDs (productivity_pulse, future templates)
- ✅ Maintains precise control for established templates (clinical_services_proposal)
- ✅ No need to hardcode every future template's section IDs

### Scalability
- When adding a new template (e.g., `white_paper`, `executive_brief`), no changes needed to SectionAgentController
- New templates automatically receive all available user inputs
- Can add specific filtering later if needed

### Maintainability
- Single point of change: `relevance_map` in one method
- New section guidance added in one place
- Word count targets managed in one method

---

## Impact

### What Changed
- Productivity_pulse documents can now be generated without errors
- New templates automatically supported without code changes

### What Stayed the Same
- Existing templates (clinical_services_proposal) work identically
- All verification and validation logic unchanged
- Template generation pipeline unchanged

### Future Implications
- New templates can be added without SectionAgentController modifications
- If specific input filtering needed for future templates, add to `relevance_map`
- The system gracefully degrades to "all inputs" for unknown patterns

---

## References

- **File:** `app/services/ai_agents/section_agent.py`
- **Classes:** `SectionAgentController`
- **Methods:** `_get_relevant_inputs()`, `_get_section_guidance()`, `_get_section_targets()`
- **Related:** `app/models/blueprint.py`, `productivity_pulse/blueprint.json`

---

## Questions & Answers

**Q: Why not just add productivity_pulse to the hardcoded map?**
A: That works for one new template, but fails when adding the 5th, 10th, etc. The template-agnostic approach scales indefinitely.

**Q: Won't providing all inputs cause the LLM to get confused?**
A: No - the LLM is guided by section-specific prompts and guidance. Extra inputs just provide more context, which helps rather than hurts.

**Q: Could we break a template by providing inputs it doesn't expect?**
A: No - Jinja2 templates simply ignore variables they don't use. The approach is safe.

**Q: What if two templates have conflicting input names?**
A: Each template only uses its own inputs via Jinja2 template rendering. Other template's inputs are simply ignored.

---

**Last Updated:** 2025-12-05  
**Status:** Production Ready ✅
