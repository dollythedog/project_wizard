# Phase 2 Complete! 

## Components Built ✅

### 1. Universal Document Editor Component
**File:** `app/components/document_editor.py`

**DocumentEditor Class:**
- Full-featured editor with Option B sidebar layout
- Custom prompt input for AI enhancements
- Quick action buttons (Wording, Tone, Simplify)
- Critique integration
- Undo functionality
- Save/Download actions
- Automatic wizard detection

**render_simple_editor Function:**
- Lightweight editor for core docs (README, CHANGELOG, etc.)
- No AI features - just preview + edit + save
- Toggle between view/edit modes
- Direct file saving

## Phase 1 + 2 Integration Guide

This document provides step-by-step instructions to integrate both Phase 1 and Phase 2 into app_v2_5.py.

### Step 1: Add All Imports

At the top of `app_v2_5.py`, after existing imports, add:

```python
from app.services.project_scaffolder import ProjectScaffolder
from app.components.document_editor import DocumentEditor, render_simple_editor
```

### Step 2: Update get_services() Function

Modify the `get_services()` function to include the scaffolder:

```python
@st.cache_resource
def get_services():
    registry = PatternRegistry()
    charter_agent = CharterAgent()
    critic_agent = CriticAgent()
    project_registry = ProjectRegistry()
    scaffolder = ProjectScaffolder()  # ADD THIS
    return registry, charter_agent, critic_agent, project_registry, scaffolder  # UPDATE THIS
```

Then update the unpacking:

```python
registry, charter_agent, critic_agent, project_registry, scaffolder = get_services()  # UPDATE THIS
```

### Step 3: Update New Project Creation

Find the "NEW PROJECT DIALOG" section (around line 350-380).

**Replace the project creation try block with:**

```python
try:
    # Create project directory
    project_full_path.mkdir(parents=True, exist_ok=True)
    
    # PHASE 1: Auto-scaffold core documents
    scaffolder.scaffold_project(
        project_full_path,
        new_project_name,
        new_project_type,
        project_owner="",  # TODO: Add owner field to form
        description=new_project_description
    )
    
    # Register project
    project_registry.register_project(
        project_full_path,
        name=new_project_name,
        description=new_project_description,
        project_type=new_project_type,
        icon=new_project_icon,
        project_owner=""  # TODO: Add owner field to form
    )
    
    # Set as current project
    st.session_state.project_path = project_full_path
    
    # Reset form for new project
    st.session_state.form_data = {
        'project_title': new_project_name,
        'project_type': new_project_type
    }
    st.session_state.charter_text = None
    st.session_state.critique = None
    st.session_state.pattern_outputs = {}
    
    st.session_state.show_new_project_dialog = False
    st.success(f"✓ Created project with core documents: {new_project_name}")
    st.rerun()
    
except Exception as e:
    st.error(f"Error creating project: {e}")
```

### Step 4: Implement Tab Locking

Add charter completion check at the beginning of tabs that should be locked.

**For Tab 3: Documentation (when you create it):**

```python
with tab3:
    st.header("📚 Documentation")
    
    # PHASE 2: Check charter status
    if not project_registry.is_charter_complete(st.session_state.project_path):
        st.warning("🔒 Please complete the Project Charter first (Tab 2)")
        st.info("The charter defines your project's direction and must be completed before creating other documents.")
        st.stop()
    
    # Rest of documentation tab code...
```

**For Tab 4: Deliverables (currently Project Home):**

```python
with tab4:
    st.header("📊 Deliverables")
    
    # PHASE 2: Check charter status
    if not project_registry.is_charter_complete(st.session_state.project_path):
        st.warning("🔒 Please complete the Project Charter first (Tab 2)")
        st.info("Deliverables can only be created after your project charter is approved.")
        st.stop()
    
    # Rest of deliverables tab code...
```

### Step 5: Mark Charter as Complete

In Tab 2 (Charter), when user saves the charter, mark it as complete:

**Find the "Save to Project" button code and add:**

```python
if st.button("💾 Save to Project", use_container_width=True):
    charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
    charter_file.write_text(st.session_state.charter_text)
    
    # PHASE 2: Mark charter as complete
    project_registry.mark_charter_complete(st.session_state.project_path)
    
    # Update project metadata
    if current_project:
        project_registry.update_project(
            st.session_state.project_path,
            last_modified=datetime.now().isoformat()
        )
    
    st.success(f"✓ Saved {charter_file.name} - Other tabs now unlocked!")
```

### Step 6: Use DocumentEditor for Charter (Optional Enhancement)

You can replace the current charter preview with the DocumentEditor component:

**In Tab 2 (Charter), replace the markdown preview section:**

```python
# OLD:
st.markdown("### Charter Preview")
st.markdown(st.session_state.charter_text)

# NEW - Using DocumentEditor:
editor = DocumentEditor(
    document_name="PROJECT_CHARTER.md",
    document_content=st.session_state.charter_text,
    charter_agent=charter_agent,
    critic_agent=critic_agent
)

updated_content, action = editor.render()

# Handle actions
if action["type"] == "save":
    charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
    charter_file.write_text(action["data"])
    project_registry.mark_charter_complete(st.session_state.project_path)
    st.success("✓ Charter saved!")
    st.rerun()
elif action["type"] == "download":
    st.download_button(
        "Download Charter",
        data=action["data"],
        file_name=f"PROJECT_CHARTER_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )
elif action["type"] == "critique":
    st.session_state.critique = action["data"]
    st.rerun()

# Update session state if content changed
if updated_content != st.session_state.charter_text:
    st.session_state.charter_text = updated_content
```

## Future Tab Structure (Phase 3)

When you're ready to restructure tabs:

```
Tab 1: 📂 Home
  - Project dashboard
  - Document status overview
  - Quick actions

Tab 2: 📋 Charter (REQUIRED FIRST)
  - Initiation → Business Case → Generate → Edit
  - Uses DocumentEditor
  - Unlocks other tabs when saved

Tab 3: 📚 Documentation  (LOCKED until charter complete)
  - Select: README | CHANGELOG | LICENSE | ISSUES
  - Uses render_simple_editor
  - Direct file editing

Tab 4: 📊 Deliverables (LOCKED until charter complete)
  - List of LEAN/PM patterns
  - Wizard for new documents
  - DocumentEditor for existing documents
```

## Testing Checklist

### Phase 1 Testing:
- [ ] Create new project
- [ ] Verify `/docs` folder created
- [ ] Verify README.md exists and renders correctly
- [ ] Verify CHANGELOG.md exists
- [ ] Verify LICENSE.md exists
- [ ] Verify ISSUES.md exists
- [ ] Verify `.project_metadata.json` created
- [ ] Check project registry shows `charter_created: false`

### Phase 2 Testing:
- [ ] Tabs 3 & 4 show lock message before charter
- [ ] Create charter and save
- [ ] Verify `charter_created` becomes `true`
- [ ] Verify tabs 3 & 4 unlock after charter saved
- [ ] Test custom prompt enhancement
- [ ] Test quick action buttons (Wording, Tone, Simplify)
- [ ] Test critique functionality
- [ ] Test simple editor for core docs
- [ ] Test save/download functionality

## Files Created/Modified

### Phase 1:
- Created: `app/templates/core_docs/*.j2` (4 files)
- Created: `app/services/document_registry.py`
- Created: `app/services/project_scaffolder.py`
- Modified: `app/services/project_registry.py`

### Phase 2:
- Created: `app/components/` (directory)
- Created: `app/components/__init__.py`
- Created: `app/components/document_editor.py`

### To Modify:
- `app_v2_5.py` (follow steps above)

## Benefits of This Architecture

✅ **Unified Document System** - Same editor for all documents  
✅ **Custom AI Prompts** - Users can give specific enhancement instructions  
✅ **Charter-First Workflow** - Ensures proper project planning  
✅ **Reusable Components** - DocumentEditor works for any document  
✅ **Simple Core Docs** - No AI overhead for basic docs  
✅ **Scalable** - Easy to add new document types  

## Ready for Phase 3! 🚀

Phase 3 will implement:
- Tab restructuring (Home, Charter, Documentation, Deliverables)
- Home dashboard with project stats
- Documentation tab with simple editors
- Deliverables tab with pattern selection
- Complete workflow from project creation to deliverables

