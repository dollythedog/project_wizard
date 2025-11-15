"""
Project Registry - Manages project metadata and tracking
"""

import json
from datetime import datetime
from pathlib import Path


class ProjectRegistry:
    """Manages project registration and metadata"""

    def __init__(self, registry_file: Path | None = None):
        if registry_file is None:
            registry_file = Path.home() / ".project_wizard_projects.json"
        self.registry_file = registry_file
        self._load_registry()

    def _load_registry(self):
        """Load registry from disk"""
        if self.registry_file.exists():
            try:
                self.projects = json.loads(self.registry_file.read_text())
            except:
                self.projects = {}
        else:
            self.projects = {}

    def _save_registry(self):
        """Save registry to disk"""
        self.registry_file.write_text(json.dumps(self.projects, indent=2))

    def register_project(
        self,
        project_path: Path,
        name: str,
        description: str = "",
        project_type: str = "Software Development",
        icon: str = "📁",
        project_owner: str = "",
    ) -> dict:
        """Register a new project"""
        project_id = str(project_path)

        project_data = {
            "name": name,
            "path": str(project_path),
            "description": description,
            "project_type": project_type,
            "project_owner": project_owner,
            "icon": icon,
            "version": "0.1.0",
            "charter_created": False,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
        }

        self.projects[project_id] = project_data
        self._save_registry()

        return project_data

    def update_project(self, project_path: Path, **kwargs):
        """Update project metadata"""
        project_id = str(project_path)

        if project_id in self.projects:
            self.projects[project_id].update(kwargs)
            self.projects[project_id]["last_modified"] = datetime.now().isoformat()
            self._save_registry()

    def mark_charter_complete(self, project_path: Path):
        """Mark charter as created for this project"""
        self.update_project(project_path, charter_created=True)

    def is_charter_complete(self, project_path: Path) -> bool:
        """Check if charter has been created"""
        project = self.get_project(project_path)
        if project:
            return project.get("charter_created", False)
        return False

    def touch_project(self, project_path: Path):
        """Update last accessed time"""
        project_id = str(project_path)

        if project_id in self.projects:
            self.projects[project_id]["last_accessed"] = datetime.now().isoformat()
            self._save_registry()

    def get_project(self, project_path: Path) -> dict | None:
        """Get project metadata"""
        project_id = str(project_path)
        return self.projects.get(project_id)

    def list_projects(self, sort_by: str = "last_accessed") -> list[dict]:
        """List all projects sorted by specified field"""
        projects_list = list(self.projects.values())

        if sort_by == "last_accessed":
            projects_list.sort(key=lambda x: x.get("last_accessed", ""), reverse=True)
        elif sort_by == "created_date":
            projects_list.sort(key=lambda x: x.get("created_date", ""), reverse=True)
        elif sort_by == "name":
            projects_list.sort(key=lambda x: x.get("name", "").lower())

        return projects_list

    def remove_project(self, project_path: Path):
        """Remove project from registry (doesn't delete files)"""
        project_id = str(project_path)

        if project_id in self.projects:
            del self.projects[project_id]
            self._save_registry()

    def project_exists(self, project_path: Path) -> bool:
        """Check if project is registered"""
        project_id = str(project_path)
        return project_id in self.projects
