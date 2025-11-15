# Phase 3: Complete Integration & Tab Restructuring

## Overview

Phase 3 completes the unified document management system by:
1. Integrating Phase 1+2 components
2. Restructuring tabs to new layout
3. Building all four main tabs
4. Creating complete end-to-end workflow

## New Tab Structure

```
🧙‍♂️ Project: [Icon] [Name]

├── 📂 Tab 1: HOME
│   └── Project dashboard, stats, quick actions
│
├── 📋 Tab 2: CHARTER (Required First)
│   ├── If not created: Initiation → Business Case → Generate
│   └── If created: Edit Mode with DocumentEditor
│
├── 📚 Tab 3: DOCUMENTATION (Locked until charter)
│   ├── Document selector: README | CHANGELOG | LICENSE | ISSUES
│   └── Simple editor for each
│
└── 📊 Tab 4: DELIVERABLES (Locked until charter)
    ├── List existing deliverables
    ├── Create new from patterns (Wizard)
    └── Edit existing (DocumentEditor)
```

## Implementation Steps

### Step 1: Backup and Integrate

**Backup current app:**
```bash
cp app_v2_5.py app_v2_5.py.pre_phase3
```

**Add imports at top of app_v2_5.py:**
```python
from app.services.project_scaffolder import ProjectScaffolder
from app.services.document_registry import DocumentRegistry
from app.components.document_editor import DocumentEditor, render_simple_editor
```

**Update get_services():**
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

### Step 2: Update New Project Creation

Find the NEW PROJECT DIALOG section and update the try block:

```python
try:
    # Create project directory
    project_full_path.mkdir(parents=True, exist_ok=True)
    
    # Auto-scaffold core documents
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
    
    # Set as current project
    st.session_state.project_path = project_full_path
    
    # Initialize session state
    st.session_state.form_data = {
        'project_title': new_project_name,
        'project_type': new_project_type
    }
    st.session_state.charter_text = None
    st.session_state.critique = None
    st.session_state.pattern_outputs = {}
    
    st.session_state.show_new_project_dialog = False
    st.success(f"✓ Created project with core documents!")
    st.rerun()
    
except Exception as e:
    st.error(f"Error creating project: {e}")
```

### Step 3: Restructure Main Tabs

Replace the current tab creation with:

```python
# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Home",
    "📋 Charter",
    "📚 Documentation",
    "📊 Deliverables"
])
```

### Step 4: Build Tab 1 - Home Dashboard

```python
with tab1:
    st.header("📂 Project Dashboard")
    
    current_project = project_registry.get_project(st.session_state.project_path)
    
    # Project info card
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Project", current_project.get('name', 'Unknown'))
    with col2:
        st.metric("Type", current_project.get('project_type', 'Unknown'))
    with col3:
        charter_status = "✅ Complete" if project_registry.is_charter_complete(st.session_state.project_path) else "⚠️ Pending"
        st.metric("Charter", charter_status)
    
    st.markdown("---")
    
    # Document stats
    doc_registry = DocumentRegistry(st.session_state.project_path)
    stats = doc_registry.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Docs", stats['total_documents'])
    with col2:
        st.metric("Core Docs", stats['core_docs'])
    with col3:
        st.metric("Deliverables", stats['deliverables'])
    with col4:
        if stats['average_critique_score']:
            st.metric("Avg Score", f"{stats['average_critique_score']:.0f}%")
        else:
            st.metric("Avg Score", "N/A")
    
    st.markdown("---")
    
    # Recent documents
    st.subheader("Recent Documents")
    recent_docs = doc_registry.list_documents()[:5]
    
    if recent_docs:
        for doc in recent_docs:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.text(f"{doc['name']}")
            with col2:
                st.caption(doc['type'])
            with col3:
                st.caption(doc['status'])
            with col4:
                if doc['critique_score']:
                    st.caption(f"{doc['critique_score']:.0f}%")
    else:
        st.info("No documents yet")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not project_registry.is_charter_complete(st.session_state.project_path):
            if st.button("📋 Complete Charter", use_container_width=True, type="primary"):
                st.info("Go to Charter tab to complete your project charter")
    
    with col2:
        if st.button("📚 Edit Documentation", use_container_width=True):
            st.info("Go to Documentation tab")
    
    with col3:
        if st.button("📊 Create Deliverable", use_container_width=True):
            if project_registry.is_charter_complete(st.session_state.project_path):
                st.info("Go to Deliverables tab")
            else:
                st.warning("Complete charter first")
```

### Step 5: Update Tab 2 - Charter

Keep existing charter logic but add completion marking:

```python
with tab2:
    st.header("📋 Project Charter")
    
    # [Keep existing Initiation and Business Case forms - Tab 1 and Tab 2 code]
    
    # [Keep existing Generate Charter button]
    
    # Update Save button to mark charter complete:
    with col3:
        if st.session_state.charter_text:
            if st.button("💾 Save to Project", use_container_width=True):
                charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
                charter_file.write_text(st.session_state.charter_text)
                
                # Mark charter as complete
                project_registry.mark_charter_complete(st.session_state.project_path)
                
                # Register document
                doc_registry = DocumentRegistry(st.session_state.project_path)
                if not doc_registry.document_exists("PROJECT_CHARTER.md"):
                    doc_registry.register_document(
                        "PROJECT_CHARTER.md",
                        doc_type="charter",
                        version="1.0.0"
                    )
                
                # Update project metadata
                if current_project:
                    project_registry.update_project(
                        st.session_state.project_path,
                        last_modified=datetime.now().isoformat()
                    )
                
                st.success(f"✓ Charter saved! Other tabs now unlocked.")
    
    # [Keep rest of charter code - critique, enhancement, preview]
```

### Step 6: Build Tab 3 - Documentation

```python
with tab3:
    st.header("📚 Core Documentation")
    
    # Check charter status
    if not project_registry.is_charter_complete(st.session_state.project_path):
        st.warning("🔒 Complete the Project Charter first")
        st.info("The charter defines your project's direction and must be completed before editing documentation.")
        st.stop()
    
    # Document selector
    doc_options = {
        "README.md": "📖 Project Overview",
        "CHANGELOG.md": "📝 Version History",
        "LICENSE.md": "⚖️ License",
        "ISSUES.md": "🐛 Issue Tracker"
    }
    
    selected_doc = st.radio(
        "Select document to edit:",
        list(doc_options.keys()),
        format_func=lambda x: doc_options[x],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Load document
    doc_file = st.session_state.project_path / selected_doc
    
    if doc_file.exists():
        doc_content = doc_file.read_text()
        
        # Use simple editor
        updated_content = render_simple_editor(
            selected_doc,
            doc_content,
            st.session_state.project_path
        )
        
        # Update document registry on save
        if st.session_state.get(f"editing_{selected_doc}", False):
            doc_registry = DocumentRegistry(st.session_state.project_path)
            doc_registry.update_document(
                selected_doc,
                word_count=len(updated_content.split())
            )
    else:
        st.error(f"{selected_doc} not found in project")
```

### Step 7: Update Tab 4 - Deliverables

```python
with tab4:
    st.header("📊 Project Deliverables")
    
    # Check charter status
    if not project_registry.is_charter_complete(st.session_state.project_path):
        st.warning("🔒 Complete the Project Charter first")
        st.info("Deliverables can only be created after your project charter is approved.")
        st.stop()
    
    # [Keep existing deliverables code from current tab4]
    # Add document registry integration when creating/editing deliverables
```

## Testing Plan

### Phase 1 Tests:
1. Create new project
2. Verify all core docs created
3. Check .project_metadata.json exists
4. Verify charter_created = false

### Phase 2 Tests:
1. Verify tabs 3 & 4 locked
2. Complete charter
3. Verify tabs unlock
4. Test custom prompt
5. Test document editors

### Phase 3 Tests:
1. Test Home dashboard stats
2. Test tab navigation
3. Test complete workflow: Create → Charter → Documentation → Deliverables
4. Verify all document registry updates
5. Test project switching

## Rollback Plan

If issues occur:
```bash
cp app_v2_5.py.pre_phase3 app_v2_5.py
```

## Success Criteria

✅ New project creates with all core docs  
✅ Home dashboard shows accurate stats  
✅ Charter completion unlocks tabs  
✅ Documentation editor works for all core docs  
✅ Deliverables can be created after charter  
✅ Document registry tracks all changes  
✅ Project switching works correctly  

## Next Steps After Phase 3

- Add undo/version history
- Implement project templates
- Add project archiving
- Enhance Home dashboard with charts
- Add bulk operations

