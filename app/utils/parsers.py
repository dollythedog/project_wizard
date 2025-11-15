"""
Utility functions for parsing and loading project documents.
"""

from pathlib import Path


def load_project_charter(project_path: Path) -> str | None:
    """
    Load existing charter from project directory.

    Args:
        project_path: Path to the project directory

    Returns:
        Charter text if file exists, None otherwise
    """
    charter_file = project_path / "PROJECT_CHARTER.md"
    if charter_file.exists():
        return charter_file.read_text()
    return None


def parse_charter_to_form_data(charter_text: str) -> dict:
    """
    Extract form data from existing charter text.

    Parses a PROJECT_CHARTER.md file and extracts key-value pairs
    for form fields based on markdown structure.

    Args:
        charter_text: Raw charter markdown text

    Returns:
        Dictionary mapping field names to their values
    """
    data = {}
    lines = charter_text.split("\n")

    # Simple parsing - look for headers and content
    current_section = None
    content_buffer = []

    for line in lines:
        if line.startswith("# Project Charter:"):
            data["project_title"] = line.replace("# Project Charter:", "").strip()
        elif line.startswith("**Project Owner:**"):
            data["project_owner"] = line.replace("**Project Owner:**", "").strip()
        elif line.startswith("**Project Type:**"):
            data["project_type"] = line.replace("**Project Type:**", "").strip()
        elif line.startswith("## "):
            # Save previous section
            if current_section and content_buffer:
                data[current_section] = "\n".join(content_buffer).strip()
            # Start new section
            section_name = line.replace("##", "").strip().lower().replace(" ", "_")
            current_section = section_name
            content_buffer = []
        elif current_section and line.strip():
            content_buffer.append(line)

    # Save last section
    if current_section and content_buffer:
        data[current_section] = "\n".join(content_buffer).strip()

    return data
