"""
Dynamic Pattern Form Generator
Auto-generates Streamlit input fields from pattern variables.json
"""

import json
import streamlit as st
from pathlib import Path


def load_content_library(pattern_path):
    """Load content library for a pattern if it exists"""
    library_path = Path(pattern_path) / "content_library.json"
    if library_path.exists():
        try:
            with open(library_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load content library: {e}")
    return None


def render_library_sidebar(content_library):
    """Render content library in sidebar for easy copying"""
    if not content_library:
        return
    
    with st.sidebar:
        st.markdown("## 📚 Content Library")
        st.caption("Copy & paste these into your form fields")
        
        for category, items in content_library.items():
            if not isinstance(items, list) or not items:
                continue
            
            # Make category name readable
            category_display = category.replace('_', ' ').title()
            
            with st.expander(f"**{category_display}** ({len(items)})"):
                for item in items:
                    st.markdown(f"**{item.get('label', 'Untitled')}**")
                    st.code(item.get('content', ''), language=None)
                    st.markdown("---")


def render_pattern_selector(pattern_registry):
    """Render pattern selector dropdown"""
    patterns = pattern_registry.list_patterns()

    if not patterns:
        st.warning("No patterns found in patterns/ directory")
        return None

    pattern_names = {
        "5w1h_analysis": "5W1H Analysis - Problem Definition",
        "sipoc": "SIPOC - Process Overview",
        "fishbone": "Fishbone Diagram - Root Cause",
        "voc": "Voice of Customer - Requirements",
        "proposal": "📄 Business Proposal",
        "project_charter": "📋 Project Charter",
        "work_plan": "📊 Work Plan",
    }

    display_names = [pattern_names.get(p, p.replace("_", " ").title()) for p in patterns]

    selected_idx = st.selectbox(
        "Select Document Type",
        range(len(patterns)),
        format_func=lambda i: display_names[i],
        key="pattern_selector",
    )

    return patterns[selected_idx]


def render_pattern_form(pattern_name, pattern_registry):
    """
    Dynamically generate input form from pattern's variables.json
    with content library in sidebar

    Returns:
        Dict of user inputs or None if pattern invalid
    """
    pattern = pattern_registry.get_pattern(pattern_name)

    if not pattern or not pattern.get("variables"):
        st.error(f"Pattern '{pattern_name}' has no variables defined")
        return None

    variables = pattern["variables"]
    
    # Load content library and show in sidebar
    pattern_path = Path("patterns") / pattern_name
    content_library = load_content_library(pattern_path)
    
    if content_library:
        render_library_sidebar(content_library)
        total_items = sum(len(v) for v in content_library.values() if isinstance(v, list))
        st.info(f"📚 {total_items} library items available in sidebar → Copy & paste into fields below")

    user_inputs = {}

    st.subheader(f"Input Form: {pattern_name.replace('_', ' ').title()}")

    for var_name, var_config in variables.items():
        # Skip comment fields but render them as headers
        if var_name.startswith("_comment"):
            if var_config and isinstance(var_config, str):
                st.markdown(f"### {var_config}")
            continue
            
        var_type = var_config.get("type", "text")
        label = var_config.get("label", var_name)
        help_text = var_config.get("help", "")
        placeholder = var_config.get("placeholder", "")
        required = var_config.get("required", False)
        library_ref = var_config.get("library", None)

        label_display = f"{label} {'*' if required else ''}"
        
        # Add library hint to help text if applicable
        if library_ref:
            help_text += " 📚 See sidebar for library items to copy"

        if var_type == "textarea":
            height = var_config.get("height", 150)
            
            user_inputs[var_name] = st.text_area(
                label_display,
                height=height,
                placeholder=placeholder,
                help=help_text,
                key=f"input_{var_name}",
            )

        elif var_type == "text":
            user_inputs[var_name] = st.text_input(
                label_display, 
                placeholder=placeholder, 
                help=help_text, 
                key=f"input_{var_name}"
            )

        elif var_type == "select":
            options = var_config.get("options", [])
            user_inputs[var_name] = st.selectbox(
                label_display, options, help=help_text, key=f"input_{var_name}"
            )

        elif var_type == "number":
            min_val = var_config.get("min", 0)
            max_val = var_config.get("max", 100)
            user_inputs[var_name] = st.number_input(
                label_display,
                min_value=min_val,
                max_value=max_val,
                help=help_text,
                key=f"input_{var_name}",
            )

        elif var_type == "checkbox":
            user_inputs[var_name] = st.checkbox(
                label_display, help=help_text, key=f"input_{var_name}"
            )

        else:
            st.warning(f"Unknown field type: {var_type}")
            user_inputs[var_name] = st.text_input(label_display, key=f"input_{var_name}")

    st.markdown("---")
    return user_inputs


def validate_required_fields(user_inputs, pattern_registry, pattern_name):
    """Check if all required fields are filled"""
    pattern = pattern_registry.get_pattern(pattern_name)
    if not pattern:
        return False, []

    variables = pattern.get("variables", {})
    missing = []

    for var_name, var_config in variables.items():
        # Skip comment fields
        if var_name.startswith("_comment"):
            continue
            
        if var_config.get("required", False):
            value = user_inputs.get(var_name, "")
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append(var_config.get("label", var_name))

    return len(missing) == 0, missing
