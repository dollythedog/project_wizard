"""
Verifier Agent for document quality assessment.

Reviews generated documents against blueprint rubrics and provides
specific improvement suggestions.
"""

import json
from typing import Optional
from dataclasses import dataclass

from app.services.blueprint_registry import get_registry
from app.services.ai_agents.llm_client import LLMClient
from app.services.ai_agents.context_builder import ProjectContext


@dataclass
class VerificationScore:
    """Score for a single rubric criterion."""
    criterion_id: str
    criterion_name: str
    score: int  # 1-5
    level: str  # excellent, good, adequate, needs_improvement, poor
    feedback: str
    weight: float


@dataclass
class VerificationResult:
    """Complete verification result for a document."""
    overall_score: float  # Weighted average 1.0-5.0
    scores: list[VerificationScore]
    strengths: list[str]
    weaknesses: list[str]
    specific_improvements: list[str]
    ready_for_approval: bool
    model_used: str
    tokens_used: int


class VerifierAgent:
    """
    Agent that verifies document quality against rubrics.
    
    Uses blueprint rubrics to score documents on clarity, completeness,
    strategic alignment, and feasibility.
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize verifier agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm_client = llm_client
        self.blueprint_registry = get_registry()
    
    def verify_document(
        self,
        template_name: str,
        document_content: str,
        project_context: Optional[ProjectContext] = None,
        user_inputs: Optional[dict] = None
    ) -> VerificationResult:
        """
        Verify a document against its blueprint rubric.
        
        Process:
        1. Load rubric from blueprint
        2. Score each criterion (clarity, completeness, alignment, feasibility)
        3. Identify strengths and weaknesses
        4. Generate specific improvement suggestions
        
        Args:
            template_name: Name of document template
            document_content: Generated document markdown
            project_context: Optional project context
            user_inputs: Optional original user inputs
            
        Returns:
            VerificationResult with scores and feedback
        """
        # Load blueprint and rubric
        blueprint = self.blueprint_registry.load_blueprint(template_name)
        
        if not hasattr(blueprint, 'rubric') or not blueprint.rubric:
            raise ValueError(f"No rubric defined for template: {template_name}")
        
        # Convert rubric to dict if it's a Pydantic model
        rubric = blueprint.rubric
        if hasattr(rubric, 'model_dump'):
            rubric = rubric.model_dump()
        elif hasattr(rubric, 'dict'):
            rubric = rubric.dict()
        
        # Build verification prompt with full document
        # (truncation removed to ensure specific feedback on all sections)
        prompt = self._build_verification_prompt(
            document_content,
            rubric,
            project_context,
            user_inputs
        )
        
        # Generate verification
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=self._build_system_message(),
            temperature=0.3,  # Lower temp for more consistent scoring
            max_tokens=20000  # Increased for longer documents (12+ pages)
        )
        
        # Parse response
        verification_data = self._parse_verification_response(response.content)
        
        # Calculate weighted overall score
        scores = []
        total_weight = 0.0
        weighted_sum = 0.0
        
        for criterion in rubric.get('criteria', []):
            criterion_id = criterion['id']
            criterion_name = criterion['name']
            weight = criterion.get('weight', 0.25)
            
            # Get score from verification data
            score_data = verification_data.get('scores', {}).get(criterion_id, {})
            score_value = score_data.get('score', 3)
            score_level = score_data.get('level', 'adequate')
            feedback = score_data.get('feedback', '')
            
            score_obj = VerificationScore(
                criterion_id=criterion_id,
                criterion_name=criterion_name,
                score=score_value,
                level=score_level,
                feedback=feedback,
                weight=weight
            )
            scores.append(score_obj)
            
            weighted_sum += score_value * weight
            total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 3.0
        
        return VerificationResult(
            overall_score=overall_score,
            scores=scores,
            strengths=verification_data.get('strengths', []),
            weaknesses=verification_data.get('weaknesses', []),
            specific_improvements=verification_data.get('improvements', []),
            ready_for_approval=overall_score >= 4.0,
            model_used=self.llm_client.model,
            tokens_used=response.tokens_used
        )
    
    def _build_system_message(self) -> str:
        """Build system message for verifier."""
        return """You are a rigorous project management document reviewer.

Your role:
- Evaluate documents against established quality rubrics
- Identify specific strengths and weaknesses
- Provide actionable improvement suggestions
- Score fairly but critically

Standards:
- Be specific: cite exact sections when providing feedback
- Be constructive: always suggest concrete improvements
- Be honest: don't inflate scores
- Be thorough: review all aspects of the rubric"""
    
    def _build_verification_prompt(
        self,
        document_content: str,
        rubric: dict,
        project_context: Optional[ProjectContext],
        user_inputs: Optional[dict]
    ) -> str:
        """Build verification prompt."""
        parts = [
            "# TASK: VERIFY DOCUMENT QUALITY",
            "",
            "Review the following document against the quality rubric.",
            "Score each criterion 1-5 and provide specific feedback.",
            ""
        ]
        
        # Add rubric criteria (condensed format)
        parts.extend([
            "## QUALITY RUBRIC",
            ""
        ])
        
        for criterion in rubric.get('criteria', []):
            parts.append(f"**{criterion['name']}** (weight: {criterion['weight']}): {criterion['description']}")
            parts.append(f"  5=excellent, 4=good, 3=adequate, 2=needs_improvement, 1=poor")
            parts.append("")
        
        # Add document to review
        parts.extend([
            "## DOCUMENT TO REVIEW",
            "",
            document_content,
            "",
            "## INSTRUCTIONS",
            "",
            "Provide your assessment in JSON format:",
            "```json",
            "{",
            '  "scores": {'
        ])
        
        # Add example scores for each criterion
        criterion_examples = []
        for i, criterion in enumerate(rubric.get('criteria', [])):
            crit_id = criterion['id']
            crit_name = criterion['name']
            is_last = (i == len(rubric.get('criteria', [])) - 1)
            comma = "" if is_last else ","
            criterion_examples.append(
                f'    "{crit_id}": {{"score": 4, "level": "good", "feedback": "Specific feedback about {crit_name}..."}}{comma}'
            )
        
        parts.extend(criterion_examples)
        parts.extend([
            "  },",
            '  "strengths": [',
            '    "List 3-5 specific strengths (cite sections)",',
            '    "Example: Clear data presentation in Executive Summary"',
            "  ],",
            '  "weaknesses": [',
            '    "List 3-5 specific weaknesses (cite sections)",',
            '    "Example: Calculation error in Trend Analysis section"',
            "  ],",
            '  "improvements": [',
            '    "List 3-5 actionable improvements",',
            '    "Example: Add growth percentage calculations for all metrics",',
            '    "Example: Include comparison table in Data Overview section"',
            "  ]",
            "}",
            "```",
            "",
            "CRITICAL:",
            "- Use exact criterion IDs from rubric above",
            "- Score honestly: 5=excellent, 4=good, 3=adequate, 2=needs_improvement, 1=poor",
            "- Be specific in feedback - cite section names/numbers",
            "- Provide at least 3 items each for strengths, weaknesses, and improvements",
            "- Improvements must be concrete and actionable",
            "- Return ONLY valid JSON"
        ])
        
        return "\n".join(parts)
    
    def _truncate_document(self, content: str, max_chars: int = 7000) -> str:
        """Truncate document to fit within token limits while keeping key sections."""
        if len(content) <= max_chars:
            return content
        
        # Keep first 5000 chars and last 1000 chars with ellipsis
        head_chars = max_chars - 1200
        tail_chars = 1000
        
        truncated = (
            content[:head_chars] + 
            "\n\n[... document truncated for verification - middle sections omitted ...]\n\n" +
            content[-tail_chars:]
        )
        return truncated
    
    def _parse_verification_response(self, response_content: str) -> dict:
        """Parse JSON response from LLM."""
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in response_content:
                start = response_content.find("```json") + 7
                end = response_content.find("```", start)
                if end == -1:  # No closing backticks, truncated response
                    json_str = response_content[start:].strip()
                else:
                    json_str = response_content[start:end].strip()
            elif "```" in response_content:
                start = response_content.find("```") + 3
                end = response_content.find("```", start)
                if end == -1:
                    json_str = response_content[start:].strip()
                else:
                    json_str = response_content[start:end].strip()
            else:
                json_str = response_content.strip()
            
            # Try to parse complete JSON
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Try to salvage partial JSON by finding the last complete section
            try:
                json_str = self._extract_partial_json(json_str)
                return json.loads(json_str)
            except:
                print(f"Failed to parse verification response: {e}")
                print(f"Response length: {len(response_content)} chars")
                print(f"Response preview: {response_content[:500]}...")
                print(f"Response end: ...{response_content[-200:]}")
                # Return default structure
                return {
                    "scores": {},
                    "strengths": ["Unable to parse verification response - response may have been truncated"],
                    "weaknesses": ["Verification incomplete - JSON parse error"],
                    "improvements": ["Document may be too long for verification. Try condensing first or retry verification."]
                }
    
    def _extract_partial_json(self, json_str: str) -> str:
        """Attempt to extract valid JSON from truncated response."""
        # Try to find the last complete array or object
        # Look for common truncation points and close them
        
        # Count braces to see if we can balance them
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        # Try to close incomplete structures
        result = json_str
        
        # If we're in the middle of a string, remove it
        if result.count('"') % 2 != 0:
            last_quote = result.rfind('"')
            result = result[:last_quote]
        
        # Remove any trailing commas before closing
        result = result.rstrip().rstrip(',')
        
        # Close arrays and objects
        if open_brackets > close_brackets:
            result += ']' * (open_brackets - close_brackets)
        if open_braces > close_braces:
            result += '}' * (open_braces - close_braces)
        
        return result
