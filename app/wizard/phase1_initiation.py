"""
Phase 1: Initiation - Charter Creation Wizard
Interactive CLI for Prompts 1 + 2
"""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import date
from typing import Dict, Any
from ..models.charter import CharterData

console = Console()


def run_initiation_wizard(project_type: str = None) -> CharterData:
    """
    Interactive wizard for project charter creation
    Follows the two-prompt structure from saved prompts
    """
    
    console.print(Panel.fit(
        "[bold cyan]Project Wizard - Phase 1: Initiation[/bold cyan]\n\n"
        "This wizard will guide you through creating a project charter\n"
        "following your established project management methodology.",
        border_style="cyan"
    ))
    
    console.print("\n[bold]Part 1: Basic Information[/bold]\n")
    
    # Basic info
    project_title = questionary.text(
        "Project Title:",
        validate=lambda text: len(text) > 0
    ).ask()
    
    project_sponsor = questionary.text(
        "Project Sponsor:",
        default="Jonathan Ives"
    ).ask()
    
    department = questionary.text(
        "Department/Organization:",
        default="Texas Pulmonary & Critical Care Consultants"
    ).ask()
    
    # Project type selection
    if not project_type:
        project_type = questionary.select(
            "Project Type:",
            choices=[
                "software_mvp",
                "clinical_workflow",
                "infrastructure",
                "landscaping",
                "research_analysis",
                "other"
            ]
        ).ask()
    
    console.print("\n[bold]Part 2: Business Case Elements (Prompt 1)[/bold]\n")
    console.print("[dim]Define the strategic context and justification[/dim]\n")
    
    business_need = questionary.text(
        "Business Need (problem/opportunity):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    desired_outcomes = questionary.text(
        "Desired Outcomes:",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    success_criteria = questionary.text(
        "Success Criteria (measurable):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    initial_risks_and_assumptions = questionary.text(
        "Initial Risks and Assumptions:",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    strategic_alignment = questionary.text(
        "Strategic Alignment (how it supports org goals):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    measurable_benefits = questionary.text(
        "Measurable Benefits (quantifiable improvements):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    high_level_requirements = questionary.text(
        "High-Level Requirements (key capabilities needed):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    console.print("\n[bold]Part 3: Charter Finalization (Prompt 2)[/bold]\n")
    console.print("[dim]Detailed planning elements[/dim]\n")
    
    project_goal = questionary.text(
        "Project Goal (overall objective):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    problem_definition = questionary.text(
        "Problem/Opportunity Definition (detailed):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    proposed_solution = questionary.text(
        "Proposed Solution (approach):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    # Selection criteria (multi-select)
    selection_criteria = questionary.checkbox(
        "Selection Criteria (why this solution):",
        choices=[
            "Compliance/Regulatory",
            "Efficiency/Cost Reduction",
            "Revenue Increase",
            "Patient/Customer Experience",
            "Staff Satisfaction",
            "Strategic Positioning",
            "Other"
        ]
    ).ask()
    
    cost_benefit_analysis = questionary.text(
        "Cost/Benefit Analysis:",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    scope = questionary.text(
        "Scope (in-scope and out-of-scope):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    deliverables = questionary.text(
        "Major Deliverables:",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    major_obstacles = questionary.text(
        "Major Obstacles:",
        multiline=True,
        instruction="(Optional - Press ESC then Enter when done)"
    ).ask() or ""
    
    risks = questionary.text(
        "Risks and Mitigation Strategies:",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    schedule_overview = questionary.text(
        "Schedule Overview (timeline summary):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()
    
    collaboration_needs = questionary.text(
        "Collaboration Needs (external dependencies):",
        multiline=True,
        instruction="(Optional - Press ESC then Enter when done)"
    ).ask() or ""
    
    # Optional: Budget and duration
    console.print("\n[bold]Optional: Budget and Timeline[/bold]\n")
    
    has_budget = questionary.confirm(
        "Do you have an estimated budget?",
        default=False
    ).ask()
    
    estimated_budget = None
    if has_budget:
        budget_str = questionary.text("Estimated Budget ($):").ask()
        try:
            estimated_budget = float(budget_str.replace("$", "").replace(",", ""))
        except:
            pass
    
    has_duration = questionary.confirm(
        "Do you have an estimated duration?",
        default=False
    ).ask()
    
    estimated_duration_days = None
    if has_duration:
        duration_str = questionary.text("Estimated Duration (days):").ask()
        try:
            estimated_duration_days = int(duration_str)
        except:
            pass
    
    # Create charter data model
    charter = CharterData(
        project_title=project_title,
        project_sponsor=project_sponsor,
        department=department,
        charter_date=date.today(),
        business_need=business_need,
        desired_outcomes=desired_outcomes,
        success_criteria=success_criteria,
        initial_risks_and_assumptions=initial_risks_and_assumptions,
        strategic_alignment=strategic_alignment,
        measurable_benefits=measurable_benefits,
        high_level_requirements=high_level_requirements,
        project_goal=project_goal,
        problem_definition=problem_definition,
        proposed_solution=proposed_solution,
        selection_criteria=selection_criteria,
        cost_benefit_analysis=cost_benefit_analysis,
        scope=scope,
        deliverables=deliverables,
        major_obstacles=major_obstacles,
        risks=risks,
        schedule_overview=schedule_overview,
        collaboration_needs=collaboration_needs,
        project_type=project_type,
        estimated_budget=estimated_budget,
        estimated_duration_days=estimated_duration_days
    )
    
    console.print("\n[bold green]✓ Charter data collected successfully![/bold green]")
    
    return charter
