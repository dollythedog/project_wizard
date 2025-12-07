"""
Step-Back Agent for clarifying project needs.

Uses step-back prompting technique to ask clarifying questions
before document generation.
"""

import json
from typing import Optional
from dataclasses import dataclass

from app.services.blueprint_registry import get_registry
from app.services.ai_agents.llm_client import LLMClient
from app.services.ai_agents.context_builder import ProjectContext


@dataclass
class StepBackResult:
    """Result from step-back prompting."""
    questions: list[str]
    summary: str
    context_used: str
    suggested_outline: Optional[str] = None


class StepBackAgent:
    """
    Agent that uses step-back prompting to clarify needs.
    
    Before generating a document, this agent asks strategic questions
    to understand the true problem and desired outcomes.
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize step-back agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm_client = llm_client
        self.blueprint_registry = get_registry()
    
    def generate_questions(
        self,
        template_name: str,
        user_inputs: Optional[dict[str, any]] = None,
        project_context: Optional[ProjectContext] = None
    ) -> list[str]:
        """
        Generate clarifying questions for a template.
        
        Args:
            template_name: Name of document template
            user_inputs: Optional blueprint inputs from form
            project_context: Optional project context
            
        Returns:
            List of clarifying questions
        """
        # Load blueprint
        blueprint = self.blueprint_registry.load_blueprint(template_name)
        
        # Load prompts
        prompts = self.blueprint_registry.load_prompts(template_name)
        step_back = prompts.get("step_back_prompts", {})
        
        # Use default questions from blueprint if available
        default_questions = step_back.get("questions", [])
        
        # If we have project context or user inputs, personalize questions
        if (project_context and project_context.full_context_text) or user_inputs:
            personalized_questions = self._personalize_questions(
                default_questions,
                project_context,
                step_back,
                user_inputs
            )
            return personalized_questions
        
        return default_questions
    
    def process_responses(
        self,
        template_name: str,
        responses: dict[str, str],
        project_context: Optional[ProjectContext] = None
    ) -> StepBackResult:
        """
        Process user responses to clarifying questions.
        
        Args:
            template_name: Name of document template
            responses: Dictionary of question -> answer
            project_context: Optional project context
            
        Returns:
            StepBackResult with summary and analysis
        """
        # Load prompts
        prompts = self.blueprint_registry.load_prompts(template_name)
        step_back = prompts.get("step_back_prompts", {})
        
        # Build prompt for LLM
        system_message = step_back.get("identity", "")
        
        user_prompt_parts = [
            "# STEP-BACK ANALYSIS",
            "",
            "## User Responses to Clarifying Questions",
            ""
        ]
        
        questions_list = []
        for question, answer in responses.items():
            user_prompt_parts.append(f"**Q: {question}**")
            user_prompt_parts.append(f"A: {answer}")
            user_prompt_parts.append("")
            questions_list.append(question)
        
        if project_context:
            user_prompt_parts.extend([
                "## Existing Project Context",
                project_context.full_context_text,
                ""
            ])
        
        user_prompt_parts.extend([
            "## Task",
            step_back.get("output_instructions", "Synthesize the responses into a clear summary."),
            "",
            "Provide a concise summary (2-3 paragraphs) that:",
            "1. Identifies the core problem or opportunity",
            "2. Highlights key requirements and constraints",
            "3. Notes any gaps or areas needing clarification",
            "4. Suggests focus areas for the document"
        ])
        
        user_prompt = "\n".join(user_prompt_parts)
        
        # Generate summary
        response = self.llm_client.generate(
            prompt=user_prompt,
            system_message=system_message,
            temperature=0.7
        )
        
        # Load blueprint to get section info
        blueprint = self.blueprint_registry.load_blueprint(template_name)
        
        # Generate suggested outline based on responses
        suggested_outline = self._generate_suggested_outline(
            template_name,
            blueprint,
            responses,
            response.content
        )
        
        return StepBackResult(
            questions=questions_list,
            summary=response.content,
            context_used=user_prompt,
            suggested_outline=suggested_outline
        )
    
    def _personalize_questions(
        self,
        default_questions: list[str],
        project_context: Optional[ProjectContext],
        step_back_config: dict,
        user_inputs: Optional[dict[str, any]] = None
    ) -> list[str]:
        """
        Personalize questions based on project context and user inputs.
        
        Uses LLM to adapt questions to the specific project.
        """
        system_message = step_back_config.get("identity", "")
        
        context_parts = []
        if project_context:
            context_parts.append(f"Project Context:\n{project_context.full_context_text}")
        
        if user_inputs:
            inputs_text = "\n".join([f"- {k}: {v}" for k, v in user_inputs.items()])
            context_parts.append(f"\nUser Inputs (from form):\n{inputs_text}")
        
        combined_context = "\n\n".join(context_parts)
        
        prompt = f"""Given this information:

{combined_context}

And these default clarifying questions:
{json.dumps(default_questions, indent=2)}

Generate 5-7 personalized clarifying questions that:
1. Are specifically relevant to this project type and context
2. Build on information already known
3. Focus on gaps and unclear areas
4. Help ensure a high-quality document

Return ONLY a JSON array of question strings, no other text:
["question 1", "question 2", ...]
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_message=system_message,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse JSON response
            # Claude sometimes wraps JSON in markdown code blocks
            content = response.content.strip()
            if content.startswith("```"):
                # Extract JSON from markdown code block
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            questions = json.loads(content)
            if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
                return questions
        except (json.JSONDecodeError, Exception) as e:
            print(f"Failed to personalize questions: {e}")
            print(f"Response content: {response.content[:500] if response else 'No response'}")
        
        # Fallback to default questions
        return default_questions
    
    def _generate_suggested_outline(
        self,
        template_name: str,
        blueprint,
        responses: dict[str, str],
        step_back_summary: str
    ) -> str:
        """
        Generate a suggested outline based on step-back responses.
        
        This outline can be modified by the user before draft generation.
        """
        # Get sections from blueprint (BlueprintSpec object, not dict)
        sections = blueprint.sections
        section_list = "\n".join([f"- {s.title}" for s in sections])
        
        # Build responses text
        responses_text = "\n".join([f"- {q}: {a}" for q, a in responses.items()])
        
        # Load prompts to get outline generation config if available
        prompts = self.blueprint_registry.load_prompts(template_name)
        outline_config = prompts.get("outline_generation", {})
        
        system_message = outline_config.get(
            "identity",
            "You are an expert document architect who creates clear, logical outlines for documents."
        )
        
        prompt = f"""Based on the user's clarifying responses and the document template, suggest a logical outline structure.

## Document Type
{template_name.replace('_', ' ').title()}

## Available Sections
{section_list}

## User Responses to Clarifying Questions
{responses_text}

## Step-Back Summary
{step_back_summary}

## Task
Generate a suggested outline for this document that:
1. Organizes sections in a logical flow
2. Suggests what key points should be covered in each section
3. Highlights any critical elements based on the user's responses
4. Can be easily modified by the user if needed

**Format your response as:**

# Suggested Document Outline

Then for each section, provide:
## [Section Name]
- Key point 1
- Key point 2
- Key point 3

Make it clear, specific, and actionable so the user can review and modify before draft generation.
"""
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                system_message=system_message,
                temperature=0.7,
                max_tokens=2000
            )
            return response.content
        except Exception as e:
            print(f"Failed to generate outline: {e}")
            return "Could not generate outline suggestion. Proceeding with default structure."
