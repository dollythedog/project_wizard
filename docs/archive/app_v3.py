"""
Project Wizard v3.0 - Pattern-Based Document Generation
With project context and dynamic LEAN activity support
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Add directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.pattern_pipeline import PatternPipeline
from app.ui.project_selector import render_project_selector
from app.ui.pattern_form import render_pattern_selector, render_pattern_form, validate_required_fields

# Page config
st.set_page_config(
    page_title="Project Wizard v3.0",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def get_pattern_registry():
    return PatternRegistry()

# Main header
st.title("🧙‍♂️ Project Wizard v3.0")
st.caption("Pattern-Based Document Generation with Project Context")

# Sidebar: Project selector
selected_project = render_project_selector()

# Initialize pattern registry
registry = get_pattern_registry()

# Main tabs
tab1, tab2, tab3 = st.tabs([
    "📋 Charter Generation",
    "🔧 LEAN Activities",  
    "📊 Project Dashboard"
])

# ============================================================================
# TAB 1: Charter Generation (Existing v2.0 functionality)
# ============================================================================
with tab1:
    st.header("Project Charter Generation")
    st.info("💡 Use Tab 2 'LEAN Activities' for 5W1H, SIPOC, Fishbone, etc.")
    st.markdown("This tab contains the existing charter generation workflow from v2.0")

# ============================================================================
# TAB 2: LEAN Activities (NEW - Pattern-based)
# ============================================================================
with tab2:
    st.header("LEAN/PM Activities")
    
    if not selected_project:
        st.warning("⚠️ Please select a project from the sidebar to enable LEAN activities")
        st.info("LEAN activities reference your project documentation for context-aware generation")
        st.stop()
    
    st.success(f"✓ Working with project: **{selected_project.name}**")
    
    # Pattern selector
    st.subheader("Step 1: Select Activity")
    selected_pattern = render_pattern_selector(registry)
    
    if not selected_pattern:
        st.error("No patterns available")
        st.stop()
    
    st.markdown("---")
    
    # Dynamic form
    st.subheader("Step 2: Fill in Details")
    user_inputs = render_pattern_form(selected_pattern, registry)
    
    # Options
    with st.expander("⚙️ Generation Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_editing = st.checkbox("Enable AI Editing", value=True, 
                                        help="Polish draft for clarity")
        with col2:
            enable_critique = st.checkbox("Enable Quality Critique", value=True,
                                         help="Evaluate against rubric")
        with col3:
            max_iterations = st.number_input("Max Revisions", min_value=0, max_value=5, 
                                            value=2, help="Critique-revision loops")
    
    # Generate button
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        generate_button = st.button("✨ Generate Document", type="primary", 
                                    use_container_width=True)
    
    with col2:
        clear_button = st.button("Clear Results", use_container_width=True)
    
    if clear_button:
        if 'pattern_result' in st.session_state:
            del st.session_state['pattern_result']
        st.rerun()
    
    # Execute pipeline
    if generate_button:
        # Validate required fields
        is_valid, missing = validate_required_fields(user_inputs, registry, selected_pattern)
        
        if not is_valid:
            st.error(f"⚠️ Please fill in required fields: {', '.join(missing)}")
            st.stop()
        
        # Initialize pipeline
        context = ProjectContext(selected_project)
        pipeline = PatternPipeline(registry, context)
        
        # Execute with progress
        with st.spinner("Generating document... This may take 30-60 seconds"):
            progress_bar = st.progress(0, text="Initializing...")
            
            try:
                # Stage updates
                progress_bar.progress(20, text="📝 Drafting initial content...")
                
                result = pipeline.execute(
                    pattern_name=selected_pattern,
                    user_inputs=user_inputs,
                    enable_editing=enable_editing,
                    enable_critique=enable_critique,
                    max_revision_iterations=max_iterations,
                    project_path=selected_project
                )
                
                progress_bar.progress(100, text="✓ Complete!")
                st.session_state['pattern_result'] = result
                st.success("✓ Document generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
    
    # Display results
    if 'pattern_result' in st.session_state:
        result = st.session_state['pattern_result']
        
        st.markdown("---")
        st.subheader("📄 Generated Document")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Document Size", f"{len(result['document'])} chars")
        
        with col2:
            if result['final_score']:
                score_val = result['final_score'] * 100
                st.metric("Quality Score", f"{score_val:.0f}%")
            else:
                st.metric("Quality Score", "N/A")
        
        with col3:
            st.metric("Revisions", result['iterations'])
        
        with col4:
            status = "✓ Approved" if result.get('critique', {}).get('approved') else "⚠️ Review"
            st.metric("Status", status)
        
        # Document tabs
        doc_tab1, doc_tab2, doc_tab3 = st.tabs(["📄 Document", "📊 Critique", "🔍 Pipeline Log"])
        
        with doc_tab1:
            st.markdown(result['document'])
            
            # Download button
            filename = f"{selected_pattern}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            st.download_button(
                "⬇️ Download Markdown",
                data=result['document'],
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
        
        with doc_tab2:
            if result.get('critique'):
                critique = result['critique']
                
                # Overall assessment
                if critique.get('overall_assessment'):
                    st.markdown("### Overall Assessment")
                    st.info(critique['overall_assessment'])
                
                # Scores
                if critique.get('scores'):
                    st.markdown("### Detailed Scores")
                    for score in critique['scores']:
                        with st.expander(f"{score['criterion']} - {score['score']}/100"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Strengths:**")
                                for strength in score.get('strengths', []):
                                    st.markdown(f"- {strength}")
                            with col2:
                                st.markdown("**Improvements:**")
                                for imp in score.get('improvements', []):
                                    st.markdown(f"- {imp}")
                
                # Critical gaps
                if critique.get('critical_gaps'):
                    st.markdown("### Critical Gaps")
                    for gap in critique['critical_gaps']:
                        st.warning(gap)
            else:
                st.info("Critique not available (may have been disabled)")
        
        with doc_tab3:
            st.markdown("### Pipeline Execution Log")
            for log_entry in result.get('pipeline_log', []):
                stage = log_entry.get('stage', 'unknown')
                if 'length' in log_entry:
                    st.text(f"• {stage}: {log_entry['length']} characters")
                if 'score' in log_entry:
                    st.text(f"  Score: {log_entry['score']:.2f}")

# ============================================================================
# TAB 3: Project Dashboard
# ============================================================================
with tab3:
    st.header("Project Dashboard")
    
    if not selected_project:
        st.info("Select a project to see dashboard")
    else:
        context = ProjectContext(selected_project)
        summary = context.get_summary()
        
        st.subheader(f"Project: {summary['project_name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            icon = "✅" if summary['has_charter'] else "❌"
            st.metric("Charter", icon)
        
        with col2:
            icon = "✅" if summary['has_readme'] else "❌"
            st.metric("README", icon)
        
        with col3:
            icon = "✅" if summary['has_issues'] else "❌"
            st.metric("Issues", icon)
        
        with col4:
            icon = "✅" if summary['has_changelog'] else "❌"
            st.metric("Changelog", icon)
        
        st.markdown("---")
        
        # Show available patterns
        st.subheader("Available LEAN Activities")
        patterns = registry.list_patterns()
        for pattern in patterns:
            st.markdown(f"- **{pattern.replace('_', ' ').title()}**")

# Footer
st.markdown("---")
st.caption("Project Wizard v3.0 - Pattern-Based Document Generation | Powered by OpenAI")
