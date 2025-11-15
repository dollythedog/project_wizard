"""
Home dashboard tab showing project overview and quick actions.
"""

import streamlit as st

from app.services.document_registry import DocumentRegistry
from app.services.project_registry import ProjectRegistry


def render_home_tab(project_registry: ProjectRegistry):
    """
    Render the home dashboard tab.

    Args:
        project_registry: ProjectRegistry instance
    """
    st.header("📂 Project Dashboard")

    current_project = project_registry.get_project(st.session_state.project_path)

    # Project info metrics
    _render_project_metrics(current_project, project_registry)

    st.markdown("---")

    # Document statistics
    _render_document_stats()

    st.markdown("---")

    # Recent documents
    _render_recent_documents()

    st.markdown("---")

    # Quick actions
    _render_quick_actions(project_registry)


def _render_project_metrics(current_project: dict, project_registry: ProjectRegistry):
    """Render project information metrics."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Project", current_project.get("name", "Unknown"))

    with col2:
        st.metric("Type", current_project.get("project_type", "Unknown"))

    with col3:
        charter_status = (
            "✅ Complete"
            if project_registry.is_charter_complete(st.session_state.project_path)
            else "⚠️ Pending"
        )
        st.metric("Charter", charter_status)


def _render_document_stats():
    """Render document statistics."""
    doc_registry = DocumentRegistry(st.session_state.project_path)
    stats = doc_registry.get_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Docs", stats["total_documents"])

    with col2:
        st.metric("Core Docs", stats["core_docs"])

    with col3:
        st.metric("Deliverables", stats["deliverables"])

    with col4:
        if stats["average_critique_score"]:
            st.metric("Avg Score", f"{stats['average_critique_score']:.0f}%")
        else:
            st.metric("Avg Score", "N/A")


def _render_recent_documents():
    """Render list of recent documents."""
    st.subheader("Recent Documents")

    doc_registry = DocumentRegistry(st.session_state.project_path)
    recent_docs = doc_registry.list_documents()[:5]

    if recent_docs:
        for doc in recent_docs:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                st.text(f"{doc['name']}")

            with col2:
                st.caption(doc["type"])

            with col3:
                st.caption(doc["status"])

            with col4:
                if doc["critique_score"]:
                    st.caption(f"{doc['critique_score']:.0f}%")
    else:
        st.info("No documents yet")


def _render_quick_actions(project_registry: ProjectRegistry):
    """Render quick action buttons."""
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
