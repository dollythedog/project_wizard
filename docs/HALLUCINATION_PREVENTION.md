# Hallucination Prevention in Productivity Pulse Metrics

**Date:** 2025-12-06  
**Status:** ✅ Fixed  
**Problem:** LLM was fabricating assignment names and invented metrics instead of using actual data

---

## The Problem

When generating the `metrics_highlights` section for productivity_pulse documents, the LLM was producing output like:

```
ICU service lines show consistent staffing patterns across our network.
HFW Bloxom Call averaged 12.3 visits/shift with 14.2 wRVU/shift,
while HSW ICU SW tracked at 10.1 visits/shift and 11.8 wRVU/shift.
```

These assignment names (**HFW Bloxom Call**, **HSW ICU SW**, etc.) and specific metrics (**12.3 visits/shift**) were **fabricated by the LLM**, not from the actual JSON data provided.

### Why This Happened

1. The LLM was told: "Extract 2-3 key findings from the JSON data"
2. But the JSON data was provided as a raw string in the prompt
3. The LLM didn't actually parse or understand the structure
4. Gaps in understanding were filled with plausible-sounding fabrications
5. No guard rails prevented mentioning assignment/facility names

---

## The Solution

### 1. Parse JSON Data Server-Side

New method `_build_metrics_data_extract()` in `SectionAgentController`:

```python
def _build_metrics_data_extract(self, user_inputs: dict) -> str:
    """Build an authoritative metrics extract from provided JSON data."""
    # Parse the JSON
    records = json.loads(user_inputs.get("json_data"))
    
    # Group by service line (facility_class), calculate stats
    grouped: Dict[str, Dict[str, list]] = {}
    for rec in records:
        service_line = rec.get("facility_class")
        # Collect all metric values for this service line
        grouped[service_line][metric_key].append(value)
    
    # Build authoritative table with ranges and means
    for service_line, metrics in grouped.items():
        # e.g., "- ICU (network-level):
        #        • avg_visits_per_shift: values [7.2, 8.5, 9.1] (range: 7.2–9.1; mean: 8.3)"
```

### 2. Inject Parsed Data Into Prompt

For the `metrics_highlights` section:

```python
if section.id == "metrics_highlights" and user_inputs.get("json_data"):
    data_extract = self._build_metrics_data_extract(user_inputs)
    parts.extend([
        "## Parsed Data (authoritative — use ONLY these numbers)",
        "",
        data_extract,
        ""
    ])
```

The LLM now sees a structured, parsed data table instead of raw JSON.

### 3. Strengthen Section Guidance

Updated `_get_section_guidance()` for `metrics_highlights`:

```python
"metrics_highlights": (
    "CRITICAL: Use ONLY numbers from 'Parsed Data' section above. "
    "Do NOT fabricate numbers.\n"
    "- Never name specific assignments, facilities, or units\n"
    "- Refer only to service line types (e.g., 'ICU assignments')\n"
    "- Present ranges and means from the data\n"
    "- Use neutral language; avoid judgmental terms"
)
```

### 4. Add Explicit Anti-Hallucination Instruction

In the prompt instructions:

```
7a. For this section: use ONLY the numbers in 'Parsed Data' above;
    if a number is not present there, do NOT include it.
    Do NOT name specific assignments or facilities — 
    refer only to service lines (e.g., ICU, Floor).
7b. Aim for {target_words} words; do NOT exceed {max_words}
```

---

## How It Works

### Before (Hallucination-Prone)

```
USER INPUTS:
json_data: [{...raw JSON...}]

PROMPT TO LLM:
"Extract 2-3 key findings from this JSON data..."
[raw JSON blob]

LLM RESPONSE:
"HFW Bloxom Call averaged 12.3 visits/shift..."  ← FABRICATED
```

### After (Grounded in Actual Data)

```
USER INPUTS:
json_data: [{...raw JSON...}]

PROMPT TO LLM:
"## Parsed Data (authoritative — use ONLY these numbers)
- ICU (network-level):
  • avg_visits_per_shift: values [7.2, 8.5, 9.1, ...] (range: 7.2–9.1; mean: 8.3)
  • wrvu_per_shift: values [8.1, 9.2, 10.3, ...] (range: 8.1–10.3; mean: 9.2)
- Floor (network-level):
  • avg_visits_per_shift: values [5.1, 6.2, 7.3, ...] (range: 5.1–7.3; mean: 6.2)
  ...

CRITICAL: Use ONLY numbers from 'Parsed Data' above.
Never name specific assignments, facilities, or units.
Refer only to service lines (e.g., 'ICU assignments show 7.2–9.1 visits/shift')."

LLM RESPONSE:
"ICU assignments show 7.2–9.1 visits/shift across our network,
with an average of 8.3 visits/shift. Floor assignments average
6.2 visits/shift, ranging from 5.1–7.3."  ← GROUNDED IN ACTUAL DATA
```

---

## Example Output Comparison

### Before (Hallucinatory)
❌ Names specific assignments: "HFW Bloxom Call averaged 12.3 visits/shift"  
❌ Makes up numbers not in data: "14.2 wRVU/shift"  
❌ Creates ranking/comparison: "HSW ICU SW tracked at 10.1"  

### After (Data-Grounded)
✅ References only service lines: "ICU assignments show..."  
✅ Uses actual statistics: "averaging 8.3 visits/shift, ranging from 7.2–9.1"  
✅ No unfair comparisons: All metrics presented as aggregates  

---

## Implementation Details

### Method: `_build_metrics_data_extract()`

**Location:** `app/services/ai_agents/section_agent.py`, line 345

**Process:**
1. Parse `json_data` from user inputs
2. Extract metric keys from `comparison_metrics` input (comma-separated)
3. Group all records by `facility_class` (service line type)
4. For each metric in each service line:
   - Collect all numeric values
   - Calculate min, max, mean
   - Format as readable range
5. Return formatted table showing:
   - Service line type
   - All metric values (first 5 shown, "…" if more)
   - Range (min–max)
   - Mean (average)

**Example Output:**
```
- ICU (network-level):
  • avg_visits_per_shift: values [7.2, 8.5, 9.1, 10.2, 9.8] (range: 7.2–10.2; mean: 9.0)
  • wrvu_per_shift: values [8.1, 9.2, 10.3, 9.8, 10.1] (range: 8.1–10.3; mean: 9.5)
- Floor (network-level):
  • avg_visits_per_shift: values [5.1, 6.2, 7.3, 6.1, 5.9] (range: 5.1–7.3; mean: 6.1)
```

### Integration Point

In `_build_section_prompt()`, lines 297-306:

```python
# For productivity_pulse metrics section, parse JSON and provide 
# an authoritative data extract
if section.id == "metrics_highlights" and user_inputs.get("json_data"):
    data_extract = self._build_metrics_data_extract(user_inputs)
    if data_extract:
        parts.extend([
            "## Parsed Data (authoritative — use ONLY these numbers)",
            "",
            data_extract,
            ""
        ])
```

---

## Testing Recommendations

When you regenerate your productivity_pulse document:

1. **Check assignment names:** None should appear (no "HFW Bloxom Call", etc.)
2. **Verify metrics:** All numbers should come from your JSON data
3. **Validate ranges:** Reported ranges should match min/max of your actual data
4. **Confirm means:** Averages should match calculated means

### What Should Appear
```
✓ "ICU assignments show 7.2–10.2 visits/shift (average 9.0)"
✓ "Floor assignments demonstrate 5.1–7.3 visits/shift (mean 6.1)"
✓ Metrics from your JSON (not fabricated)
```

### What Should NOT Appear
```
✗ Specific assignment names (HFW, HSW, MCA, etc.)
✗ Numbers not in your parsed data table
✗ Facility-level comparisons
✗ Judgmental framing ("best", "worst", "underperforming")
```

---

## Why This Approach Works

### 1. **Ground Truth in Code**
- JSON is parsed on server (not in LLM's hallucinatory space)
- LLM can't invent data that's not explicitly provided
- Metrics are computed deterministically (mean, range, etc.)

### 2. **Reduce Decision Space**
- LLM sees "these are the ONLY numbers available"
- Removes temptation to fill gaps with fabrications
- Makes following instructions safer (can't deviate from parsed data)

### 3. **Prevent Name Fabrication**
- Don't include assignment/facility names in parsed data
- Only include service line type (ICU, Floor, etc.)
- LLM has no names to reference, so can't name them

### 4. **Explicit Constraints**
- "Use ONLY the numbers in 'Parsed Data' above"
- "If a number is not present there, do NOT include it"
- "Do NOT name specific assignments or facilities"

---

## Limitations & Future Improvements

### Current Limitations
1. Only applies to `metrics_highlights` section
2. Assumes JSON has `facility_class` field for service line
3. Requires user to specify `comparison_metrics` in correct format

### Future Improvements
1. Extend to other sections that might hallucinate (e.g., `opening_paragraph`)
2. Add JSON schema validation before parsing
3. Provide example JSON format in blueprint help text
4. Add verification step that checks if all numbers in output appear in parsed data

---

## References

- **File:** `app/services/ai_agents/section_agent.py`
- **Method:** `_build_metrics_data_extract()` (line 345)
- **Integration:** `_build_section_prompt()` (lines 297-306)
- **Guidance:** `_get_section_guidance()` (metrics_highlights entry)
- **Related:** `productivity_pulse/blueprint.json`, `productivity_pulse/prompts.json`

---

**Last Updated:** 2025-12-06  
**Status:** Production Ready ✅
