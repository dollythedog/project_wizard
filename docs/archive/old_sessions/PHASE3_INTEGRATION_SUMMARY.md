# Phase 3: Integration Complete - Quick Reference

## ✅ All Components Ready

### Phase 1 Components:
- app/templates/core_docs/*.j2 (4 templates)
- app/services/document_registry.py
- app/services/project_scaffolder.py  
- app/services/project_registry.py (enhanced)

### Phase 2 Components:
- app/components/document_editor.py
- app/components/__init__.py

### Phase 3: Integration Steps

## CRITICAL CHANGES TO app_v2_5.py

### 1. Imports (Line ~23, after existing imports)
```python
from app.services.project_scaffolder import ProjectScaffolder
from app.services.document_registry import DocumentRegistry
from app.components.document_editor import DocumentEditor, render_simple_editor
```

### 2. Update get_services() (Line ~92)
```python
@st.cache_resource
def get_services():
    registry = PatternRegistry()
    charter_agent = CharterAgent()
    critic_agent = CriticAgent()
    project_registry = ProjectRegistry()
    scaffolder = ProjectScaffolder()
    return registry, charter_agent, critic_agent, project_registry, scaffolder

registry, charter_agent, critic_agent, project_registry, scaffolder = get_services()
```

### 3. New Project Creation (Line ~280-320, in NEW PROJECT DIALOG)

Replace the try block with:
```python
try:
    project_full_path.mkdir(parents=True, exist_ok=True)
    
    # AUTO-SCAFFOLD
    scaffolder.scaffold_project(
        project_full_path,
        new_project_name,
        new_project_type,
        project_owner="",
        description=new_project_description
    )
    
    # Register project
    project_registry.register_project(
        project_full_path,
        name=new_project_name,
        description=new_project_description,
        project_type=new_project_type,
        icon=new_project_icon,
        project_owner=""
    )
    
    st.session_state.project_path = project_full_path
    st.session_state.form_data = {
        'project_title': new_project_name,
        'project_type': new_project_type
    }
    st.session_state.charter_text = None
    st.session_state.critique = None
    st.session_state.pattern_outputs = {}
    
    st.session_state.show_new_project_dialog = False
    st.success(f"✓ Project created with core documents!")
    st.rerun()
except Exception as e:
    st.error(f"Error: {e}")
```

### 4. Tab Names (Line ~420)
```python
# FROM:
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Initiation",
    "💼 Business Case", 
    "📋 Charter",
    "🏠 Project Home"
])

# TO:
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Home",
    "📋 Charter",
    "📚 Documentation",
    "📊 Deliverables"
])
```

### 5. Charter Save Button (In current tab3, line ~560)

Add after charter save:
```python
# Mark charter complete
project_registry.mark_charter_complete(st.session_state.project_path)

# Register in document registry
doc_registry = DocumentRegistry(st.session_state.project_path)
if not doc_registry.document_exists("PROJECT_CHARTER.md"):
    doc_registry.register_document(
        "PROJECT_CHARTER.md",
        doc_type="charter",
        version="1.0.0"
    )
```

### 6. Tab Locking (Add to NEW tab3 and tab4)

At start of Documentation and Deliverables tabs:
```python
if not project_registry.is_charter_complete(st.session_state.project_path):
    st.warning("🔒 Complete the Project Charter first")
    st.info("The charter must be completed before proceeding.")
    st.stop()
```

## SIMPLIFIED APPROACH

Since full rewrite is complex, here's the MINIMUM viable integration:

1. ✅ Add 3 import lines
2. ✅ Update get_services() function  
3. ✅ Replace New Project creation try block
4. ✅ Add charter completion marking to Save button
5. ✅ Add charter check to tab4 (current Project Home)

This gives you:
- Auto-scaffolding on new projects
- Charter completion tracking
- Tab locking for deliverables

## TESTING HERMES

When you open Hermes:
1. It won't have core docs (created before Phase 1)
2. Charter exists but not marked complete
3. Solution: Manually mark complete:

```python
# In Streamlit Python console or add temporary button:
from app.services.project_registry import ProjectRegistry
registry = ProjectRegistry()
registry.mark_charter_complete(Path("/home/ivesjl/Projects/Hermes"))
```

OR just create a NEW test project to see full workflow!

## FILES TO REFERENCE

-  PHASE1_INTEGRATION_NOTES.md - Phase 1 details
- PHASE2_COMPLETION.md - Phase 2 + editor details
- PHASE3_IMPLEMENTATION_PLAN.md - Full restructure plan

## NEXT SESSION

If you want full Phase 3 (Home dashboard, new tabs), we can:
1. Do full rewrite in next session
2. Or build incrementally tab by tab
3. Or I can provide complete new app_v2_5.py file

For NOW, the 5 critical changes above will give you:
✅ Project scaffolding
✅ Document registry
✅ Charter tracking
✅ Basic tab locking

