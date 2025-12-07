"""
Project registry service for CRUD operations.

Handles creating, reading, updating, and deleting projects, notes, and files.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from app.models.database import Project, ProjectNote, SupportingFile


class ProjectRegistry:
    """Service for managing projects in the database."""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ===== Project CRUD =====
    
    def create_project(
        self,
        title: str,
        project_type: str,
        description: Optional[str] = None
    ) -> Project:
        """Create a new project."""
        project = Project(
            title=title,
            project_type=project_type,
            description=description,
            status="initiating"
        )
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self.session.get(Project, project_id)
    
    def list_projects(
        self,
        status: Optional[str] = None,
        project_type: Optional[str] = None
    ) -> list[Project]:
        """
        List all projects, optionally filtered by status or type.
        """
        statement = select(Project)
        
        if status:
            statement = statement.where(Project.status == status)
        if project_type:
            statement = statement.where(Project.project_type == project_type)
        
        statement = statement.order_by(Project.updated_at.desc())
        results = self.session.exec(statement)
        return list(results.all())
    
    def update_project(
        self,
        project_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        charter_data: Optional[str] = None
    ) -> Optional[Project]:
        """Update a project."""
        project = self.get_project(project_id)
        if not project:
            return None
        
        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status
        if charter_data is not None:
            project.charter_data = charter_data
        
        project.updated_at = datetime.utcnow()
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project
    
    def delete_project(self, project_id: int) -> bool:
        """Delete a project (cascades to notes, files, document_runs)."""
        project = self.get_project(project_id)
        if not project:
            return False
        
        self.session.delete(project)
        self.session.commit()
        return True
    
    # ===== Note CRUD =====
    
    def create_note(
        self,
        project_id: int,
        title: str,
        content: str,
        note_type: str = "general",
        tags: Optional[str] = None
    ) -> Optional[ProjectNote]:
        """Create a new note for a project."""
        # Verify project exists
        project = self.get_project(project_id)
        if not project:
            return None
        
        note = ProjectNote(
            project_id=project_id,
            title=title,
            content=content,
            note_type=note_type,
            tags=tags
        )
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        
        # Update project timestamp
        project.updated_at = datetime.utcnow()
        self.session.add(project)
        self.session.commit()
        
        return note
    
    def get_note(self, note_id: int) -> Optional[ProjectNote]:
        """Get a note by ID."""
        return self.session.get(ProjectNote, note_id)
    
    def list_notes(
        self,
        project_id: int,
        note_type: Optional[str] = None
    ) -> list[ProjectNote]:
        """List all notes for a project."""
        statement = select(ProjectNote).where(ProjectNote.project_id == project_id)
        
        if note_type:
            statement = statement.where(ProjectNote.note_type == note_type)
        
        statement = statement.order_by(ProjectNote.created_at.desc())
        results = self.session.exec(statement)
        return list(results.all())
    
    def update_note(
        self,
        note_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        note_type: Optional[str] = None,
        tags: Optional[str] = None
    ) -> Optional[ProjectNote]:
        """Update a note."""
        note = self.get_note(note_id)
        if not note:
            return None
        
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if note_type is not None:
            note.note_type = note_type
        if tags is not None:
            note.tags = tags
        
        note.updated_at = datetime.utcnow()
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note."""
        note = self.get_note(note_id)
        if not note:
            return False
        
        self.session.delete(note)
        self.session.commit()
        return True
    
    # ===== File CRUD =====
    
    def create_file(
        self,
        project_id: int,
        filename: str,
        filepath: str,
        file_type: str,
        file_size: int
    ) -> Optional[SupportingFile]:
        """Create a new file record for a project."""
        # Verify project exists
        project = self.get_project(project_id)
        if not project:
            return None
        
        file = SupportingFile(
            project_id=project_id,
            filename=filename,
            filepath=filepath,
            file_type=file_type,
            file_size=file_size
        )
        self.session.add(file)
        self.session.commit()
        self.session.refresh(file)
        
        # Update project timestamp
        project.updated_at = datetime.utcnow()
        self.session.add(project)
        self.session.commit()
        
        return file
    
    def get_file(self, file_id: int) -> Optional[SupportingFile]:
        """Get a file by ID."""
        return self.session.get(SupportingFile, file_id)
    
    def list_files(self, project_id: int) -> list[SupportingFile]:
        """List all files for a project."""
        statement = select(SupportingFile).where(
            SupportingFile.project_id == project_id
        ).order_by(SupportingFile.uploaded_at.desc())
        
        results = self.session.exec(statement)
        return list(results.all())
    
    def delete_file(self, file_id: int) -> bool:
        """Delete a file record."""
        file = self.get_file(file_id)
        if not file:
            return False
        
        self.session.delete(file)
        self.session.commit()
        return True
