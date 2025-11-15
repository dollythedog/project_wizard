"""Utility functions for document processing and cleanup."""


def clean_markdown_output(content: str) -> str:
    """
    Remove markdown code fence wrappers that may accidentally be added by LLM.

    Strips:
    - Opening ``` with optional language specifier (```markdown, ```python, etc.)
    - Closing ```

    But preserves fences that are legitimately part of the document content.

    Args:
        content: Raw content that may have fence wrappers

    Returns:
        Cleaned content with outer fences removed if present
    """
    # Only strip if the ENTIRE document is wrapped in fences
    content = content.strip()

    # Check if document starts and ends with triple backticks
    if content.startswith("```") and content.endswith("```"):
        lines = content.split("\n")

        # Remove first line (opening fence with optional language specifier)
        if lines[0].startswith("```"):
            lines = lines[1:]

        # Remove last line (closing fence)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    return content
