"""
Repository Bootstrapper
Creates standardized project structure
"""

import os
import shutil
import subprocess
from pathlib import Path
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
            
            # Copy standard utility scripts from project_template
            RepoBootstrapper._copy_utility_scripts(base_path)
            
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
            
            console.print("[green]✓[/green] Initialized git repository")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]⚠[/yellow] Git initialization failed: {e}")
            return False
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}")
            return False
    
    @staticmethod
    def _copy_utility_scripts(project_path: Path) -> bool:
        """Copy standard utility modules from project_template to new project"""
        try:
            # Find project_template directory
            # Assume it's at C:\Projects\project_template
            template_utils = Path("C:/Projects/project_template/scripts/utils")
            
            if not template_utils.exists():
                console.print(f"[yellow]⚠[/yellow] Template utils not found at {template_utils}, skipping")
                return False
            
            target_utils = project_path / "scripts" / "utils"
            
            # Standard utility files to copy
            utility_files = [
                "__init__.py",
                "config_loader.py",
                "db_utils.py",
                "email_utils.py",
                "log_utils.py",
                "time_utils.py"
            ]
            
            copied_count = 0
            for util_file in utility_files:
                source = template_utils / util_file
                if source.exists():
                    dest = target_utils / util_file
                    shutil.copy2(source, dest)
                    copied_count += 1
            
            if copied_count > 0:
                console.print(f"[green]✓[/green] Copied {copied_count} utility scripts")
                return True
            else:
                console.print("[yellow]⚠[/yellow] No utility scripts found to copy")
                return False
                
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Failed to copy utilities: {e}")
            return False
