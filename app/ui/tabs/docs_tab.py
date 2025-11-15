"""
Documentation tab for managing project documents (README, CHANGELOG, LICENSE).
"""

import streamlit as st

from app.utils.constants import (
    CHANGELOG_TEMPLATE,
    DOCUMENT_FILES,
    LICENSE_TEMPLATE,
    README_TEMPLATE,
)


def render_docs_tab():
    """Render the documentation management tab."""
    st.header("📚 Project Documentation")

    # Document selector
    doc_type = st.radio(
        "Select Document", list(DOCUMENT_FILES.keys()), horizontal=True, key="doc_selector"
    )

    st.markdown("---")

    doc_file = st.session_state.project_path / DOCUMENT_FILES[doc_type]

    if doc_file.exists():
        _render_existing_document(doc_file, doc_type)
    else:
        _render_create_document(doc_file, doc_type)


def _render_existing_document(doc_file, doc_type):
    """Render an existing document with edit capability."""
    doc_content = doc_file.read_text()

    # Header with edit button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"{doc_type}")
    with col2:
        if st.button("✏️ Edit", use_container_width=True, key=f"edit_{doc_type}"):
            st.session_state[f"editing_{doc_type}"] = True

    st.markdown("---")

    # Edit mode or view mode
    if st.session_state.get(f"editing_{doc_type}", False):
        _render_edit_mode(doc_file, doc_type, doc_content)
    else:
        _render_view_mode(doc_content, doc_type)


def _render_edit_mode(doc_file, doc_type, doc_content):
    """Render document in edit mode."""
    edited_content = st.text_area(
        f"Edit {doc_type}", value=doc_content, height=400, key=f"editor_{doc_type}"
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("💾 Save", type="primary", use_container_width=True, key=f"save_{doc_type}"):
            doc_file.write_text(edited_content)
            st.session_state[f"editing_{doc_type}"] = False
            st.success(f"✓ Saved {doc_type}")
            st.rerun()

    with col2:
        if st.button("❌ Cancel", use_container_width=True, key=f"cancel_{doc_type}"):
            st.session_state[f"editing_{doc_type}"] = False
            st.rerun()


def _render_view_mode(doc_content, doc_type):
    """Render document in view mode."""
    st.markdown(doc_content)

    # Download button
    st.download_button(
        "⬇️ Download",
        data=doc_content,
        file_name=DOCUMENT_FILES[doc_type],
        mime="text/markdown",
        use_container_width=False,
        key=f"download_{doc_type}",
    )


def _render_create_document(doc_file, doc_type):
    """Render create document interface."""
    st.warning(f"⚠️ {doc_type} not found")

    if st.button(f"➕ Create {doc_type}", type="primary", key=f"create_{doc_type}"):
        template = _get_template(doc_type)
        doc_file.write_text(template)
        st.success(f"✓ Created {doc_type}")
        st.rerun()


def _get_template(doc_type):
    """Get the appropriate template for a document type."""
    project_title = st.session_state.form_data.get("project_title", "Project")

    if doc_type == "README":
        return README_TEMPLATE.format(project_title=project_title)
    elif doc_type == "CHANGELOG":
        return CHANGELOG_TEMPLATE
    else:  # LICENSE
        return LICENSE_TEMPLATE
