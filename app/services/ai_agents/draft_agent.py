"""
Draft Agent
First stage: Generate initial document from user inputs and pattern
"""

import logging

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class DraftAgent:
    """
    Generates first draft of documents based on patterns and user inputs.
    Follows Unix philosophy: does ONE thing well - creates initial content.
    """

    def __init__(self, llm_client: LLMClient = None):
        """Initialize with LLM client"""
        self.llm = llm_client or LLMClient()

    def generate_draft(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.3, max_tokens: int = 2000
    ) -> str:
        """
        Generate initial draft from prompts

        Args:
            system_prompt: Pattern's system.md content (AI instructions)
            user_prompt: Rendered user.md with variables and context
            temperature: LLM temperature (lower = more deterministic)
            max_tokens: Maximum response length

        Returns:
            Draft document content
        """
        logger.info("DraftAgent: Generating initial draft")

        try:
            draft = self.llm.complete(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if not draft or not draft.strip():
                logger.error("DraftAgent: Received empty draft from LLM")
                return "[ERROR: Empty response from AI]"

            logger.info(f"DraftAgent: Generated draft ({len(draft)} chars)")
            return draft.strip()

        except Exception as e:
            logger.error(f"DraftAgent: Draft generation failed: {e}")
            return f"[ERROR: Draft generation failed - {str(e)}]"

    def generate_with_context(
        self,
        system_prompt: str,
        user_inputs: dict[str, str],
        project_context: dict[str, str],
        user_template_renderer,
        **llm_kwargs,
    ) -> str:
        """
        Convenience method: render user prompt with context and generate draft

        Args:
            system_prompt: System instructions
            user_inputs: User-provided variables
            project_context: Project documentation context
            user_template_renderer: Callable that renders user.md template
            **llm_kwargs: Additional LLM parameters

        Returns:
            Draft document
        """
        # Merge user inputs with project context
        all_variables = {**user_inputs, **project_context}

        # Render user prompt
        user_prompt = user_template_renderer(**all_variables)

        # Generate draft
        return self.generate_draft(
            system_prompt=system_prompt, user_prompt=user_prompt, **llm_kwargs
        )
