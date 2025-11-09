"""
Project Wizard v2.0 - Streamlit Web Interface
Structured data collection following formal PM methodology
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from services.ai_agents.charter_agent import CharterAgent
from services.ai_agents.critic_agent import CriticAgent
from services.ai_agents.llm_client import LLMClient

# Page config
st.set_page_config(
    page_title="Project Wizard v2.0",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'enhanced_data' not in st.session_state:
    st.session_state.enhanced_data = {}
if 'manual_edits' not in st.session_state:
    st.session_state.manual_edits = {}
if 'charter_text' not in st.session_state:
    st.session_state.charter_text = None
if 'critique' not in st.session_state:
    st.session_state.critique = None

# Initialize agents
@st.cache_resource
def get_charter_agent():
    return CharterAgent()

@st.cache_resource
def get_critic_agent():
    return CriticAgent()

charter_agent = get_charter_agent()
critic_agent = get_critic_agent()

# Sidebar
with st.sidebar:
    st.title("🧙‍♂️ Project Wizard v2.0")
    st.markdown("**Structured PM Methodology**")
    st.markdown("---")
    
    st.markdown("### 📋 Workflow")
    st.markdown("""
    1. **Initiate** - Define business need
    2. **Business Case** - Justify the project
    3. **AI Enhancement** - Polish your inputs
    4. **Generate Charter** - Create the document
    5. **Quality Review** - AI critique
    6. **Create Project** - Scaffold structure
    """)
    
    st.markdown("---")
    st.caption("v2.0.0 | MVP Release")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1️⃣ Project Initiation",
    "2️⃣ Business Case", 
    "3️⃣ AI Enhancement",
    "4️⃣ Generate Charter",
    "5️⃣ Quality Review",
    "6️⃣ Create Project"
])

# ============================================================================
# TAB 1: PROJECT INITIATION REQUEST
# ============================================================================
with tab1:
    st.header("📝 Project Initiation Request")
    st.markdown("*Define the core problem and desired outcomes*")
    st.markdown("---")
    
    with st.form("initiation_form"):
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input(
                "Project Name *",
                value=st.session_state.form_data.get('project_name', ''),
                placeholder="e.g., Website Redesign Project"
            )
        with col2:
            project_owner = st.text_input(
                "Project Owner *",
                value=st.session_state.form_data.get('project_owner', ''),
                placeholder="Your name"
            )
        
        st.markdown("---")
        st.subheader("Problem & Outcomes")
        
        business_need = st.text_area(
            "Business Need / Problem Statement *",
            value=st.session_state.form_data.get('business_need', ''),
            placeholder="What problem are you solving? Be specific about current pain points.",
            height=120,
            help="Describe the problem clearly. Do NOT include metrics unless you have them."
        )
        
        desired_outcomes = st.text_area(
            "Desired Outcomes *",
            value=st.session_state.form_data.get('desired_outcomes', ''),
            placeholder="What do you want to achieve? What will success look like?",
            height=120,
            help="Focus on qualitative outcomes, not implementation details."
        )
        
        success_criteria = st.text_area(
            "Success Criteria *",
            value=st.session_state.form_data.get('success_criteria', ''),
            placeholder="How will you measure success? What are the specific, measurable criteria?",
            height=120,
            help="If you have specific metrics, include them. Otherwise, describe measurable indicators."
        )
        
        initial_risks = st.text_area(
            "Initial Risks & Assumptions",
            value=st.session_state.form_data.get('initial_risks', ''),
            placeholder="What risks do you foresee? What assumptions are you making?",
            height=100
        )
        
        submitted1 = st.form_submit_button("Save Initiation Request", type="primary", use_container_width=True)
        
        if submitted1:
            if not all([project_name, project_owner, business_need, desired_outcomes, success_criteria]):
                st.error("❌ Please fill in all required fields (*)")
            else:
                st.session_state.form_data.update({
                    'project_name': project_name,
                    'project_owner': project_owner,
                    'business_need': business_need,
                    'desired_outcomes': desired_outcomes,
                    'success_criteria': success_criteria,
                    'initial_risks': initial_risks
                })
                st.success("✅ Initiation Request saved! Continue to Tab 2.")

# ============================================================================
# TAB 2: BUSINESS CASE
# ============================================================================
with tab2:
    st.header("💼 Business Case")
    st.markdown("*Justify the project and define the approach*")
    st.markdown("---")
    
    if 'project_name' not in st.session_state.form_data:
        st.warning("⚠️ Please complete Tab 1 (Project Initiation) first.")
    else:
        with st.form("business_case_form"):
            st.subheader("Strategic Context")
            
            strategic_alignment = st.text_area(
                "Strategic Alignment *",
                value=st.session_state.form_data.get('strategic_alignment', ''),
                placeholder="How does this align with organizational goals/strategy?",
                height=100,
                help="Connect to broader organizational objectives."
            )
            
            st.markdown("---")
            st.subheader("Solution Analysis")
            
            potential_solutions = st.text_area(
                "Potential Solutions Considered",
                value=st.session_state.form_data.get('potential_solutions', ''),
                placeholder="What options did you consider? (Optional if you have only one obvious solution)",
                height=100
            )
            
            preferred_solution = st.text_area(
                "Preferred Solution / Approach *",
                value=st.session_state.form_data.get('preferred_solution', ''),
                placeholder="What solution do you recommend and why?",
                height=120,
                help="Describe your chosen approach and rationale."
            )
            
            st.markdown("---")
            st.subheader("Requirements & Resources")
            
            measurable_benefits = st.text_area(
                "Measurable Benefits *",
                value=st.session_state.form_data.get('measurable_benefits', ''),
                placeholder="What specific benefits will this deliver? Include metrics if available.",
                height=100,
                help="Quantify when possible, qualify when not."
            )
            
            high_level_requirements = st.text_area(
                "High-Level Requirements *",
                value=st.session_state.form_data.get('high_level_requirements', ''),
                placeholder="What are the key requirements? (technical, functional, compliance, etc.)",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                budget_estimate = st.text_input(
                    "Budget Estimate",
                    value=st.session_state.form_data.get('budget_estimate', ''),
                    placeholder="e.g., $10,000 or 'Internal resources only'"
                )
            with col2:
                duration_estimate = st.text_input(
                    "Duration Estimate *",
                    value=st.session_state.form_data.get('duration_estimate', ''),
                    placeholder="e.g., 3 months, 12 weeks"
                )
            
            submitted2 = st.form_submit_button("Save Business Case", type="primary", use_container_width=True)
            
            if submitted2:
                required = [strategic_alignment, preferred_solution, measurable_benefits, 
                           high_level_requirements, duration_estimate]
                if not all(required):
                    st.error("❌ Please fill in all required fields (*)")
                else:
                    st.session_state.form_data.update({
                        'strategic_alignment': strategic_alignment,
                        'potential_solutions': potential_solutions,
                        'preferred_solution': preferred_solution,
                        'measurable_benefits': measurable_benefits,
                        'high_level_requirements': high_level_requirements,
                        'budget_estimate': budget_estimate,
                        'duration_estimate': duration_estimate
                    })
                    st.success("✅ Business Case saved! Continue to Tab 3 for AI Enhancement.")

# ============================================================================
# TAB 3: AI ENHANCEMENT
# ============================================================================
with tab3:
    st.header("✨ AI Enhancement")
    st.markdown("*Polish your inputs with AI assistance*")
    st.markdown("---")
    
    if len(st.session_state.form_data) < 10:
        st.warning("⚠️ Please complete Tabs 1 and 2 first.")
    else:
        st.info("💡 AI will enhance your text for clarity and professional structure WITHOUT adding facts or data you didn't provide.")
        
        # Map fields to enhancement keys
        field_map = {
            'business_need': 'business_need',
            'desired_outcomes': 'desired_outcomes',
            'success_criteria': 'success_criteria',
            'strategic_alignment': 'strategic_alignment',
            'preferred_solution': 'preferred_solution',
            'measurable_benefits': 'measurable_benefits',
            'high_level_requirements': 'high_level_requirements'
        }
        
        st.markdown("### Review & Enhance Each Section")
        
        for field_label, field_key in field_map.items():
            with st.expander(f"📄 {field_label.replace('_', ' ').title()}", expanded=False):
                original = st.session_state.form_data.get(field_key, '')
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Your Original Text:**")
                    st.text_area(
                        "Original",
                        value=original,
                        height=100,
                        disabled=True,
                        key=f"orig_{field_key}",
                        label_visibility="collapsed"
                    )
                
                with col2:
                    if st.button(f"✨ Enhance", key=f"btn_enhance_{field_key}", use_container_width=True):
                        with st.spinner("Enhancing..."):
                            try:
                                enhanced = charter_agent.enhance_section(field_key, original)
                                st.session_state.enhanced_data[field_key] = enhanced
                                st.success("✅ Enhanced!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Enhancement failed: {e}")
                
                # Show enhanced version if available
                if field_key in st.session_state.enhanced_data:
                    st.markdown("**✨ AI-Enhanced Version:**")
                    st.markdown(st.session_state.enhanced_data[field_key])
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✅ Accept", key=f"accept_{field_key}", use_container_width=True):
                            st.session_state.form_data[field_key] = st.session_state.enhanced_data[field_key]
                            del st.session_state.enhanced_data[field_key]
                            st.success("Accepted!")
                            st.rerun()
                    with col_b:
                        if st.button("❌ Reject", key=f"reject_{field_key}", use_container_width=True):
                            del st.session_state.enhanced_data[field_key]
                            st.info("Keeping original")
                            st.rerun()
                    with col_c:
                        if st.button("✏️ Edit Manually", key=f"edit_{field_key}", use_container_width=True):
                            st.session_state.manual_edits[field_key] = st.session_state.enhanced_data[field_key]
                            st.rerun()
                    
                    # Show editable version if Edit was clicked
                    if field_key in st.session_state.manual_edits:
                        st.markdown("**✏️ Edit Your Version:**")
                        edited_text = st.text_area(
                            "Edit",
                            value=st.session_state.manual_edits[field_key],
                            height=150,
                            key=f"manual_edit_{field_key}",
                            label_visibility="collapsed"
                        )
                        if st.button("💾 Save Manual Edit", key=f"save_manual_{field_key}"):
                            st.session_state.form_data[field_key] = edited_text
                            del st.session_state.manual_edits[field_key]
                            if field_key in st.session_state.enhanced_data:
                                del st.session_state.enhanced_data[field_key]
                            st.success("✅ Manual edit saved!")
                            st.rerun()

# ============================================================================
# TAB 4: GENERATE CHARTER
# ============================================================================
with tab4:
    st.header("📜 Generate Project Charter")
    st.markdown("*Create the formal charter document*")
    st.markdown("---")
    
    if len(st.session_state.form_data) < 10:
        st.warning("⚠️ Please complete Tabs 1-3 first.")
    else:
        st.success("✅ All required information collected!")
        
        if st.button("🎯 Generate Charter Document", type="primary", use_container_width=True):
            with st.spinner("Generating charter..."):
                # Build charter from user data (NOT AI generation)
                charter_sections = []
                
                charter_sections.append(f"# PROJECT CHARTER: {st.session_state.form_data['project_name'].upper()}")
                charter_sections.append(f"\n**Project Owner:** {st.session_state.form_data['project_owner']}")
                charter_sections.append(f"**Date:** {date.today().strftime('%B %d, %Y')}")
                charter_sections.append(f"**Status:** Draft\n")
                
                charter_sections.append("---\n")
                charter_sections.append("## 1. BUSINESS NEED")
                charter_sections.append(st.session_state.form_data['business_need'])
                
                charter_sections.append("\n## 2. DESIRED OUTCOMES")
                charter_sections.append(st.session_state.form_data['desired_outcomes'])
                
                charter_sections.append("\n## 3. SUCCESS CRITERIA")
                charter_sections.append(st.session_state.form_data['success_criteria'])
                
                charter_sections.append("\n## 4. STRATEGIC ALIGNMENT")
                charter_sections.append(st.session_state.form_data['strategic_alignment'])
                
                charter_sections.append("\n## 5. PROPOSED SOLUTION")
                charter_sections.append(st.session_state.form_data['preferred_solution'])
                
                if st.session_state.form_data.get('potential_solutions'):
                    charter_sections.append("\n### Alternatives Considered")
                    charter_sections.append(st.session_state.form_data['potential_solutions'])
                
                charter_sections.append("\n## 6. MEASURABLE BENEFITS")
                charter_sections.append(st.session_state.form_data['measurable_benefits'])
                
                charter_sections.append("\n## 7. HIGH-LEVEL REQUIREMENTS")
                charter_sections.append(st.session_state.form_data['high_level_requirements'])
                
                charter_sections.append("\n## 8. RESOURCES & TIMELINE")
                charter_sections.append(f"**Duration:** {st.session_state.form_data['duration_estimate']}")
                if st.session_state.form_data.get('budget_estimate'):
                    charter_sections.append(f"**Budget:** {st.session_state.form_data['budget_estimate']}")
                
                if st.session_state.form_data.get('initial_risks'):
                    charter_sections.append("\n## 9. RISKS & ASSUMPTIONS")
                    charter_sections.append(st.session_state.form_data['initial_risks'])
                
                charter_sections.append("\n---")
                charter_sections.append("\n## APPROVAL")
                charter_sections.append("**Project Owner:** _________________ Date: _______")
                charter_sections.append("\n**Project Manager:** _________________ Date: _______")
                
                st.session_state.charter_text = "\n\n".join(charter_sections)
                st.success("✅ Charter generated!")
                st.rerun()
        
        if st.session_state.charter_text:
            st.markdown("### 📄 Generated Charter")
            st.markdown(st.session_state.charter_text)
            
            st.download_button(
                label="⬇️ Download Charter (Markdown)",
                data=st.session_state.charter_text,
                file_name=f"{st.session_state.form_data['project_name'].replace(' ', '_')}_CHARTER.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            st.info("💡 Continue to Tab 5 for AI Quality Review")

# ============================================================================
# TAB 5: QUALITY REVIEW
# ============================================================================
with tab5:
    st.header("🎯 AI Quality Review")
    st.markdown("*Evaluate charter against PM best practices*")
    st.markdown("---")
    
    if not st.session_state.charter_text:
        st.warning("⚠️ Please generate a charter in Tab 4 first.")
    else:
        if st.button("🔍 Run Quality Critique", type="primary", use_container_width=True):
            with st.spinner("Running AI critique..."):
                try:
                    critique_result = critic_agent.critique_charter(st.session_state.charter_text)
                    st.session_state.critique = critique_result
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Critique failed: {e}")
        
        if st.session_state.critique:
            result = st.session_state.critique
            
            # Transform critic_agent output to display format
            weighted_score = result.get('weighted_score', 0.0)
            overall_score = int(weighted_score * 100)  # Convert 0.0-1.0 to 0-100%
            passed = result.get('approved', False)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{overall_score}%")
            with col2:
                st.metric("Status", "✅ PASS" if passed else "⚠️ NEEDS WORK")
            with col3:
                st.metric("Threshold", "75%")
            
            st.markdown("---")
            st.markdown("### 📊 Detailed Scores")
            
            # Transform scores array to display format
            scores = result.get('scores', [])
            for item in scores:
                criterion = item.get('criterion', 'Unknown')
                score = item.get('score', 0)
                strengths = item.get('strengths', '')
                weaknesses = item.get('weaknesses', '')
                improvements = item.get('improvements', '')
                
                with st.expander(f"**{criterion}** - {score}/100", 
                               expanded=(score < 70)):
                    st.markdown(f"**Score:** {score}/100")
                    if strengths:
                        st.markdown(f"**✅ Strengths:** {strengths}")
                    if weaknesses:
                        st.markdown(f"**⚠️ Weaknesses:** {weaknesses}")
                    if improvements:
                        st.markdown(f"**💡 Improvements:** {improvements}")
            
            st.markdown("---")
            st.markdown("### 💡 Overall Assessment")
            summary = result.get('overall_assessment', 'No summary available')
            st.info(summary)
            
            # Show critical gaps if any
            critical_gaps = result.get('critical_gaps', [])
            if critical_gaps:
                st.markdown("### ⚠️ Critical Gaps")
                for gap in critical_gaps:
                    st.markdown(f"- {gap}")
            
            # Show next steps if any
            next_steps = result.get('recommended_next_steps', [])
            if next_steps:
                st.markdown("### 📋 Recommended Next Steps")
                for i, step in enumerate(next_steps, 1):
                    st.markdown(f"{i}. {step}")
            
            if not passed:
                st.warning("⚠️ Charter scored below 75%. Consider revising based on feedback above.")
# TAB 6: CREATE PROJECT (PLACEHOLDER)
# ============================================================================
with tab6:
    st.header("🚀 Create Project")
    st.markdown("*Scaffold project structure and integrate with OpenProject*")
    st.markdown("---")
    
    st.info("🚧 **Coming Soon**: This tab will scaffold project folder structure and integrate with OpenProject API.")
    
    if st.session_state.charter_text:
        st.markdown("### Preview: Project Structure")
        st.code(f"""
{st.session_state.form_data.get('project_name', 'project_name')}/
├── PROJECT_CHARTER.md
├── README.md
├── CHANGELOG.md
├── LICENSE.md
├── .gitignore
├── docs/
│   └── PROJECT_PLAN.md
├── src/
└── tests/
        """, language="text")
        
        st.markdown("### OpenProject Integration")
        st.markdown("✅ You've already implemented OpenProject API integration")
        st.markdown("This tab will use your existing integration to create tasks automatically.")
