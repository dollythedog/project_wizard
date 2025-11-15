"""
Issue data model for Kanban board.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class IssueStatus(Enum):
    """Issue status states."""
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

    @classmethod
    def from_emoji(cls, emoji: str) -> "IssueStatus":
        """Convert emoji status to enum."""
        mapping = {
            "🔵": cls.BACKLOG,
            "🟢": cls.IN_PROGRESS,
            "🟡": cls.REVIEW,
            "✅": cls.DONE,
        }
        return mapping.get(emoji, cls.BACKLOG)

    def to_emoji(self) -> str:
        """Convert enum to emoji."""
        mapping = {
            self.BACKLOG: "🔵",
            self.IN_PROGRESS: "🟢",
            self.REVIEW: "🟡",
            self.DONE: "✅",
        }
        return mapping.get(self, "🔵")

    def to_display_name(self) -> str:
        """Convert enum to display name."""
        mapping = {
            self.BACKLOG: "Backlog",
            self.IN_PROGRESS: "In Progress",
            self.REVIEW: "Review",
            self.DONE: "Done",
        }
        return mapping.get(self, "Backlog")


class IssuePriority(Enum):
    """Issue priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def from_string(cls, priority_str: str) -> "IssuePriority":
        """Convert string to enum."""
        priority_str = priority_str.lower().strip()
        mapping = {
            "high": cls.HIGH,
            "medium": cls.MEDIUM,
            "low": cls.LOW,
        }
        return mapping.get(priority_str, cls.MEDIUM)

    def to_emoji(self) -> str:
        """Convert priority to emoji."""
        mapping = {
            self.HIGH: "🔴",
            self.MEDIUM: "🟡",
            self.LOW: "🔵",
        }
        return mapping.get(self, "🟡")

    def to_color(self) -> str:
        """Convert priority to color for UI."""
        mapping = {
            self.HIGH: "red",
            self.MEDIUM: "orange",
            self.LOW: "blue",
        }
        return mapping.get(self, "gray")


@dataclass
class Issue:
    """Represents a project issue."""
    id: str
    title: str
    status: IssueStatus
    priority: IssuePriority
    component: str
    project: str
    description: str = ""
    solution: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def get_short_title(self, max_length: int = 50) -> str:
        """Get truncated title for display."""
        if len(self.title) <= max_length:
            return self.title
        return self.title[:max_length - 3] + "..."

    def get_project_tag(self) -> str:
        """Get short project tag for display."""
        if self.project.lower() == "project_wizard":
            return "PW"
        # Use first 2 letters of each word
        words = self.project.replace("_", " ").split()
        return "".join(w[0].upper() for w in words[:2])
