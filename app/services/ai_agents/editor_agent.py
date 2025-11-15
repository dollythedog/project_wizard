"""
Editor Agent
Second stage: Polish and refine draft without adding fabricated content
"""

import logging

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class EditorAgent:
    """
    Edits and polishes drafts for clarity, grammar, and professional tone.
    Does NOT add content - only improves structure and readability.
    """

    SYSTEM_PROMPT = """# IDENTITY and PURPOSE

You are a professional technical editor specializing in project management and LEAN documentation. Your role is to improve clarity, grammar, and structure WITHOUT adding fabricated information.

# CONSTRAINTS (CRITICAL)

- NEVER add metrics, numbers, or data not in the original text
- NEVER invent stakeholder names, quotes, or details
- NEVER add timeline specifics or performance baselines
- ONLY improve: sentence structure, grammar, clarity, professional tone, organization
- Preserve ALL facts exactly as stated

# EDITING GUIDELINES

1. **Clarity**: Simplify complex sentences, remove ambiguity
2. **Grammar**: Fix errors, improve punctuation and flow
3. **Structure**: Organize content logically with clear headers
4. **Tone**: Maintain formal but accessible professional tone
5. **Conciseness**: Remove redundancy without losing meaning
6. **Formatting**: Use markdown effectively (bullets, bold, tables where appropriate)

# WHAT TO PRESERVE

- All specific facts, numbers, names, dates from original
- Original intent and meaning
- Technical terminology (when appropriate)
- All user-provided data points

# OUTPUT

Return the edited document maintaining the original markdown structure. If the draft is already good, minimal changes are acceptable."""

    def __init__(self, llm_client: LLMClient = None):
        """Initialize with LLM client"""
        self.llm = llm_client or LLMClient()

    def edit_draft(
        self, draft: str, specific_guidance: str = None, temperature: float = 0.2
    ) -> str:
        """
        Edit and polish draft

        Args:
            draft: Original draft to edit
            specific_guidance: Optional specific editing instructions
            temperature: LLM temperature (lower for editing consistency)

        Returns:
            Edited document
        """
        logger.info("EditorAgent: Polishing draft")

        if not draft or draft.startswith("[ERROR"):
            logger.warning("EditorAgent: Received error draft, returning as-is")
            return draft

        user_prompt = f"""# DOCUMENT TO EDIT

{draft}

# TASK

Edit the above document for clarity, grammar, and professional tone. Follow all constraints - do NOT add fabricated information.
"""

        if specific_guidance:
            user_prompt += f"\n# SPECIFIC GUIDANCE\n\n{specific_guidance}\n"

        try:
            edited = self.llm.complete(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=len(draft) + 500,  # Allow slightly more for reformatting
            )

            if not edited or not edited.strip():
                logger.warning("EditorAgent: Empty response, returning original draft")
                return draft

            logger.info(f"EditorAgent: Edited draft ({len(draft)} → {len(edited)} chars)")
            return edited.strip()

        except Exception as e:
            logger.error(f"EditorAgent: Editing failed: {e}")
            logger.info("EditorAgent: Returning original draft due to error")
            return draft  # Return original on error

    def suggest_improvements(self, draft: str) -> dict:
        """
        Analyze draft and suggest specific improvements (without editing)

        Returns:
            Dict with 'suggestions': list of improvement ideas
        """
        user_prompt = f"""Analyze this document and list 3-5 specific improvements that would enhance clarity or professionalism, WITHOUT adding fabricated data.

Document:
{draft}

Return a JSON object with format:
{{
  "suggestions": [
    "Improvement 1",
    "Improvement 2",
    ...
  ]
}}"""

        try:
            response = self.llm.complete(
                system_prompt="You are a document analysis expert. Provide constructive feedback.",
                user_prompt=user_prompt,
                temperature=0.3,
                max_tokens=500,
            )

            # Try to parse JSON
            import json

            # Extract JSON if wrapped in code blocks
            if "```" in response:
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]

            return json.loads(response.strip())

        except Exception as e:
            logger.error(f"EditorAgent: Suggestion generation failed: {e}")
            return {"suggestions": ["Error generating suggestions"]}
