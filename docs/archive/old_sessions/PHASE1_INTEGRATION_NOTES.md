# Phase 1 Integration Notes

## Completed Components

### 1. Document Templates ✅
Created in `app/templates/core_docs/`:
- `README.md.j2` - Project overview template
- `CHANGELOG.md.j2` - Version history (Keep a Changelog format)
- `LICENSE.md.j2` - MIT License template
- `ISSUES.md.j2` - Issue tracking template

### 2. ProjectRegistry Updates ✅
File: `app/services/project_registry.py`

Added fields:
- `charter_created`: Boolean flag (default: False)
- `project_owner`: String for owner name
- `version`: String for project version (default: "0.1.0")

New methods:
- `mark_charter_complete(project_path)` - Sets charter_created = True
- `is_charter_complete(project_path)` - Returns charter status

### 3. DocumentRegistry Service ✅
File: `app/services/document_registry.py`

Tracks per-project documents with metadata:
- Document name, type (core/charter/deliverable)
- Version, word count, critique score
- Created date, last modified, status

Methods:
- `register_document()` - Add new document
- `update_document()` - Update metadata
- `set_word_count()`, `set_critique_score()`, `set_version()`
- `list_documents()` - Get all docs (filterable)
- `get_stats()` - Project statistics

Storage: `.project_metadata.json` in project root

### 4. ProjectScaffolder Service ✅
File: `app/services/project_scaffolder.py`

Handles initial project setup:
- Creates `docs/` directory
- Renders and creates all core documents from templates
- Registers documents in DocumentRegistry
- Returns DocumentRegistry instance

## Required Integration in app_v2_5.py

### Step 1: Add Import
At top of file, after existing imports:

```python
from app.services.project_scaffolder import ProjectScaffolder
```

### Step 2: Initialize Scaffolder
In `get_services()` function, add:

```python
scaffolder = ProjectScaffolder()
return registry, charter_agent, critic_agent, project_registry, scaffolder
```

Then update the unpacking:

```python
registry, charter_agent, critic_agent, project_registry, scaffolder = get_services()
```

### Step 3: Update New Project Creation
Find the "NEW PROJECT DIALOG" section where projects are created.

**Current code (around line 350-380):**
```python
try:
    # Create project directory
    project_full_path.mkdir(parents=True, exist_ok=True)
    
    # Register project
    project_registry.register_project(
        project_full_path,
        name=new_project_name,
        description=new_project_description,
        project_type=new_project_type,
        icon=new_project_icon
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
    st.success(f"✓ Created project: {new_project_name}")
    st.rerun()
    
except Exception as e:
    st.error(f"Error creating project: {e}")
```

**Updated code with scaffolding:**
```python
try:
    # Create project directory
    project_full_path.mkdir(parents=True, exist_ok=True)
    
    # AUTO-SCAFFOLD: Create core documents
    scaffolder.scaffold_project(
        project_full_path,
        new_project_name,
        new_project_type,
        project_owner="",  # Can add owner field to form later
        description=new_project_description
    )
    
    # Register project
    project_registry.register_project(
        project_full_path,
        name=new_project_name,
        description=new_project_description,
        project_type=new_project_type,
        icon=new_project_icon,
        project_owner=""  # Can add owner field to form later
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

## Testing Phase 1

After integration, test by:

1. Create a new project via UI
2. Check that project folder contains:
   - `README.md`
   - `CHANGELOG.md`
   - `LICENSE.md`
   - `ISSUES.md`
   - `docs/` folder (empty)
   - `.project_metadata.json`
3. Verify templates are properly rendered with project name
4. Check that project registry shows `charter_created: false`

## Next Steps (Phase 2)

- Create universal Edit Mode (Option B) component
- Add custom prompt input to Enhancement section
- Implement tab locking based on charter status
- Build simple editor for core docs (no wizard)
