"""Enhanced document editor with pattern-specific critique and markdown editing."""

import streamlit as st
import json
from pathlib import Path
from typing import Optional, Dict, Tuple, Any


class DocumentEditor:
    """Universal document editor supporting any pattern with critique and enhancement."""
    
    def __init__(
        self,
        document_name: str,
        document_content: str,
        charter_agent=None,
        critic_agent=None,
        pattern_key: Optional[str] = None,
        rubric_path: Optional[Path] = None
    ):
        """
        Initialize document editor.
        
        Args:
            document_name: Name of the document (e.g., "PROJECT_CHARTER.md")
            document_content: Current document content
            charter_agent: Agent for enhancements (optional)
            critic_agent: Agent for critique (optional)
            pattern_key: Pattern identifier (e.g., "work_plan", "5w1h_analysis")
            rubric_path: Path to pattern-specific rubric.json
        """
        self.document_name = document_name
        self.document_content = document_content
        self.charter_agent = charter_agent
        self.critic_agent = critic_agent
        self.pattern_key = pattern_key
        self.rubric = self._load_rubric(rubric_path) if rubric_path else None
        
        # Initialize session state for edit mode
        if f'edit_mode_{document_name}' not in st.session_state:
            st.session_state[f'edit_mode_{document_name}'] = False
    
    def _load_rubric(self, rubric_path: Path) -> Optional[Dict]:
        """Load rubric from pattern directory."""
        try:
            if rubric_path.exists():
                with open(rubric_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.warning(f"Could not load rubric: {e}")
        return None
    
    def _has_wizard(self) -> bool:
        """Check if this document type has a wizard for regeneration."""
        # Charter and deliverables have wizards
        return self.document_name in ["PROJECT_CHARTER.md"] or self.pattern_key is not None
    
    def render(self) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Render the editor interface.
        
        Returns:
            Tuple of (updated_content, action_taken)
            action_taken is a dict with 'type' and 'data' keys if an action occurred
        """
        # Initialize or retrieve working content from session state
        working_content_key = f'working_content_{self.document_name}'
        if working_content_key not in st.session_state:
            st.session_state[working_content_key] = self.document_content
        
        col1, col2 = st.columns([2, 1])
        
        action_taken = None
        updated_content = st.session_state[working_content_key]
        
        # LEFT COLUMN: Document Preview/Edit
        with col1:
            st.subheader("📄 Document")
            
            # Edit mode toggle
            edit_mode = st.session_state[f'edit_mode_{self.document_name}']
            
            if st.button("✏️ Edit Raw Markdown" if not edit_mode else "👁️ Preview Mode", key=f"toggle_edit_{self.document_name}"):
                st.session_state[f'edit_mode_{self.document_name}'] = not edit_mode
                st.rerun()
            
            if edit_mode:
                # Raw markdown editing
                st.info("📝 Edit Mode - Direct markdown editing")
                edited_content = st.text_area(
                    "Markdown Content",
                    value=updated_content,
                    height=600,
                    key=f"markdown_editor_{self.document_name}"
                )
                
                if edited_content != updated_content:
                    updated_content = edited_content
                
                if st.button("💾 Save Changes", type="primary", use_container_width=True, key=f"save_changes_{self.document_name}"):
                    # Clear working content on save
                    if working_content_key in st.session_state:
                        del st.session_state[working_content_key]
                    action_taken = {"type": "save", "data": updated_content}
            else:
                # Rendered preview
                st.markdown(updated_content)
        
        # RIGHT COLUMN: Actions
        with col2:
            st.subheader("🛠️ Actions")
            
            # Re-Wizard option (if available)
            if self._has_wizard():
                if st.button("🔄 Re-open Wizard", use_container_width=True, key=f"wizard_{self.document_name}"):
                    action_taken = {"type": "wizard", "data": None}
            
            st.markdown("---")
            
            # Enhancement section
            if self.charter_agent:
                st.subheader("✨ Enhance")
                
                # Custom enhancement
                with st.expander("Custom Enhancement", expanded=False):
                    custom_prompt = st.text_area(
                        "Describe changes you want:",
                        placeholder="Make the language more technical...",
                        height=100,
                        key=f"custom_enhance_{self.document_name}"
                    )
                    
                    if st.button("Send Custom", key=f"custom_btn_{self.document_name}"):
                        if custom_prompt.strip():
                            with st.spinner("Enhancing..."):
                                try:
                                    enhanced = self.charter_agent.enhance_large_document(
                                        updated_content,
                                        feedback=custom_prompt,
                                        chunk_size=1000
                                    )
                                    updated_content = enhanced
                                    st.session_state[working_content_key] = enhanced
                                    action_taken = {"type": "enhance_custom", "data": custom_prompt}
                                    st.success("✓ Enhanced!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Enhancement failed: {e}")
                
                # Quick actions
                st.markdown("**Quick Actions:**")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📝 Wording", use_container_width=True, key=f"wording_{self.document_name}"):
                        with st.spinner("Improving wording..."):
                            try:
                                enhanced = self.charter_agent.enhance_large_document(
                                    updated_content,
                                    feedback="Improve word choice and sentence structure for clarity and professionalism",
                                    chunk_size=1000
                                )
                                updated_content = enhanced
                                st.session_state[working_content_key] = enhanced
                                action_taken = {"type": "enhance_wording", "data": None}
                                st.success("✓ Improved!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {e}")
                
                with col_b:
                    if st.button("🎯 Tone", use_container_width=True, key=f"tone_{self.document_name}"):
                        with st.spinner("Adjusting tone..."):
                            try:
                                enhanced = self.charter_agent.enhance_large_document(
                                    updated_content,
                                    feedback="Rewrite in a more professional and authoritative tone",
                                    chunk_size=1000
                                )
                                updated_content = enhanced
                                st.session_state[working_content_key] = enhanced
                                action_taken = {"type": "enhance_tone", "data": None}
                                st.success("✓ Adjusted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {e}")
                
                if st.button("🔍 Simplify", use_container_width=True, key=f"simplify_{self.document_name}"):
                    with st.spinner("Simplifying..."):
                        try:
                            enhanced = self.charter_agent.enhance_section(
                                "general",
                                updated_content,
                                feedback="Simplify language and reduce jargon"
                            )
                            updated_content = enhanced
                            st.session_state[working_content_key] = enhanced
                            action_taken = {"type": "enhance_simplify", "data": None}
                            st.success("✓ Simplified!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed: {e}")
            
            st.markdown("---")
            
            # Critique section
            if self.critic_agent:
                st.subheader("🔍 Critique")
                
                if st.button("Run Analysis", use_container_width=True, type="primary", key=f"critique_{self.document_name}"):
                    with st.spinner("Analyzing document..."):
                        try:
                            # Use pattern-specific rubric if available
                            critique = self.critic_agent.critique_charter(
                                updated_content,
                                rubric=self.rubric
                            )
                            st.session_state[f'critique_results_{self.document_name}'] = critique
                            action_taken = {"type": "critique", "data": critique}
                            st.success("✓ Analysis complete!")
                        except Exception as e:
                            st.error(f"Error during critique: {e}")
                            st.session_state[f'critique_results_{self.document_name}'] = {
                                "error": str(e),
                                "scores": [],
                                "weighted_score": 0.0,
                                "approved": False
                            }
                
                # Display critique results
                if f'critique_results_{self.document_name}' in st.session_state:
                    results = st.session_state[f'critique_results_{self.document_name}']
                    
                    if results.get("error"):
                        st.error(f"Error: {results['error']}")
                    else:
                        # Summary metrics
                        score_pct = results.get("weighted_score", 0) * 100
                        approved = results.get("approved", False)
                        
                        st.metric(
                            "Overall Score",
                            f"{score_pct:.1f}%",
                            delta="Approved" if approved else "Needs Work",
                            delta_color="normal" if approved else "inverse"
                        )
                        
                        # Detailed scores
                        with st.expander("📊 Detailed Scores", expanded=True):
                            for item in results.get("scores", []):
                                st.markdown(f"**{item['criterion']}**: {item['score']}/100")
                                if item.get('strengths'):
                                    st.markdown(f"✅ {item['strengths']}")
                                if item.get('weaknesses'):
                                    st.markdown(f"⚠️ {item['weaknesses']}")
                                if item.get('improvements'):
                                    st.markdown(f"💡 {item['improvements']}")
                                st.markdown("---")
                        
                        # Overall assessment
                        if results.get("overall_assessment"):
                            st.info(results["overall_assessment"])
                        
                        # Critical gaps
                        if results.get("critical_gaps"):
                            st.warning("**Critical Gaps:**")
                            for gap in results["critical_gaps"]:
                                st.markdown(f"- {gap}")
            else:
                st.info("Critique agent not available for this document type.")
            
            st.markdown("---")
            
            # Save button (always available)
            if st.button("💾 Save Document", type="primary", use_container_width=True, key=f"save_{self.document_name}"):
                action_taken = {"type": "save", "data": updated_content}
        
        return updated_content, action_taken


def render_simple_editor(document_content: str, document_name: str) -> Tuple[str, bool]:
    """Simple fallback editor without AI features."""
    st.markdown(document_content)
    
    if st.button("✏️ Edit", key=f"edit_{document_name}"):
        return document_content, True
    
    return document_content, False
