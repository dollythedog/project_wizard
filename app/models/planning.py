"""
Planning Data Models
Represents project work breakdown structure
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Task(BaseModel):
    """Individual task within a milestone"""
    title: str
    duration: Optional[str] = None  # e.g., "1 hour", "30 min"
    completed: bool = False
    notes: Optional[str] = None


class Milestone(BaseModel):
    """Project milestone with tasks"""
    title: str
    phase: str  # e.g., "Phase 1", "Phase 2"
    duration: Optional[str] = None
    tasks: List[Task] = []
    description: Optional[str] = None


class ProjectPlan(BaseModel):
    """Complete project work breakdown structure"""
    project_title: str
    total_duration: Optional[str] = None  # e.g., "7 days"
    milestones: List[Milestone] = []
    created_date: date = date.today()
    notes: Optional[str] = None
