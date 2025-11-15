"""
Project gallery modal for browsing and managing projects.
"""

from pathlib import Path

import streamlit as st

from app.services.project_registry import ProjectRegistry
from app.utils.parsers import load_project_charter, parse_charter_to_form_data


def render_project_gallery(project_registry: ProjectRegistry):
    """
    Render the project gallery modal.

    Args:
        project_registry: ProjectRegistry instance for managing projects
    """
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
        _render_project_grid(projects, project_registry)

    st.stop()


def _render_project_grid(projects: list, project_registry: ProjectRegistry):
    """
    Render projects in a grid layout.

    Args:
        projects: List of project dictionaries
        project_registry: ProjectRegistry instance
    """
    cols_per_row = 3

    for i in range(0, len(projects), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            if i + j < len(projects):
                project = projects[i + j]
                with col:
                    _render_project_card(project, project_registry)


def _render_project_card(project: dict, project_registry: ProjectRegistry):
    """
    Render a single project card.

    Args:
        project: Project dictionary with metadata
        project_registry: ProjectRegistry instance
    """
    project_path = Path(project["path"])

    with st.container():
        st.markdown(f"### {project['icon']} {project['name']}")
        st.caption(f"**Type:** {project['project_type']}")

        # Description
        if project.get("description"):
            desc = project["description"]
            display_desc = desc[:100] + "..." if len(desc) > 100 else desc
            st.caption(display_desc)

        st.caption(f"📅 Created: {project['created_date'][:10]}")

        # Action buttons
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("📂 Open", key=f"open_{project['path']}", use_container_width=True):
                _open_project(project_path, project_registry)

        with col_b:
            if st.button(
                "🗑️",
                key=f"remove_{project['path']}",
                help="Remove from list",
                use_container_width=True,
            ):
                project_registry.remove_project(project_path)
                st.rerun()

    st.markdown("---")


def _open_project(project_path: Path, project_registry: ProjectRegistry):
    """
    Open a project and load its charter.

    Args:
        project_path: Path to the project directory
        project_registry: ProjectRegistry instance
    """
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
