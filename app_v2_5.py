"""
Project Wizard v2.5 - Integrated Pattern-Based Workflow
Unified charter generation with LEAN activities hub
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.pattern_pipeline import PatternPipeline
from app.services.ai_agents import CharterAgent, CriticAgent
from app.services.project_registry import ProjectRegistry
from app.services.project_scaffolder import ProjectScaffolder
from app.services.document_registry import DocumentRegistry
from app.components.document_editor import DocumentEditor, render_simple_editor

def load_project_charter(project_path):
    """Load existing charter from project directory"""
    charter_file = project_path / "PROJECT_CHARTER.md"
    if charter_file.exists():
        return charter_file.read_text()
    return None

def parse_charter_to_form_data(charter_text):
    """Extract form data from existing charter"""
    data = {}
    lines = charter_text.split('\n')
    
    # Simple parsing - look for headers and content
    current_section = None
    content_buffer = []
    
    for line in lines:
        if line.startswith('# Project Charter:'):
            data['project_title'] = line.replace('# Project Charter:', '').strip()
        elif line.startswith('**Project Owner:**'):
            data['project_owner'] = line.replace('**Project Owner:**', '').strip()
        elif line.startswith('**Project Type:**'):
            data['project_type'] = line.replace('**Project Type:**', '').strip()
        elif line.startswith('## '):
            # Save previous section
            if current_section and content_buffer:
                data[current_section] = '\n'.join(content_buffer).strip()
            # Start new section
            section_name = line.replace('##', '').strip().lower().replace(' ', '_')
            current_section = section_name
            content_buffer = []
        elif current_section and line.strip():
            content_buffer.append(line)
    
    # Save last section
    if current_section and content_buffer:
        data[current_section] = '\n'.join(content_buffer).strip()
    
    return data

# Emoji options for projects
PROJECT_EMOJIS = [
    "📁", "🚀", "💼", "⚡", "🎯", "🔧", "💡", "🏥", "🔬", "📊",
    "🎨", "🏗️", "🌐", "📱", "💻", "🔐", "📈", "🎓", "🔍", "⚙️"
]

# Page config
st.set_page_config(
    page_title="Project Wizard v2.5",
    page_icon="🧙‍♂️",
    layout="wide"
)

# Initialize services
@st.cache_resource
def get_services():
    registry = PatternRegistry()
    charter_agent = CharterAgent()
    critic_agent = CriticAgent()
    project_registry = ProjectRegistry()
    scaffolder = ProjectScaffolder()
    return registry, charter_agent, critic_agent, project_registry, scaffolder

registry, charter_agent, critic_agent, project_registry, scaffolder = get_services()

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'enhanced_data' not in st.session_state:
    st.session_state.enhanced_data = {}
if 'charter_text' not in st.session_state:
    st.session_state.charter_text = None
if 'critique' not in st.session_state:
    st.session_state.critique = None
if 'project_path' not in st.session_state:
    st.session_state.project_path = None
if 'pattern_outputs' not in st.session_state:
    st.session_state.pattern_outputs = {}
if 'show_new_project_dialog' not in st.session_state:
    st.session_state.show_new_project_dialog = False
if 'show_project_gallery' not in st.session_state:
    st.session_state.show_project_gallery = False

# ============================================================================
# SIDEBAR: Project Management
# ============================================================================
with st.sidebar:
    st.header("🧙‍♂️ Project Wizard")
    
    # Current project display
    if st.session_state.project_path:
        current_project = project_registry.get_project(st.session_state.project_path)
        if current_project:
            st.success(f"{current_project['icon']} **{current_project['name']}**")
            st.caption(f"`{Path(current_project['path']).name}`")
        else:
            st.info("📂 No project loaded")
    else:
        st.info("📂 No project loaded")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 My Projects", use_container_width=True):
            st.session_state.show_project_gallery = True
            st.rerun()
    
    with col2:
        if st.button("➕ New Project", use_container_width=True):
            st.session_state.show_new_project_dialog = True
            st.rerun()
    
    st.markdown("---")
    
    # Recent projects quick access
    projects = project_registry.list_projects(sort_by="last_accessed")
    
    if projects:
        st.subheader("Recent Projects")
        
        for project in projects[:5]:  # Show 5 most recent
            project_path = Path(project['path'])
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.caption(f"{project['icon']} {project['name']}")
            
            with col2:
                if st.button("📂", key=f"quick_load_{project['path']}", help="Load project"):
                    if project_path.exists():
                        st.session_state.project_path = project_path
                        project_registry.touch_project(project_path)
                        
                        # Load existing charter
                        existing_charter = load_project_charter(project_path)
                        if existing_charter:
                            st.session_state.charter_text = existing_charter
                            parsed_data = parse_charter_to_form_data(existing_charter)
                            st.session_state.form_data.update(parsed_data)
                        
                        st.rerun()
                    else:
                        st.error("Project directory not found")
    
    st.markdown("---")
    st.caption("Project Wizard v2.5")

# ============================================================================
# PROJECT GALLERY MODAL
# ============================================================================
if st.session_state.show_project_gallery:
    st.title("📚 My Projects")
    
    # Close button
    if st.button("✖ Close Gallery", type="secondary"):
        st.session_state.show_project_gallery = False
        st.rerun()
    
    st.markdown("---")
    
    projects = project_registry.list_projects(sort_by="last_accessed")
    
    if not projects:
        st.info("No projects yet. Click '➕ New Project' to create your first project!")
    else:
        # Display as grid of cards
        cols_per_row = 3
        
        for i in range(0, len(projects), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(projects):
                    project = projects[i + j]
                    project_path = Path(project['path'])
                    
                    with col:
                        # Project card
                        with st.container():
                            st.markdown(f"### {project['icon']} {project['name']}")
                            st.caption(f"**Type:** {project['project_type']}")
                            
                            if project.get('description'):
                                st.caption(project['description'][:100] + "..." if len(project.get('description', '')) > 100 else project.get('description', ''))
                            
                            st.caption(f"📅 Created: {project['created_date'][:10]}")
                            
                            # Action buttons
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                if st.button("📂 Open", key=f"open_{project['path']}", use_container_width=True):
                                    if project_path.exists():
                                        st.session_state.project_path = project_path
                                        project_registry.touch_project(project_path)
                                        
                                        # Load charter
                                        existing_charter = load_project_charter(project_path)
                                        if existing_charter:
                                            st.session_state.charter_text = existing_charter
                                            parsed_data = parse_charter_to_form_data(existing_charter)
                                            st.session_state.form_data.update(parsed_data)
                                        
                                        st.session_state.show_project_gallery = False
                                        st.rerun()
                                    else:
                                        st.error("Project not found")
                            
                            with col_b:
                                if st.button("🗑️", key=f"remove_{project['path']}", help="Remove from list", use_container_width=True):
                                    project_registry.remove_project(project_path)
                                    st.rerun()
                        
                        st.markdown("---")
    
    st.stop()

# ============================================================================
# NEW PROJECT DIALOG
# ============================================================================
if st.session_state.show_new_project_dialog:
    st.title("➕ Create New Project")
    
    # Close button
    if st.button("✖ Cancel", type="secondary"):
        st.session_state.show_new_project_dialog = False
        st.rerun()
    
    st.markdown("---")
    
    with st.form("new_project_form"):
        st.subheader("Project Details")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_project_name = st.text_input(
                "Project Name *",
                placeholder="e.g., Hermes - Trading Application",
                help="Descriptive name for your project"
            )
        
        with col2:
            new_project_icon = st.selectbox(
                "Icon",
                PROJECT_EMOJIS,
                index=0
            )
        
        new_project_type = st.selectbox(
            "Project Type *",
            ["Software Development", "Process Improvement", "Clinical Initiative", 
             "Research", "Infrastructure", "Other"]
        )
        
        new_project_description = st.text_area(
            "Description (optional)",
            placeholder="Brief description of the project...",
            height=100
        )
        
        st.markdown("---")
        st.subheader("Project Location")
        
        # Default location
        default_base = Path.home() / "Projects"
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            base_directory = st.text_input(
                "Base Directory",
                value=str(default_base),
                help="Where to create the project folder"
            )
        
        with col2:
            st.caption("Project folder will be created here")
        
        # Show what will be created
        if new_project_name:
            # Sanitize project name for folder
            folder_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in new_project_name)
            folder_name = folder_name.replace(' ', '_')
            
            project_full_path = Path(base_directory) / folder_name
            
            st.info(f"📁 Project will be created at: `{project_full_path}`")
        
        submitted = st.form_submit_button("🚀 Create Project", type="primary", use_container_width=True)
        
        if submitted:
            if not new_project_name:
                st.error("Please provide a project name")
            else:
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
    
    st.stop()

# ============================================================================
# MAIN APP (only shown if no modal is active)
# ============================================================================

# Check if project is loaded
if not st.session_state.project_path:
    st.title("🧙‍♂️ Welcome to Project Wizard v2.5")
    st.markdown("### Get started by creating a new project or opening an existing one")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        if st.button("📚 Browse My Projects", use_container_width=True, type="primary"):
            st.session_state.show_project_gallery = True
            st.rerun()
        
        st.markdown("**or**")
        
        if st.button("➕ Create New Project", use_container_width=True):
            st.session_state.show_new_project_dialog = True
            st.rerun()
    
    st.stop()

# Header
current_project = project_registry.get_project(st.session_state.project_path)
if current_project:
    st.title(f"{current_project['icon']} {current_project['name']}")
    st.caption(f"**{current_project['project_type']}** • `{st.session_state.project_path}`")
else:
    st.title(f"📂 {st.session_state.project_path.name}")
    st.caption(f"`{st.session_state.project_path}`")

# Show if charter loaded
if st.session_state.charter_text and st.session_state.form_data.get('project_title'):
    st.success(f"✓ Charter loaded for: **{st.session_state.form_data['project_title']}**")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Home",
    "📋 Charter", 
    "📚 Documentation",
    "📦 Deliverables"
])

# ============================================================================
# TAB 1: Home Dashboard
# ============================================================================
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

# ============================================================================
# TAB 2: Charter
# ============================================================================
with tab2:
    st.header("📋 Project Charter")
    
    charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
    charter_exists = charter_file.exists()
    
    # Load existing charter if it exists
    if charter_exists:
        charter_text = charter_file.read_text()
        
        # Mark charter as complete
        project_registry.mark_charter_complete(st.session_state.project_path)
        
        # EDIT MODE: Use DocumentEditor
        st.info("✅ Charter exists - Edit Mode")
        
        editor = DocumentEditor(
            document_name="PROJECT_CHARTER.md",
            document_content=charter_text,
            charter_agent=charter_agent,
            critic_agent=critic_agent
        )
        
        updated_content, action = editor.render()
        
        # Handle save action
        if action and action.get("type") == "save":
            charter_file.write_text(updated_content)
            
            # Update registry
            current_project = project_registry.get_project(st.session_state.project_path)
            if current_project:
                project_registry.update_project(
                    st.session_state.project_path,
                    last_modified=datetime.now().isoformat()
                )
                project_registry.mark_charter_complete(st.session_state.project_path)
            
            st.success(f"✓ Saved to {charter_file.name}")
            st.rerun()
    
    else:
        # WIZARD MODE: Initiation → Business Case → Generate
        st.info("⚠️ No charter found - Wizard Mode")
        
        # Create sub-tabs for wizard steps
        wizard_tab1, wizard_tab2, wizard_tab3 = st.tabs([
            "📝 Step 1: Initiation",
            "💼 Step 2: Business Case",
            "🎯 Step 3: Generate"
        ])
        
        # WIZARD STEP 1: Initiation
        with wizard_tab1:
            st.subheader("Project Initiation")
            
            with st.form("initiation_form"):
                project_title = st.text_input(
                    "Project Title *",
                    value=st.session_state.form_data.get('project_title', ''),
                    help="Official project name"
                )
                
                project_type = st.selectbox(
                    "Project Type *",
                    ["Software Development", "Infrastructure", "Data/Analytics", 
                     "Process Improvement", "Research", "Other"],
                    index=0
                )
                
                executive_sponsor = st.text_input(
                    "Executive Sponsor",
                    value=st.session_state.form_data.get('executive_sponsor', ''),
                    help="Senior leader accountable for success"
                )
                
                project_manager = st.text_input(
                    "Project Manager",
                    value=st.session_state.form_data.get('project_manager', ''),
                    help="Day-to-day leader"
                )
                
                problem_statement = st.text_area(
                    "Problem Statement *",
                    value=st.session_state.form_data.get('problem_statement', ''),
                    height=120,
                    help="What problem are we solving?"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Target Start Date",
                        value=datetime.now()
                    )
                with col2:
                    end_date = st.date_input(
                        "Target End Date",
                        value=datetime.now() + timedelta(days=90)
                    )
                
                submitted = st.form_submit_button("Save & Continue →", use_container_width=True)
                
                if submitted:
                    st.session_state.form_data.update({
                        'project_title': project_title,
                        'project_type': project_type,
                        'executive_sponsor': executive_sponsor,
                        'project_manager': project_manager,
                        'problem_statement': problem_statement,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    })
                    st.success("✓ Initiation saved! Go to Step 2: Business Case")
        
        # WIZARD STEP 2: Business Case
        with wizard_tab2:
            st.subheader("Business Case Justification")
            
            if not st.session_state.form_data.get('project_title'):
                st.warning("⚠️ Complete Step 1: Initiation first")
            else:
                with st.form("business_case_form"):
                    strategic_alignment = st.text_area(
                        "Strategic Alignment *",
                        value=st.session_state.form_data.get('strategic_alignment', ''),
                        height=120,
                        help="How does this support organizational goals?"
                    )
                    
                    potential_solutions = st.text_area(
                        "Potential Solutions Considered",
                        value=st.session_state.form_data.get('potential_solutions', ''),
                        height=100,
                        help="Alternative approaches evaluated"
                    )
                    
                    preferred_solution = st.text_area(
                        "Preferred Solution & Rationale *",
                        value=st.session_state.form_data.get('preferred_solution', ''),
                        height=120,
                        help="Recommended approach and why"
                    )
                    
                    measurable_benefits = st.text_area(
                        "Measurable Benefits *",
                        value=st.session_state.form_data.get('measurable_benefits', ''),
                        height=100,
                        help="Expected value delivery"
                    )
                    
                    requirements = st.text_area(
                        "High-Level Requirements",
                        value=st.session_state.form_data.get('requirements', ''),
                        height=120,
                        help="Technical, functional, compliance needs"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        budget_estimate = st.text_input(
                            "Budget Estimate",
                            value=st.session_state.form_data.get('budget_estimate', ''),
                            help="e.g., $50k-100k"
                        )
                    with col2:
                        resource_needs = st.text_input(
                            "Resource Needs",
                            value=st.session_state.form_data.get('resource_needs', ''),
                            help="e.g., 2 devs, 1 PM"
                        )
                    
                    submitted = st.form_submit_button("Save & Continue →", use_container_width=True)
                    
                    if submitted:
                        st.session_state.form_data.update({
                            'strategic_alignment': strategic_alignment,
                            'potential_solutions': potential_solutions,
                            'preferred_solution': preferred_solution,
                            'measurable_benefits': measurable_benefits,
                            'requirements': requirements,
                            'budget_estimate': budget_estimate,
                            'resource_needs': resource_needs
                        })
                        st.success("✓ Business Case saved! Go to Step 3: Generate")
        
        # WIZARD STEP 3: Generate Charter
        with wizard_tab3:
            st.subheader("Generate Charter")
            
            if not st.session_state.form_data.get('strategic_alignment'):
                st.warning("⚠️ Complete Step 2: Business Case first")
            else:
                st.info("Ready to generate your charter from the information provided.")
                
                # Pattern selection
                available_patterns = registry.list_patterns()
                selected_patterns = st.multiselect(
                    "Select Optional Patterns to Include",
                    available_patterns,
                    help="Add specialized sections to your charter"
                )
                
                if st.button("🎯 Generate Charter", type="primary", use_container_width=True):
                    with st.spinner("Generating charter..."):
                        charter_text = charter_agent.generate_charter(
                            st.session_state.form_data
                        )
                        st.session_state.charter_text = charter_text
                        
                        # Save charter
                        charter_file.write_text(charter_text)
                        
                        # Mark complete
                        project_registry.mark_charter_complete(st.session_state.project_path)
                        
                        st.success("✓ Charter generated and saved!")
                        st.rerun()


# ============================================================================
# TAB 3: Documentation
# ============================================================================
with tab3:
    st.header("📚 Project Documentation")
    
    # Document selector
    doc_type = st.radio(
        "Select Document",
        ["README", "CHANGELOG", "LICENSE"],
        horizontal=True,
        key="doc_selector"
    )
    
    st.markdown("---")
    
    # Map document to file
    doc_files = {
        "README": "README.md",
        "CHANGELOG": "CHANGELOG.md",
        "LICENSE": "LICENSE"
    }
    
    doc_file = st.session_state.project_path / doc_files[doc_type]
    
    # Display document
    if doc_file.exists():
        doc_content = doc_file.read_text()
        
        # Show with edit capability
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{doc_type}")
        with col2:
            if st.button("✏️ Edit", use_container_width=True, key=f"edit_{doc_type}"):
                st.session_state[f'editing_{doc_type}'] = True
        
        st.markdown("---")
        
        # Edit mode or view mode
        if st.session_state.get(f'editing_{doc_type}', False):
            # Edit mode
            edited_content = st.text_area(
                f"Edit {doc_type}",
                value=doc_content,
                height=400,
                key=f"editor_{doc_type}"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 Save", type="primary", use_container_width=True, key=f"save_{doc_type}"):
                    doc_file.write_text(edited_content)
                    st.session_state[f'editing_{doc_type}'] = False
                    st.success(f"✓ Saved {doc_type}")
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True, key=f"cancel_{doc_type}"):
                    st.session_state[f'editing_{doc_type}'] = False
                    st.rerun()
        else:
            # View mode
            st.markdown(doc_content)
            
            # Download button
            st.download_button(
                "⬇️ Download",
                data=doc_content,
                file_name=doc_files[doc_type],
                mime="text/markdown",
                use_container_width=False,
                key=f"download_{doc_type}"
            )
    else:
        st.warning(f"⚠️ {doc_type} not found")
        
        if st.button(f"➕ Create {doc_type}", type="primary", key=f"create_{doc_type}"):
            # Create with template
            if doc_type == "README":
                template = f"""# {st.session_state.form_data.get('project_title', 'Project')}

## Overview

[Project description]

## Quick Start

[Getting started instructions]

## Documentation

- [Project Charter](PROJECT_CHARTER.md)
- [Project Plan](PROJECT_PLAN.md)

## License

[License information]
"""
            elif doc_type == "CHANGELOG":
                template = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
"""
            else:  # LICENSE
                template = """MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
            
            doc_file.write_text(template)
            st.success(f"✓ Created {doc_type}")
            st.rerun()

# ============================================================================
# TAB 4: Project Home
# ============================================================================
with tab4:
    st.header("🏠 Project Home Dashboard")
    
    # Project metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Project Name", st.session_state.form_data.get('project_title', 'Not Set'))
    with col2:
        st.metric("Owner", st.session_state.form_data.get('project_owner', 'Not Set'))
    with col3:
        st.metric("Type", st.session_state.form_data.get('project_type', 'Not Set'))
    
    st.markdown("---")
    
    # Scaffold structure
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Project Structure")
    with col2:
        if st.button("🏗️ Scaffold Project", use_container_width=True):
            st.info("Scaffold feature coming in next update")
    
    st.markdown("---")
    
    # Activity selector
    st.subheader("LEAN/PM Activities")
    
    # Get available patterns
    patterns = registry.list_patterns()
    
    # Activity radio with status
    activities = [
        ("📊 Project Plan", "project_plan"),
        ("❓ 5W1H Analysis", "5w1h_analysis"),
        ("🔄 SIPOC", "sipoc"),
        ("🐟 Fishbone", "fishbone"),
        ("🎤 Voice of Customer", "voc")
    ]
    
    selected_activity = st.radio(
        "Select Activity",
        [a[0] for a in activities],
        key="activity_selector"
    )
    
    # Get selected pattern key
    selected_idx = [a[0] for a in activities].index(selected_activity)
    pattern_key = activities[selected_idx][1]
    
    # Check if output exists
    has_output = pattern_key in st.session_state.pattern_outputs
    
    st.markdown("---")
    
    # Show status and action
    if has_output:
        st.success(f"✓ {selected_activity} completed")
        
        # Show output
        output = st.session_state.pattern_outputs[pattern_key]
        st.markdown("### Document")
        st.markdown(output['document'])
        
        # Download button
        filename = f"{pattern_key}_{datetime.now().strftime('%Y%m%d')}.md"
        st.download_button(
            "⬇️ Download",
            data=output['document'],
            file_name=filename,
            mime="text/markdown"
        )
        
        # Regenerate option
        if st.button("🔄 Regenerate", key=f"regen_{pattern_key}"):
            del st.session_state.pattern_outputs[pattern_key]
            st.rerun()
    
    else:
        # Check if pattern exists
        if pattern_key in patterns:
            st.info(f"📋 {selected_activity} not yet created")
            
            # Show pattern info
            pattern = registry.get_pattern(pattern_key)
            if pattern and pattern.get('variables'):
                with st.expander("📝 Template Preview - What You'll Need"):
                    st.markdown("**Required Information:**")
                    for var_name, var_config in pattern['variables'].items():
                        required = "✱" if var_config.get('required') else ""
                        st.markdown(f"- **{var_config['label']}** {required}")
                        if var_config.get('help'):
                            st.caption(f"  _{var_config['help']}_")
            
            # Create button
            if st.button(f"✨ Create {selected_activity}", type="primary", use_container_width=True):
                st.session_state.selected_pattern_to_create = pattern_key
                st.session_state.show_pattern_form = True
                st.rerun()
        else:
            st.warning(f"⚠️ {selected_activity} pattern not yet available")
            st.caption("Coming in future update")
    
    # Show pattern creation form if triggered
    if st.session_state.get('show_pattern_form') and st.session_state.get('selected_pattern_to_create'):
        pattern_key = st.session_state.selected_pattern_to_create
        pattern = registry.get_pattern(pattern_key)
        
        st.markdown("---")
        st.subheader(f"Create: {selected_activity}")
        
        # Dynamic form from pattern
        user_inputs = {}
        for var_name, var_config in pattern['variables'].items():
            label = var_config['label']
            if var_config.get('required'):
                label += " *"
            
            if var_config['type'] == 'textarea':
                user_inputs[var_name] = st.text_area(
                    label,
                    height=var_config.get('height', 120),
                    placeholder=var_config.get('placeholder', ''),
                    help=var_config.get('help', ''),
                    key=f"create_{var_name}"
                )
            else:
                user_inputs[var_name] = st.text_input(
                    label,
                    placeholder=var_config.get('placeholder', ''),
                    help=var_config.get('help', ''),
                    key=f"create_{var_name}"
                )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("✨ Generate", type="primary", use_container_width=True):
                with st.spinner("Generating document..."):
                    context = ProjectContext(st.session_state.project_path)
                    pipeline = PatternPipeline(registry, context)
                    
                    result = pipeline.execute(
                        pattern_name=pattern_key,
                        user_inputs=user_inputs,
                        enable_editing=True,
                        enable_critique=True,
                        project_path=st.session_state.project_path
                    )
                    
                    st.session_state.pattern_outputs[pattern_key] = result
                    st.session_state.show_pattern_form = False
                    st.success("✓ Document created!")
                    st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_pattern_form = False
                st.rerun()

# Footer
st.markdown("---")
st.caption("Project Wizard v2.5 - Integrated Workflow | Powered by OpenAI")
