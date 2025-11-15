"""
New project creation modal.
"""

from pathlib import Path

import streamlit as st

from app.services.project_registry import ProjectRegistry
from app.utils.constants import PROJECT_EMOJIS, PROJECT_TYPES


def render_new_project_dialog(project_registry: ProjectRegistry):
    """
    Render the new project creation dialog.

    Args:
        project_registry: ProjectRegistry instance for managing projects
    """
    st.title("➕ Create New Project")

    # Close button
    if st.button("✖ Cancel", type="secondary"):
        st.session_state.show_new_project_dialog = False
        st.rerun()

    st.markdown("---")

    with st.form("new_project_form"):
        _render_project_details_section()

        st.markdown("---")

        project_full_path = _render_location_section()

        submitted = st.form_submit_button(
            "🚀 Create Project", type="primary", use_container_width=True
        )

        if submitted:
            _handle_project_creation(project_full_path, project_registry)

    st.stop()


def _render_project_details_section():
    """Render project details input fields and return values."""
    st.subheader("Project Details")

    col1, col2 = st.columns([3, 1])

    with col1:
        new_project_name = st.text_input(
            "Project Name *",
            placeholder="e.g., Hermes - Trading Application",
            help="Descriptive name for your project",
            key="new_proj_name",
        )

    with col2:
        new_project_icon = st.selectbox("Icon", PROJECT_EMOJIS, index=0, key="new_proj_icon")

    new_project_type = st.selectbox("Project Type *", PROJECT_TYPES, key="new_proj_type")

    new_project_description = st.text_area(
        "Description (optional)",
        placeholder="Brief description of the project...",
        height=100,
        key="new_proj_desc",
    )

    return new_project_name, new_project_icon, new_project_type, new_project_description


def _render_location_section():
    """Render project location section and return the full path."""
    st.subheader("Project Location")

    # Default location
    default_base = Path.home() / "Projects"

    col1, col2 = st.columns([2, 1])

    with col1:
        base_directory = st.text_input(
            "Base Directory",
            value=str(default_base),
            help="Where to create the project folder",
            key="new_proj_base",
        )

    with col2:
        st.caption("Project folder will be created here")

    # Show what will be created
    new_project_name = st.session_state.get("new_proj_name", "")
    if new_project_name:
        # Sanitize project name for folder
        folder_name = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "_" for c in new_project_name
        )
        folder_name = folder_name.replace(" ", "_")

        project_full_path = Path(base_directory) / folder_name

        st.info(f"📁 Project will be created at: `{project_full_path}`")
        return project_full_path

    return None


def _handle_project_creation(project_full_path: Path, project_registry: ProjectRegistry):
    """
    Handle the project creation process.

    Args:
        project_full_path: Full path where project should be created
        project_registry: ProjectRegistry instance
    """
    new_project_name = st.session_state.get("new_proj_name", "")

    if not new_project_name:
        st.error("Please provide a project name")
        return

    if not project_full_path:
        st.error("Invalid project path")
        return

    try:
        # Create project directory
        project_full_path.mkdir(parents=True, exist_ok=True)

        # Register project
        project_registry.register_project(
            project_full_path,
            name=new_project_name,
            description=st.session_state.get("new_proj_desc", ""),
            project_type=st.session_state.get("new_proj_type", "Other"),
            icon=st.session_state.get("new_proj_icon", "📁"),
        )

        # Set as current project
        st.session_state.project_path = project_full_path

        # Reset form for new project
        st.session_state.form_data = {
            "project_title": new_project_name,
            "project_type": st.session_state.get("new_proj_type", "Other"),
        }
        st.session_state.charter_text = None
        st.session_state.critique = None
        st.session_state.pattern_outputs = {}

        st.session_state.show_new_project_dialog = False
        st.success(f"✓ Created project: {new_project_name}")
        st.rerun()

    except Exception as e:
        st.error(f"Error creating project: {e}")
