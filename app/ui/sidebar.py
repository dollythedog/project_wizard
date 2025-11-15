"""
Sidebar component for project management and navigation.
"""

from pathlib import Path

import streamlit as st

from app.services.project_registry import ProjectRegistry
from app.utils.parsers import load_project_charter, parse_charter_to_form_data


def render_sidebar(project_registry: ProjectRegistry):
    """
    Render the sidebar with project management controls.

    Args:
        project_registry: ProjectRegistry instance for managing projects
    """
    with st.sidebar:
        st.header("🧙‍♂️ Project Wizard")

        # Current project display
        _render_current_project(project_registry)

        st.markdown("---")

        # Action buttons
        _render_action_buttons()

        st.markdown("---")

        # Recent projects quick access
        _render_recent_projects(project_registry)

        st.markdown("---")
        st.caption("Project Wizard v2.5")


def _render_current_project(project_registry: ProjectRegistry):
    """Display the currently loaded project."""
    if st.session_state.project_path:
        current_project = project_registry.get_project(st.session_state.project_path)
        if current_project:
            st.success(f"{current_project['icon']} **{current_project['name']}**")
            st.caption(f"`{Path(current_project['path']).name}`")
        else:
            st.info("📂 No project loaded")
    else:
        st.info("📂 No project loaded")


def _render_action_buttons():
    """Render action buttons for project gallery and new project."""
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 My Projects", use_container_width=True):
            st.session_state.show_project_gallery = True
            st.rerun()

    with col2:
        if st.button("➕ New Project", use_container_width=True):
            st.session_state.show_new_project_dialog = True
            st.rerun()


def _render_recent_projects(project_registry: ProjectRegistry):
    """Display recent projects with quick load buttons."""
    projects = project_registry.list_projects(sort_by="last_accessed")

    if projects:
        st.subheader("Recent Projects")

        for project in projects[:5]:  # Show 5 most recent
            project_path = Path(project["path"])

            col1, col2 = st.columns([4, 1])

            with col1:
                st.caption(f"{project['icon']} {project['name']}")

            with col2:
                if st.button("📂", key=f"quick_load_{project['path']}", help="Load project"):
                    _load_project(project_path, project_registry)


def _load_project(project_path: Path, project_registry: ProjectRegistry):
    """
    Load a project and its charter if it exists.

    Args:
        project_path: Path to the project directory
        project_registry: ProjectRegistry instance
    """
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
