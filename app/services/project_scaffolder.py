"""
Project Scaffolder - Creates initial project structure and documents
"""

from datetime import datetime
from pathlib import Path

from jinja2 import Template

from .document_registry import DocumentRegistry


class ProjectScaffolder:
    """Handles creation of project structure and core documents"""

    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates" / "core_docs"

    def scaffold_project(
        self,
        project_path: Path,
        project_name: str,
        project_type: str,
        project_owner: str = "",
        description: str = "",
    ):
        """Create complete project structure with core documents"""
        (project_path / "docs").mkdir(parents=True, exist_ok=True)

        context = {
            "project_name": project_name,
            "project_type": project_type,
            "project_owner": project_owner,
            "description": description if description else f"A {project_type} project",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "year": datetime.now().year,
        }

        doc_registry = DocumentRegistry(project_path)

        core_docs = {
            "README.md": "core",
            "CHANGELOG.md": "core",
            "LICENSE.md": "core",
            "ISSUES.md": "core",
        }

        for doc_name, doc_type in core_docs.items():
            self._create_document_from_template(project_path, doc_name, context)
            doc_registry.register_document(doc_name, doc_type=doc_type, version="0.1.0")

        return doc_registry

    def _create_document_from_template(self, project_path: Path, doc_name: str, context: dict):
        """Create a document from its template"""
        template_file = self.template_dir / f"{doc_name}.j2"

        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_file}")

        template_content = template_file.read_text()
        template = Template(template_content)
        rendered = template.render(**context)

        output_file = project_path / doc_name
        output_file.write_text(rendered)

        return output_file
