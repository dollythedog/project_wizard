#!/usr/bin/env python3
"""
Project Wizard - CLI Entry Point
Interactive project management tool
"""

import click
import os
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from .wizard.phase1_initiation import run_initiation_wizard
from .services.document_generator import DocumentGenerator
from .services.repo_bootstrapper import RepoBootstrapper

console = Console()


@click.group()
@click.version_option(version="0.1.0")
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
        console.print(f"[green]✓[/green] Generated PROJECT_CHARTER.md")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to generate charter: {e}")
        return
    
    # Generate README.md
    readme_path = project_path / "README.md"
    try:
        doc_gen.generate_readme(charter_data, str(readme_path))
        console.print(f"[green]✓[/green] Generated README.md")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to generate README: {e}")
    
    # Save charter data as JSON
    charter_json_path = project_path / "data" / "inbox" / "charter.json"
    try:
        with open(charter_json_path, 'w') as f:
            json.dump(charter_data.model_dump(mode='json'), f, indent=2, default=str)
        console.print(f"[green]✓[/green] Saved charter data")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Failed to save charter JSON: {e}")
    
    # Initialize git
    if not no_git:
        RepoBootstrapper.init_git_repo(
            str(project_path),
            f"feat: Initial {charter_data.project_title} project setup\n\n- Created project charter\n- Generated README\n- Set up standard folder structure"
        )
    
    # Success message
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        f"[bold green]✓ Project '{charter_data.project_title}' created successfully![/bold green]\n\n"
        f"Location: {project_path}\n\n"
        "[bold]Next steps:[/bold]\n"
        f"  1. cd {project_path}\n"
        "  2. Review docs/PROJECT_CHARTER.md\n"
        "  3. Run: project-wizard plan (to create work breakdown)\n"
        "  4. Run: project-wizard sync (to create in OpenProject)",
        border_style="green"
    ))
    console.print("="*60 + "\n")


@cli.command()
def plan():
    """
    Create project plan and work breakdown (Phase 2).
    
    Run this from within a project directory.
    """
    console.print("[yellow]Planning wizard coming soon![/yellow]")
    console.print("This will create PROJECT_PLAN.md and ISSUES.md")


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
