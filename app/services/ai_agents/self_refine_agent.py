"""
Self-Refine Agent for iterative summary improvement.

Uses self-refinement prompting to iteratively improve analytical summaries
through cycles of generation → evaluation → refinement.
"""

from typing import Optional
from dataclasses import dataclass

from app.services.ai_agents.llm_client import LLMClient


@dataclass
class RefinementResult:
    """Result from self-refinement process."""
    refined_summary: str
    iterations_performed: int
    improvements_made: list[str]
    tokens_used: int


class SelfRefineAgent:
    """
    Agent that iteratively refines analytical summaries.
    
    Uses self-critique and iterative improvement to produce high-yield,
    concise summaries (4-6 sentences) that capture the essence of complex analysis.
    """
    
    def __init__(self, llm_client: LLMClient, max_iterations: int = 3):
        """
        Initialize self-refine agent.
        
        Args:
            llm_client: LLM client for API calls
            max_iterations: Maximum refinement iterations (default: 3)
        """
        self.llm_client = llm_client
        self.max_iterations = max_iterations
    
    def refine_summary(
        self,
        original_summary: str,
        context: Optional[str] = None
    ) -> RefinementResult:
        """
        Refine an analytical summary through iterative improvement.
        
        Process:
        1. Generate initial concise summary from original
        2. Evaluate: What's missing? What's incorrect? What can improve? Why?
        3. Refine based on evaluation
        4. Repeat until max iterations or quality threshold met
        
        Args:
            original_summary: Full analytical summary to distill
            context: Optional additional context (project notes, etc.)
            
        Returns:
            RefinementResult with refined 4-6 sentence summary
        """
        current_summary = None
        improvements_made = []
        total_tokens = 0
        
        for iteration in range(self.max_iterations):
            if iteration == 0:
                # First iteration: distill to 4-6 sentences
                current_summary, tokens = self._initial_distillation(
                    original_summary, context
                )
                total_tokens += tokens
            else:
                # Subsequent iterations: evaluate and refine
                evaluation, eval_tokens = self._evaluate_summary(
                    current_summary, original_summary, context
                )
                total_tokens += eval_tokens
                
                # Check if refinement needed
                if not evaluation["needs_improvement"]:
                    improvements_made.append(f"Iteration {iteration}: Quality threshold met")
                    break
                
                # Refine based on evaluation
                current_summary, refine_tokens = self._refine_summary(
                    current_summary, evaluation, original_summary, context
                )
                total_tokens += refine_tokens
                improvements_made.append(
                    f"Iteration {iteration + 1}: {evaluation['improvement_focus']}"
                )
        
        return RefinementResult(
            refined_summary=current_summary,
            iterations_performed=iteration + 1,
            improvements_made=improvements_made,
            tokens_used=total_tokens
        )
    
    def _initial_distillation(
        self,
        original_summary: str,
        context: Optional[str]
    ) -> tuple[str, int]:
        """
        Distill lengthy analytical summary to 4-6 high-yield sentences.
        
        Returns:
            Tuple of (distilled summary, tokens used)
        """
        system_message = """You are an expert at distilling complex analysis into concise, high-impact summaries.
Your goal is to capture the HIGHEST YIELD information in 4-6 sentences that:
- Identify the core problem/opportunity
- Highlight key decisions and their rationale
- Note critical risks or gaps
- Convey strategic importance

Focus on what matters most for executive decision-making."""

        prompt_parts = [
            "# TASK: DISTILL ANALYTICAL SUMMARY",
            "",
            "You will receive a lengthy analytical summary. Your job is to distill it into 4-6 high-yield sentences.",
            "",
            "## ORIGINAL ANALYTICAL SUMMARY",
            "",
            original_summary,
            ""
        ]
        
        if context:
            prompt_parts.extend([
                "## ADDITIONAL CONTEXT",
                "",
                context,
                ""
            ])
        
        prompt_parts.extend([
            "## INSTRUCTIONS",
            "",
            "Create a 4-6 sentence distilled summary that:",
            "1. Captures the CORE problem/opportunity (1-2 sentences)",
            "2. Highlights KEY decisions, numbers, or critical information (2-3 sentences)",
            "3. Notes the most important risk or gap (1 sentence)",
            "",
            "Focus on:",
            "- Specific numbers, metrics, dollar amounts, timelines",
            "- Critical decisions and their rationale",
            "- What makes this different from alternatives",
            "- What failure looks like",
            "",
            "Return ONLY the 4-6 sentence summary, no additional commentary."
        ])
        
        prompt = "\n".join(prompt_parts)
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=500
        )
        
        return response.content.strip(), response.tokens_used
    
    def _evaluate_summary(
        self,
        current_summary: str,
        original_summary: str,
        context: Optional[str]
    ) -> tuple[dict, int]:
        """
        Evaluate current summary for improvement opportunities.
        
        Returns:
            Tuple of (evaluation dict, tokens used)
        """
        system_message = """You are a critical evaluator of executive summaries.
Your job is to identify what's missing, incorrect, or could be improved."""

        prompt = f"""# TASK: EVALUATE SUMMARY QUALITY

## CURRENT SUMMARY (4-6 sentences)
{current_summary}

## ORIGINAL FULL ANALYSIS (for reference)
{original_summary[:2000]}... [truncated]

## EVALUATION CRITERIA

Analyze the current summary and answer:
1. **What's missing?** (Critical information from original that's absent)
2. **What's incorrect?** (Inaccuracies or misrepresentations)
3. **What can be improved?** (Clarity, specificity, impact)
4. **Why does it matter?** (Impact on decision-making)

Return your evaluation in JSON format:
{{
    "needs_improvement": true/false,
    "missing_info": "What critical info is absent",
    "inaccuracies": "What's wrong or misleading",
    "improvement_opportunities": "What could be clearer/stronger",
    "improvement_focus": "One-sentence priority for next iteration"
}}

If the summary is already excellent (captures all critical info, accurate, clear), set needs_improvement to false.
"""
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3,
            max_tokens=800
        )
        
        # Parse evaluation
        import json
        try:
            content = response.content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
                content = content.strip()
            evaluation = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: assume no improvement needed
            evaluation = {
                "needs_improvement": False,
                "missing_info": "None",
                "inaccuracies": "None",
                "improvement_opportunities": "None",
                "improvement_focus": "Summary is adequate"
            }
        
        return evaluation, response.tokens_used
    
    def _refine_summary(
        self,
        current_summary: str,
        evaluation: dict,
        original_summary: str,
        context: Optional[str]
    ) -> tuple[str, int]:
        """
        Refine summary based on evaluation feedback.
        
        Returns:
            Tuple of (refined summary, tokens used)
        """
        system_message = """You are refining an executive summary based on critical feedback.
Maintain the 4-6 sentence constraint while addressing identified issues."""

        prompt = f"""# TASK: REFINE SUMMARY BASED ON EVALUATION

## CURRENT SUMMARY
{current_summary}

## EVALUATION FEEDBACK
- **Missing Information:** {evaluation.get('missing_info', 'None')}
- **Inaccuracies:** {evaluation.get('inaccuracies', 'None')}
- **Improvement Opportunities:** {evaluation.get('improvement_opportunities', 'None')}
- **Priority Focus:** {evaluation.get('improvement_focus', 'None')}

## ORIGINAL FULL ANALYSIS (for reference)
{original_summary[:2000]}... [truncated]

## INSTRUCTIONS

Produce a REFINED version of the summary that:
1. Addresses the evaluation feedback
2. Remains 4-6 sentences
3. Maintains high specificity (numbers, metrics, timelines)
4. Preserves the most critical strategic information

Return ONLY the refined summary, no additional commentary.
"""
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=500
        )
        
        return response.content.strip(), response.tokens_used
