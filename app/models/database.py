"""
Database models for Project Wizard v3.0.

Uses SQLModel for ORM with Pydantic validation.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Project(SQLModel, table=True):
    """
    Project container - stores all project metadata and relationships.
    
    A project is the central entity that holds charter data, notes, files,
    and document generation history.
    """
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    project_type: str = Field(max_length=50)  # software_mvp, clinical_workflow, etc.
    description: Optional[str] = None
    status: str = Field(default="initiating", max_length=50)  # initiating, planning, executing, closing
    
    # Charter data (stored as JSON for flexibility)
    charter_data: Optional[str] = None  # JSON string
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    notes: list["ProjectNote"] = Relationship(back_populates="project", cascade_delete=True)
    files: list["SupportingFile"] = Relationship(back_populates="project", cascade_delete=True)
    document_runs: list["DocumentRun"] = Relationship(back_populates="project", cascade_delete=True)


class ProjectNote(SQLModel, table=True):
    """
    Notes attached to a project.
    
    Used to capture context, decisions, technical details, lessons learned, etc.
    All notes are aggregated as context for AI document generation.
    """
    __tablename__ = "project_notes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    title: str = Field(max_length=255)
    content: str  # Markdown format
    note_type: str = Field(default="general", max_length=50)  # general, technical, decision, lesson
    tags: Optional[str] = None  # Comma-separated tags
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Optional[Project] = Relationship(back_populates="notes")


class SupportingFile(SQLModel, table=True):
    """
    Files attached to a project (PDFs, DOCX, etc.).
    
    Files are processed to extract text and generate summaries for AI context.
    """
    __tablename__ = "supporting_files"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    filename: str = Field(max_length=255)
    filepath: str  # Relative path from project root
    file_type: str = Field(max_length=50)  # pdf, docx, txt, markdown
    file_size: int  # Bytes
    
    # AI-extracted content
    summary: Optional[str] = None  # AI-generated summary
    extracted_text: Optional[str] = None  # For searchability
    
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Optional[Project] = Relationship(back_populates="files")


class DocumentRun(SQLModel, table=True):
    """
    Record of a document generation workflow.
    
    Stores all intermediate outputs from the agentic pipeline:
    step-back, draft, verification, refinement, memory.
    """
    __tablename__ = "document_runs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    template_name: str = Field(max_length=100, index=True)  # project_charter, white_paper, etc.
    
    # Pipeline stages (stored as JSON or text)
    user_inputs: Optional[str] = None  # JSON string of user inputs
    step_back_summary: Optional[str] = None  # Text summary from StepBackAgent
    initial_draft: Optional[str] = None  # Markdown
    verification_questions: Optional[str] = None  # JSON array
    verification_answers: Optional[str] = None  # JSON array
    refined_draft: Optional[str] = None  # Markdown
    executive_summary: Optional[str] = None  # Text
    
    # Memory system
    memory_log: Optional[str] = None  # What was learned
    improvements_applied: Optional[str] = None  # JSON array
    
    # Status tracking
    status: str = Field(default="in_progress", max_length=50)  # in_progress, completed, failed
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Relationships
    project: Optional[Project] = Relationship(back_populates="document_runs")


class MemoryEntry(SQLModel, table=True):
    """
    Memory-of-thought system for continuous improvement.
    
    Stores lessons learned, best practices, and patterns discovered
    during document generation. Used to improve future generations.
    """
    __tablename__ = "memory_entries"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    template_name: Optional[str] = Field(default=None, max_length=100, index=True)  # None = global
    category: str = Field(max_length=50)  # best_practice, lesson_learned, pattern, anti_pattern
    content: str
    
    # Source tracking
    source_document_run_id: Optional[int] = Field(default=None, foreign_key="document_runs.id")
    
    # Effectiveness tracking
    times_applied: int = Field(default=0)
    effectiveness_score: float = Field(default=0.0)  # 0.0 to 1.0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_applied: Optional[datetime] = None
