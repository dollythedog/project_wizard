"""
Project Wizard v2.5 - Integrated Pattern-Based Workflow
Unified charter generation with LEAN activities hub
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.pattern_pipeline import PatternPipeline
from app.services.ai_agents import CharterAgent, CriticAgent

# Recent projects file
RECENT_PROJECTS_FILE = Path.home() / ".project_wizard_recent.json"

def load_recent_projects():
    """Load recently accessed projects"""
    if RECENT_PROJECTS_FILE.exists():
        try:
            return json.loads(RECENT_PROJECTS_FILE.read_text())
        except:
            return []
    return []

def save_recent_project(project_path):
    """Add project to recent list"""
    recent = load_recent_projects()
    if str(project_path) in recent:
        recent.remove(str(project_path))
    recent.append(str(project_path))
    recent = recent[-10:]  # Keep last 10
    RECENT_PROJECTS_FILE.write_text(json.dumps(recent, indent=2))

def load_project_charter(project_path):
    """Load existing charter from project directory"""
    charter_file = project_path / "PROJECT_CHARTER.md"
    if charter_file.exists():
        return charter_file.read_text()
    return None

def parse_charter_to_form_data(charter_text):
    """Extract form data from existing charter"""
    data = {}
    lines = charter_text.split('\n')
    
    # Simple parsing - look for headers and content
    current_section = None
    content_buffer = []
    
    for line in lines:
        if line.startswith('# Project Charter:'):
            data['project_title'] = line.replace('# Project Charter:', '').strip()
        elif line.startswith('**Project Owner:**'):
            data['project_owner'] = line.replace('**Project Owner:**', '').strip()
        elif line.startswith('**Project Type:**'):
            data['project_type'] = line.replace('**Project Type:**', '').strip()
        elif line.startswith('## '):
            # Save previous section
            if current_section and content_buffer:
                data[current_section] = '\n'.join(content_buffer).strip()
            # Start new section
            section_name = line.replace('##', '').strip().lower().replace(' ', '_')
            current_section = section_name
            content_buffer = []
        elif current_section and line.strip():
            content_buffer.append(line)
    
    # Save last section
    if current_section and content_buffer:
        data[current_section] = '\n'.join(content_buffer).strip()
    
    return data

# Page config
st.set_page_config(
    page_title="Project Wizard v2.5",
    page_icon="🧙‍♂️",
    layout="wide"
)

# Initialize services
@st.cache_resource
def get_services():
    registry = PatternRegistry()
    charter_agent = CharterAgent()
    critic_agent = CriticAgent()
    return registry, charter_agent, critic_agent

registry, charter_agent, critic_agent = get_services()

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'enhanced_data' not in st.session_state:
    st.session_state.enhanced_data = {}
if 'charter_text' not in st.session_state:
    st.session_state.charter_text = None
if 'critique' not in st.session_state:
    st.session_state.critique = None
if 'project_path' not in st.session_state:
    st.session_state.project_path = Path.cwd()
if 'pattern_outputs' not in st.session_state:
    st.session_state.pattern_outputs = {}

# ============================================================================
# SIDEBAR: Project Management
# ============================================================================
with st.sidebar:
    st.header("📁 Project Management")
    
    # Show current project
    st.subheader("Current Project")
    st.caption(f"**{st.session_state.project_path.name}**")
    st.caption(f"`{st.session_state.project_path}`")
    
    st.markdown("---")
    
    # Recent projects
    recent = load_recent_projects()
    if recent:
        st.subheader("Recent Projects")
        
        for proj_path in reversed(recent[-5:]):  # Show last 5
            proj_name = Path(proj_path).name
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.caption(proj_name)
            
            with col2:
                if st.button("📂", key=f"load_{proj_path}", help="Load this project"):
                    project_path = Path(proj_path)
                    if project_path.exists():
                        st.session_state.project_path = project_path
                        
                        # Try to load existing charter
                        existing_charter = load_project_charter(project_path)
                        if existing_charter:
                            st.session_state.charter_text = existing_charter
                            # Try to parse into form data
                            parsed_data = parse_charter_to_form_data(existing_charter)
                            st.session_state.form_data.update(parsed_data)
                            st.success(f"✓ Loaded {proj_name}")
                        else:
                            st.info(f"Loaded {proj_name} (no existing charter)")
                        
                        st.rerun()
                    else:
                        st.error("Project not found")
        
        st.markdown("---")
    
    # New/Browse project
    st.subheader("Load Different Project")
    
    new_project_path = st.text_input(
        "Project Path",
        placeholder="/path/to/project",
        help="Path to project directory"
    )
    
    if st.button("📂 Open Project", use_container_width=True):
        if new_project_path:
            project_path = Path(new_project_path)
            if project_path.exists() and project_path.is_dir():
                st.session_state.project_path = project_path
                save_recent_project(project_path)
                
                # Try to load existing charter
                existing_charter = load_project_charter(project_path)
                if existing_charter:
                    st.session_state.charter_text = existing_charter
                    parsed_data = parse_charter_to_form_data(existing_charter)
                    st.session_state.form_data.update(parsed_data)
                    st.success(f"✓ Loaded project with existing charter!")
                else:
                    st.info("Loaded project (starting new charter)")
                
                st.rerun()
            else:
                st.error("Invalid project path")
    
    st.markdown("---")
    
    # New project button
    if st.button("➕ New Project", use_container_width=True):
        st.session_state.form_data = {}
        st.session_state.charter_text = None
        st.session_state.critique = None
        st.session_state.pattern_outputs = {}
        st.success("✓ Started new project")
        st.rerun()
    
    st.markdown("---")
    st.caption("Project Wizard v2.5")

# Header
st.title("🧙‍♂️ Project Wizard v2.5")
st.caption(f"Working on: **{st.session_state.project_path.name}**")

# Show if charter loaded
if st.session_state.charter_text and st.session_state.form_data.get('project_title'):
    st.success(f"✓ Loaded existing project: **{st.session_state.form_data['project_title']}**")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Initiation",
    "💼 Business Case", 
    "📋 Charter",
    "🏠 Project Home"
])

# ============================================================================
# TAB 1: Project Initiation
# ============================================================================
with tab1:
    st.header("Project Initiation Request")
    st.markdown("Define the core problem and desired outcomes")
    
    with st.form("initiation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_title = st.text_input(
                "Project Name *",
                value=st.session_state.form_data.get('project_title', ''),
                help="Brief descriptive name"
            )
            
            project_owner = st.text_input(
                "Project Owner *",
                value=st.session_state.form_data.get('project_owner', ''),
                help="Name and title"
            )
        
        with col2:
            project_type = st.selectbox(
                "Project Type",
                ["Software Development", "Process Improvement", "Clinical Initiative", 
                 "Research", "Infrastructure", "Other"],
                index=["Software Development", "Process Improvement", "Clinical Initiative", 
                       "Research", "Infrastructure", "Other"].index(
                    st.session_state.form_data.get('project_type', 'Software Development')
                ) if st.session_state.form_data.get('project_type') else 0
            )
        
        business_need = st.text_area(
            "Business Need *",
            value=st.session_state.form_data.get('business_need', ''),
            height=150,
            help="What problem are you solving? Be specific.",
            placeholder="Example: Current claims processing takes 72 hours, exceeding payer benchmarks..."
        )
        
        desired_outcomes = st.text_area(
            "Desired Outcomes *",
            value=st.session_state.form_data.get('desired_outcomes', ''),
            height=120,
            help="What does success look like?",
            placeholder="Example: Reduce processing time to 24 hours, improve staff efficiency..."
        )
        
        success_criteria = st.text_area(
            "Success Criteria",
            value=st.session_state.form_data.get('success_criteria', ''),
            height=120,
            help="Measurable indicators",
            placeholder="Example: 95% of claims processed within 24 hours..."
        )
        
        initial_risks = st.text_area(
            "Initial Risks & Assumptions",
            value=st.session_state.form_data.get('initial_risks', ''),
            height=100,
            help="Known risks or key assumptions"
        )
        
        submitted = st.form_submit_button("Save Initiation", use_container_width=True)
        
        if submitted:
            st.session_state.form_data.update({
                'project_title': project_title,
                'project_owner': project_owner,
                'project_type': project_type,
                'business_need': business_need,
                'desired_outcomes': desired_outcomes,
                'success_criteria': success_criteria,
                'initial_risks': initial_risks
            })
            st.success("✓ Initiation data saved! Continue to Business Case tab.")

# ============================================================================
# TAB 2: Business Case
# ============================================================================
with tab2:
    st.header("Business Case Justification")
    
    if not st.session_state.form_data.get('project_title'):
        st.warning("⚠️ Please complete Project Initiation first (Tab 1)")
        st.stop()
    
    with st.form("business_case_form"):
        strategic_alignment = st.text_area(
            "Strategic Alignment *",
            value=st.session_state.form_data.get('strategic_alignment', ''),
            height=120,
            help="How does this support organizational goals?"
        )
        
        potential_solutions = st.text_area(
            "Potential Solutions Considered",
            value=st.session_state.form_data.get('potential_solutions', ''),
            height=100,
            help="Alternative approaches evaluated"
        )
        
        preferred_solution = st.text_area(
            "Preferred Solution & Rationale *",
            value=st.session_state.form_data.get('preferred_solution', ''),
            height=120,
            help="Recommended approach and why"
        )
        
        measurable_benefits = st.text_area(
            "Measurable Benefits *",
            value=st.session_state.form_data.get('measurable_benefits', ''),
            height=100,
            help="Expected value delivery"
        )
        
        requirements = st.text_area(
            "High-Level Requirements",
            value=st.session_state.form_data.get('requirements', ''),
            height=120,
            help="Technical, functional, compliance needs"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            budget_estimate = st.text_input(
                "Budget Estimate",
                value=st.session_state.form_data.get('budget_estimate', ''),
                help="Rough cost estimate"
            )
        with col2:
            duration_estimate = st.text_input(
                "Duration Estimate",
                value=st.session_state.form_data.get('duration_estimate', ''),
                help="Expected timeline"
            )
        
        submitted = st.form_submit_button("Save Business Case", use_container_width=True)
        
        if submitted:
            st.session_state.form_data.update({
                'strategic_alignment': strategic_alignment,
                'potential_solutions': potential_solutions,
                'preferred_solution': preferred_solution,
                'measurable_benefits': measurable_benefits,
                'requirements': requirements,
                'budget_estimate': budget_estimate,
                'duration_estimate': duration_estimate
            })
            st.success("✓ Business Case saved! Generate charter in next tab.")

# ============================================================================
# TAB 3: Charter (Living Document)
# ============================================================================
with tab3:
    st.header("Project Charter - Living Document")
    
    if not st.session_state.form_data.get('preferred_solution'):
        st.warning("⚠️ Please complete Business Case first (Tab 2)")
        st.stop()
    
    # Generate charter button
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        if st.button("📄 Generate Charter", type="primary", use_container_width=True):
            with st.spinner("Generating charter..."):
                charter_content = f"""# Project Charter: {st.session_state.form_data['project_title']}

**Project Owner:** {st.session_state.form_data['project_owner']}  
**Project Type:** {st.session_state.form_data['project_type']}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** Draft

## Business Need

{st.session_state.form_data['business_need']}

## Desired Outcomes

{st.session_state.form_data['desired_outcomes']}

## Success Criteria

{st.session_state.form_data['success_criteria']}

## Strategic Alignment

{st.session_state.form_data['strategic_alignment']}

## Preferred Solution

{st.session_state.form_data['preferred_solution']}

## Measurable Benefits

{st.session_state.form_data['measurable_benefits']}

## Requirements

{st.session_state.form_data['requirements']}

## Budget & Timeline

**Budget:** {st.session_state.form_data.get('budget_estimate', 'TBD')}  
**Duration:** {st.session_state.form_data.get('duration_estimate', 'TBD')}

## Risks & Assumptions

{st.session_state.form_data['initial_risks']}

## Approvals

**Sponsor:** ___________________________ Date: ___________  
**Project Owner:** ______________________ Date: ___________  
**Stakeholder:** ________________________ Date: ___________
"""
                st.session_state.charter_text = charter_content
                st.success("✓ Charter generated!")
    
    with col2:
        if st.button("🔍 Critique", use_container_width=True):
            if st.session_state.charter_text:
                with st.spinner("Running quality critique..."):
                    st.session_state.critique = critic_agent.critique_charter(
                        st.session_state.charter_text
                    )
                st.success("✓ Critique complete!")
    
    with col3:
        if st.session_state.charter_text:
            if st.button("💾 Save to Project", use_container_width=True):
                charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
                charter_file.write_text(st.session_state.charter_text)
                save_recent_project(st.session_state.project_path)
                st.success(f"✓ Saved to {charter_file.name}")
    
    with col4:
        if st.session_state.charter_text:
            filename = f"PROJECT_CHARTER_{datetime.now().strftime('%Y%m%d')}.md"
            st.download_button(
                "⬇️ Download",
                data=st.session_state.charter_text,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
    
    # Quality KPIs at top
    if st.session_state.critique:
        critique = st.session_state.critique
        
        col1, col2, col3 = st.columns(3)
        with col1:
            score = critique.get('weighted_score', 0) * 100
            st.metric("Quality Score", f"{score:.0f}%")
        with col2:
            approved = "✅ Approved" if critique.get('approved') else "⚠️ Review Needed"
            st.metric("Status", approved)
        with col3:
            criteria_count = len(critique.get('scores', []))
            st.metric("Criteria Evaluated", criteria_count)
    
    st.markdown("---")
    
    # Charter viewer with enhancement options
    if st.session_state.charter_text:
        # Enhancement options in expander
        with st.expander("✨ AI Enhancement Options"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Improve Wording", use_container_width=True):
                    st.info("Enhancement feature coming soon")
            
            with col2:
                if st.button("Professional Tone", use_container_width=True):
                    st.info("Enhancement feature coming soon")
            
            with col3:
                if st.button("Simplify Language", use_container_width=True):
                    st.info("Enhancement feature coming soon")
        
        # Live markdown viewer
        st.markdown("### Charter Preview")
        st.markdown(st.session_state.charter_text)
        
        # Critique details in expander
        if st.session_state.critique:
            with st.expander("📊 Detailed Critique"):
                critique = st.session_state.critique
                
                for score in critique.get('scores', []):
                    st.markdown(f"**{score['criterion']}**: {score['score']}/100")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption("Strengths:")
                        for s in score.get('strengths', []):
                            st.markdown(f"- {s}")
                    with col2:
                        st.caption("Improvements:")
                        for i in score.get('improvements', []):
                            st.markdown(f"- {i}")
                    st.markdown("---")
    else:
        st.info("👆 Click 'Generate Charter' to create the document")

# ============================================================================
# TAB 4: Project Home
# ============================================================================
with tab4:
    st.header("🏠 Project Home Dashboard")
    
    # Project metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Project Name", st.session_state.form_data.get('project_title', 'Not Set'))
    with col2:
        st.metric("Owner", st.session_state.form_data.get('project_owner', 'Not Set'))
    with col3:
        st.metric("Type", st.session_state.form_data.get('project_type', 'Not Set'))
    
    st.markdown("---")
    
    # Scaffold structure
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Project Structure")
    with col2:
        if st.button("🏗️ Scaffold Project", use_container_width=True):
            st.info("Scaffold feature coming in next update")
    
    st.markdown("---")
    
    # Activity selector
    st.subheader("LEAN/PM Activities")
    
    # Get available patterns
    patterns = registry.list_patterns()
    
    # Activity radio with status
    activities = [
        ("📊 Project Plan", "project_plan"),
        ("❓ 5W1H Analysis", "5w1h_analysis"),
        ("🔄 SIPOC", "sipoc"),
        ("🐟 Fishbone", "fishbone"),
        ("🎤 Voice of Customer", "voc")
    ]
    
    selected_activity = st.radio(
        "Select Activity",
        [a[0] for a in activities],
        key="activity_selector"
    )
    
    # Get selected pattern key
    selected_idx = [a[0] for a in activities].index(selected_activity)
    pattern_key = activities[selected_idx][1]
    
    # Check if output exists
    has_output = pattern_key in st.session_state.pattern_outputs
    
    st.markdown("---")
    
    # Show status and action
    if has_output:
        st.success(f"✓ {selected_activity} completed")
        
        # Show output
        output = st.session_state.pattern_outputs[pattern_key]
        st.markdown("### Document")
        st.markdown(output['document'])
        
        # Download button
        filename = f"{pattern_key}_{datetime.now().strftime('%Y%m%d')}.md"
        st.download_button(
            "⬇️ Download",
            data=output['document'],
            file_name=filename,
            mime="text/markdown"
        )
        
        # Regenerate option
        if st.button("🔄 Regenerate", key=f"regen_{pattern_key}"):
            del st.session_state.pattern_outputs[pattern_key]
            st.rerun()
    
    else:
        # Check if pattern exists
        if pattern_key in patterns:
            st.info(f"📋 {selected_activity} not yet created")
            
            # Show pattern info
            pattern = registry.get_pattern(pattern_key)
            if pattern and pattern.get('variables'):
                with st.expander("📝 Template Preview - What You'll Need"):
                    st.markdown("**Required Information:**")
                    for var_name, var_config in pattern['variables'].items():
                        required = "✱" if var_config.get('required') else ""
                        st.markdown(f"- **{var_config['label']}** {required}")
                        if var_config.get('help'):
                            st.caption(f"  _{var_config['help']}_")
            
            # Create button
            if st.button(f"✨ Create {selected_activity}", type="primary", use_container_width=True):
                st.session_state.selected_pattern_to_create = pattern_key
                st.session_state.show_pattern_form = True
                st.rerun()
        else:
            st.warning(f"⚠️ {selected_activity} pattern not yet available")
            st.caption("Coming in future update")
    
    # Show pattern creation form if triggered
    if st.session_state.get('show_pattern_form') and st.session_state.get('selected_pattern_to_create'):
        pattern_key = st.session_state.selected_pattern_to_create
        pattern = registry.get_pattern(pattern_key)
        
        st.markdown("---")
        st.subheader(f"Create: {selected_activity}")
        
        # Dynamic form from pattern
        user_inputs = {}
        for var_name, var_config in pattern['variables'].items():
            label = var_config['label']
            if var_config.get('required'):
                label += " *"
            
            if var_config['type'] == 'textarea':
                user_inputs[var_name] = st.text_area(
                    label,
                    height=var_config.get('height', 120),
                    placeholder=var_config.get('placeholder', ''),
                    help=var_config.get('help', ''),
                    key=f"create_{var_name}"
                )
            else:
                user_inputs[var_name] = st.text_input(
                    label,
                    placeholder=var_config.get('placeholder', ''),
                    help=var_config.get('help', ''),
                    key=f"create_{var_name}"
                )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("✨ Generate", type="primary", use_container_width=True):
                with st.spinner("Generating document..."):
                    context = ProjectContext(st.session_state.project_path)
                    pipeline = PatternPipeline(registry, context)
                    
                    result = pipeline.execute(
                        pattern_name=pattern_key,
                        user_inputs=user_inputs,
                        enable_editing=True,
                        enable_critique=True,
                        project_path=st.session_state.project_path
                    )
                    
                    st.session_state.pattern_outputs[pattern_key] = result
                    st.session_state.show_pattern_form = False
                    st.success("✓ Document created!")
                    st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_pattern_form = False
                st.rerun()

# Footer
st.markdown("---")
st.caption("Project Wizard v2.5 - Integrated Workflow | Powered by OpenAI")
