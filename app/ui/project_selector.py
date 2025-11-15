"""
Project Selector UI Component
Sidebar widget for browsing and switching between projects
"""

import json
from pathlib import Path

import streamlit as st

RECENT_PROJECTS_FILE = Path.home() / ".project_wizard_recent.json"


def load_recent_projects():
    """Load recently accessed projects"""
    if RECENT_PROJECTS_FILE.exists():
        try:
            return json.loads(RECENT_PROJECTS_FILE.read_text())
        except:
            return []
    return []


def save_recent_projects(projects):
    """Save recent projects list"""
    projects = projects[-10:]
    RECENT_PROJECTS_FILE.write_text(json.dumps(projects, indent=2))


def add_recent_project(project_path):
    """Add project to recent list"""
    recent = load_recent_projects()
    if project_path in recent:
        recent.remove(project_path)
    recent.append(project_path)
    save_recent_projects(recent)


def render_project_selector():
    """Render project selector in sidebar. Returns selected project path or None"""
    st.sidebar.header("📁 Project Context")

    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None

    recent = load_recent_projects()

    if recent:
        st.sidebar.subheader("Recent Projects")
        recent_names = [Path(p).name for p in recent]
        recent_names.insert(0, "-- Select Recent --")

        selected_idx = st.sidebar.selectbox(
            "Quick Select",
            range(len(recent_names)),
            format_func=lambda i: recent_names[i],
            key="recent_project_select",
        )

        if selected_idx > 0:
            selected_path = recent[selected_idx - 1]
            if st.sidebar.button("Load Project", key="load_recent"):
                st.session_state.selected_project = Path(selected_path)
                add_recent_project(selected_path)
                st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Or Enter Path")

    default_path = (
        str(st.session_state.selected_project) if st.session_state.selected_project else ""
    )
    project_path_input = st.sidebar.text_input(
        "Project Directory", value=default_path, placeholder="/path/to/project"
    )

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("Load", key="load_manual", use_container_width=True):
            if project_path_input:
                path = Path(project_path_input)
                if path.exists() and path.is_dir():
                    st.session_state.selected_project = path
                    add_recent_project(str(path))
                    st.rerun()
                else:
                    st.sidebar.error("Invalid path")

    with col2:
        if st.button("Clear", key="clear_project", use_container_width=True):
            st.session_state.selected_project = None
            st.rerun()

    if st.session_state.selected_project:
        project = st.session_state.selected_project
        st.sidebar.success("✓ Project Loaded")
        st.sidebar.markdown(f"**{project.name}**")
        st.sidebar.caption(f"`{project}`")

        docs = {
            "Charter": (project / "PROJECT_CHARTER.md").exists(),
            "README": (project / "README.md").exists(),
            "Issues": (project / "ISSUES.md").exists(),
            "Changelog": (project / "CHANGELOG.md").exists(),
        }

        st.sidebar.markdown("**Available Docs:**")
        for doc_name, exists in docs.items():
            icon = "✅" if exists else "❌"
            st.sidebar.caption(f"{icon} {doc_name}")

        return project

    return None
