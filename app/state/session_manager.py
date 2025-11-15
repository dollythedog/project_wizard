"""
Centralized session state management for the Project Wizard.
"""

import streamlit as st


def initialize_session_state():
    """
    Initialize all session state variables used throughout the application.

    This should be called once at the start of the application to ensure
    all required session state keys exist with default values.
    """
    # Form data for charter generation
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}

    # Enhanced data from AI agents
    if "enhanced_data" not in st.session_state:
        st.session_state.enhanced_data = {}

    # Generated charter text
    if "charter_text" not in st.session_state:
        st.session_state.charter_text = None

    # Critique from critic agent
    if "critique" not in st.session_state:
        st.session_state.critique = None

    # Current project path
    if "project_path" not in st.session_state:
        st.session_state.project_path = None

    # Pattern outputs from pipeline
    if "pattern_outputs" not in st.session_state:
        st.session_state.pattern_outputs = {}

    # UI state flags
    if "show_new_project_dialog" not in st.session_state:
        st.session_state.show_new_project_dialog = False

    if "show_project_gallery" not in st.session_state:
        st.session_state.show_project_gallery = False


def reset_project_state():
    """
    Reset project-specific state when loading or creating a new project.
    """
    st.session_state.charter_text = None
    st.session_state.critique = None
    st.session_state.pattern_outputs = {}
    st.session_state.enhanced_data = {}


def update_form_data(**kwargs):
    """
    Update form data in session state.

    Args:
        **kwargs: Key-value pairs to update in form_data
    """
    st.session_state.form_data.update(kwargs)


def get_form_data(key: str, default=None):
    """
    Get a value from form data.

    Args:
        key: The key to retrieve
        default: Default value if key doesn't exist

    Returns:
        The value associated with the key, or default
    """
    return st.session_state.form_data.get(key, default)
