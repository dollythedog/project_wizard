"""
Phase 2: Planning Wizard
AI-assisted work breakdown structure creation
"""

import re

import questionary
from rich.console import Console
from rich.panel import Panel

from ..models.charter import CharterData
from ..models.planning import Milestone, ProjectPlan, Task

console = Console()


def run_planning_wizard(charter: CharterData) -> ProjectPlan:
    """
    Run Phase 2 planning wizard with AI-assisted workflow
    """
    console.print(Panel.fit(
        f"[bold cyan]📋 Project Planning - Phase 2[/bold cyan]\n\n"
        f"Project: [bold]{charter.project_title}[/bold]\n\n"
        "This wizard will help you create a detailed work breakdown.\n"
        "Paste an AI-generated plan when prompted.",
        border_style="cyan"
    ))

    # Generate AI prompt for user
    ai_prompt = _generate_ai_prompt(charter)
    
    console.print("\n" + "="*80)
    console.print(Panel(
        "[bold cyan]📋 COPY THIS PROMPT TO YOUR AI AGENT[/bold cyan]\n\n"
        "[dim]Copy the text below and send it to your AI assistant (e.g., Warp Agent)\n"
        "The AI will ask clarifying questions, then generate a properly formatted plan.[/dim]",
        border_style="cyan"
    ))
    console.print("="*80 + "\n")
    
    # Display the generated prompt
    console.print("[bold green]" + "─" * 80 + "[/bold green]")
    console.print(ai_prompt)
    console.print("[bold green]" + "─" * 80 + "[/bold green]\n")
    
    # Wait for user to copy and interact with AI
    questionary.press_any_key_to_continue(
        "Press any key after you've sent this to your AI and received the response..."
    ).ask()
    
    # Get AI-generated plan via paste
    console.print("\n[bold]Now paste the AI's response below:[/bold]\n")
    ai_plan_text = questionary.text(
        "Paste AI-generated work breakdown here (Ctrl+V):",
        multiline=True,
        instruction="(Press ESC then Enter when done)"
    ).ask()

    if not ai_plan_text:
        console.print("[yellow]No plan provided. Using simple template.[/yellow]")
        return _create_simple_plan(charter)

    # Parse the AI-generated markdown
    console.print("\n[bold]Parsing work breakdown...[/bold]")
    project_plan = _parse_markdown_plan(ai_plan_text, charter.project_title)

    total_tasks = sum(len(m.tasks) for m in project_plan.milestones)

    if len(project_plan.milestones) == 0:
        console.print("[yellow]⚠ Warning:[/yellow] No milestones found")
        console.print("\n[dim]Expected format:[/dim]")
        console.print("  ## Phase 1: Title")
        console.print("  - [ ] Task name")
        console.print("\n[dim]Or plain text:[/dim]")
        console.print("  Phase 1: Planning")
        console.print("  - Task name")
        return _create_simple_plan(charter)

    if total_tasks == 0:
        console.print("[yellow]⚠ Warning:[/yellow] No tasks found in milestones")
        console.print("Using simple template instead...")
        return _create_simple_plan(charter)

    console.print(f"[green]✓[/green] Parsed {len(project_plan.milestones)} milestones "
                  f"with {total_tasks} tasks")

    # Allow user to review/confirm
    console.print("\n[bold]Plan Preview:[/bold]")
    for milestone in project_plan.milestones[:3]:  # Show first 3
        console.print(f"  • {milestone.title} ({len(milestone.tasks)} tasks)")

    if len(project_plan.milestones) > 3:
        console.print(f"  ... and {len(project_plan.milestones) - 3} more")

    confirmed = questionary.confirm(
        "\nAccept this plan?",
        default=True
    ).ask()

    if not confirmed:
        console.print("[yellow]Plan cancelled. You can re-run 'project-wizard plan'[/yellow]")
        return None

    console.print("\n[bold green]✓ Plan accepted![/bold green]")
    return project_plan


def _generate_ai_prompt(charter: CharterData) -> str:
    """
    Generate a pre-formed prompt for the AI agent to create a work breakdown
    """
    # Truncate long fields for readability
    def truncate(text: str, max_len: int = 200) -> str:
        if len(text) <= max_len:
            return text
        return text[:max_len] + "..."
    
    prompt = f"""I need help creating a detailed project plan based on my charter.

PROJECT CHARTER SUMMARY:
────────────────────────
Project: {charter.project_title}
Goal: {truncate(charter.project_goal)}
Timeline: {truncate(charter.schedule_overview)}
Key Deliverables: {truncate(charter.deliverables)}

Business Need: {truncate(charter.business_need)}
Proposed Solution: {truncate(charter.proposed_solution)}

Constraints/Risks:
{truncate(charter.risks)}
────────────────────────

INSTRUCTIONS:
1. Review the charter details above carefully
2. Ask me 3-5 clarifying questions about:
   - Scope boundaries and priorities
   - Resource constraints (people, budget, time)
   - Dependencies and prerequisites
   - Success criteria and acceptance
3. After asking questions, answer them yourself with reasonable assumptions
   (This helps me understand your reasoning)
4. Generate a detailed work breakdown structure

REQUIRED FORMAT:
────────────────────────
Use EXACTLY this format (with "PHASE" in all caps):

PHASE 1: Phase Name (Days X-Y)

Issue 1.1: Task Name
• Subtask description
• Another subtask description
• One more subtask

Issue 1.2: Another Task Name  
• Subtask description
• Subtask description

PHASE 2: Next Phase Name (Days Y-Z)

Issue 2.1: Task Name
• Subtask description
• Subtask description
────────────────────────

FORMATTING RULES:
• Use "PHASE" not "Phase" or "phase" 
• Include duration estimates in parentheses: (Days 1-2) or (Week 1)
• Use "Issue X.Y:" for task headers (where X is phase number)
• Use bullet points (•) for subtasks, NOT dashes (-)
• Do NOT use parentheses for clarifications - put them in the subtask text
• Break work into 5-10 phases
• Each phase should have 2-6 main tasks (Issues)
• Each task should have 3-8 subtasks
• Keep subtask descriptions clear and actionable

AFTER GENERATING THE PLAN:
Include a "Critical Path Items" section listing blocking tasks.
Include a "Dependencies" section listing prerequisites between phases.

Ready? Please start by asking me your clarifying questions!"""
    
    return prompt


def _parse_markdown_plan(markdown_text: str, project_title: str) -> ProjectPlan:
    """
    Parse markdown-formatted work breakdown into ProjectPlan model
    Handles both structured markdown and plain text formats
    """
    lines = markdown_text.split('\n')
    milestones = []
    current_milestone = None
    current_phase = None
    current_phase_num = 1
    total_duration = None

    for line in lines:
        line = line.strip()

        # Extract total duration from header
        if "duration:" in line.lower() and not total_duration:
            match = re.search(r'duration[:\s]+(\d+\s+\w+)', line, re.IGNORECASE)
            if match:
                total_duration = match.group(1)

        # Phase/Milestone headers - handle multiple formats
        # Format 1: ## Phase X: Title
        # Format 2: ### Milestone X.X: Title
        # Format 3: Plain text "Phase X:" or "Milestone X:"
        is_phase_header = False

        if line.startswith('## ') or line.startswith('### '):
            # Markdown headers
            header_text = line.lstrip('#').strip()
            if 'phase' in header_text.lower() or 'milestone' in header_text.lower():
                is_phase_header = True
                phase_match = re.search(r'(Phase \d+|Milestone \d+\.\d+):\s*(.+)', header_text, re.IGNORECASE)
                if phase_match:
                    current_phase = phase_match.group(1)
                    title = phase_match.group(2).strip()
                else:
                    current_phase = f"Phase {current_phase_num}"
                    title = header_text
                    current_phase_num += 1
        elif re.match(r'^(Phase|Milestone)\s+\d+', line, re.IGNORECASE):
            # Plain text phase headers
            is_phase_header = True
            phase_match = re.search(r'(Phase \d+|Milestone \d+\.\d+)[:\s]+(.+)', line, re.IGNORECASE)
            if phase_match:
                current_phase = phase_match.group(1)
                title = phase_match.group(2).strip()
            else:
                # Just "Phase 1" with no colon
                phase_match = re.match(r'(Phase|Milestone)\s+(\d+)', line, re.IGNORECASE)
                if phase_match:
                    current_phase = f"{phase_match.group(1)} {phase_match.group(2)}"
                    title = line.strip()
                    current_phase_num += 1

        if is_phase_header:
            # Save previous milestone
            if current_milestone:
                milestones.append(current_milestone)

            current_milestone = Milestone(
                title=title,
                phase=current_phase,
                tasks=[]
            )

        # Milestone metadata
        elif line.startswith('**Duration:**') and current_milestone:
            duration = line.replace('**Duration:**', '').strip()
            current_milestone.duration = duration

        elif line.startswith('**Description:**') and current_milestone:
            desc = line.replace('**Description:**', '').strip()
            current_milestone.description = desc

        # Tasks - handle multiple formats
        # Format 1: - [ ] Task name (duration)
        # Format 2: - Task name
        # Format 3: • Task name
        # Format 4: ◦ Task name (sub-bullet)
        # Format 5: Plain text starting with action verb
        elif current_milestone:
            # Checkbox format
            if re.match(r'^-\s*\[[ x]\]\s+', line):
                task_text = re.sub(r'^-\s*\[[ x]\]\s+', '', line)
                # Remove ** markdown bold if present
                task_text = re.sub(r'\*\*(.+?)\*\*', r'\1', task_text)
                duration_match = re.search(r'\(([^)]+)\)$', task_text)
                if duration_match:
                    duration = duration_match.group(1)
                    task_title = task_text[:duration_match.start()].strip()
                else:
                    task_title = task_text.strip()
                    duration = None

                if task_title:
                    current_milestone.tasks.append(Task(
                        title=task_title,
                        duration=duration
                    ))

            # Bullet format (-, •)
            elif re.match(r'^[-•]\s+', line) and not line.startswith('---'):
                task_text = re.sub(r'^[-•]\s+', '', line)
                # Skip if it looks like metadata or dependency
                skip_keywords = ['duration:', 'status:', 'description:', 'depends on', 'requires', 'must complete']
                if not any(x in task_text.lower() for x in skip_keywords):
                    duration_match = re.search(r'\(([^)]+)\)$', task_text)
                    if duration_match:
                        duration = duration_match.group(1)
                        task_title = task_text[:duration_match.start()].strip()
                    else:
                        task_title = task_text.strip()
                        duration = None

                    if task_title and len(task_title) > 5:  # Avoid noise
                        current_milestone.tasks.append(Task(
                            title=task_title,
                            duration=duration
                        ))

    # Add last milestone
    if current_milestone:
        milestones.append(current_milestone)

    return ProjectPlan(
        project_title=project_title,
        total_duration=total_duration,
        milestones=milestones
    )


def _create_simple_plan(charter: CharterData) -> ProjectPlan:
    """Fallback: Create simple plan from charter"""
    return ProjectPlan(
        project_title=charter.project_title,
        total_duration="To be determined",
        milestones=[
            Milestone(
                title="Planning & Preparation",
                phase="Phase 1",
                tasks=[
                    Task(title="Review charter and define scope"),
                    Task(title="Identify key stakeholders"),
                    Task(title="Create initial timeline")
                ]
            ),
            Milestone(
                title="Execution",
                phase="Phase 2",
                tasks=[
                    Task(title="Begin primary work"),
                    Task(title="Regular status updates"),
                    Task(title="Risk monitoring")
                ]
            )
        ]
    )
