"""
Issue Manager service for managing issues across projects.
"""
from pathlib import Path
from typing import List, Optional

from app.models.issue import Issue, IssueStatus, IssuePriority
from app.parsers.issues_parser import IssuesParser


class IssueManager:
    """Manage issues for Project Wizard and created projects."""

    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize IssueManager.
        
        Args:
            project_path: Path to project. If None, uses project_wizard's ISSUES.md
        """
        if project_path:
            self.issues_file = Path(project_path) / "ISSUES.md"
        else:
            # Default to project_wizard's ISSUES.md
            self.issues_file = Path(__file__).parent.parent.parent / "ISSUES.md"
        
        self.parser = IssuesParser(self.issues_file)

    def get_all_issues(self) -> List[Issue]:
        """Get all active issues from ISSUES.md."""
        return self.parser.parse()

    def get_issues_by_status(self, status: IssueStatus) -> List[Issue]:
        """Get issues filtered by status."""
        all_issues = self.get_all_issues()
        return [issue for issue in all_issues if issue.status == status]

    def get_issues_by_priority(self, priority: IssuePriority) -> List[Issue]:
        """Get issues filtered by priority."""
        all_issues = self.get_all_issues()
        return [issue for issue in all_issues if issue.priority == priority]

    def get_issues_by_project(self, project: str) -> List[Issue]:
        """Get issues filtered by project."""
        all_issues = self.get_all_issues()
        return [issue for issue in all_issues if issue.project.lower() == project.lower()]

    def get_issue_by_id(self, issue_id: str) -> Optional[Issue]:
        """Get a specific issue by ID."""
        all_issues = self.get_all_issues()
        for issue in all_issues:
            if issue.id == issue_id:
                return issue
        return None

    def get_unique_projects(self) -> List[str]:
        """Get list of unique projects that have issues."""
        all_issues = self.get_all_issues()
        projects = set(issue.project for issue in all_issues)
        return sorted(list(projects))

    def get_issue_counts_by_status(self) -> dict:
        """Get count of issues in each status."""
        all_issues = self.get_all_issues()
        counts = {
            IssueStatus.BACKLOG: 0,
            IssueStatus.IN_PROGRESS: 0,
            IssueStatus.REVIEW: 0,
            IssueStatus.DONE: 0,
        }
        for issue in all_issues:
            counts[issue.status] += 1
        return counts

    def get_issue_counts_by_priority(self) -> dict:
        """Get count of issues by priority."""
        all_issues = self.get_all_issues()
        counts = {
            IssuePriority.HIGH: 0,
            IssuePriority.MEDIUM: 0,
            IssuePriority.LOW: 0,
        }
        for issue in all_issues:
            counts[issue.priority] += 1
        return counts
