"""
Project Context Service
Loads and provides access to core project documentation
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ProjectContext:
    """Loads project documentation for context injection into AI agents"""

    def __init__(self, project_path: Path):
        """
        Initialize with project root directory

        Args:
            project_path: Path to project root (contains PROJECT_CHARTER.md, README.md, etc.)
        """
        self.project_path = Path(project_path)
        self._cache = {}

    def load_context(self, include_docs: list[str] = None) -> dict[str, str]:
        """
        Load project documentation files

        Args:
            include_docs: List of docs to include. Options:
                - 'charter' (PROJECT_CHARTER.md)
                - 'readme' (README.md)
                - 'issues' (ISSUES.md)
                - 'changelog' (CHANGELOG.md)
                If None, loads all available

        Returns:
            Dictionary with document contents
        """
        if include_docs is None:
            include_docs = ["charter", "readme", "issues", "changelog"]

        context = {}

        doc_mapping = {
            "charter": "PROJECT_CHARTER.md",
            "readme": "README.md",
            "issues": "ISSUES.md",
            "changelog": "CHANGELOG.md",
        }

        for doc_key in include_docs:
            filename = doc_mapping.get(doc_key)
            if not filename:
                logger.warning(f"Unknown document type: {doc_key}")
                continue

            content = self._load_file(filename)
            context[f"project_{doc_key}"] = content or f"[{filename} not found or empty]"

        return context

    def _load_file(self, filename: str) -> str | None:
        """Load a single file from project directory"""
        # Check cache first
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.project_path / filename

        if not file_path.exists():
            logger.info(f"File not found: {file_path}")
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            self._cache[filename] = content
            return content
        except Exception as e:
            logger.error(f"Failed to read {filename}: {e}")
            return None

    def get_project_name(self) -> str:
        """Extract project name from README or directory name"""
        readme = self._load_file("README.md")
        if readme:
            # Try to extract from first H1 header
            lines = readme.split("\n")
            for line in lines:
                if line.startswith("# "):
                    return line[2:].strip()

        # Fallback to directory name
        return self.project_path.name

    def get_summary(self) -> dict[str, str]:
        """Get quick summary of project from docs"""
        return {
            "project_name": self.get_project_name(),
            "has_charter": (self.project_path / "PROJECT_CHARTER.md").exists(),
            "has_readme": (self.project_path / "README.md").exists(),
            "has_issues": (self.project_path / "ISSUES.md").exists(),
            "has_changelog": (self.project_path / "CHANGELOG.md").exists(),
        }

    def clear_cache(self):
        """Clear cached file contents"""
        self._cache = {}
