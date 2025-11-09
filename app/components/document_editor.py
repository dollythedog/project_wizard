"""
Universal Document Editor Component
Provides Option B sidebar layout for editing any document
"""

import streamlit as st
from pathlib import Path
from typing import Optional, Callable

class DocumentEditor:
    """Universal document editor with preview and action sidebar"""
    
    def __init__(
        self,
        document_name: str,
        document_content: str,
        charter_agent=None,
        critic_agent=None
    ):
        self.document_name = document_name
        self.document_content = document_content
        self.charter_agent = charter_agent
        self.critic_agent = critic_agent
    
    def render(self):
        """
        Render the document editor with sidebar
        Returns: (updated_content, action_taken)
        """
        # Main layout: preview (left) + actions (right)
        col_preview, col_actions = st.columns([3, 1])
        
        action_taken = {"type": None, "data": None}
        updated_content = self.document_content
        
        # Right sidebar: Actions
        with col_actions:
            st.markdown("### ACTIONS")
            
            # Section: Re-wizard (if applicable)
            if self._has_wizard():
                st.markdown("#### Re-Wizard")
                if st.button("Re-open Wizard", use_container_width=True, key=f"wizard_{self.document_name}"):
                    action_taken = {"type": "wizard", "data": None}
                st.markdown("---")
            
            # Section: AI Enhancement
            st.markdown("#### Enhance")
            
            # Custom prompt input
            custom_prompt = st.text_area(
                "Custom prompt:",
                placeholder="e.g., Add more detail about security...",
                height=80,
                key=f"custom_prompt_{self.document_name}"
            )
            
            if st.button("Send Custom", use_container_width=True, key=f"custom_{self.document_name}"):
                if custom_prompt and self.charter_agent:
                    with st.spinner("Enhancing..."):
                        enhanced = self.charter_agent.enhance_section(
                            "general",
                            self.document_content,
                            feedback=custom_prompt
                        )
                        updated_content = enhanced
                        action_taken = {"type": "enhance_custom", "data": custom_prompt}
                elif not custom_prompt:
                    st.warning("Please enter a prompt")
            
            st.caption("Quick actions:")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("Wording", use_container_width=True, key=f"wording_{self.document_name}"):
                    if self.charter_agent:
                        with st.spinner("Improving..."):
                            enhanced = self.charter_agent.enhance_section(
                                "general",
                                self.document_content,
                                feedback="Improve word choice and sentence structure"
                            )
                            updated_content = enhanced
                            action_taken = {"type": "enhance_wording", "data": None}
            
            with col_b:
                if st.button("Tone", use_container_width=True, key=f"tone_{self.document_name}"):
                    if self.charter_agent:
                        with st.spinner("Adjusting..."):
                            enhanced = self.charter_agent.enhance_section(
                                "general",
                                self.document_content,
                                feedback="Rewrite in professional tone"
                            )
                            updated_content = enhanced
                            action_taken = {"type": "enhance_tone", "data": None}
            
            if st.button("Simplify", use_container_width=True, key=f"simplify_{self.document_name}"):
                if self.charter_agent:
                    with st.spinner("Simplifying..."):
                        enhanced = self.charter_agent.enhance_section(
                            "general",
                            self.document_content,
                            feedback="Simplify language"
                        )
                        updated_content = enhanced
                        action_taken = {"type": "enhance_simplify", "data": None}
            
            st.markdown("---")
            
            # Section: Quality Check
            st.markdown("#### Critique")
            
            if st.button("Run Analysis", use_container_width=True, key=f"critique_{self.document_name}"):
                if self.critic_agent:
                    with st.spinner("Analyzing..."):
                        try:
                            critique = self.critic_agent.critique_charter(self.document_content)
                            if critique:
                                st.session_state[f'critique_results_{self.document_name}'] = critique
                                action_taken = {"type": "critique", "data": critique}
                                st.success("✓ Analysis complete!")
                            else:
                                st.error("Critique returned empty result")
                        except Exception as e:
                            st.error(f"Error during critique: {str(e)}")
                            st.session_state[f'critique_results_{self.document_name}'] = {
                                "error": str(e),
                                "scores": [],
                                "weighted_score": 0.0,
                                "approved": False
                            }
                else:
                    st.warning("Critic agent not available")
            
            # Display critique results if available
            if f'critique_results_{self.document_name}' in st.session_state:
                critique_data = st.session_state[f'critique_results_{self.document_name}']
                
                if critique_data:
                    if "error" in critique_data:
                        st.error(f"Error: {critique_data['error']}")
                    else:
                        # KPI Summary
                        st.markdown("---")
                        
                        # Weighted score as main KPI
                        weighted_score = critique_data.get('weighted_score', 0) * 100
                        approved = critique_data.get('approved', False)
                        
                        # Color-coded score display
                        if approved:
                            st.success(f"**Overall Score: {weighted_score:.0f}%** ✓")
                        else:
                            st.warning(f"**Overall Score: {weighted_score:.0f}%**")
                        
                        # Expandable detailed results
                        with st.expander("📊 Detailed Analysis", expanded=False):
                            # Overall assessment
                            if critique_data.get('overall_assessment'):
                                st.markdown("**Overall Assessment**")
                                st.info(critique_data['overall_assessment'])
                            
                            # Scores by criterion
                            if critique_data.get('scores'):
                                st.markdown("**Scores by Criterion**")
                                for item in critique_data['scores']:
                                    score = item.get('score', 0)
                                    criterion = item.get('criterion', 'Unknown')
                                    
                                    # Progress bar for each criterion
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.markdown(f"*{criterion}*")
                                        st.progress(score / 100)
                                    with col2:
                                        st.markdown(f"**{score}%**")
                                    
                                    # Show strengths/weaknesses in sub-expander
                                    with st.expander(f"Details: {criterion}", expanded=False):
                                        if item.get('strengths'):
                                            st.markdown(f"✅ **Strengths:** {item['strengths']}")
                                        if item.get('weaknesses'):
                                            st.markdown(f"⚠️ **Weaknesses:** {item['weaknesses']}")
                                        if item.get('improvements'):
                                            st.markdown(f"💡 **Improvements:** {item['improvements']}")
                            
                            # Critical gaps
                            if critique_data.get('critical_gaps'):
                                st.markdown("**Critical Gaps**")
                                for gap in critique_data['critical_gaps']:
                                    st.markdown(f"- 🔴 {gap}")
                            
                            # Recommended next steps
                            if critique_data.get('recommended_next_steps'):
                                st.markdown("**Recommended Next Steps**")
                                for step in critique_data['recommended_next_steps']:
                                    st.markdown(f"- 🎯 {step}")
                else:
                    st.info("No critique results available")
            
            # Section: Save
            st.markdown("#### Save")
            
            if st.button("Undo", use_container_width=True, key=f"undo_{self.document_name}"):
                action_taken = {"type": "undo", "data": None}
            
            if st.button("Save", use_container_width=True, type="primary", key=f"save_{self.document_name}"):
                action_taken = {"type": "save", "data": updated_content}
            
            if st.button("Download", use_container_width=True, key=f"download_{self.document_name}"):
                action_taken = {"type": "download", "data": updated_content}
        
        # Left side: Preview
        with col_preview:
            st.markdown("### Document Preview")
            st.markdown(updated_content)
        
        return updated_content, action_taken
    
    def _has_wizard(self):
        """Check if this document type has a wizard"""
        wizard_types = ["PROJECT_CHARTER.md"]
        return self.document_name in wizard_types


def render_simple_editor(document_name, document_content, project_path):
    """
    Simplified editor for core documents (no AI features)
    """
    st.markdown(f"### {document_name}")
    
    col_preview, col_actions = st.columns([3, 1])
    
    updated_content = document_content
    
    with col_actions:
        st.markdown("### ACTIONS")
        
        if st.button("Edit", use_container_width=True, key=f"edit_simple_{document_name}"):
            st.session_state[f"editing_{document_name}"] = True
        
        if st.button("Save", use_container_width=True, type="primary", key=f"save_simple_{document_name}"):
            doc_file = project_path / document_name
            doc_file.write_text(st.session_state.get(f"temp_content_{document_name}", document_content))
            st.success(f"Saved {document_name}")
            st.session_state[f"editing_{document_name}"] = False
        
        if st.button("Download", use_container_width=True, key=f"download_simple_{document_name}"):
            st.download_button(
                "Download",
                data=document_content,
                file_name=document_name,
                mime="text/markdown"
            )
    
    with col_preview:
        if st.session_state.get(f"editing_{document_name}", False):
            edited = st.text_area(
                "Edit markdown:",
                value=document_content,
                height=500,
                key=f"editor_{document_name}"
            )
            st.session_state[f"temp_content_{document_name}"] = edited
            updated_content = edited
        else:
            st.markdown(document_content)
    
    return updated_content
