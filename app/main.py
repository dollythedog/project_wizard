#!/usr/bin/env python3
"""
Project Wizard - CLI Entry Point
Interactive project management tool
"""

import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from .models.charter import CharterData
from .services.document_generator import DocumentGenerator
from .services.phase_manager import PhaseManager
from .services.phase_navigator import display_quest_map
from .services.repo_bootstrapper import RepoBootstrapper
from .wizard.phase1_initiation import run_initiation_wizard
from .wizard.phase2_planning import run_planning_wizard

console = Console()


@click.group()
@click.version_option(version="0.4.1")
def cli():
    """
    Project Wizard - Your personal project management automation tool
    Guides you through creating projects following formal PM methodology.
    """
    pass


@cli.command()
@click.argument('project_name', required=False)
@click.option('--type', '-t', 'project_type',
              type=click.Choice(['software_mvp', 'clinical_workflow', 'infrastructure', 'landscaping', 'research_analysis', 'other']),
              help='Project type')
@click.option('--path', '-p', default=None, help='Project directory path')
@click.option('--no-git', is_flag=True, help='Skip git initialization')
def init(project_name, project_type, path, no_git):
    """
    Initialize a new project with charter creation wizard.
    Example:
        project-wizard init "My New Project"
        project-wizard init --type software_mvp
    """
    console.print(Panel.fit(
        "[bold cyan]🚀 Project Wizard[/bold cyan]\n\n"
        "Let's create a new project following your proven methodology!",
        border_style="cyan"
    ))
    # Run the charter wizard
    try:
        charter_data = run_initiation_wizard(project_type=project_type)
    except KeyboardInterrupt:
        console.print("\n[yellow]Wizard cancelled by user[/yellow]")
        return
    except Exception as e:
        console.print(f"\n[red]Error in wizard: {e}[/red]")
        return
    # Determine project path
    if not path:
        # Create in current directory or ~/projects
        projects_dir = Path.home() / "projects"
        projects_dir.mkdir(exist_ok=True)
        # Sanitize project name for directory
        dir_name = charter_data.project_title.lower().replace(" ", "-").replace("&", "and")
        dir_name = "".join(c for c in dir_name if c.isalnum() or c in ['-', '_'])
        project_path = projects_dir / dir_name
    else:
        project_path = Path(path)
    console.print(f"\n[bold]Creating project at:[/bold] {project_path}\n")
    # Create project structure
    if not RepoBootstrapper.create_project_structure(str(project_path), charter_data.project_title):
        console.print("[red]Failed to create project structure[/red]")
        return
    # Generate documents
    doc_gen = DocumentGenerator()
    # Generate PROJECT_CHARTER.md
    charter_path = project_path / "docs" / "PROJECT_CHARTER.md"
    try:
        doc_gen.generate_charter(charter_data, str(charter_path))
        console.print("[green]✓[/green] Generated PROJECT_CHARTER.md")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to generate charter: {e}")
        return
    # Generate README.md
    readme_path = project_path / "README.md"
    try:
        doc_gen.generate_readme(charter_data, str(readme_path))
        console.print("[green]✓[/green] Generated README.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate README: {e}")
    # Generate CONTRIBUTING.md
    contributing_path = project_path / "CONTRIBUTING.md"
    try:
        doc_gen.generate_contributing(charter_data, str(contributing_path))
        console.print("[green]✓[/green] Generated CONTRIBUTING.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate CONTRIBUTING: {e}")
    # Generate CODE_OF_CONDUCT.md
    coc_path = project_path / "CODE_OF_CONDUCT.md"
    try:
        doc_gen.generate_code_of_conduct(charter_data, str(coc_path))
        console.print("[green]✓[/green] Generated CODE_OF_CONDUCT.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate CODE_OF_CONDUCT: {e}")
    # Generate LICENSE.md
    license_path = project_path / "LICENSE.md"
    try:
        doc_gen.generate_license(charter_data, str(license_path))
        console.print("[green]✓[/green] Generated LICENSE.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate LICENSE: {e}")
    # Generate CHANGELOG.md
    changelog_path = project_path / "docs" / "CHANGELOG.md"
    try:
        doc_gen.generate_changelog(charter_data, str(changelog_path))
        console.print("[green]✓[/green] Generated CHANGELOG.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate CHANGELOG: {e}")
    # Generate QUICKSTART.md
    quickstart_path = project_path / "QUICKSTART.md"
    try:
        doc_gen.generate_quickstart(charter_data, str(quickstart_path))
        console.print("[green]✓[/green] Generated QUICKSTART.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate QUICKSTART: {e}")
    # Save charter data as JSON
    charter_json_path = project_path / "data" / "inbox" / "charter.json"
    try:
        with open(charter_json_path, 'w', encoding='utf-8') as f:
            json.dump(charter_data.model_dump(mode='json'), f, indent=2, default=str)
        console.print("[green]✓[/green] Saved charter data")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to save charter JSON: {e}")
    # Initialize phase state
    phase_manager = PhaseManager(project_path)
    phase_state = phase_manager.init_state(charter_data)
    phase_manager.save_state(phase_state)
    console.print("[green]✓[/green] Initialized project phase tracking")
    # Initialize git
    if not no_git:
        RepoBootstrapper.init_git_repo(
            str(project_path),
            f"feat: Initial {charter_data.project_title} project setup\n\n- Created project charter\n- Generated README\n- Set up standard folder structure"
        )
    # Show quest map
    console.print("\n")
    display_quest_map(phase_state, detailed=False)
    # Success message
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        f"[bold green]✓ Project '{charter_data.project_title}' created successfully![/bold green]\n\n"
        f"Location: {project_path}\n\n"
        "[bold]Next steps:[/bold]\n"
        f"  1. cd {project_path}\n"
        "  2. Review docs/PROJECT_CHARTER.md\n"
        "  3. Run: project-wizard plan (to create work breakdown)\n"
        "  4. Run: project-wizard status (to see your quest map)",
        border_style="green"
    ))
    console.print("="*60 + "\n")


@cli.command()
def plan():
    """
    Create project plan and work breakdown (Phase 2).
    Run this from within a project directory.
    """
    # Find charter.json in current directory
    charter_path = Path.cwd() / "data" / "inbox" / "charter.json"
    if not charter_path.exists():
        console.print("[red]Error:[/red] charter.json not found")
        console.print("Make sure you're in a project directory created with 'project-wizard init'")
        console.print(f"\nLooked in: {charter_path}")
        return
    # Load charter
    try:
        with open(charter_path, encoding='utf-8') as f:
            charter_dict = json.load(f)
            charter = CharterData(**charter_dict)
    except Exception as e:
        console.print(f"[red]Error loading charter:[/red] {e}")
        return
    console.print(f"[bold]Loaded charter for:[/bold] {charter.project_title}\n")
    # Load phase state
    phase_manager = PhaseManager()
    phase_state = phase_manager.load_state()
    if not phase_state:
        console.print("[yellow]Warning:[/yellow] Phase state not found, initializing...")
        phase_state = phase_manager.init_state(charter)
        phase_manager.save_state(phase_state)
    # Run planning wizard
    try:
        project_plan = run_planning_wizard(charter)
    except KeyboardInterrupt:
        console.print("\n[yellow]Planning cancelled by user[/yellow]")
        return
    except Exception as e:
        console.print(f"\n[red]Error in planning wizard: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    if not project_plan:
        console.print("[yellow]Planning cancelled[/yellow]")
        return
    # Save plan as JSON
    plan_json_path = Path.cwd() / "data" / "inbox" / "plan.json"
    try:
        with open(plan_json_path, 'w', encoding='utf-8') as f:
            json.dump(project_plan.model_dump(mode='json'), f, indent=2, default=str)
        console.print(f"\n[green]✓[/green] Saved plan data to {plan_json_path.name}")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to save plan JSON: {e}")
    # Generate documents
    doc_gen = DocumentGenerator()
    # Generate PROJECT_PLAN.md
    plan_md_path = Path.cwd() / "docs" / "PROJECT_PLAN.md"
    try:
        doc_gen.generate_project_plan(project_plan, charter, str(plan_md_path))
        console.print("[green]✓[/green] Generated PROJECT_PLAN.md")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to generate PROJECT_PLAN.md: {e}")
        import traceback
        traceback.print_exc()
    # Generate ISSUES.md
    issues_md_path = Path.cwd() / "docs" / "ISSUES.md"
    try:
        doc_gen.generate_issues(project_plan, str(issues_md_path))
        console.print("[green]✓[/green] Generated ISSUES.md")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to generate ISSUES.md: {e}")
    # Update phase state - complete planning and approve RfE gate
    phase_manager.complete_planning(phase_state)
    phase_manager.save_state(phase_state)
    # Show updated quest map
    console.print("\n")
    display_quest_map(phase_state, detailed=False)
    # Success
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        "[bold green]✓ Project plan created![/bold green]\n\n"
        "[bold]Generated files:[/bold]\n"
        "  • docs/PROJECT_PLAN.md - Detailed work breakdown\n"
        "  • docs/ISSUES.md - Task tracking\n"
        "  • data/inbox/plan.json - Plan data\n\n"
        "[bold]Next steps:[/bold]\n"
        "  1. Review docs/PROJECT_PLAN.md\n"
        "  2. Adjust tasks in docs/ISSUES.md\n"
        "  3. Run: project-wizard sync (to create in OpenProject)",
        border_style="green"
    ))
    console.print("="*60 + "\n")


@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed phase information')
def status(detailed):
    """
    Show project quest map and phase status.
    Displays your current position in the project journey.
    """
    # Load phase state
    phase_manager = PhaseManager()
    phase_state = phase_manager.load_state()
    if not phase_state:
        console.print("[red]Error:[/red] No project found in current directory")
        console.print("Make sure you're in a project directory created with 'project-wizard init'")
        return
    # Display quest map
    display_quest_map(phase_state, detailed=detailed)


@cli.command()
def sync():
    """
    Sync project to OpenProject.
    Creates project and work packages in OpenProject.
    """
    console.print("[yellow]OpenProject sync coming soon![/yellow]")
    console.print("This will create the project in OpenProject")


if __name__ == '__main__':
    cli()
