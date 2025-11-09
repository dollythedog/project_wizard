"""
Project Registry - Manages project metadata and tracking
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ProjectRegistry:
    """Manages project registration and metadata"""
    
    def __init__(self, registry_file: Optional[Path] = None):
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
        icon: str = "📁"
    ) -> Dict:
        """Register a new project"""
        project_id = str(project_path)
        
        project_data = {
            "name": name,
            "path": str(project_path),
            "description": description,
            "project_type": project_type,
            "icon": icon,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
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
    
    def touch_project(self, project_path: Path):
        """Update last accessed time"""
        project_id = str(project_path)
        
        if project_id in self.projects:
            self.projects[project_id]["last_accessed"] = datetime.now().isoformat()
            self._save_registry()
    
    def get_project(self, project_path: Path) -> Optional[Dict]:
        """Get project metadata"""
        project_id = str(project_path)
        return self.projects.get(project_id)
    
    def list_projects(self, sort_by: str = "last_accessed") -> List[Dict]:
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
