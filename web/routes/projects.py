"""
Project management routes.

Handles listing, creating, viewing, and editing projects.
"""

from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pathlib import Path

from app.services.database import get_db_session
from app.services.project_registry import ProjectRegistry

router = APIRouter()

# Templates
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    session: Session = Depends(get_db_session)
):
    """List all projects."""
    registry = ProjectRegistry(session)
    projects = registry.list_projects()
    
    return templates.TemplateResponse(
        "projects/list.html",
        {
            "request": request,
            "projects": projects
        }
    )


@router.get("/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_form(
    request: Request,
    project_id: int,
    session: Session = Depends(get_db_session)
):
    """Show project edit form."""
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return templates.TemplateResponse(
        "projects/edit.html",
        {
            "request": request,
            "project": project
        }
    )


@router.post("/{project_id}/edit", response_class=HTMLResponse)
async def update_project(
    request: Request,
    project_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    project_type: str = Form(...),
    status: str = Form("initiating"),
    session: Session = Depends(get_db_session)
):
    """Update project metadata."""
    from datetime import datetime
    
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate status
    valid_statuses = ["initiating", "planning", "executing", "closing"]
    if status not in valid_statuses:
        status = "initiating"
    
    # Update project
    project.title = title
    project.description = description
    project.project_type = project_type
    project.status = status
    project.updated_at = datetime.utcnow()
    
    session.add(project)
    session.commit()
    session.refresh(project)
    
    # Check if HTMX request
    hx_request = request.headers.get("HX-Request")
    if hx_request:
        # Return updated project info card
        return templates.TemplateResponse(
            "partials/project_info_card.html",
            {
                "request": request,
                "project": project
            }
        )
    
    # Regular request - redirect to project detail
    return templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "project": project,
            "notes": registry.list_notes(project_id),
            "files": registry.list_files(project_id),
            "document_runs": sorted(project.document_runs, key=lambda d: d.created_at, reverse=True)
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_project_form(request: Request):
    """Show create project form."""
    # Removed fixed project types - user can now enter custom types
    return templates.TemplateResponse(
        "projects/create.html",
        {
            "request": request
        }
    )


@router.post("/create", response_class=HTMLResponse)
async def create_project(
    request: Request,
    title: str = Form(...),
    project_type: str = Form(...),
    description: str = Form(None),
    session: Session = Depends(get_db_session)
):
    """Create a new project."""
    registry = ProjectRegistry(session)
    project = registry.create_project(
        title=title,
        project_type=project_type,
        description=description
    )
    
    # Check if HTMX request
    hx_request = request.headers.get("HX-Request")
    if hx_request:
        # Return partial template for HTMX
        return templates.TemplateResponse(
            "partials/project_card.html",
            {
                "request": request,
                "project": project
            }
        )
    
    # Regular request - redirect to project detail
    return templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "project": project,
            "notes": [],
            "files": []
        }
    )


@router.get("/{project_id}", response_class=HTMLResponse)
async def view_project(
    request: Request,
    project_id: int,
    session: Session = Depends(get_db_session)
):
    """View project details."""
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    notes = registry.list_notes(project_id)
    files = registry.list_files(project_id)
    
    # Get generated documents (sorted by most recent)
    document_runs = sorted(project.document_runs, key=lambda d: d.created_at, reverse=True)
    
    return templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "project": project,
            "notes": notes,
            "files": files,
            "document_runs": document_runs
        }
    )


@router.post("/{project_id}/notes", response_class=HTMLResponse)
async def add_note(
    request: Request,
    project_id: int,
    title: str = Form(...),
    content: str = Form(...),
    note_type: str = Form("general"),
    tags: Optional[str] = Form(None),
    session: Session = Depends(get_db_session)
):
    """Add a note to a project."""
    registry = ProjectRegistry(session)
    note = registry.create_note(
        project_id=project_id,
        title=title,
        content=content,
        note_type=note_type,
        tags=tags
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Return partial template for HTMX
    return templates.TemplateResponse(
        "partials/note_card.html",
        {
            "request": request,
            "note": note
        }
    )


@router.put("/{project_id}/notes/{note_id}", response_class=HTMLResponse)
@router.post("/{project_id}/notes/{note_id}/update", response_class=HTMLResponse)
async def update_note(
    request: Request,
    project_id: int,
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    note_type: str = Form("general"),
    tags: Optional[str] = Form(None),
    session: Session = Depends(get_db_session)
):
    """Update an existing note."""
    from app.models.database import ProjectNote
    from datetime import datetime
    
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    note = session.query(ProjectNote).filter(
        ProjectNote.id == note_id,
        ProjectNote.project_id == project_id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Update note fields
    note.title = title
    note.content = content
    note.note_type = note_type
    note.tags = tags
    note.updated_at = datetime.utcnow()
    
    session.add(note)
    session.commit()
    session.refresh(note)
    
    # Return updated note card
    return templates.TemplateResponse(
        "partials/note_card.html",
        {
            "request": request,
            "note": note
        }
    )


@router.delete("/{project_id}/notes/{note_id}")
@router.post("/{project_id}/notes/{note_id}/delete")
async def delete_note(
    project_id: int,
    note_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete a note from a project."""
    from app.models.database import ProjectNote
    
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    note = session.query(ProjectNote).filter(
        ProjectNote.id == note_id,
        ProjectNote.project_id == project_id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    session.delete(note)
    session.commit()
    
    return {"success": True}
