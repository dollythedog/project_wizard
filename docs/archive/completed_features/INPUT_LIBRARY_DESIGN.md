# Input Library Feature - Infrastructure Analysis & Design

## Current Infrastructure Review

### ✅ What Already Exists

1. **Pattern System** (`app/services/pattern_registry.py`)
   - Dynamically loads patterns from `patterns/` directory
   - Each pattern has `variables.json` defining input schema
   - Variables include: type, label, help, placeholder, required, height

2. **Wizard Form** (`app/ui/tabs/deliverables_tab.py`)
   - Function: `_render_wizard_form()`
   - Dynamically builds forms from `variables.json`
   - Currently supports pre-population from existing deliverables
   - Uses session state keys: `{pattern_key}_{var_name}`

3. **Session State Management** (`app/state/session_manager.py`)
   - Central `form_data` dictionary for charter
   - Per-deliverable session state via dynamic keys
   - Reset/update helpers available

4. **Project Structure**
   - Each project has a directory: `/path/to/project/`
   - Could easily add: `/path/to/project/.wizard_library/`

### 🎯 Feature Requirements

Based on typical use cases:

1. **Save Input Sets**
   - User fills out wizard form
   - Option to "Save as Snippet" with a name
   - Store for reuse across projects

2. **Load Input Sets**
   - Dropdown or search to find saved snippets
   - One-click to populate form fields
   - Option to load partially (specific fields only)

3. **Manage Library**
   - View all saved snippets
   - Edit/rename/delete snippets
   - Organize by pattern type or tags
   - Export/import for sharing

## Proposed Architecture

### 1. Data Storage

**Option A: Per-User Global Library** (Recommended)
```
~/.project_wizard/
  input_library/
    5w1h_analysis/
      discharge_workflow_issue.json
      medication_reconciliation.json
    project_charter/
      clinical_it_project.json
      quality_improvement.json
```

**Option B: Per-Project Library**
```
/path/to/project/
  .wizard_library/
    saved_inputs.json
```

**Recommendation:** Option A for global reuse + Option B for project-specific

### 2. Data Schema

```json
{
  "name": "Discharge Workflow Issue",
  "pattern_key": "5w1h_analysis",
  "description": "Common discharge process problems",
  "tags": ["healthcare", "discharge", "workflow"],
  "created": "2025-11-14T19:30:00Z",
  "last_used": "2025-11-14T19:35:00Z",
  "inputs": {
    "what": "Discharge paperwork missing medication lists...",
    "when": "Occurs during evening shift discharges...",
    "where": "In the discharge workflow between...",
    "who": "Affects patients and caregivers...",
    "why": "Increases readmission rates...",
    "how": "Patients call with medication questions..."
  }
}
```

### 3. New Service: `InputLibraryService`

Location: `app/services/input_library.py`

```python
class InputLibraryService:
    """Manage reusable input snippets for wizard forms."""
    
    def __init__(self, library_path: Path):
        self.library_path = library_path
    
    def save_snippet(self, pattern_key, name, inputs, description="", tags=None)
    def load_snippet(self, pattern_key, snippet_name)
    def list_snippets(self, pattern_key=None, tags=None)
    def delete_snippet(self, pattern_key, snippet_name)
    def export_snippet(self, pattern_key, snippet_name) -> dict
    def import_snippet(self, snippet_data: dict)
    def search_snippets(self, query: str)
```

### 4. UI Integration

#### A. In Wizard Form (deliverables_tab.py)

**Before form fields:**
```python
# Library integration
library = InputLibraryService()
snippets = library.list_snippets(pattern_key)

if snippets:
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_snippet = st.selectbox(
            "📚 Load from library:",
            options=[""] + [s["name"] for s in snippets],
            key=f"snippet_selector_{pattern_key}"
        )
    with col2:
        if st.button("Load", disabled=not selected_snippet):
            snippet_data = library.load_snippet(pattern_key, selected_snippet)
            # Pre-populate form with snippet inputs
            st.session_state[f"loaded_snippet_{pattern_key}"] = snippet_data["inputs"]
            st.rerun()
```

**After form (when inputs are entered):**
```python
# Option to save current inputs
with st.expander("💾 Save to Library"):
    snippet_name = st.text_input("Snippet Name", key=f"save_name_{pattern_key}")
    snippet_desc = st.text_area("Description (optional)", key=f"save_desc_{pattern_key}")
    snippet_tags = st.text_input("Tags (comma-separated)", key=f"save_tags_{pattern_key}")
    
    if st.button("Save Snippet") and snippet_name:
        library.save_snippet(
            pattern_key=pattern_key,
            name=snippet_name,
            inputs=user_inputs,
            description=snippet_desc,
            tags=[t.strip() for t in snippet_tags.split(",")]
        )
        st.success(f"✓ Saved '{snippet_name}' to library")
```

#### B. New Tab: "📚 Input Library" (Optional)

Manage all saved snippets:
- Browse by pattern type
- Search/filter
- Preview inputs
- Edit/delete
- Export/import

### 5. Implementation Priority

**Phase 1: MVP (Essential)**
1. Create `InputLibraryService` class
2. Implement save/load/list functions
3. Add "Load from library" dropdown to wizard
4. Add "Save to library" button after form
5. Store in `~/.project_wizard/input_library/`

**Phase 2: Enhanced**
1. Add tags and search
2. Add usage tracking (last_used, use_count)
3. Add snippet preview before loading
4. Partial load (select specific fields)

**Phase 3: Advanced**
1. Library management UI tab
2. Export/import for sharing
3. Team libraries (shared location)
4. AI-suggested snippets based on context

## Integration Points

### Modified Files:
1. **`app/services/input_library.py`** (NEW)
   - Core library service

2. **`app/ui/tabs/deliverables_tab.py`**
   - Add snippet loader before form
   - Add snippet saver after form
   - Integrate with `_render_wizard_form()`

3. **`app/state/session_manager.py`**
   - Add `loaded_snippets` to session state
   - Helper to merge snippet data with form

4. **`app.py`**
   - Initialize InputLibraryService
   - Pass to deliverables_tab

### New Files:
1. **`app/ui/tabs/library_tab.py`** (Phase 3)
   - Full library management UI

## Example User Flow

```
1. User opens Deliverables → Select "5W1H Analysis"
2. User sees "📚 Load from library:" dropdown
3. Dropdown shows:
   - "" (empty - start fresh)
   - "Discharge Workflow Issue"
   - "Medication Reconciliation Error"
   - "Lab Result Delay"
4. User selects "Discharge Workflow Issue"
5. Clicks "Load" button
6. Form fields populate with saved values
7. User edits/tweaks for current project
8. User generates deliverable
9. User optionally saves as NEW snippet:
   "Discharge Workflow - Pediatrics"
```

## Benefits

✅ **Time Savings:** Reuse common input patterns
✅ **Consistency:** Standardize terminology across projects
✅ **Knowledge Base:** Build library of organizational issues
✅ **Onboarding:** New users can learn from examples
✅ **Collaboration:** Share snippets with team
✅ **Quality:** Start with proven, well-written inputs

## Considerations

### Storage Location
- **Global (~/.project_wizard/)**: Accessible across all projects
- **Per-project (.wizard_library/)**: Project-specific snippets
- **Recommendation**: Support both with priority to global

### Privacy
- Don't save sensitive information in snippets
- Add warning when saving
- Option to encrypt library files (future)

### Portability
- Use JSON for easy export/import
- Include schema version for future compatibility
- Allow backup/restore of entire library

---

## Next Steps

1. ✅ Review this design
2. Implement Phase 1 MVP
3. Test with real use cases
4. Gather feedback
5. Iterate to Phase 2/3

**Estimated Effort:**
- Phase 1 MVP: 2-3 hours
- Phase 2: 1-2 hours  
- Phase 3: 3-4 hours

