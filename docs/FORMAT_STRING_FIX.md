# Format String Fix - Unmatched Braces in Section Prompt Generation

**Date:** 2025-12-06  
**Status:** ✅ Fixed and Tested  
**Error:** `unmatched '{' in format spec` when generating productivity_pulse documents

---

## Problem

When attempting to generate a productivity_pulse document, the system failed with:
```
⚠️ Document Generation Failed
Error Details: unmatched '{' in format spec
```

This error occurred during section prompt generation in the `SectionAgentController._build_section_prompt()` method.

---

## Root Cause Analysis

### The Issue

The `_build_section_prompt()` method was constructing a prompt string with placeholder markers like `{target_words}` and `{max_words}`, then calling Python's `.format()` method on the entire assembled string:

```python
parts = [
    # ... various parts added ...
    "7. Aim for {target_words} words; do NOT exceed {max_words}",
    # ... more parts ...
]

# This calls .format() on the entire assembled string
return "\n".join(parts).format(target_words=target_words, max_words=max_words)
```

### Why It Failed

The productivity_pulse template accepts a `json_data` input containing service line data in JSON format. When this JSON data was included in the prompt, it contained literal braces:

```json
[
  {"assignment_name": "ICU Assignment 1", "facility_class": "ICU", ...},
  {"assignment_name": "Floor Assignment 1", "facility_class": "Floor", ...}
]
```

When Python's `.format()` method encountered these braces in the assembled string, it tried to interpret them as format placeholders. Since they didn't match the expected `{target_words}` or `{max_words}` patterns, it threw an `unmatched '{' in format spec` error.

### Why This Affected Productivity_Pulse

- **Clinical proposal templates**: User inputs are text fields (names, descriptions, etc.) - no braces
- **Productivity_pulse template**: Includes `json_data` input with JSON containing literal `{` and `}` characters

So the error manifested only when using productivity_pulse with JSON data.

---

## Solution

### Approach: Eliminate `.format()` Dependency

Instead of using `.format()` on the final assembled string, use f-strings throughout to build values directly:

**Before:**
```python
parts = [
    # ... build with placeholder strings ...
    "🚨 If your response exceeds {max_words} words, it will be rejected.",
    # ...
    "7. Aim for {target_words} words; do NOT exceed {max_words}",
]
return "\n".join(parts).format(target_words=target_words, max_words=max_words)
```

**After:**
```python
parts = [
    # ... build with f-strings directly ...
    f"🚨 If your response exceeds {max_words} words, it will be rejected.",
    # ...
    f"7. Aim for {target_words} words; do NOT exceed {max_words}",
]
return "\n".join(parts)  # No .format() call needed!
```

### Why This Works

- F-strings evaluate expressions at the point of definition, not later
- No risk of user input data being misinterpreted as format placeholders
- Cleaner, more Pythonic code
- No special escaping needed for user data

---

## Changes Made

### File: `app/services/ai_agents/section_agent.py`

**Line 263:**
```python
# Before
"🚨 If your response exceeds {max_words} words, it will be rejected.",

# After
f"🚨 If your response exceeds {max_words} words, it will be rejected.",
```

**Line 322:**
```python
# Before
"7. Aim for {target_words} words; do NOT exceed {max_words}",

# After
f"7. Aim for {target_words} words; do NOT exceed {max_words}",
```

**Line 333:**
```python
# Before
return "\n".join(parts).format(target_words=target_words, max_words=max_words)

# After
return "\n".join(parts)
```

---

## Testing

### Test Case: JSON Data with Braces

```python
user_inputs = {
    "json_data": json.dumps([
        {"assignment_name": "ICU Assignment 1", "facility_class": "ICU", ...},
        {"assignment_name": "Floor Assignment 1", "facility_class": "Floor", ...}
    ]),
    # ... other fields ...
}

# Build section prompt with JSON data containing braces
prompt = section_controller._build_section_prompt(
    section,
    target_words=60,
    max_words=66,
    user_inputs=user_inputs,  # Contains braces in json_data!
    project_context=None,
    strictness="STRICT"
)

# Result: ✅ Prompt builds successfully with no format errors
```

### Test Results

✅ Prompt generation with JSON data: **PASS**
✅ All target_words/max_words values correctly included: **PASS**
✅ No format() errors: **PASS**
✅ Prompt is valid string: **PASS**
✅ JSON data values present in prompt: **PASS**

---

## Impact

### Fixed
- ✅ productivity_pulse document generation no longer fails with brace errors
- ✅ Templates with JSON inputs now work correctly
- ✅ Code is simpler and more Pythonic (f-strings instead of .format())

### Unchanged
- ✅ Clinical proposal templates work identically
- ✅ All other template generation unchanged
- ✅ Word count constraints still enforced correctly

### Future-Proof
- ✅ Any new template with complex JSON data will work
- ✅ No need to escape braces in user input data
- ✅ F-string approach is standard Python practice

---

## Key Learnings

### String Formatting Pitfalls
1. `.format()` on assembled strings with user data can cause unexpected errors
2. F-strings are evaluated immediately (safer with dynamic data)
3. Always consider what data might be included in strings before calling `.format()`

### Prevention Strategy
- Use f-strings for template/prompt construction
- Avoid `.format()` calls on strings containing user-provided data
- If using `.format()`, ensure all placeholders are accounted for or escape problematic characters

---

## Code Pattern: Best Practice

```python
# ❌ AVOID: Building with placeholders then calling .format()
parts = [
    "Target: {target}",
    f"User input: {user_data}",  # May contain braces!
]
return "\n".join(parts).format(target=100)  # Error if user_data has braces

# ✅ PREFER: Use f-strings throughout
parts = [
    f"Target: {target}",
    f"User input: {user_data}",  # Safe - no format() call later
]
return "\n".join(parts)  # Direct string join, no format errors

# ✅ ALSO GOOD: If you must use .format(), escape user data
val_str = user_data.replace('{', '{{').replace('}', '}}')
parts = [
    "Target: {target}",
    f"User input: {val_str}",
]
return "\n".join(parts).format(target=100)
```

---

## References

- **File:** `app/services/ai_agents/section_agent.py`
- **Methods:** `_build_section_prompt()`
- **Related:** `productivity_pulse/blueprint.json`, `LLMClient.generate()`
- **Test:** Created and verified with `test_format_fix.py`

---

## Questions & Answers

**Q: Why not just escape the braces in user input?**
A: Escaping works but is fragile. The f-string approach is cleaner, simpler, and doesn't require special handling of user data.

**Q: Will this affect other templates?**
A: No - all templates benefit from this fix. Templates without JSON data are unaffected; those with JSON data (or other brace-containing data) now work correctly.

**Q: Is there a performance impact?**
A: No - f-strings are actually slightly faster than `.format()` calls since they're evaluated at parse time.

**Q: Should all `.format()` calls be replaced with f-strings?**
A: Generally yes, unless you have specific reasons to defer evaluation. F-strings are the modern Python standard (3.6+).

---

**Last Updated:** 2025-12-06  
**Status:** Production Ready ✅  
**Related Issue:** productivity_pulse generation error
