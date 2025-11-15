"""
Project Wizard v2.7 - Kanban Board Phase 1 Complete
Integrated pattern-based workflow with visual issue tracking.
"""

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "app"))

# Import services
from app.services.ai_agents import CharterAgent, CriticAgent
from app.services.pattern_registry import PatternRegistry
from app.services.project_registry import ProjectRegistry
from app.services.project_scaffolder import ProjectScaffolder
from app.services.issue_manager import IssueManager

# Import UI components
from app.state.session_manager import initialize_session_state
from app.ui.modals.new_project import render_new_project_dialog
from app.ui.modals.project_gallery import render_project_gallery
from app.ui.sidebar import render_sidebar
from app.ui.tabs import (
    render_charter_tab,
    render_deliverables_tab,
    render_docs_tab,
    render_home_tab,
    render_issues_tab,
)

# Page config
st.set_page_config(page_title="Project Wizard v2.7", page_icon="🧙‍♂️", layout="wide")


@st.cache_resource
def get_services():
    """Initialize and cache services."""
    patterns_dir = Path(__file__).parent / "patterns"
    registry = PatternRegistry(patterns_dir)
    charter_agent = CharterAgent()
    critic_agent = CriticAgent()
    project_registry = ProjectRegistry()
    scaffolder = ProjectScaffolder()
    issue_manager = IssueManager()
    return registry, charter_agent, critic_agent, project_registry, scaffolder, issue_manager


# Initialize services
registry, charter_agent, critic_agent, project_registry, scaffolder, issue_manager = (
    get_services()
)

# Initialize session state
initialize_session_state()

# Render sidebar
render_sidebar(project_registry)

# Handle modals
if st.session_state.get("show_project_gallery", False):
    render_project_gallery(project_registry)

if st.session_state.get("show_new_project_dialog", False):
    render_new_project_dialog(project_registry)

# Main content
if not st.session_state.get("project_path"):
    # Welcome screen with Issues and README tabs
    st.title("🧙‍♂️ Welcome to Project Wizard v2.7")
    
    # Tabs for welcome screen - Home, Issues, and README
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "📋 Issues", "📖 README"])
    
    with tab1:
        st.markdown(
            """
            Create well-structured projects with AI-powered document generation.
            
            **Get Started:**
            - 📂 Browse existing projects
            - ✨ Start a new project
            """
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Browse Projects", use_container_width=True):
                st.session_state.show_project_gallery = True
                st.rerun()

        with col2:
            if st.button("✨ Start New Project", use_container_width=True):
                st.session_state.show_new_project_dialog = True
                st.rerun()
    
    with tab2:
        # Show Project Wizard's own issues
        render_issues_tab(issue_manager)
    
    with tab3:
        # Show Project Wizard's README
        readme_path = Path(__file__).parent / "README.md"
        if readme_path.exists():
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            st.markdown(readme_content)
        else:
            st.error("README.md not found")
    
    st.stop()

# Project is loaded - show project name in header
current_project = project_registry.get_project(st.session_state.project_path)
if current_project:
    st.title(f"{current_project.get('icon', '🧙‍♂️')} {current_project['name']}")
    st.caption(f"**{current_project.get('project_type', 'Project')}** • `{st.session_state.project_path}`")
else:
    st.title(f"🧙‍♂️ Project")
    st.caption(f"📁 {st.session_state.project_path}")

# Show success message if charter was just created
if st.session_state.get("charter_text") and st.session_state.get("form_data", {}).get(
    "project_title"
):
    st.success("✅ Project charter created successfully!")

# Main tabs for project view
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Home", "📋 Charter", "📚 Documentation", "📦 Deliverables"]
)

with tab1:
    render_home_tab(project_registry)

with tab2:
    render_charter_tab(charter_agent, critic_agent, registry, project_registry)

with tab3:
    render_docs_tab()

with tab4:
    render_deliverables_tab(registry, charter_agent, critic_agent)

# Footer
st.divider()
st.caption("Project Wizard v2.7 - Integrated Workflow | Powered by OpenAI")
