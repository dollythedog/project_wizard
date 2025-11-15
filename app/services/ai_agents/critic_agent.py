"""AI agent for critiquing and improving project charters."""

import json
import logging
import re

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class CriticAgent:
    """AI agent specialized in reviewing and critiquing project charters."""

    SYSTEM_PROMPT = """You are a senior project management consultant specializing in quality assurance for project charters.

Your role is to:
- Evaluate charters against best practices
- Identify gaps, weaknesses, and missing elements
- Provide specific, actionable feedback
- Score sections objectively

Be constructive but rigorous. Flag issues that could lead to project failure.

CRITICAL: You must respond with valid JSON only. No markdown, no code blocks, no extra text."""

    def __init__(self, llm_client: LLMClient | None = None):
        """
        Initialize critic agent.

        Args:
            llm_client: LLMClient instance (creates default if not provided)
        """
        self.llm = llm_client or LLMClient()
        logger.info("CriticAgent initialized")

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from text that might contain markdown or other wrapping."""
        # Remove markdown code blocks
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)

        # Try to find JSON object
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # If that fails, try the whole text
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response text: {text[:500]}")
            raise

    def critique_charter(self, charter_text: str, rubric: dict | None = None) -> dict:
        """
        Provide comprehensive critique of a charter.

        Args:
            charter_text: Full charter text
            rubric: Scoring rubric (criteria and weights)

        Returns:
            Dict with scores, feedback, and approval status
        """
        default_rubric = {
            "criteria": [
                {"name": "Clarity of Goal", "weight": 0.20},
                {"name": "Scope & Deliverables", "weight": 0.20},
                {"name": "Risks & Mitigations", "weight": 0.15},
                {"name": "Success Criteria", "weight": 0.15},
                {"name": "Strategic Alignment", "weight": 0.15},
                {"name": "Stakeholders & Resources", "weight": 0.15},
            ],
            "threshold": 0.75,
        }

        rubric = rubric or default_rubric

        prompt = f"""Evaluate this project charter against the following criteria:

{self._format_rubric(rubric)}

CHARTER TO EVALUATE:
{charter_text}

For each criterion, provide:
1. Score (0-100)
2. Strengths (brief, 1-2 sentences)
3. Weaknesses (brief, 1-2 sentences)
4. Improvements (specific actions, 1-2 sentences)

Respond with ONLY valid JSON in this exact format (no markdown, no code blocks):
{{
  "scores": [
    {{"criterion": "Clarity of Goal", "score": 85, "strengths": "Clear goal statement", "weaknesses": "Could be more measurable", "improvements": "Add specific metrics"}},
    {{"criterion": "Scope & Deliverables", "score": 80, "strengths": "...", "weaknesses": "...", "improvements": "..."}},
    {{"criterion": "Risks & Mitigations", "score": 75, "strengths": "...", "weaknesses": "...", "improvements": "..."}},
    {{"criterion": "Success Criteria", "score": 85, "strengths": "...", "weaknesses": "...", "improvements": "..."}},
    {{"criterion": "Strategic Alignment", "score": 80, "strengths": "...", "weaknesses": "...", "improvements": "..."}},
    {{"criterion": "Stakeholders & Resources", "score": 75, "strengths": "...", "weaknesses": "...", "improvements": "..."}}
  ],
  "overall_assessment": "Brief overall summary",
  "critical_gaps": ["Gap 1", "Gap 2"],
  "recommended_next_steps": ["Step 1", "Step 2"]
}}"""

        try:
            response = self.llm.complete(
                self.SYSTEM_PROMPT, prompt, temperature=0.2, max_tokens=2000
            )

            critique = self._extract_json(response)

            # Calculate weighted score
            critique["weighted_score"] = self._calculate_weighted_score(
                critique.get("scores", []), rubric["criteria"]
            )
            critique["approved"] = critique["weighted_score"] >= rubric["threshold"]

            return critique

        except Exception as e:
            logger.error(f"Critique failed: {e}")
            return {
                "scores": [],
                "weighted_score": 0.0,
                "approved": False,
                "error": f"Critique failed: {str(e)}",
            }

    def quick_review(self, section_name: str, section_text: str) -> dict:
        """
        Quick review of a single charter section.

        Args:
            section_name: Name of the section
            section_text: Section content

        Returns:
            Dict with score and feedback
        """
        prompt = f"""Review this {section_name} section from a project charter:

{section_text}

Evaluate on:
- Clarity and specificity
- Completeness
- Professional quality
- Actionability

Respond with ONLY valid JSON (no markdown):
{{
  "score": 85,
  "strengths": ["Strength 1", "Strength 2"],
  "improvements": ["Improvement 1", "Improvement 2"]
}}"""

        try:
            response = self.llm.complete(self.SYSTEM_PROMPT, prompt, temperature=0.2)
            return self._extract_json(response)
        except Exception as e:
            logger.error(f"Quick review failed: {e}")
            return {"score": 0, "error": f"Review failed: {str(e)}"}

    def suggest_improvements(self, charter_text: str, critique_results: dict) -> str:
        """
        Generate specific improvement suggestions based on critique.

        Args:
            charter_text: Current charter text
            critique_results: Results from critique_charter()

        Returns:
            Improvement suggestions as formatted text
        """
        gaps = critique_results.get("critical_gaps", [])
        gaps_text = "\n".join([f"- {gap}" for gap in gaps])

        prompt = f"""Based on this charter critique, provide specific, actionable improvements:

IDENTIFIED GAPS:
{gaps_text}

CURRENT CHARTER:
{charter_text[:1000]}...

For each gap, suggest:
1. What specifically should be added/changed
2. Where it should be added
3. Example text (1-2 sentences)

Format as a numbered action list."""

        return self.llm.complete(self.SYSTEM_PROMPT, prompt, temperature=0.4)

    def _format_rubric(self, rubric: dict) -> str:
        """Format rubric for prompt."""
        lines = []
        for criterion in rubric["criteria"]:
            weight_pct = int(criterion["weight"] * 100)
            lines.append(f"- {criterion['name']} ({weight_pct}% weight)")
        return "\n".join(lines)

    def _calculate_weighted_score(self, scores: list[dict], criteria: list[dict]) -> float:
        """Calculate weighted average score."""
        if not scores or not criteria:
            return 0.0

        total = 0.0
        for score_item in scores:
            # Find matching criterion
            criterion = next((c for c in criteria if c["name"] == score_item["criterion"]), None)
            if criterion:
                # Normalize score to 0-1 and apply weight
                normalized = score_item["score"] / 100.0
                total += normalized * criterion["weight"]

        return round(total, 3)
