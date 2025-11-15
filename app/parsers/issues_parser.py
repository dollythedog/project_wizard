"""
Parser for ISSUES.md files to extract issue data.
"""
import re
from pathlib import Path
from typing import List

from app.models.issue import Issue, IssueStatus, IssuePriority


class IssuesParser:
    """Parse ISSUES.md files to extract issue information."""

    def __init__(self, issues_file_path: Path):
        """Initialize parser with path to ISSUES.md."""
        self.issues_file_path = issues_file_path

    def parse(self) -> List[Issue]:
        """Parse ISSUES.md and return list of Issue objects."""
        if not self.issues_file_path.exists():
            return []

        with open(self.issues_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find the Active Issues section
        active_section_match = re.search(r'## 🎯 Active Issues', content)
        if not active_section_match:
            return []
        
        active_section_start = active_section_match.end()
        
        # Find where resolved issues start (to exclude them)
        resolved_section_match = re.search(r'## ✅ Recently Resolved Issues', content)
        if resolved_section_match:
            active_section_end = resolved_section_match.start()
        else:
            active_section_end = len(content)
        
        # Get just the active issues section
        active_content = content[active_section_start:active_section_end]

        issues = []
        
        # Split by issue headers (lines starting with **#)
        issue_pattern = r'\*\*#(\d+):\s*([^*]+)\*\*'
        matches = list(re.finditer(issue_pattern, active_content))
        
        for i, match in enumerate(matches):
            issue_id = f"#{match.group(1)}"
            title = match.group(2).strip()
            
            # Get the block of text for this issue
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(active_content)
            issue_block = active_content[start_pos:end_pos]
            
            # Extract metadata
            status = self._extract_status(issue_block)
            priority = self._extract_priority(issue_block)
            component = self._extract_component(issue_block)
            project = self._extract_project(issue_block)
            description = self._extract_description(issue_block)
            solution = self._extract_solution(issue_block)
            
            issue = Issue(
                id=issue_id,
                title=title,
                status=status,
                priority=priority,
                component=component,
                project=project,
                description=description,
                solution=solution,
            )
            issues.append(issue)
        
        return issues

    def _extract_status(self, block: str) -> IssueStatus:
        """Extract status from issue block."""
        status_match = re.search(r'\*\*Status:\*\*\s*([🔵🟢🟡🔴✅])\s*([A-Za-z\s]+)', block)
        if status_match:
            emoji = status_match.group(1)
            text = status_match.group(2).lower().strip()
            
            # Map text to status
            if "progress" in text:
                return IssueStatus.IN_PROGRESS
            elif "planned" in text or "backlog" in text:
                return IssueStatus.BACKLOG
            elif "review" in text or "fix" in text:
                return IssueStatus.REVIEW
            elif "done" in text or "resolved" in text:
                return IssueStatus.DONE
            
            # Fallback to emoji
            return IssueStatus.from_emoji(emoji)
        
        return IssueStatus.BACKLOG

    def _extract_priority(self, block: str) -> IssuePriority:
        """Extract priority from issue block."""
        priority_match = re.search(r'\*\*Priority:\*\*\s*([A-Za-z]+)', block)
        if priority_match:
            priority_str = priority_match.group(1)
            return IssuePriority.from_string(priority_str)
        return IssuePriority.MEDIUM

    def _extract_component(self, block: str) -> str:
        """Extract component from issue block."""
        component_match = re.search(r'\*\*Component:\*\*\s*([A-Za-z\s/]+)', block)
        if component_match:
            return component_match.group(1).strip()
        return "General"

    def _extract_project(self, block: str) -> str:
        """Extract project from issue block."""
        # Look for Project: field
        project_match = re.search(r'\*\*Project:\*\*\s*([A-Za-z_\s]+)', block)
        if project_match:
            return project_match.group(1).strip()
        
        # Default to project_wizard
        return "project_wizard"

    def _extract_description(self, block: str) -> str:
        """Extract description from issue block."""
        desc_match = re.search(r'\*\*Description:\*\*\s*\n(.+?)(?:\n\*\*|\n##|\Z)', block, re.DOTALL)
        if desc_match:
            return desc_match.group(1).strip()
        return ""

    def _extract_solution(self, block: str) -> str:
        """Extract solution from issue block."""
        sol_match = re.search(r'\*\*Solution:\*\*\s*\n(.+?)(?:\n\*\*|\n##|\Z)', block, re.DOTALL)
        if sol_match:
            return sol_match.group(1).strip()
        return ""
