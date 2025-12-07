"""
Refinement Agent for applying user-guided improvements to documents.

Takes verifier feedback and/or custom user instructions and applies them
to refine a document through targeted improvements.
"""

from typing import Optional
from dataclasses import dataclass

from app.services.ai_agents.llm_client import LLMClient
from app.services.ai_agents.context_builder import ProjectContext


@dataclass
class RefinementResult:
    """Result from refinement process."""
    refined_content: str
    model_used: str
    tokens_used: int
    improvements_applied: list[str]
    summary: str  # One-line summary of what was improved


class RefinementAgent:
    """
    Agent that refines documents based on user-guided improvements.
    
    Takes a document and specific improvement instructions, then applies
    those improvements while maintaining the core content and structure.
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize refinement agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm_client = llm_client
    
    def refine_document(
        self,
        document_content: str,
        improvement_instructions: list[str],
        context: Optional[ProjectContext] = None,
        focus_areas: Optional[list[str]] = None,
        max_iterations: int = 1
    ) -> RefinementResult:
        """
        Refine a document based on specific improvement instructions.
        
        Process:
        1. Build refinement prompt with document + instructions
        2. Call LLM to apply improvements
        3. Validate output
        4. Return refined document
        
        Args:
            document_content: Full markdown document to refine
            improvement_instructions: List of specific improvements to apply
                Example: ["Remove repetitive sections", "Condense to 40% shorter"]
            context: Optional project context for grounding
            focus_areas: Optional sections to focus on
                Example: ["Executive Summary", "Business Case"]
            max_iterations: Iterations to apply improvements (default: 1)
            
        Returns:
            RefinementResult with refined_content and summary
        """
        current_content = document_content
        improvements_applied = []
        total_tokens = 0
        
        for iteration in range(max_iterations):
            # Build refinement prompt
            prompt = self._build_refinement_prompt(
                current_content,
                improvement_instructions,
                focus_areas,
                context,
                iteration
            )
            
            # Generate refined version
            response = self.llm_client.generate(
                prompt=prompt,
                system_message=self._build_system_message(),
                temperature=0.5,
                max_tokens=15000  # Allow longer outputs
            )
            
            current_content = response.content.strip()
            total_tokens += response.tokens_used
            
            improvements_applied.append(
                f"Iteration {iteration + 1}: Applied targeted improvements"
            )
        
        # Build summary
        summary = self._build_summary(
            document_content,
            current_content,
            improvement_instructions
        )
        
        return RefinementResult(
            refined_content=current_content,
            model_used=self.llm_client.model,
            tokens_used=total_tokens,
            improvements_applied=improvements_applied,
            summary=summary
        )
    
    def condense_and_improve(
        self,
        document_content: str,
        quality_feedback: dict,
        target_reduction: float = 0.4,
        context: Optional[ProjectContext] = None
    ) -> RefinementResult:
        """
        Condense document while applying quality improvements.
        
        Combines condensing (reduce by target_reduction %) with specific
        quality feedback from verifier.
        
        Args:
            document_content: Full markdown document
            quality_feedback: Dict with keys: weaknesses, improvements, issues
            target_reduction: Target reduction percentage (0.4 = 40% shorter)
            context: Optional project context
            
        Returns:
            RefinementResult with condensed + improved document
        """
        # Extract improvements from quality feedback
        improvements = []
        
        if "improvements" in quality_feedback:
            improvements.extend(quality_feedback["improvements"])
        
        if "weaknesses" in quality_feedback:
            # Convert weaknesses to improvement instructions
            improvements.append(f"Fix these issues: {'; '.join(quality_feedback['weaknesses'][:3])}")
        
        if "issues" in quality_feedback:
            improvements.append(f"Address: {'; '.join(quality_feedback['issues'][:3])}")
        
        # Always include condensing instruction
        current_word_count = len(document_content.split())
        target_words = int(current_word_count * (1 - target_reduction))
        improvements.append(f"Reduce from {current_word_count} to ~{target_words} words (remove repetition and verbose sections)")
        
        # Apply refinements
        return self.refine_document(
            document_content,
            improvements,
            context=context
        )
    
    def _build_system_message(self) -> str:
        """Build system message for refinement."""
        return """You are an expert document editor and refiner.

Your role:
- Apply specific improvements while maintaining document structure
- Preserve all critical information and data
- Improve clarity, conciseness, and flow
- Fix identified issues and weaknesses
- Maintain professional tone and formatting

Standards:
- Never remove important data or analysis
- Cross-reference instead of repeating information
- Use active voice and clear language
- Keep bold formatting for key metrics
- Maintain markdown formatting (headings, tables, lists)"""
    
    def _build_refinement_prompt(
        self,
        document_content: str,
        improvement_instructions: list[str],
        focus_areas: Optional[list[str]],
        context: Optional[ProjectContext],
        iteration: int
    ) -> str:
        """Build refinement prompt."""
        parts = [
            "# TASK: REFINE DOCUMENT WITH SPECIFIC IMPROVEMENTS",
            "",
            "You will receive a document and specific improvement instructions.",
            "Apply the improvements while maintaining structure and critical content.",
            ""
        ]
        
        # Add improvement instructions
        parts.extend([
            "## IMPROVEMENTS TO APPLY",
            ""
        ])
        for i, instruction in enumerate(improvement_instructions, 1):
            parts.append(f"{i}. {instruction}")
        
        # Add focus areas if specified
        if focus_areas:
            parts.extend([
                "",
                "## FOCUS AREAS (prioritize these sections)",
                ""
            ])
            for area in focus_areas:
                parts.append(f"- {area}")
        
        # Add context if available
        if context:
            parts.extend([
                "",
                "## PROJECT CONTEXT (use for grounding)",
                context.full_context_text[:2000],
                ""
            ])
        
        # Add document
        parts.extend([
            "",
            "## CURRENT DOCUMENT",
            "",
            document_content,
            ""
        ])
        
        # Add instructions
        parts.extend([
            "## INSTRUCTIONS",
            "",
            "Apply each improvement above while:",
            "1. **Preserving structure** - Keep same sections and order",
            "2. **Preserving data** - All numbers, dates, key facts stay intact",
            "3. **Improving clarity** - Remove vague language, be specific",
            "4. **Reducing repetition** - Mention each point once, cross-reference later",
            "5. **Maintaining tone** - Professional, executive-appropriate",
            "6. **Fixing formatting** - Bold metrics, organize lists, use tables for data",
            "",
            "## QUALITY CHECKLIST",
            "",
            "Before returning, verify:",
            "- [ ] All critical data and analysis preserved",
            "- [ ] Specific improvements applied",
            "- [ ] No unnecessary repetition",
            "- [ ] Clear, concise language",
            "- [ ] Professional formatting",
            "- [ ] Tables and lists properly formatted",
            "",
            "Return ONLY the refined markdown document, no commentary."
        ])
        
        return "\n".join(parts)
    
    def _build_summary(
        self,
        original: str,
        refined: str,
        improvements: list[str]
    ) -> str:
        """Build one-line summary of refinements."""
        original_words = len(original.split())
        refined_words = len(refined.split())
        reduction = int((1 - refined_words / original_words) * 100)
        
        summary_parts = []
        
        if reduction > 0:
            summary_parts.append(f"Reduced by {reduction}%")
        
        # Identify main improvements
        if "repetition" in " ".join(improvements).lower():
            summary_parts.append("removed repetition")
        if "condense" in " ".join(improvements).lower():
            summary_parts.append("condensed")
        if "improve" in " ".join(improvements).lower():
            summary_parts.append("improved clarity")
        
        if summary_parts:
            return ", ".join(summary_parts)
        else:
            return "Applied targeted refinements"
