#!/usr/bin/env python3
"""
Streamlit Web UI for AI-Enhanced Project Wizard
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ai_agents import CharterAgent, CriticAgent
from app.models.charter import CharterData
import json

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Project Wizard",
    page_icon="🧙‍♂️",
    layout="wide"
)

# Initialize session state
if 'charter_data' not in st.session_state:
    st.session_state.charter_data = {}
if 'ai_drafts' not in st.session_state:
    st.session_state.ai_drafts = {}
if 'critique' not in st.session_state:
    st.session_state.critique = None

# Initialize agents (cached)
@st.cache_resource
def get_agents():
    return CharterAgent(), CriticAgent()

charter_agent, critic_agent = get_agents()

# Header
st.title("🧙‍♂️ AI Project Wizard")
st.markdown("*Generate professional project charters with AI assistance*")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    project_title = st.text_input(
        "Project Title",
        value=st.session_state.charter_data.get('project_title', ''),
        placeholder="My Awesome Project"
    )
    
    project_type = st.selectbox(
        "Project Type",
        ["software_mvp", "clinical_workflow", "infrastructure", "landscaping", "research_analysis", "other"],
        index=0
    )
    
    department = st.text_input(
        "Department",
        value="Texas Pulmonary & Critical Care Consultants"
    )
    
    sponsor = st.text_input(
        "Project Sponsor",
        value="Jonathan Ives"
    )
    
    budget = st.number_input(
        "Budget (USD)",
        min_value=0,
        value=5000,
        step=500
    )
    
    duration = st.number_input(
        "Duration (days)",
        min_value=1,
        value=90,
        step=10
    )
    
    st.divider()
    st.caption("💰 Cost per charter: ~$0.002")
    st.caption("⚡ Generation time: ~30 seconds")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Draft Charter", "🤖 AI Sections", "⭐ Critique", "📥 Export"])

# Tab 1: Project Brief & AI Generation
with tab1:
    st.header("Step 1: Describe Your Project")
    
    project_brief = st.text_area(
        "Project Brief",
        placeholder="Describe your project in 3-5 sentences. What are you building? Who benefits? Why now?",
        height=150,
        help="The AI will use this to draft all charter sections"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🤖 Generate with AI", type="primary", disabled=not project_brief):
            with st.spinner("AI is drafting your charter sections..."):
                context = {
                    "department": department,
                    "project_type": project_type,
                    "budget": budget
                }
                
                try:
                    # Generate all sections
                    progress = st.progress(0)
                    
                    st.session_state.ai_drafts['business_need'] = charter_agent.draft_business_need(project_brief, context)
                    progress.progress(14)
                    
                    st.session_state.ai_drafts['success_criteria'] = charter_agent.draft_success_criteria(project_brief, context)
                    progress.progress(28)
                    
                    st.session_state.ai_drafts['proposed_solution'] = charter_agent.draft_proposed_solution(project_brief, context)
                    progress.progress(42)
                    
                    st.session_state.ai_drafts['risks'] = charter_agent.draft_risks_and_mitigation(project_brief, context)
                    progress.progress(57)
                    
                    st.session_state.ai_drafts['scope'] = charter_agent.draft_scope(project_brief, context)
                    progress.progress(71)
                    
                    st.session_state.ai_drafts['deliverables'] = charter_agent.draft_deliverables(project_brief, context)
                    progress.progress(85)
                    
                    st.session_state.ai_drafts['schedule'] = charter_agent.draft_schedule_overview(project_brief, duration, context)
                    progress.progress(100)
                    
                    st.success("✅ All sections drafted! Review them in the 'AI Sections' tab.")
                    
                except Exception as e:
                    st.error(f"Error generating charter: {e}")
    
    with col2:
        if st.session_state.ai_drafts:
            st.info(f"✨ {len(st.session_state.ai_drafts)} sections drafted. Review in next tab →")

# Tab 2: Review & Edit AI Drafts
with tab2:
    st.header("Step 2: Review & Edit AI-Generated Sections")
    
    if not st.session_state.ai_drafts:
        st.info("👈 Generate charter sections in the 'Draft Charter' tab first")
    else:
        sections = [
            ("Business Need", "business_need"),
            ("Success Criteria", "success_criteria"),
            ("Proposed Solution", "proposed_solution"),
            ("Risks & Mitigation", "risks"),
            ("Scope", "scope"),
            ("Deliverables", "deliverables"),
            ("Schedule Overview", "schedule")
        ]
        
        for label, key in sections:
            if key in st.session_state.ai_drafts:
                with st.expander(f"📄 {label}", expanded=False):
                    edited = st.text_area(
                        f"Edit {label}",
                        value=st.session_state.ai_drafts[key],
                        height=200,
                        key=f"edit_{key}",
                        label_visibility="collapsed"
                    )
                    st.session_state.charter_data[key] = edited
        
        if st.button("💾 Save All Sections"):
            st.success("✅ All sections saved! Proceed to 'Critique' tab for quality review.")

# Tab 3: AI Critique
with tab3:
    st.header("Step 3: AI Quality Critique")
    
    if not st.session_state.charter_data:
        st.info("👈 Complete and save sections first")
    else:
        if st.button("🔍 Run AI Critique", type="primary"):
            with st.spinner("AI Critic is reviewing your charter..."):
                # Combine all sections into charter text
                charter_text = f"""
# PROJECT CHARTER: {project_title}

## Business Need
{st.session_state.charter_data.get('business_need', '')}

## Success Criteria
{st.session_state.charter_data.get('success_criteria', '')}

## Proposed Solution
{st.session_state.charter_data.get('proposed_solution', '')}

## Risks & Mitigation
{st.session_state.charter_data.get('risks', '')}

## Scope
{st.session_state.charter_data.get('scope', '')}

## Deliverables
{st.session_state.charter_data.get('deliverables', '')}

## Schedule
{st.session_state.charter_data.get('schedule', '')}
"""
                
                try:
                    st.session_state.critique = critic_agent.critique_charter(charter_text)
                except Exception as e:
                    st.error(f"Critique error: {e}")
        
        if st.session_state.critique:
            critique = st.session_state.critique
            
            # Overall score
            score = critique.get('weighted_score', 0) * 100
            approved = critique.get('approved', False)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{score:.1f}%", delta=None)
            with col2:
                st.metric("Status", "✅ Approved" if approved else "⚠️ Needs Work")
            with col3:
                st.metric("Threshold", "75%")
            
            # Detailed scores
            st.subheader("📊 Detailed Scores")
            
            scores = critique.get('scores', [])
            for item in scores:
                with st.expander(f"**{item['criterion']}** - Score: {item['score']}/100"):
                    st.markdown(f"**Strengths:**\n{item.get('strengths', 'N/A')}")
                    st.markdown(f"**Weaknesses:**\n{item.get('weaknesses', 'N/A')}")
                    st.markdown(f"**Improvements:**\n{item.get('improvements', 'N/A')}")
            
            # Critical gaps
            if critique.get('critical_gaps'):
                st.subheader("🚨 Critical Gaps")
                for gap in critique['critical_gaps']:
                    st.warning(gap)

# Tab 4: Export
with tab4:
    st.header("Step 4: Export Charter")
    
    if not st.session_state.charter_data:
        st.info("👈 Complete charter sections first")
    else:
        charter_md = f"""# 📋 PROJECT CHARTER

**Project Title:** {project_title}  
**Project Sponsor:** {sponsor}  
**Department:** {department}  
**Date:** {date.today().strftime('%B %Y')}

---

## 1. Business Need / Opportunity

{st.session_state.charter_data.get('business_need', 'Not provided')}

---

## 2. Success Criteria

{st.session_state.charter_data.get('success_criteria', 'Not provided')}

---

## 3. Proposed Solution

{st.session_state.charter_data.get('proposed_solution', 'Not provided')}

---

## 4. Risks & Mitigation

{st.session_state.charter_data.get('risks', 'Not provided')}

---

## 5. Scope

{st.session_state.charter_data.get('scope', 'Not provided')}

---

## 6. Deliverables

{st.session_state.charter_data.get('deliverables', 'Not provided')}

---

## 7. Schedule Overview

{st.session_state.charter_data.get('schedule', 'Not provided')}

---

**Budget:** ${budget:,.2f}  
**Duration:** {duration} days

---

*Generated by AI Project Wizard on {date.today().strftime('%Y-%m-%d')}*
"""
        
        st.markdown("### Preview")
        st.markdown(charter_md)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.download_button(
                label="📥 Download Charter (Markdown)",
                data=charter_md,
                file_name=f"{project_title.lower().replace(' ', '_')}_charter.md",
                mime="text/markdown"
            )
        
        with col2:
            if st.session_state.critique:
                critique_json = json.dumps(st.session_state.critique, indent=2)
                st.download_button(
                    label="📊 Download Critique (JSON)",
                    data=critique_json,
                    file_name=f"{project_title.lower().replace(' ', '_')}_critique.json",
                    mime="application/json"
                )

# Footer
st.divider()
st.caption("🧙‍♂️ AI Project Wizard | Built by Jonathan Ives | Texas Pulmonary & Critical Care Consultants")
