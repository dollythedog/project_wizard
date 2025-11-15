"""AI agent for drafting and enhancing project charter sections."""

import json
import logging
from pathlib import Path

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class CharterAgent:
    """AI agent specialized in drafting and enhancing project charter content."""

    def __init__(self, llm_client: LLMClient | None = None):
        """
        Initialize charter agent.

        Args:
            llm_client: LLMClient instance (creates default if not provided)
        """
        self.llm = llm_client or LLMClient()
        self.prompts_config = self._load_prompts()
        logger.info("CharterAgent initialized with structured prompts")

    def _load_prompts(self) -> dict:
        """Load structured enhancement prompts from config."""
        try:
            config_path = (
                Path(__file__).parent.parent.parent / "configs" / "enhancement_prompts.json"
            )
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load enhancement prompts: {e}, using defaults")
            return {"meta": {}, "business_need": {}}

    def enhance_section(self, section_key: str, user_text: str, feedback: str | None = None) -> str:
        """
        Enhance a charter section using structured prompts.

        Args:
            section_key: The section to enhance (e.g., 'business_need')
            user_text: User's original text
            feedback: Optional specific feedback

        Returns:
            Enhanced section text
        """
        if not user_text or not user_text.strip():
            return user_text

        # Get configuration for this section
        config = self.prompts_config.get(section_key, {})
        meta = self.prompts_config.get("meta", {})

        if not config:
            logger.warning(f"No config for {section_key}, using generic enhancement")
            return self._generic_enhance(user_text)

        # Build system prompt with constraints
        constraints = meta.get("constraints", [])
        forbidden = config.get("forbidden", [])

        system_prompt = f"""You are a {meta.get("role", "professional project manager")}.

Style: {meta.get("style", "clear and professional")}
Max words: {config.get("max_words", 150)}

CRITICAL CONSTRAINTS (you MUST follow these):
{chr(10).join(f"- {c}" for c in constraints)}

FORBIDDEN ACTIONS (you MUST NOT do these):
{chr(10).join(f"- {f}" for f in forbidden)}

Your role is to enhance CLARITY and STRUCTURE, not to add content or data."""

        # Build user prompt with example
        feedback_text = f"\n\nSpecific feedback to address: {feedback}" if feedback else ""

        user_prompt = f"""{config.get("instruction", "Enhance this text.")}

Format: {config.get("format", "clear paragraph")}
Tone: {config.get("tone", "professional")}

Example of good output:
{config.get("example", "N/A")}

User's original text (PRESERVE ALL USER FACTS):
{user_text}{feedback_text}

Task: Enhance for clarity and professional structure ONLY. Do NOT add metrics, numbers, or facts the user did not provide. Output ONLY the enhanced text, nothing else."""

        try:
            enhanced = self.llm.complete(
                system_prompt,
                user_prompt,
                temperature=0.3,  # Conservative
                max_tokens=config.get("max_words", 150) * 2,
            )
            return enhanced.strip()
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            return user_text

    def _generic_enhance(self, text: str) -> str:
        """Fallback generic enhancement."""
        system_prompt = """You are a professional project manager.
Enhance text for clarity and structure ONLY.
Do NOT add facts, metrics, or data the user didn't provide."""

        user_prompt = f"""Enhance this for professional clarity:

{text}

Output only the enhanced text."""

        return self.llm.complete(system_prompt, user_prompt, temperature=0.3)

    def enhance_large_document(self, text: str, feedback: str, chunk_size: int = 1000) -> str:
        """
        Enhance a large document by processing it in chunks while preserving markdown structure.

        Args:
            text: Full document text
            feedback: Enhancement instructions
            chunk_size: Characters per chunk (approximate)

        Returns:
            Enhanced full document with preserved formatting
        """
        if len(text) <= chunk_size:
            return self._generic_enhance(text)

        # Split into paragraphs
        paragraphs = text.split("\n\n")

        # Group paragraphs into chunks
        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para)
            if current_size + para_size > chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        # Enhance each chunk
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            system_prompt = f"""You are a professional editor enhancing part {i + 1} of {len(chunks)} of a markdown document.

{feedback}

CRITICAL REQUIREMENTS:
1. Preserve ALL markdown formatting (headers #, lists -, bullets *, bold **, etc.)
2. Preserve ALL section structure and hierarchy
3. Do NOT remove or change any headers
4. Do NOT change list formatting or numbering
5. ONLY improve the wording within the existing structure
6. Output ONLY the enhanced markdown text with no explanations or meta-commentary"""

            user_prompt = f"""Enhance the text content while preserving ALL markdown structure:

{chunk}

Remember: Keep exact same headers, lists, and formatting. Only improve the prose."""

            try:
                enhanced = self.llm.complete(system_prompt, user_prompt, temperature=0.2)
                enhanced_chunks.append(enhanced.strip())
            except Exception as e:
                logger.error(f"Enhancement failed for chunk {i + 1}: {e}")
                enhanced_chunks.append(chunk)  # Use original on error

        return "\n\n".join(enhanced_chunks)

    # Legacy methods for backward compatibility
    def draft_business_need(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_success_criteria(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_proposed_solution(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_risks_and_mitigation(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_scope(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_deliverables(self, project_brief: str, context: dict = None) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)

    def draft_schedule_overview(
        self, project_brief: str, duration_days: int = None, context: dict = None
    ) -> str:
        """Legacy method - kept for compatibility."""
        return self._generic_enhance(project_brief)
