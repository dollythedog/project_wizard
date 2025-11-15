"""
Charter tab for creating and editing project charters.
"""

from datetime import datetime, timedelta

import streamlit as st

from app.components.document_editor import DocumentEditor
from app.services.ai_agents import CharterAgent, CriticAgent
from app.services.pattern_pipeline import PatternPipeline
from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.project_registry import ProjectRegistry


def render_charter_tab(
    charter_agent: CharterAgent,
    critic_agent: CriticAgent,
    registry: PatternRegistry,
    project_registry: ProjectRegistry,
):
    """
    Render the charter tab with wizard or edit mode.

    Args:
        charter_agent: CharterAgent instance
        critic_agent: CriticAgent instance
        registry: PatternRegistry instance
        project_registry: ProjectRegistry instance
    """
    st.header("📋 Project Charter")

    charter_file = st.session_state.project_path / "PROJECT_CHARTER.md"
    charter_exists = charter_file.exists()

    if charter_exists:
        _render_edit_mode(charter_file, charter_agent, critic_agent, project_registry)
    else:
        _render_wizard_mode(charter_file, charter_agent, critic_agent, registry, project_registry)


def _render_edit_mode(charter_file, charter_agent, critic_agent, project_registry):
    """Render edit mode for existing charter."""
    # Always read file fresh - don't rely on session state
    try:
        charter_text = charter_file.read_text()
    except Exception as e:
        st.error(f"Error reading charter file: {e}")
        return

    # Mark charter as complete
    project_registry.mark_charter_complete(st.session_state.project_path)

    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.info("✅ Charter exists - Edit Mode")
    with col2:
        if st.button("🔄 Regenerate", help="Start over with the charter wizard"):
            # Delete existing charter
            charter_file.unlink()
            # Clear all charter-related session state
            st.session_state.form_data = {}
            st.session_state.charter_text = None
            if "edit_mode_PROJECT_CHARTER.md" in st.session_state:
                del st.session_state["edit_mode_PROJECT_CHARTER.md"]
            if "working_content_PROJECT_CHARTER.md" in st.session_state:
                del st.session_state["working_content_PROJECT_CHARTER.md"]
            st.success("Charter deleted. Reloading wizard...")
            st.rerun()

    editor = DocumentEditor(
        key_prefix="charter_tab_",
        document_name="PROJECT_CHARTER.md",
        document_content=charter_text,
        charter_agent=charter_agent,
        critic_agent=critic_agent,
    )

    updated_content, action = editor.render()

    # Handle save action
    if action and action.get("type") == "save":
        charter_file.write_text(updated_content)

        # Update registry
        current_project = project_registry.get_project(st.session_state.project_path)
        if current_project:
            project_registry.update_project(
                st.session_state.project_path, last_modified=datetime.now().isoformat()
            )
            project_registry.mark_charter_complete(st.session_state.project_path)

        st.success(f"✓ Saved to {charter_file.name}")
        st.rerun()


def _render_wizard_mode(charter_file, charter_agent, critic_agent, registry, project_registry):
    """Render wizard mode for creating new charter."""
    st.info("⚠️ No charter found - Wizard Mode")

    # Create sub-tabs for wizard steps
    wizard_tab1, wizard_tab2, wizard_tab3 = st.tabs(
        ["📝 Step 1: Initiation", "💼 Step 2: Business Case", "🎯 Step 3: Generate"]
    )

    with wizard_tab1:
        _render_initiation_step()

    with wizard_tab2:
        _render_business_case_step()

    with wizard_tab3:
        _render_generate_step(charter_file, registry, project_registry)


def _render_initiation_step():
    """Render Step 1: Project Initiation."""
    st.subheader("Project Initiation")

    with st.form("initiation_form"):
        project_title = st.text_input(
            "Project Title *",
            value=st.session_state.form_data.get("project_title", ""),
            help="Official project name",
        )

        project_type = st.selectbox(
            "Project Type *",
            [
                "Software Development",
                "Infrastructure",
                "Data/Analytics",
                "Process Improvement",
                "Research",
                "Other",
            ],
            index=0,
        )

        executive_sponsor = st.text_input(
            "Executive Sponsor",
            value=st.session_state.form_data.get("executive_sponsor", ""),
            help="Senior leader accountable for success",
        )

        project_manager = st.text_input(
            "Project Manager",
            value=st.session_state.form_data.get("project_manager", ""),
            help="Day-to-day leader",
        )

        problem_statement = st.text_area(
            "Problem Statement *",
            value=st.session_state.form_data.get("problem_statement", ""),
            height=120,
            help="What problem are we solving?",
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Target Start Date", value=datetime.now())
        with col2:
            end_date = st.date_input("Target End Date", value=datetime.now() + timedelta(days=90))

        submitted = st.form_submit_button("Save & Continue →", use_container_width=True)

        if submitted:
            st.session_state.form_data.update(
                {
                    "project_title": project_title,
                    "project_type": project_type,
                    "executive_sponsor": executive_sponsor,
                    "project_manager": project_manager,
                    "problem_statement": problem_statement,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                }
            )
            st.success("✓ Initiation saved! Go to Step 2: Business Case")


def _render_business_case_step():
    """Render Step 2: Business Case Justification."""
    st.subheader("Business Case Justification")

    if not st.session_state.form_data.get("project_title"):
        st.warning("⚠️ Complete Step 1: Initiation first")
        return

    with st.form("business_case_form"):
        strategic_alignment = st.text_area(
            "Strategic Alignment *",
            value=st.session_state.form_data.get("strategic_alignment", ""),
            height=120,
            help="How does this support organizational goals?",
        )

        potential_solutions = st.text_area(
            "Potential Solutions Considered",
            value=st.session_state.form_data.get("potential_solutions", ""),
            height=100,
            help="Alternative approaches evaluated",
        )

        preferred_solution = st.text_area(
            "Preferred Solution & Rationale *",
            value=st.session_state.form_data.get("preferred_solution", ""),
            height=120,
            help="Recommended approach and why",
        )

        measurable_benefits = st.text_area(
            "Measurable Benefits *",
            value=st.session_state.form_data.get("measurable_benefits", ""),
            height=100,
            help="Expected value delivery",
        )

        requirements = st.text_area(
            "High-Level Requirements",
            value=st.session_state.form_data.get("requirements", ""),
            height=120,
            help="Technical, functional, compliance needs",
        )

        col1, col2 = st.columns(2)
        with col1:
            budget_estimate = st.text_input(
                "Budget Estimate",
                value=st.session_state.form_data.get("budget_estimate", ""),
                help="e.g., $50k-100k",
            )
        with col2:
            resource_needs = st.text_input(
                "Resource Needs",
                value=st.session_state.form_data.get("resource_needs", ""),
                help="e.g., 2 devs, 1 PM",
            )

        submitted = st.form_submit_button("Save & Continue →", use_container_width=True)

        if submitted:
            st.session_state.form_data.update(
                {
                    "strategic_alignment": strategic_alignment,
                    "potential_solutions": potential_solutions,
                    "preferred_solution": preferred_solution,
                    "measurable_benefits": measurable_benefits,
                    "requirements": requirements,
                    "budget_estimate": budget_estimate,
                    "resource_needs": resource_needs,
                }
            )
            st.success("✓ Business Case saved! Go to Step 3: Generate")


def _render_generate_step(charter_file, registry, project_registry):
    """Render Step 3: Generate Charter."""
    st.subheader("Generate Charter")

    if not st.session_state.form_data.get("strategic_alignment"):
        st.warning("⚠️ Complete Step 2: Business Case first")
        return

    st.info("Ready to generate your charter from the information provided.")

    # Pattern selection
    available_patterns = registry.list_patterns()
    selected_patterns = st.multiselect(
        "Select Optional Patterns to Include",
        available_patterns,
        help="Add specialized sections to your charter",
    )

    if st.button("🎯 Generate Charter", type="primary", use_container_width=True):
        with st.spinner("Generating charter..."):
            try:
                # Use pattern pipeline for charter generation
                project_context = ProjectContext(st.session_state.project_path)
                pipeline = PatternPipeline(pattern_registry=registry, project_context=project_context)
                result = pipeline.execute(
                    pattern_name="project_charter",
                    user_inputs=st.session_state.form_data,
                    enable_editing=False,
                    enable_critique=False,
                    project_path=st.session_state.project_path,
                )

                charter_text = result["document"]
                
                # Verify charter has content before saving
                if not charter_text or len(charter_text.strip()) < 100:
                    st.error(f"Charter generation failed: Output too short ({len(charter_text)} bytes)")
                    return

                # Save charter to file
                charter_file.write_text(charter_text)
                
                # Clear session state to force fresh read on reload
                st.session_state.charter_text = None
                if "edit_mode_PROJECT_CHARTER.md" in st.session_state:
                    del st.session_state["edit_mode_PROJECT_CHARTER.md"]
                if "working_content_PROJECT_CHARTER.md" in st.session_state:
                    del st.session_state["working_content_PROJECT_CHARTER.md"]

                # Mark complete
                project_registry.mark_charter_complete(st.session_state.project_path)

                st.success("✓ Charter generated and saved!")
                st.rerun()
            except Exception as e:
                st.error(f"Charter generation failed: {e}")
                import traceback
                st.error(traceback.format_exc())
