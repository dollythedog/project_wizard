"""
Pattern Pipeline
Orchestrates the full document generation workflow using specialized agents
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .ai_agents import CriticAgent, DraftAgent, EditorAgent
from .pattern_registry import PatternRegistry
from .project_context import ProjectContext

logger = logging.getLogger(__name__)


class PatternPipeline:
    """
    Unix-style pipeline for document generation:
    User Input → Draft → Edit → Critique → [Revision Loop] → Format → Output
    """

    def __init__(self, pattern_registry: PatternRegistry, project_context: ProjectContext = None):
        """
        Initialize pipeline

        Args:
            pattern_registry: Registry of available patterns
            project_context: Optional project context for documentation injection
        """
        self.registry = pattern_registry
        self.project_context = project_context

        # Initialize specialized agents
        self.draft_agent = DraftAgent()
        self.editor_agent = EditorAgent()
        self.critic_agent = CriticAgent()

        logger.info("PatternPipeline: Initialized")

    def execute(
        self,
        pattern_name: str,
        user_inputs: dict[str, Any],
        enable_editing: bool = True,
        enable_critique: bool = True,
        max_revision_iterations: int = 2,
        project_path: Path = None,
    ) -> dict[str, Any]:
        """
        Execute full pipeline for a pattern

        Args:
            pattern_name: Name of pattern to execute
            user_inputs: User-provided variables
            enable_editing: Whether to run editor agent
            enable_critique: Whether to run critic agent
            max_revision_iterations: Max critique-revision loops
            project_path: Optional path to project for context loading

        Returns:
            Result dictionary with 'document', 'metadata', 'critique', etc.
        """
        logger.info(f"Pipeline: Starting execution for pattern '{pattern_name}'")

        # Load pattern
        pattern = self.registry.get_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern not found: {pattern_name}")

        # Load project context if available
        context = {}
        if project_path and self.project_context:
            self.project_context.project_path = Path(project_path)
            context = self.project_context.load_context()
            logger.info(f"Pipeline: Loaded project context from {project_path}")

        # Stage 1: DRAFT
        logger.info("Pipeline: Stage 1 - Drafting")
        user_prompt = self.registry.render_user_prompt(pattern_name, **user_inputs, **context)
        draft = self.draft_agent.generate_draft(
            system_prompt=pattern["system"],
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=2500,
        )

        # Track pipeline state
        pipeline_log = [{"stage": "draft", "content": draft, "length": len(draft)}]

        # Stage 2: EDIT (optional)
        if enable_editing:
            logger.info("Pipeline: Stage 2 - Editing")
            edited = self.editor_agent.edit_draft(draft)
            pipeline_log.append({"stage": "edit", "content": edited, "length": len(edited)})
        else:
            edited = draft
            logger.info("Pipeline: Stage 2 - Editing skipped")

        # Stage 3: CRITIQUE & REVISION (optional)
        critique_result = None
        final_content = edited

        if enable_critique and pattern["rubric"]:
            logger.info("Pipeline: Stage 3 - Critique & Revision")

            for iteration in range(max_revision_iterations):
                critique_result = self.critic_agent.critique_charter(
                    final_content, rubric=pattern["rubric"]
                )

                score = critique_result.get("weighted_score", 0)
                threshold = pattern["rubric"].get("threshold", 0.75)

                logger.info(
                    f"Pipeline: Critique iteration {iteration + 1} - Score: {score:.2f} (threshold: {threshold})"
                )

                if score >= threshold:
                    logger.info("Pipeline: Quality threshold met")
                    break

                if iteration < max_revision_iterations - 1:
                    # Revision pass
                    logger.info("Pipeline: Running revision based on critique")
                    revision_prompt = self._build_revision_prompt(final_content, critique_result)
                    final_content = self.editor_agent.edit_draft(
                        final_content, specific_guidance=revision_prompt
                    )
                    pipeline_log.append(
                        {
                            "stage": f"revision_{iteration + 1}",
                            "content": final_content,
                            "score": score,
                            "length": len(final_content),
                        }
                    )

            pipeline_log.append(
                {
                    "stage": "final_critique",
                    "score": critique_result.get("weighted_score", 0),
                    "approved": critique_result.get("approved", False),
                }
            )
        else:
            logger.info("Pipeline: Stage 3 - Critique skipped")

        # Stage 4: FORMAT OUTPUT
        logger.info("Pipeline: Stage 4 - Formatting output")

        metadata = {
            "project_name": self.project_context.get_project_name()
            if self.project_context
            else "Unknown",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "pattern": pattern_name,
            "version": "1.0",
            "author": "Project Team",
            "status": "Draft",
        }

        formatted_doc = self.registry.render_output(pattern_name, content=final_content, **metadata)

        # Return complete result
        return {
            "document": formatted_doc,
            "raw_content": final_content,
            "metadata": metadata,
            "critique": critique_result,
            "pipeline_log": pipeline_log,
            "iterations": len([log for log in pipeline_log if "revision" in log.get("stage", "")]),
            "final_score": critique_result.get("weighted_score") if critique_result else None,
        }

    def _build_revision_prompt(self, content: str, critique: dict) -> str:
        """Build specific revision guidance from critique"""
        guidance = "Based on quality review, address these specific issues:\n\n"

        # Extract critical gaps
        if critique.get("critical_gaps"):
            guidance += "## Critical Gaps\n"
            for gap in critique["critical_gaps"][:3]:  # Top 3
                guidance += f"- {gap}\n"
            guidance += "\n"

        # Extract low-scoring criteria
        if critique.get("scores"):
            low_scores = [s for s in critique["scores"] if s.get("score", 100) < 70]
            if low_scores:
                guidance += "## Areas Needing Improvement\n"
                for score in low_scores[:2]:  # Top 2
                    guidance += (
                        f"- **{score['criterion']}**: {', '.join(score.get('improvements', []))}\n"
                    )

        return guidance
