"""
Pydantic models for Project Charter
Based on PROJECT_STEP_BY_STEP.md variable definitions
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class CharterData(BaseModel):
    """Complete project charter data structure"""

    # Basic project info
    project_title: str = Field(..., description="Project name")
    project_sponsor: str = Field(..., description="Executive sponsor")
    department: str = Field(default="", description="Department or organization")
    charter_date: date = Field(default_factory=date.today)

    # Step 1: Initiation (Prompt 1 fields)
    business_need: str = Field(..., description="Problem, need, or opportunity being addressed")
    desired_outcomes: str = Field(..., description="Expected results and strategic alignment")
    success_criteria: str = Field(..., description="Measurable standards for success")
    initial_risks_and_assumptions: str = Field(..., description="High-level risks and assumptions")
    strategic_alignment: str = Field(..., description="How project supports organizational goals")
    measurable_benefits: str = Field(..., description="Quantifiable improvements")
    high_level_requirements: str = Field(..., description="Essential capabilities needed")

    # Step 2: Charter Finalization (Prompt 2 fields)
    project_goal: str = Field(..., description="Overall project goal")
    problem_definition: str = Field(..., description="Detailed problem/opportunity statement")
    proposed_solution: str = Field(..., description="Approach to address the problem")
    selection_criteria: List[str] = Field(default_factory=list, description="Why this solution")
    cost_benefit_analysis: str = Field(default="", description="Cost/benefit breakdown")
    scope: str = Field(..., description="What is in and out of scope")
    deliverables: str = Field(..., description="Major project outputs")
    major_obstacles: str = Field(default="", description="Anticipated challenges")
    risks: str = Field(default="", description="Detailed risk assessment")
    schedule_overview: str = Field(default="", description="Timeline summary")
    collaboration_needs: str = Field(default="", description="External dependencies")

    # Optional/computed fields
    project_type: Optional[str] = Field(default=None, description="software_mvp, clinical_workflow, etc.")
    estimated_budget: Optional[float] = Field(default=None, description="Total estimated cost")
    estimated_duration_days: Optional[int] = Field(default=None, description="Project length in days")


class ProjectMetadata(BaseModel):
    """Minimal project metadata for tracking"""

    project_id: str
    project_title: str
    project_type: str
    status: str = "initiating"  # initiating, planning, executing, closing, closed
    created_date: date = Field(default_factory=date.today)
    openproject_id: Optional[int] = None
    openproject_url: Optional[str] = None
    repo_path: Optional[str] = None
