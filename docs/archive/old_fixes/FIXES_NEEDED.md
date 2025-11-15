# Fixes for Work Plan Pattern Integration

## Issue 1: Critique Agent Not Working for Work Plan
**Problem:** CriticAgent works for charter but not for work_plan pattern
**Root Cause:** DocumentEditor doesn't pass pattern-specific rubric to CriticAgent

**Solution:**
1. Modify `DocumentEditor.__init__()` to accept `pattern_key` and `rubric_path` parameters
2. Load rubric from `rubric_path` if provided
3. Pass rubric to `critic_agent.critique_charter()` (rename this method to `critique_document()` for clarity)
4. Update Deliverables tab to pass pattern info when creating DocumentEditor

## Issue 2: No OpenProject Upload Button
**Problem:** User must go to terminal to run export script
**Solution:**
1. Add "📤 Upload to OpenProject" button in Deliverables tab when viewing ISSUES.md
2. Button calls the export script using subprocess
3. Show progress spinner and success/error messages
4. Requires environment variables or config for OpenProject URL and API key

## Issue 3: No Raw Markdown Editing Mode
**Problem:** Can only view rendered markdown, can't edit source directly
**Solution:**
1. Add toggle in DocumentEditor sidebar: "View Mode" vs "Edit Mode"
2. In Edit Mode, replace `st.markdown()` with `st.text_area()` for raw editing
3. Keep all enhancement and critique features available in both modes
4. Save updates content regardless of mode

## Implementation Order
1. Fix DocumentEditor to support pattern-specific rubrics (enables critique for all patterns)
2. Update Deliverables tab to use DocumentEditor properly
3. Add markdown editing mode to DocumentEditor
4. Add OpenProject upload button for ISSUES.md
