"""
Repository Bootstrapper
Creates standardized project structure
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()


class RepoBootstrapper:
    """Creates and initializes project repository structure"""
    
    @staticmethod
    def create_project_structure(project_path: str, project_name: str) -> bool:
        """
        Create standardized folder structure based on user's template
        """
        try:
            base_path = Path(project_path)
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Standard folder structure
            folders = [
                "configs",
                "data/inbox",
                "data/staging",
                "data/archive",
                "scripts/utils",
                "docs",
                ".github/workflows"
            ]
            
            for folder in folders:
                (base_path / folder).mkdir(parents=True, exist_ok=True)
            
            # Create .gitkeep files
            (base_path / "data" / "staging" / ".gitkeep").touch()
            (base_path / "data" / "archive" / ".gitkeep").touch()
            
            # Create .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Credentials
configs/*.env
!configs/*.env.example
*.key
*.pem

# Data
data/staging/*
!data/staging/.gitkeep
data/archive/*
!data/archive/.gitkeep

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# IDEs
.vscode/
.idea/
"""
            (base_path / ".gitignore").write_text(gitignore_content)
            
            console.print(f"[green]✓[/green] Created project structure at {base_path}")
            return True
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to create structure: {e}")
            return False
    
    @staticmethod
    def init_git_repo(project_path: str, initial_message: str = None) -> bool:
        """Initialize git repository"""
        try:
            os.chdir(project_path)
            
            # Init git
            subprocess.run(["git", "init"], check=True, capture_output=True)
            
            # Initial commit
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            commit_msg = initial_message or "feat: Initial project setup with charter"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                check=True,
                capture_output=True
            )
            
            console.print(f"[green]✓[/green] Initialized git repository")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]⚠[/yellow] Git initialization failed: {e}")
            return False
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}")
            return False
