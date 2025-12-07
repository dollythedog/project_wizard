"""
Document generation routes.

Handles the AI-powered document generation workflow:
1. Template selection
2. Step-back questions
3. Draft generation
4. Display and download
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pathlib import Path
from typing import Optional

from app.services.database import get_db_session
from app.services.project_registry import ProjectRegistry
from app.services.blueprint_registry import get_registry
from app.services.ai_agents import (
    LLMClient,
    ContextBuilder,
    StepBackAgent,
    DraftAgent,
    DraftResult,
    VerifierAgent,
    RefinementAgent,
    SectionAgentController
)
from app.services.ai_agents.self_refine_agent import SelfRefineAgent
from app.models.database import DocumentRun, Project
import json
from datetime import datetime

router = APIRouter()

# Templates
WEB_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = WEB_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def select_template(
    request: Request,
    project_id: int
):
    """Select document template to generate."""
    # Get project
    session = next(get_db_session())
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get available templates
    blueprint_registry = get_registry()
    templates_list = blueprint_registry.list_blueprints()
    
    # Get blueprint details for each template
    template_details = []
    for template_name in templates_list:
        blueprint = blueprint_registry.load_blueprint(template_name)
        template_details.append({
            "name": template_name,
            "display_name": blueprint.name.replace("_", " ").title(),
            "description": blueprint.description,
            "version": blueprint.version
        })
    
    return templates.TemplateResponse(
        "generate/select_template.html",
        {
            "request": request,
            "project": project,
            "templates": template_details
        }
    )


@router.get("/{project_id}/{template_name}/select-notes", response_class=HTMLResponse)
async def select_notes(
    request: Request,
    project_id: int,
    template_name: str
):
    """Show note selection screen (Step 1)."""
    # Get project
    session = next(get_db_session())
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all notes for this project
    notes = registry.list_notes(project_id)
    
    # Load blueprint for display name
    blueprint_registry = get_registry()
    blueprint = blueprint_registry.load_blueprint(template_name)
    
    return templates.TemplateResponse(
        "generate/select_notes.html",
        {
            "request": request,
            "project": project,
            "template_name": template_name,
            "template_display_name": blueprint.name.replace("_", " ").title(),
            "notes": notes
        }
    )


@router.post("/{project_id}/{template_name}/inputs", response_class=HTMLResponse)
@router.get("/{project_id}/{template_name}/inputs", response_class=HTMLResponse)
async def show_input_form(
    request: Request,
    project_id: int,
    template_name: str
):
    """Show blueprint input form (Step 2)."""
    # Get project
    session = next(get_db_session())
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get selected notes from form (POST) or query params (GET)
    selected_note_ids = []
    if request.method == "POST":
        form_data = await request.form()
        selected_note_ids = [int(id) for id in form_data.getlist("selected_notes")]
    
    # Load blueprint
    blueprint_registry = get_registry()
    blueprint = blueprint_registry.load_blueprint(template_name)
    
    return templates.TemplateResponse(
        "generate/input_form.html",
        {
            "request": request,
            "project": project,
            "template_name": template_name,
            "blueprint": blueprint,
            "selected_note_ids": selected_note_ids,
            "notes_count": len(selected_note_ids)
        }
    )


@router.post("/{project_id}/{template_name}/submit-inputs", response_class=HTMLResponse)
async def submit_inputs_and_show_questions(
    request: Request,
    project_id: int,
    template_name: str
):
    """Process blueprint inputs and show step-back questions (Step 2)."""
    # Get form data
    form_data = await request.form()
    
    # Parse form data - handle multiselect fields (checkboxes) as lists
    # Separate selected_notes from user inputs
    selected_note_ids = [int(id) for id in form_data.getlist("selected_notes")]
    
    user_inputs = {}
    for key in form_data.keys():
        if key == "selected_notes":
            continue  # Skip, already handled
        values = form_data.getlist(key)
        if len(values) > 1:
            # Multiple values = multiselect/checkbox field
            user_inputs[key] = values
        else:
            # Single value = text/textarea/select/etc
            user_inputs[key] = values[0]
    
    # DEBUG: Print what we got
    print(f"\n=== FORM DATA DEBUG ===")
    for key, value in user_inputs.items():
        print(f"{key}: {type(value).__name__} = {value if not isinstance(value, str) or len(value) < 50 else value[:50]+'...'}")
    print(f"=== END DEBUG ===\n")
    
    # Get project and build context
    session = next(get_db_session())
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build context with selected notes only
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(project_id, note_ids=selected_note_ids if selected_note_ids else None)
    
    # Initialize LLM client (check if configured)
    try:
        llm_client = LLMClient()
        step_back_agent = StepBackAgent(llm_client)
        
        # Generate questions based on inputs + context
        questions = step_back_agent.generate_questions(
            template_name,
            user_inputs=user_inputs,
            project_context=context
        )
    except ValueError as e:
        # No AI provider configured
        return templates.TemplateResponse(
            "generate/no_api_key.html",
            {
                "request": request,
                "error": str(e),
                "project": project
            }
        )
    
    # Store inputs in session for next step (in production, use redis/database)
    # For now, pass through form
    inputs_encoded = "&".join([f"input_{k}={v}" for k, v in user_inputs.items()])
    
    # Generate a suggested outline based on inputs (optional, for preview)
    suggested_outline = None
    suggested_outline_html = None
    try:
        blueprint_registry = get_registry()
        blueprint = blueprint_registry.load_blueprint(template_name)
        # We don't have responses yet, so create a dummy response dict with user inputs as context
        suggested_outline = step_back_agent._generate_suggested_outline(
            template_name,
            blueprint,
            user_inputs,  # Use user inputs as initial context
            "Based on the provided inputs. You can refine this further with your responses below."
        )
        # Just pass the raw outline as-is, template will handle formatting
        suggested_outline_html = suggested_outline
    except Exception as e:
        print(f"Failed to generate suggested outline: {e}")
        suggested_outline = None
        suggested_outline_html = None
    
    return templates.TemplateResponse(
        "generate/questions.html",
        {
            "request": request,
            "project": project,
            "template_name": template_name,
            "questions": questions,
            "context_summary": f"{context.notes_count} notes, {context.files_count} files",
            "user_inputs": user_inputs,  # Pass to questions page
            "selected_note_ids": selected_note_ids,  # Pass note IDs forward
            "suggested_outline": suggested_outline,  # Raw (debug)
            "suggested_outline_html": suggested_outline_html  # Rendered HTML for display
        }
    )


@router.post("/review-outline", response_class=HTMLResponse)
async def review_outline(
    request: Request,
    project_id: int = Form(...),
    template_name: str = Form(...),
    session: Session = Depends(get_db_session)
):
    """Show refined outline based on clarifying question answers (Step 2.5)."""
    # Get form data
    form_data = await request.form()
    
    # Separate user inputs and question responses
    selected_note_ids = [int(id) for id in form_data.getlist("selected_notes")]
    user_inputs = {}
    responses = {}
    
    for key in form_data.keys():
        if key == "selected_notes":
            continue
        elif key.startswith("input_"):
            input_key = key.replace("input_", "")
            values = form_data.getlist(key)
            user_inputs[input_key] = values[0] if len(values) == 1 else values
        elif key.startswith("question_"):
            question_text = key.replace("question_", "").replace("_", " ")
            values = form_data.getlist(key)
            responses[question_text] = values[0] if len(values) == 1 else values
    
    # Get project
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build context
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(project_id, note_ids=selected_note_ids if selected_note_ids else None)
    
    # Generate refined outline using step-back responses
    refined_outline = None
    refined_outline_html = None
    try:
        llm_client = LLMClient()
        step_back_agent = StepBackAgent(llm_client)
        blueprint_registry = get_registry()
        blueprint = blueprint_registry.load_blueprint(template_name)
        
        # Generate outline using BOTH inputs and question responses
        refined_outline = step_back_agent._generate_suggested_outline(
            template_name,
            blueprint,
            responses,  # Use responses (not inputs) for refined outline
            "Based on your clarifying question answers. You can review this structure before we generate the full draft."
        )
        # Just pass the raw outline as-is, template will handle formatting
        refined_outline_html = refined_outline
    except Exception as e:
        print(f"Failed to generate refined outline: {e}")
        refined_outline = "Could not generate refined outline. Proceeding with draft generation."
        refined_outline_html = None
    
    return templates.TemplateResponse(
        "generate/review_outline.html",
        {
            "request": request,
            "project": project,
            "template_name": template_name,
            "refined_outline": refined_outline,
            "refined_outline_html": refined_outline_html,
            "user_inputs": user_inputs,
            "responses": responses,
            "selected_note_ids": selected_note_ids
        }
    )


@router.post("", response_class=HTMLResponse)
async def generate_draft(
    request: Request,
    project_id: int = Form(...),
    template_name: str = Form(...),
    session: Session = Depends(get_db_session)
):
    """Generate document draft from inputs + responses (Step 3)."""
    # Get form data
    form_data = await request.form()
    
    # Separate user inputs (from Step 1), question responses (from Step 2), and selected notes
    selected_note_ids = [int(id) for id in form_data.getlist("selected_notes")]
    user_inputs = {}
    responses = {}
    user_edited_outline = None
    
    for key in form_data.keys():
        if key == "selected_notes":
            continue  # Already handled
        elif key == "refined_outline":
            # Capture user's edited outline to use for draft generation
            user_edited_outline = form_data.get(key)
            continue
        elif key.startswith("input_"):
            # Original blueprint inputs
            input_key = key.replace("input_", "")
            values = form_data.getlist(key)
            if len(values) > 1:
                # Multiple values = multiselect field preserved from Step 1
                user_inputs[input_key] = values
            else:
                user_inputs[input_key] = values[0]
        elif key.startswith("question_"):
            # Step-back question responses
            question_text = key.replace("question_", "").replace("_", " ")
            values = form_data.getlist(key)
            responses[question_text] = values[0] if len(values) == 1 else values
    
    # Get project
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build context with selected notes only
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(project_id, note_ids=selected_note_ids if selected_note_ids else None)
    
    # Initialize AI agents
    try:
        llm_client = LLMClient()
        step_back_agent = StepBackAgent(llm_client)
        refine_agent = SelfRefineAgent(llm_client, max_iterations=3)
        
        # Process step-back responses
        step_back_result = step_back_agent.process_responses(
            template_name,
            responses,
            project_context=context
        )
        
        # Load blueprint for section-by-section generation
        blueprint_registry = get_registry()
        blueprint = blueprint_registry.load_blueprint(template_name)
        
        # Load prompts for section generation
        prompts = blueprint_registry.load_prompts(template_name)
        
        # Extract charter if it exists in user inputs (e.g., from project_charter or project_charter_lite)
        charter_dict = None
        if "project_goal" in user_inputs and "success_criteria" in user_inputs:
            # Build charter object from user inputs
            charter_dict = {
                "project_goal": user_inputs.get("project_goal", ""),
                "success_criteria": user_inputs.get("success_criteria", ""),
                "scope_out": user_inputs.get("scope_out") or user_inputs.get("initial_risks_and_assumptions", ""),
            }
        
        # Use SectionAgentController for section-by-section generation with constraints
        section_controller = SectionAgentController(llm_client, blueprint, pattern_name=template_name)
        sections = section_controller.generate_all_sections(
            user_inputs=user_inputs,
            prompts=prompts,
            project_context=context,
            max_regenerations=2,
            charter=charter_dict
        )
        
        # Assemble final document
        draft_content = section_controller.assemble_document(
            document_title=user_inputs.get("project_name") or "Generated Proposal",
            prepend_header=True
        )
        
        # Create DraftResult-compatible object for existing template code
        draft_result = DraftResult(
            content=draft_content,
            model_used=llm_client.model,
            tokens_used=sum(getattr(s, 'regeneration_count', 0) for s in sections.values()) * 2000,
            sections_generated=list(sections.keys())
        )
        
        # Refine the analytical summary (self-refine prompting)
        refinement_result = refine_agent.refine_summary(
            original_summary=step_back_result.summary,
            context=context.full_context_text if context else None
        )
        
        # Check if DocumentRun already exists for this template
        existing_run = session.query(DocumentRun).filter(
            DocumentRun.project_id == project_id,
            DocumentRun.template_name == template_name
        ).first()
        
        if existing_run:
            # Update existing
            existing_run.user_inputs = json.dumps(user_inputs)
            existing_run.step_back_summary = step_back_result.summary
            existing_run.executive_summary = refinement_result.refined_summary
            existing_run.initial_draft = draft_result.content
            existing_run.status = "completed"
            existing_run.completed_at = datetime.utcnow()
            document_run = existing_run
        else:
            # Create new
            document_run = DocumentRun(
                project_id=project_id,
                template_name=template_name,
                user_inputs=json.dumps(user_inputs),
                step_back_summary=step_back_result.summary,
                executive_summary=refinement_result.refined_summary,
                initial_draft=draft_result.content,
                status="completed",
                completed_at=datetime.utcnow()
            )
            session.add(document_run)
        
        session.commit()
        session.refresh(document_run)
        
        return templates.TemplateResponse(
            "generate/draft.html",
            {
                "request": request,
                "project": project,
                "template_name": template_name,
                "draft_content": draft_result.content,
                "model_used": draft_result.model_used,
                "tokens_used": draft_result.tokens_used,
                "step_back_summary": step_back_result.summary,
                "refined_summary": refinement_result.refined_summary,
                "refinement_iterations": refinement_result.iterations_performed,
                "document_run_id": document_run.id  # Pass ID for download
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "generate/error.html",
            {
                "request": request,
                "project": project,
                "error": str(e)
            }
        )


@router.get("/document/{document_run_id}")
async def view_document(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """View a previously generated document."""
    try:
        print(f"\n=== VIEW DOCUMENT DEBUG ===")
        print(f"Requested document_run_id: {document_run_id}")
        
        document_run = session.get(DocumentRun, document_run_id)
        print(f"DocumentRun found: {document_run is not None}")
        
        if not document_run:
            raise HTTPException(status_code=404, detail="Document not found")
        
        project = session.get(Project, document_run.project_id)
        print(f"Project found: {project is not None}")
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        print(f"Template dir: {TEMPLATES_DIR}")
        print(f"Template exists: {(TEMPLATES_DIR / 'generate' / 'draft.html').exists()}")
        print(f"Rendering template...")
        
        result = templates.TemplateResponse(
            "generate/draft.html",
            {
                "request": request,
                "project": project,
                "template_name": document_run.template_name,
                "draft_content": document_run.initial_draft,
                "model_used": "Previously Generated",
                "tokens_used": 0,
                "step_back_summary": document_run.step_back_summary,
                "refined_summary": document_run.executive_summary,
                "refinement_iterations": None,
                "document_run_id": document_run.id
            }
        )
        print(f"Template rendered successfully")
        print(f"=== END DEBUG ===\n")
        return result
        
    except Exception as e:
        print(f"\n!!! ERROR IN VIEW_DOCUMENT !!!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"!!! END ERROR !!!\n")
        raise


@router.get("/download/{document_run_id}")
async def download_document(
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Download a saved document as markdown file."""
    document_run = session.get(DocumentRun, document_run_id)
    
    if not document_run:
        raise HTTPException(status_code=404, detail="Document not found")
    
    project = session.get(Project, document_run.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create filename:
    safe_title = project.title.replace(" ", "_").replace("/", "-")
    date_str = document_run.created_at.strftime("%Y%m%d")
    filename = f"{safe_title}_{document_run.template_name}_{date_str}.md"
    
    return Response(
        content=document_run.initial_draft,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/document/{document_run_id}/update")
async def update_document(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Update document content with user edits."""
    try:
        # Get JSON body
        body = await request.json()
        new_content = body.get('content')
        
        if not new_content:
            return {"success": False, "error": "No content provided"}
        
        # Get document
        document_run = session.get(DocumentRun, document_run_id)
        
        if not document_run:
            return {"success": False, "error": "Document not found"}
        
        # Update content
        document_run.initial_draft = new_content
        session.commit()
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/document/{document_run_id}/refine-guidance", response_class=HTMLResponse)
async def refine_with_guidance(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Show refinement guidance interface where user can edit improvement recommendations."""
    document_run = session.get(DocumentRun, document_run_id)
    
    if not document_run:
        raise HTTPException(status_code=404, detail="Document not found")
    
    project = session.get(Project, document_run.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Run verifier to get fresh recommendations
    try:
        llm_client = LLMClient()
        verifier = VerifierAgent(llm_client)
        
        registry = ProjectRegistry(session)
        context_builder = ContextBuilder(registry)
        context = context_builder.build_context(project.id)
        
        user_inputs = None
        if document_run.user_inputs:
            try:
                user_inputs = json.loads(document_run.user_inputs)
            except:
                pass
        
        verification = verifier.verify_document(
            template_name=document_run.template_name,
            document_content=document_run.initial_draft,
            project_context=context,
            user_inputs=user_inputs
        )
        
        return templates.TemplateResponse(
            "generate/refine_guidance.html",
            {
                "request": request,
                "project": project,
                "document_run": document_run,
                "verification": verification,
                "template_name": document_run.template_name
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "generate/error.html",
            {
                "request": request,
                "project": project,
                "error": f"Failed to load refinement guidance: {str(e)}"
            }
        )


@router.post("/document/{document_run_id}/apply-refinement", response_class=HTMLResponse)
async def apply_guided_refinement(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Apply user-guided refinements to document."""
    document_run = session.get(DocumentRun, document_run_id)
    
    if not document_run:
        raise HTTPException(status_code=404, detail="Document not found")
    
    project = session.get(Project, document_run.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Get form data
        form_data = await request.form()
        
        # Extract improvement instructions from form
        # Form has: improvement_1, improvement_2, etc. (editable by user)
        improvements = []
        focus_areas = []
        
        i = 1
        while f"improvement_{i}" in form_data:
            improvement = form_data[f"improvement_{i}"].strip()
            if improvement:  # Only add non-empty improvements
                improvements.append(improvement)
            i += 1
        
        # Extract focus areas (checkboxes)
        j = 1
        while f"focus_area_{j}" in form_data:
            focus_area = form_data[f"focus_area_{j}"].strip()
            if focus_area:
                focus_areas.append(focus_area)
            j += 1
        
        if not improvements:
            raise ValueError("No improvement instructions provided")
        
        # Get project context
        registry = ProjectRegistry(session)
        context_builder = ContextBuilder(registry)
        context = context_builder.build_context(project.id)
        
        # Initialize refinement agent
        llm_client = LLMClient()
        refinement_agent = RefinementAgent(llm_client)
        
        # Apply refinements
        refinement_result = refinement_agent.refine_document(
            document_content=document_run.initial_draft,
            improvement_instructions=improvements,
            context=context,
            focus_areas=focus_areas if focus_areas else None
        )
        
        # Save refined version
        document_run.refined_draft = refinement_result.refined_content
        session.commit()
        
        # Show refined document
        return templates.TemplateResponse(
            "generate/draft.html",
            {
                "request": request,
                "project": project,
                "template_name": document_run.template_name,
                "draft_content": refinement_result.refined_content,
                "model_used": refinement_result.model_used,
                "tokens_used": refinement_result.tokens_used,
                "step_back_summary": "Guided Refinement",
                "refined_summary": refinement_result.summary,
                "refinement_iterations": 1,
                "document_run_id": document_run.id,
                "is_refined": True
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "generate/error.html",
            {
                "request": request,
                "project": project,
                "error": f"Refinement failed: {str(e)}"
            }
        )


@router.post("/document/{document_run_id}/condense", response_class=HTMLResponse)
async def condense_document(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Condense document by removing repetition and verbose paragraphs."""
    document_run = session.get(DocumentRun, document_run_id)
    
    if not document_run:
        raise HTTPException(status_code=404, detail="Document not found")
    
    project = session.get(Project, document_run.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        llm_client = LLMClient()
        verifier = VerifierAgent(llm_client)
        
        # Run verification first to get specific issues
        registry = ProjectRegistry(session)
        context_builder = ContextBuilder(registry)
        context = context_builder.build_context(project.id)
        
        user_inputs = None
        if document_run.user_inputs:
            try:
                user_inputs = json.loads(document_run.user_inputs)
            except:
                pass
        
        verification = verifier.verify_document(
            template_name=document_run.template_name,
            document_content=document_run.initial_draft,
            project_context=context,
            user_inputs=user_inputs
        )
        
        # Build improvement instructions from verification feedback
        improvement_instructions = []
        if verification.issues:
            improvement_instructions.append("## CRITICAL ISSUES TO FIX:")
            for issue in verification.issues[:5]:  # Top 5 issues
                improvement_instructions.append(f"- {issue}")
        
        if verification.recommendations:
            improvement_instructions.append("\n## APPLY THESE IMPROVEMENTS:")
            for rec in verification.recommendations[:5]:  # Top 5 recommendations
                improvement_instructions.append(f"- {rec}")
        
        improvements_text = "\n".join(improvement_instructions) if improvement_instructions else "Focus on removing repetition and condensing verbose paragraphs."
        
        system_message = """You are an expert editor who condenses verbose documents while fixing data inconsistencies.

Your goals:
1. Fix any data inconsistencies (use the source data to verify numbers)
2. Remove repetition - mention key stats once, reference them later
3. Cut paragraphs to 3-4 sentences max
4. Keep all tables and calculations
5. Complete any incomplete sections

Rules:
- Verify all numbers against source data
- Executive Summary: 500-700 words maximum
- No repetitive paragraphs
- Cross-reference instead of repeating: "As shown in Section X..."
- Keep bold formatting for metrics"""
        
        prompt = f"""# TASK: CONDENSE AND FIX THIS DOCUMENT

Current length: {len(document_run.initial_draft)} characters ({len(document_run.initial_draft.split())} words)
Target: 40-50% shorter (remove repetition, tighten paragraphs)

{improvements_text}

## SOURCE DATA (for verification)
{context.notes_summary[:3000] if context else 'No source data available'}

## CURRENT DOCUMENT

{document_run.initial_draft}

## INSTRUCTIONS

1. Fix data inconsistencies first (verify against source data above)
2. Condense Executive Summary to 500-700 words
3. Remove repetitive sections - mention key stats ONCE, reference them later
4. Cut paragraphs to 3-4 sentences
5. Complete any incomplete sections (Business Implications ends mid-sentence)
6. Keep ALL tables and calculations
7. Use cross-references: "As detailed in Executive Summary..." instead of repeating

Return ONLY the condensed markdown, no commentary."""
        
        response = llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3,
            max_tokens=8000
        )
        
        # Save condensed version as refined_draft
        document_run.refined_draft = response.content.strip()
        session.commit()
        
        # Show the condensed version
        return templates.TemplateResponse(
            "generate/draft.html",
            {
                "request": request,
                "project": project,
                "template_name": document_run.template_name,
                "draft_content": response.content.strip(),
                "model_used": llm_client.model,
                "tokens_used": response.tokens_used,
                "step_back_summary": "Condensed Version (40-50% shorter)",
                "refined_summary": document_run.executive_summary,
                "refinement_iterations": 1,
                "document_run_id": document_run.id,
                "is_condensed": True
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "generate/error.html",
            {
                "request": request,
                "project": project,
                "error": f"Condensing failed: {str(e)}"
            }
        )


@router.get("/document/{document_run_id}/review", response_class=HTMLResponse)
async def review_document(
    request: Request,
    document_run_id: int,
    session: Session = Depends(get_db_session)
):
    """Review document with AI verifier and show improvement suggestions."""
    document_run = session.get(DocumentRun, document_run_id)
    
    if not document_run:
        raise HTTPException(status_code=404, detail="Document not found")
    
    project = session.get(Project, document_run.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build context
    registry = ProjectRegistry(session)
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(project.id)
    
    # Run verifier
    try:
        llm_client = LLMClient()
        verifier = VerifierAgent(llm_client)
        
        # Get user inputs if available
        user_inputs = None
        if document_run.user_inputs:
            try:
                user_inputs = json.loads(document_run.user_inputs)
            except:
                pass
        
        verification = verifier.verify_document(
            template_name=document_run.template_name,
            document_content=document_run.initial_draft,
            project_context=context,
            user_inputs=user_inputs
        )
        
        return templates.TemplateResponse(
            "generate/review.html",
            {
                "request": request,
                "project": project,
                "document_run": document_run,
                "verification": verification,
                "template_name": document_run.template_name
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "generate/error.html",
            {
                "request": request,
                "project": project,
                "error": f"Verification failed: {str(e)}"
            }
        )
