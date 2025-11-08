"""
Dynamic Pattern Form Generator
Auto-generates Streamlit input fields from pattern variables.json
"""

import streamlit as st
from typing import Dict, Any


def render_pattern_selector(pattern_registry):
    """Render pattern selector dropdown"""
    patterns = pattern_registry.list_patterns()
    
    if not patterns:
        st.warning("No patterns found in patterns/ directory")
        return None
    
    pattern_names = {
        '5w1h_analysis': '5W1H Analysis - Problem Definition',
        'sipoc': 'SIPOC - Process Overview',
        'fishbone': 'Fishbone Diagram - Root Cause',
        'voc': 'Voice of Customer - Requirements'
    }
    
    display_names = [pattern_names.get(p, p.replace('_', ' ').title()) for p in patterns]
    
    selected_idx = st.selectbox(
        "Select LEAN Activity",
        range(len(patterns)),
        format_func=lambda i: display_names[i],
        key="pattern_selector"
    )
    
    return patterns[selected_idx]


def render_pattern_form(pattern_name, pattern_registry):
    """
    Dynamically generate input form from pattern's variables.json
    
    Returns:
        Dict of user inputs or None if pattern invalid
    """
    pattern = pattern_registry.get_pattern(pattern_name)
    
    if not pattern or not pattern.get('variables'):
        st.error(f"Pattern '{pattern_name}' has no variables defined")
        return None
    
    variables = pattern['variables']
    user_inputs = {}
    
    st.subheader(f"Input Form: {pattern_name.replace('_', ' ').title()}")
    
    for var_name, var_config in variables.items():
        var_type = var_config.get('type', 'text')
        label = var_config.get('label', var_name)
        help_text = var_config.get('help', '')
        placeholder = var_config.get('placeholder', '')
        required = var_config.get('required', False)
        
        label_display = f"{label} {'*' if required else ''}"
        
        if var_type == 'textarea':
            height = var_config.get('height', 150)
            user_inputs[var_name] = st.text_area(
                label_display,
                height=height,
                placeholder=placeholder,
                help=help_text,
                key=f"input_{var_name}"
            )
        
        elif var_type == 'text':
            user_inputs[var_name] = st.text_input(
                label_display,
                placeholder=placeholder,
                help=help_text,
                key=f"input_{var_name}"
            )
        
        elif var_type == 'select':
            options = var_config.get('options', [])
            user_inputs[var_name] = st.selectbox(
                label_display,
                options,
                help=help_text,
                key=f"input_{var_name}"
            )
        
        elif var_type == 'number':
            min_val = var_config.get('min', 0)
            max_val = var_config.get('max', 100)
            user_inputs[var_name] = st.number_input(
                label_display,
                min_value=min_val,
                max_value=max_val,
                help=help_text,
                key=f"input_{var_name}"
            )
        
        elif var_type == 'checkbox':
            user_inputs[var_name] = st.checkbox(
                label_display,
                help=help_text,
                key=f"input_{var_name}"
            )
        
        else:
            st.warning(f"Unknown field type: {var_type}")
            user_inputs[var_name] = st.text_input(
                label_display,
                key=f"input_{var_name}"
            )
    
    st.markdown("---")
    return user_inputs


def validate_required_fields(user_inputs, pattern_registry, pattern_name):
    """Check if all required fields are filled"""
    pattern = pattern_registry.get_pattern(pattern_name)
    if not pattern:
        return False, []
    
    variables = pattern.get('variables', {})
    missing = []
    
    for var_name, var_config in variables.items():
        if var_config.get('required', False):
            value = user_inputs.get(var_name, '')
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append(var_config.get('label', var_name))
    
    return len(missing) == 0, missing
