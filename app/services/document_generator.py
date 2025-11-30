"""
Document Generation Service
Uses Jinja2 templates to generate project documentation
"""

from pathlib import Path
from typing import Optional, Dict

from jinja2 import Environment, FileSystemLoader

from ..models.charter import CharterData
from .blueprint_registry import get_registry


class DocumentGenerator:
    """Generates project documents from templates"""

    def __init__(self, template_dir: Optional[str] = None, use_blueprints: bool = False):
        if template_dir is None:
            # Default to app/templates/documents
            base_dir = Path(__file__).parent.parent
            template_dir = base_dir / "templates" / "documents"

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        # New: support blueprint-based generation
        self.use_blueprints = use_blueprints
        self._blueprint_registry = None

    @property
    def blueprint_registry(self):
        """Lazy-load the blueprint registry."""
        if self._blueprint_registry is None:
            self._blueprint_registry = get_registry()
        return self._blueprint_registry

    def generate_from_blueprint(
        self,
        blueprint_name: str,
        context: Dict[str, any],
        output_path: Optional[str] = None
    ) -> str:
        """Generate a document from a blueprint-defined template."""
        # Ensure blueprint exists and is valid
        self.blueprint_registry.load_blueprint(blueprint_name)
        template_path = self.blueprint_registry.get_template_path(blueprint_name)

        env = Environment(
            loader=FileSystemLoader(str(template_path.parent)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template(template_path.name)
        content = template.render(**context)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return content

    def generate_charter(self, charter_data: CharterData, output_path: Optional[str] = None) -> str:
        """Generate PROJECT_CHARTER.md from template (legacy or blueprint)."""
        if self.use_blueprints:
            return self.generate_from_blueprint(
                "project_charter",
                charter_data.model_dump(),
                output_path,
            )
        # Legacy path
        template = self.env.get_template("PROJECT_CHARTER.md.j2")
        content = template.render(charter_data.model_dump())
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return content

    def generate_project_plan(self, project_plan, charter, output_path: Optional[str] = None) -> str:
        """Generate PROJECT_PLAN.md from template (legacy or blueprint)."""
        # Calculate total tasks
        total_tasks = sum(len(m.tasks) for m in project_plan.milestones)
        context = {
            "project_title": project_plan.project_title,
            "created_date": project_plan.created_date,
            "total_duration": project_plan.total_duration,
            "charter_goal": charter.project_goal,
            "charter_solution": charter.proposed_solution,
            "milestones": project_plan.milestones,
            "total_tasks": total_tasks,
        }
        if self.use_blueprints:
            return self.generate_from_blueprint("work_plan", context, output_path)
        # Legacy path
        template = self.env.get_template("PROJECT_PLAN.md.j2")
        content = template.render(**context)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return content

    def generate_issues(self, project_plan, output_path: str = None) -> str:
        """Generate ISSUES.md from template"""
        template = self.env.get_template("ISSUES.md.j2")

        # Calculate metrics
        total_tasks = sum(len(m.tasks) for m in project_plan.milestones)
        completed_tasks = sum(1 for m in project_plan.milestones for t in m.tasks if t.completed)
        progress = int((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)

        content = template.render(
            project_title=project_plan.project_title,
            created_date=project_plan.created_date,
            milestones=project_plan.milestones,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            progress=progress
        )

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_readme(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate README.md from template"""
        # For now, simple template
        content = f"""# {charter_data.project_title}

## Overview

{charter_data.project_goal}

**Project Type:** {charter_data.project_type}
**Status:** Initiating

## Problem Statement

{charter_data.problem_definition}

## Proposed Solution

{charter_data.proposed_solution}

## Success Criteria

{charter_data.success_criteria}

## Project Timeline

{charter_data.schedule_overview}

## Documentation

- [PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) - Detailed project charter
- [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) - Work breakdown and schedule (run `project-wizard plan`)
- [ISSUES.md](docs/ISSUES.md) - Task tracking and status
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history and changes
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Code of conduct

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for setup instructions.

---

*Generated by Project Wizard*
"""

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_contributing(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate CONTRIBUTING.md from template"""
        template = self.env.get_template("CONTRIBUTING.md.j2")
        content = template.render(charter_data.model_dump())

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_code_of_conduct(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate CODE_OF_CONDUCT.md from template"""
        template = self.env.get_template("CODE_OF_CONDUCT.md.j2")

        # Add contact_email if available
        data = charter_data.model_dump()
        data['contact_email'] = f"{charter_data.project_sponsor}@example.com"  # Placeholder

        content = template.render(data)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_license(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate LICENSE.md from template"""
        template = self.env.get_template("LICENSE.md.j2")
        content = template.render(charter_data.model_dump())

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_changelog(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate CHANGELOG.md from template"""
        template = self.env.get_template("CHANGELOG.md.j2")
        content = template.render(charter_data.model_dump())

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_quickstart(self, charter_data: CharterData, output_path: str = None) -> str:
        """Generate QUICKSTART.md from template"""
        template = self.env.get_template("QUICKSTART.md.j2")
        content = template.render(charter_data.model_dump())

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content
