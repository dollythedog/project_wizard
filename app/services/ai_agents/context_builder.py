"""
Context Builder service.

Aggregates project context from all sources (charter, notes, files, history)
and formats it for AI consumption.
"""

import json
from typing import Optional
from dataclasses import dataclass

from app.models.database import Project, DocumentRun
from app.services.project_registry import ProjectRegistry


@dataclass
class ProjectContext:
    """Aggregated project context for AI agents."""
    project_id: int
    project_title: str
    project_type: str
    description: Optional[str]
    status: str
    
    # Context components
    notes_summary: str
    notes_count: int
    files_summary: str
    files_count: int
    charter_data: Optional[dict]
    
    # Formatted for AI
    full_context_text: str
    token_estimate: int


class ContextBuilder:
    """
    Builds rich context for AI document generation.
    
    Aggregates all project knowledge and formats it for LLM consumption.
    """
    
    def __init__(self, registry: ProjectRegistry):
        """
        Initialize context builder.
        
        Args:
            registry: ProjectRegistry for database access
        """
        self.registry = registry
    
    def build_context(
        self,
        project_id: int,
        include_notes: bool = True,
        include_files: bool = True,
        include_charter: bool = True,
        max_notes: Optional[int] = None,
        note_ids: Optional[list[int]] = None
    ) -> ProjectContext:
        """
        Build comprehensive project context.
        
        Args:
            project_id: Project ID
            include_notes: Include project notes
            include_files: Include file summaries
            include_charter: Include charter data
            max_notes: Maximum number of notes to include (most recent)
            
        Returns:
            ProjectContext with aggregated information
            
        Raises:
            ValueError: If project not found
        """
        project = self.registry.get_project(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Build context components
        notes_summary, notes_count = self._build_notes_context(
            project_id, 
            max_notes,
            note_ids
        ) if include_notes else ("", 0)
        
        files_summary, files_count = self._build_files_context(
            project_id
        ) if include_files else ("", 0)
        
        # Load charter from most recent DocumentRun (new) or legacy charter_data field
        charter_data = None
        if include_charter:
            charter_data = self._load_charter_from_document_runs(project)
            if not charter_data and project.charter_data:
                charter_data = self._parse_charter_data(project.charter_data)
        
        # Build full context text
        full_text = self._format_full_context(
            project,
            notes_summary,
            files_summary,
            charter_data
        )
        
        # Estimate tokens (rough: ~4 chars per token)
        token_estimate = len(full_text) // 4
        
        return ProjectContext(
            project_id=project.id,
            project_title=project.title,
            project_type=project.project_type,
            description=project.description,
            status=project.status,
            notes_summary=notes_summary,
            notes_count=notes_count,
            files_summary=files_summary,
            files_count=files_count,
            charter_data=charter_data,
            full_context_text=full_text,
            token_estimate=token_estimate
        )
    
    def _build_notes_context(
        self,
        project_id: int,
        max_notes: Optional[int],
        note_ids: Optional[list[int]] = None
    ) -> tuple[str, int]:
        """
        Build context from project notes.
        
        Args:
            project_id: Project ID
            max_notes: Maximum number of notes to include
            note_ids: Optional list of specific note IDs to include (filters to only these)
        
        Returns:
            Tuple of (summary text, count)
        """
        notes = self.registry.list_notes(project_id)
        
        # Filter to specific note IDs if provided
        if note_ids is not None:
            notes = [n for n in notes if n.id in note_ids]
        
        if not notes:
            return ("No notes available.", 0)
        
        # Limit number of notes if specified
        if max_notes and len(notes) > max_notes:
            notes = notes[:max_notes]
        
        # Group by type
        notes_by_type = {}
        for note in notes:
            if note.note_type not in notes_by_type:
                notes_by_type[note.note_type] = []
            notes_by_type[note.note_type].append(note)
        
        # Format summary
        summary_parts = [f"Project has {len(notes)} note(s):\n"]
        
        for note_type, typed_notes in notes_by_type.items():
            summary_parts.append(f"\n{note_type.upper()} NOTES ({len(typed_notes)}):")
            for note in typed_notes:
                summary_parts.append(f"- **{note.title}**")
                # Include full note content (no truncation) - AI needs all context
                summary_parts.append(f"  {note.content}")
        
        return ("\n".join(summary_parts), len(notes))
    
    def _build_files_context(
        self,
        project_id: int
    ) -> tuple[str, int]:
        """
        Build context from supporting files.
        
        Returns:
            Tuple of (summary text, count)
        """
        files = self.registry.list_files(project_id)
        
        if not files:
            return ("No files attached.", 0)
        
        summary_parts = [f"Project has {len(files)} file(s):\n"]
        
        for file in files:
            summary_parts.append(f"- {file.filename} ({file.file_type})")
            if file.summary:
                summary_parts.append(f"  Summary: {file.summary}")
        
        return ("\n".join(summary_parts), len(files))
    
    def _load_charter_from_document_runs(self, project: Project) -> Optional[dict]:
        """
        Load charter data from most recent completed DocumentRun.
        
        Returns:
            Charter user_inputs as dict, or None if no charter found
        """
        # Find most recent completed charter
        charter_runs = [
            dr for dr in project.document_runs 
            if dr.template_name == 'project_charter' and dr.status == 'completed'
        ]
        
        if not charter_runs:
            return None
        
        # Get most recent
        charter_run = max(charter_runs, key=lambda dr: dr.created_at)
        
        # Parse user_inputs JSON
        return self._parse_charter_data(charter_run.user_inputs)
    
    def _parse_charter_data(self, charter_json: str) -> Optional[dict]:
        """Parse charter data from JSON string."""
        try:
            return json.loads(charter_json)
        except (json.JSONDecodeError, TypeError):
            return None
    
    def _format_full_context(
        self,
        project: Project,
        notes_summary: str,
        files_summary: str,
        charter_data: Optional[dict]
    ) -> str:
        """
        Format all context into a single text block for AI.
        
        This is the main context that will be injected into AI prompts.
        """
        parts = [
            "# PROJECT CONTEXT",
            "",
            f"**Project:** {project.title}",
            f"**Type:** {project.project_type.replace('_', ' ').title()}",
            f"**Status:** {project.status}",
            ""
        ]
        
        if project.description:
            parts.extend([
                "## Project Description",
                project.description,
                ""
            ])
        
        if charter_data:
            parts.extend([
                "## Charter Information",
                self._format_charter(charter_data),
                ""
            ])
        
        # Include full charter markdown if available
        charter_markdown = self._get_charter_markdown(project)
        if charter_markdown:
            parts.extend([
                "## Completed Project Charter",
                "(Use this as background context for proposals and other documents)",
                charter_markdown,
                ""
            ])
        
        if notes_summary and notes_summary != "No notes available.":
            parts.extend([
                "## Project Notes",
                notes_summary,
                ""
            ])
        
        if files_summary and files_summary != "No files attached.":
            parts.extend([
                "## Supporting Files",
                files_summary,
                ""
            ])
        
        return "\n".join(parts)
    
    def _get_charter_markdown(self, project: Project) -> Optional[str]:
        """Get completed charter markdown from DocumentRuns."""
        # Find most recent completed charter
        charter_runs = [
            dr for dr in project.document_runs
            if dr.template_name == 'project_charter' 
            and dr.status == 'completed'
            and dr.initial_draft
        ]
        
        if not charter_runs:
            return None
        
        # Get most recent
        charter_run = max(charter_runs, key=lambda dr: dr.created_at)
        return charter_run.initial_draft
    
    def _format_charter(self, charter: dict) -> str:
        """Format charter data for context."""
        parts = []
        
        # Common charter fields
        if "goal" in charter:
            parts.append(f"**Goal:** {charter['goal']}")
        if "problem" in charter:
            parts.append(f"**Problem:** {charter['problem']}")
        if "solution" in charter:
            parts.append(f"**Solution:** {charter['solution']}")
        if "success_criteria" in charter:
            parts.append(f"**Success Criteria:** {charter['success_criteria']}")
        if "scope" in charter:
            parts.append(f"**Scope:** {charter['scope']}")
        if "deliverables" in charter:
            parts.append(f"**Deliverables:** {charter['deliverables']}")
        
        return "\n".join(parts) if parts else "(Charter data structure not recognized)"
