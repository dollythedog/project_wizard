"""
Draft Agent for AI-powered document generation.

Enriches user inputs with AI, then renders templates.
"""

import json
from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime

from app.services.blueprint_registry import get_registry
from app.services.ai_agents.llm_client import LLMClient
from app.services.ai_agents.context_builder import ProjectContext
from app.services.ai_agents.step_back_agent import StepBackResult
from app.models.blueprint import GenerationStrategy


@dataclass
class DraftResult:
    """Result from draft generation."""
    content: str
    model_used: str
    tokens_used: int
    sections_generated: list[str]


class DraftAgent:
    """
    Agent that generates document drafts.
    
    Uses blueprint templates, prompts, and project context to generate
    high-quality document sections.
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize draft agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm_client = llm_client
        self.blueprint_registry = get_registry()
    
    def generate_draft(
        self,
        template_name: str,
        user_inputs: dict[str, any],
        project_context: Optional[ProjectContext] = None,
        step_back_result: Optional[StepBackResult] = None
    ) -> DraftResult:
        """
        Generate a complete document draft.
        
        Process branches based on blueprint's generation_strategy:
        
        FIELD_ENRICHMENT:
        1. Use AI to ENRICH user inputs (expand brief answers into detailed content)
        2. Render template.j2 with enriched values
        3. Return formatted markdown
        
        SKELETON_OF_THOUGHT:
        1. Generate skeleton outline with key points per section
        2. Expand each section in detail using the skeleton
        3. Assemble sections into final document
        4. Return formatted markdown
        
        Args:
            template_name: Name of document template
            user_inputs: User-provided inputs for template
            project_context: Optional project context
            step_back_result: Optional step-back analysis result
            
        Returns:
            DraftResult with rendered template content
        """
        # Load blueprint and prompts
        blueprint = self.blueprint_registry.load_blueprint(template_name)
        prompts = self.blueprint_registry.load_prompts(template_name)
        draft_config = prompts.get("draft_generation", {})
        
        # Branch based on generation strategy
        if blueprint.generation_strategy == GenerationStrategy.SKELETON_OF_THOUGHT:
            return self._generate_with_skeleton(
                blueprint,
                prompts,
                user_inputs,
                project_context,
                step_back_result
            )
        else:
            # Default: field enrichment
            return self._generate_with_field_enrichment(
                blueprint,
                draft_config,
                template_name,
                user_inputs,
                project_context,
                step_back_result
            )
    
    def _build_system_message(self, draft_config: dict) -> str:
        """Build system message for LLM."""
        parts = []
        
        # Identity
        if "identity" in draft_config:
            parts.append(draft_config["identity"])
        
        # Goals
        if "goals" in draft_config:
            parts.append("\nYour goals:")
            for goal in draft_config["goals"]:
                parts.append(f"- {goal}")
        
        # Quality standards
        if "quality_standards" in draft_config:
            parts.append("\nQuality Standards:")
            for standard, description in draft_config["quality_standards"].items():
                parts.append(f"**{standard.replace('_', ' ').title()}:** {description}")
        
        # Rules
        if "rules" in draft_config:
            rules = draft_config["rules"]
            if "do" in rules:
                parts.append("\nDO:")
                for rule in rules["do"]:
                    parts.append(f"- {rule}")
            if "do_not" in rules:
                parts.append("\nDO NOT:")
                for rule in rules["do_not"]:
                    parts.append(f"- {rule}")
        
        # Tone and style
        if "tone_and_style" in draft_config:
            tone = draft_config["tone_and_style"]
            parts.append("\nTone and Style:")
            for key, value in tone.items():
                parts.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(parts)
    
    def _enrich_inputs(
        self,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult],
        draft_config: dict
    ) -> dict:
        """
        Use AI to enrich user inputs with detailed, professional content.
        
        Takes brief user inputs and expands them into 2-3 paragraph detailed content.
        Preserves arrays (from multiselect/checkbox inputs) as-is.
        """
        system_message = self._build_system_message(draft_config)
        
        prompt_parts = [
            "# TASK: ENRICH USER INPUTS",
            "",
            "You will receive brief user inputs for a project charter.",
            "Your job is to EXPAND each input into detailed, professional content (2-3 paragraphs each).",
            "Use the project context and step-back analysis to add relevant details.",
            ""
        ]
        
        # Add project context
        if project_context:
            prompt_parts.extend([
                "## PROJECT CONTEXT (use this to enrich inputs)",
                project_context.full_context_text,
                ""
            ])
        
        # Add step-back analysis
        if step_back_result:
            prompt_parts.extend([
                "## STEP-BACK ANALYSIS (use this to enrich inputs)",
                step_back_result.summary,
                ""
            ])
        
        # Separate inputs: strings to enrich vs. arrays/numbers to preserve
        inputs_to_enrich = {}
        inputs_to_preserve = {}
        
        for key, value in user_inputs.items():
            # Skip empty or 'done' values
            if not value or value == 'done':
                continue
            # Preserve lists (from multiselect checkboxes), numbers, bools as-is
            # These come from form controls, not user-written text
            if isinstance(value, (list, int, float, bool)):
                inputs_to_preserve[key] = value
            else:
                # Text and textarea fields get enriched
                inputs_to_enrich[key] = value
        
        # Add inputs to enrich to prompt
        prompt_parts.extend([
            "## USER INPUTS TO ENRICH",
            ""
        ])
        
        for key, value in inputs_to_enrich.items():
            prompt_parts.append(f"### {key}")
            prompt_parts.append(f"Original: {value}")
            prompt_parts.append("")
        
        prompt_parts.extend([
            "## INSTRUCTIONS",
            "",
            "For EACH input above, expand it into detailed, professional content:",
            "- Add 2-3 paragraphs of detail per input",
            "- If the input contains a markdown list (bullets with - or *), expand EACH bullet point",
            "- **CRITICAL:** Use SPECIFIC numbers, metrics, and data points from the Project Context notes",
            "- Examples: dollar amounts, headcount, percentages, timelines, rates",
            "- DO NOT use vague terms like 'significant' or 'substantial' when specific numbers exist in notes",
            "- Reference specific roles, departments, and stakeholders mentioned in the context",
            "- Maintain professional PM tone while being concrete and data-driven",
            "",
            "Return ONLY a JSON object with enriched values:",
            '{"input_name": "enriched content here (2-3 paragraphs)", ...}',
            "",
            "IMPORTANT: Return ONLY valid JSON, no other text."
        ])
        
        prompt = "\n".join(prompt_parts)
        
        # Generate enriched inputs
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.7,
            max_tokens=6000  # Increased for detailed content
        )
        
        try:
            # Claude sometimes wraps JSON in markdown code blocks
            content = response.content.strip()
            
            # Remove markdown code fences
            if content.startswith("```"):
                # Find the actual JSON content
                lines = content.split("\n")
                # Remove first line (```json or ```) and find closing ```
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith("```") and not in_json:
                        in_json = True
                        continue
                    elif line.strip() == "```" and in_json:
                        break
                    elif in_json:
                        json_lines.append(line)
                content = "\n".join(json_lines).strip()
            
            # Try to parse JSON
            enriched = json.loads(content)
            
            # Validate it's a dict
            if not isinstance(enriched, dict):
                raise ValueError("Response is not a JSON object")
            
            # Add back preserved inputs (arrays, numbers, dates)
            enriched.update(inputs_to_preserve)
            # Add back any inputs that weren't enriched
            for key, value in user_inputs.items():
                if key not in enriched:
                    enriched[key] = value
            # Track tokens
            enriched['_tokens_used'] = response.tokens_used
            return enriched
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback: return original inputs
            print(f"Failed to parse enriched inputs: {e}")
            print(f"Response length: {len(response.content)}")
            print(f"Response start: {response.content[:200]}")
            print(f"Response end: {response.content[-200:]}")
            # Return originals with token tracking
            result = user_inputs.copy()
            result['_tokens_used'] = response.tokens_used
            return result
    
    def _render_template(
        self,
        template_name: str,
        enriched_inputs: dict
    ) -> str:
        """
        Render Jinja2 template with enriched input values.
        """
        # Get template path
        template_path = self.blueprint_registry.get_template_path(template_name)
        
        # Set up Jinja2 environment
        template_dir = template_path.parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Load template
        template = env.get_template(template_path.name)
        
        # Convert date strings to datetime objects if needed
        context = enriched_inputs.copy()
        if 'charter_date' in context and isinstance(context['charter_date'], str):
            try:
                context['charter_date'] = datetime.strptime(context['charter_date'], '%Y-%m-%d')
            except:
                context['charter_date'] = datetime.now()
        
        # Render template
        rendered = template.render(**context)
        return rendered
    
    def _generate_with_field_enrichment(
        self,
        blueprint,
        draft_config: dict,
        template_name: str,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult]
    ) -> DraftResult:
        """
        Generate draft using field enrichment strategy.
        
        Enrich each user input individually, then render template.
        """
        # Enrich user inputs using AI
        enriched_inputs = self._enrich_inputs(
            user_inputs,
            project_context,
            step_back_result,
            draft_config
        )
        
        # Render template with enriched values
        rendered_content = self._render_template(
            template_name,
            enriched_inputs
        )
        
        # Extract sections
        sections = [section.title for section in blueprint.sections]
        
        return DraftResult(
            content=rendered_content,
            model_used=self.llm_client.model,
            tokens_used=enriched_inputs.get('_tokens_used', 0),
            sections_generated=sections
        )
    
    def _generate_with_skeleton(
        self,
        blueprint,
        prompts: dict,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult]
    ) -> DraftResult:
        """
        Generate draft using Skeleton-of-Thought strategy.
        
        Supports two approaches:
        1. UNIFIED SKELETON (recommended): One skeleton for entire document, parallel section expansion
        2. INDIVIDUAL SKELETONS (legacy): Separate skeleton per section
        
        Uses unified approach if 'unified_skeleton_generation' config exists.
        """
        draft_config = prompts.get("draft_generation", {})
        skeleton_config = prompts.get("skeleton_generation", {})
        unified_skeleton_config = prompts.get("unified_skeleton_generation", {})
        
        total_tokens = 0
        
        # Step 1: Generate skeleton (unified or individual)
        if unified_skeleton_config:
            # Use UNIFIED skeleton approach
            skeleton, tokens = self._generate_unified_skeleton(
                blueprint,
                unified_skeleton_config,
                user_inputs,
                project_context,
                step_back_result
            )
        else:
            # Use traditional INDIVIDUAL skeleton approach
            skeleton, tokens = self._generate_skeleton(
                blueprint,
                skeleton_config,
                user_inputs,
                project_context,
                step_back_result
            )
        total_tokens += tokens
        
        # DEBUG: Log skeleton keys vs blueprint section IDs
        blueprint_ids = [s.id for s in blueprint.sections]
        skeleton_keys = list(skeleton.keys())
        print(f"\n=== SKELETON DEBUG ===")
        print(f"Blueprint section IDs: {blueprint_ids}")
        print(f"Skeleton keys: {skeleton_keys}")
        missing_in_skeleton = set(blueprint_ids) - set(skeleton_keys)
        extra_in_skeleton = set(skeleton_keys) - set(blueprint_ids)
        if missing_in_skeleton:
            print(f"⚠️  Missing in skeleton: {missing_in_skeleton}")
        if extra_in_skeleton:
            print(f"⚠️  Extra in skeleton: {extra_in_skeleton}")
        print(f"======================\n")
        
        # Step 2: Expand each section (with deduplication context)
        # expansion_limits may be in draft_config or at top level
        expansion_limits = draft_config.get("expansion_limits", {})
        if not expansion_limits:
            expansion_limits = prompts.get("expansion_limits", {})
        expanded_sections, tokens = self._expand_sections(
            skeleton,
            draft_config,
            user_inputs,
            project_context,
            step_back_result,
            expansion_limits=expansion_limits
        )
        total_tokens += tokens
        
        # Step 3: Assemble document
        final_document = self._assemble_document(
            blueprint,
            expanded_sections
        )
        
        # Step 4: Add header from user inputs if analysis document
        if 'analysis_title' in user_inputs:
            header_parts = [
                f"# 📊 {user_inputs.get('analysis_title', 'Analysis')}",
                "",
                f"**Time Period:** {user_inputs.get('time_period', 'N/A')}  ",
                f"**Prepared For:** {user_inputs.get('target_audience', 'Stakeholders')}  ",
                f"**Date:** 2025-12-02",
                "",
                "---",
                "",
                final_document,
                "",
                "---",
                "",
                "*Analysis generated by Project Wizard on 2025-12-02*"
            ]
            final_document = "\n".join(header_parts)
        
        sections = [section.title for section in blueprint.sections]
        
        return DraftResult(
            content=final_document,
            model_used=self.llm_client.model,
            tokens_used=total_tokens,
            sections_generated=sections
        )
    
    def _generate_unified_skeleton(
        self,
        blueprint,
        unified_config: dict,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult]
    ) -> tuple[dict, int]:
        """
        Generate a SINGLE unified skeleton for the entire document.
        
        This skeleton:
        - Defines the narrative arc across all sections
        - Assigns unique purpose to each section (no overlap)
        - Provides deduplication rules
        - Gets used to expand all sections in parallel
        
        Returns:
            Tuple of (skeleton dict with section-specific outlines, tokens used)
        """
        system_message = unified_config.get(
            "identity",
            "You are a strategic data analyst creating a unified analytical framework."
        )
        
        # Build prompt
        prompt_parts = [
            "# TASK: CREATE UNIFIED DOCUMENT SKELETON",
            "",
            "Generate a SINGLE cohesive outline for the entire data analysis report.",
            "This skeleton will guide ALL sections, ensuring unified voice and zero redundancy.",
            ""
        ]
        
        # Add goals
        if "goals" in unified_config:
            prompt_parts.append("## Your Goals:")
            for goal in unified_config["goals"]:
                prompt_parts.append(f"- {goal}")
            prompt_parts.append("")
        
        # Add deduplication rules
        if "deduplication_rules" in unified_config:
            prompt_parts.append("## Deduplication Rules (CRITICAL):")
            for rule in unified_config["deduplication_rules"]:
                prompt_parts.append(f"- {rule}")
            prompt_parts.append("")
        
        # Add strategic context
        if step_back_result:
            prompt_parts.extend([
                "## STRATEGIC CONTEXT",
                step_back_result.summary,
                ""
            ])
        
        # Add project context
        if project_context:
            prompt_parts.extend([
                "## PROJECT CONTEXT",
                project_context.full_context_text[:3000],
                ""
            ])
        
        # Add user inputs
        inputs_summary = "\n".join([f"- {k}: {str(v)[:100]}" for k, v in user_inputs.items() if v])
        prompt_parts.extend([
            "## USER INPUTS",
            inputs_summary,
            ""
        ])
        
        # Add section structure
        prompt_parts.extend([
            "## REQUIRED SECTIONS",
            ""
        ])
        for section in blueprint.sections:
            prompt_parts.append(f"### {section.title}")
            prompt_parts.append(f"Description: {section.description}")
            prompt_parts.append("")
        
        # Add example structure
        if "instructions" in unified_config:
            prompt_parts.append("## Instructions:")
            for instruction in unified_config["instructions"]:
                prompt_parts.append(instruction)
            prompt_parts.append("")
        
        # Add output format
        section_ids_list = [section.id for section in blueprint.sections]
        prompt_parts.extend([
            "## OUTPUT FORMAT",
            "",
            "Return a JSON object with this structure:",
            "{",
        ])
        for section_id in section_ids_list:
            prompt_parts.append(f'  "{section_id}": {{')
            prompt_parts.append('    "purpose": "Unique role of this section",  ')
            prompt_parts.append('    "key_points": ["Point 1", "Point 2", "Point 3"],  ')
            prompt_parts.append('    "data_to_include": ["Specific metrics or tables"],  ')
            prompt_parts.append('    "connection_to_narrative": "How this fits the overall story"')
            prompt_parts.append('  },')
        prompt_parts.append("  ... (repeat for all sections)")
        prompt_parts.extend([
            "}",
            "",
            "CRITICAL REQUIREMENTS:",
            f"- Return EXACTLY {len(section_ids_list)} sections: {', '.join(section_ids_list)}",
            "- Each section must have unique purpose (NO OVERLAP)",
            "- Key points must be specific and concrete",
            "- Ensure the narrative flows: Executive Summary → Trends → Findings → Conclusions",
            "- Return ONLY valid JSON with NO markdown formatting, no other text."
        ])
        
        prompt = "\n".join(prompt_parts)
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=12000  # Generous for unified skeleton
        )
        
        # Parse unified skeleton
        try:
            content = response.content.strip()
            print(f"\n=== RAW UNIFIED SKELETON (first 1000 chars) ===")
            print(content[:1000])
            print(f"=== END (total length: {len(content)}) ===")
            
            # Remove markdown code fences if present
            if content.startswith("```"):
                lines = content.split("\n")
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith("```") and not in_json:
                        in_json = True
                        continue
                    elif line.strip() == "```" and in_json:
                        break
                    elif in_json:
                        json_lines.append(line)
                content = "\n".join(json_lines).strip()
            
            skeleton = json.loads(content)
            print(f"\n[OK] Successfully parsed unified skeleton with {len(skeleton)} sections")
            
            # Verify all required sections are present
            required_section_ids = {s.id for s in blueprint.sections}
            skeleton_section_ids = set(skeleton.keys())
            missing_sections = required_section_ids - skeleton_section_ids
            
            if missing_sections:
                print(f"[WARNING] Unified skeleton missing {len(missing_sections)} sections: {missing_sections}")
                print(f"   Adding fallback skeletons...")
                
                for section_id in missing_sections:
                    section = next((s for s in blueprint.sections if s.id == section_id), None)
                    if section:
                        skeleton[section_id] = {
                            "purpose": section.description,
                            "key_points": ["Key insight 1", "Key insight 2"],
                            "data_to_include": ["Relevant metrics"],
                            "connection_to_narrative": f"Contributes to overall analysis"
                        }
                        print(f"   [OK] Added fallback for: {section_id}")
            
            return skeleton, response.tokens_used
            
        except json.JSONDecodeError as e:
            print(f"\n[ERROR] Failed to parse unified skeleton JSON")
            print(f"Error: {e}")
            print(f"\nRaw response (first 1500 chars):\n{response.content[:1500]}")
            print(f"\nRaw response (last 500 chars):\n{response.content[-500:]}")
            
            # Fallback: create basic skeleton from blueprint
            skeleton = {}
            for section in blueprint.sections:
                skeleton[section.id] = {
                    "purpose": section.description,
                    "key_points": ["Key insight 1", "Key insight 2"],
                    "data_to_include": ["Relevant metrics"],
                    "connection_to_narrative": "Part of overall analysis"
                }
            return skeleton, response.tokens_used
    
    def _generate_skeleton(
        self,
        blueprint,
        skeleton_config: dict,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult]
    ) -> tuple[dict, int]:
        """
        Generate document skeleton (outline with key points).
        
        Returns:
            Tuple of (skeleton dict, tokens used)
        """
        system_message = skeleton_config.get(
            "identity",
            "You are a document architect creating detailed outlines."
        )
        
        prompt_parts = [
            "# TASK: CREATE DOCUMENT SKELETON",
            "",
            "Generate a detailed outline for a professional document.",
            "For each section, provide:",
            "- Section title",
            "- 3-5 key points to cover",
            "- Specific data/metrics to include",
            ""
        ]
        
        # Add step-back summary (most important context)
        if step_back_result:
            prompt_parts.extend([
                "## STRATEGIC CONTEXT (use this as your guide)",
                step_back_result.summary,
                ""
            ])
        
        # Add project context
        if project_context:
            prompt_parts.extend([
                "## PROJECT CONTEXT",
                project_context.full_context_text[:3000],  # Truncate if needed
                ""
            ])
        
        # Add user inputs summary
        inputs_summary = "\n".join([f"- {k}: {str(v)[:100]}..." for k, v in user_inputs.items() if v])
        prompt_parts.extend([
            "## USER INPUTS",
            inputs_summary,
            ""
        ])
        
        # Add section structure from blueprint
        prompt_parts.extend([
            "## REQUIRED SECTIONS",
            ""
        ])
        for section in blueprint.sections:
            prompt_parts.append(f"### {section.title}")
            prompt_parts.append(f"Description: {section.description}")
            if section.subsections:
                prompt_parts.append("Subsections:")
                for subsection in section.subsections:
                    prompt_parts.append(f"  - {subsection.title}: {subsection.description}")
            prompt_parts.append("")
        
        # Build the expected section IDs explicitly
        section_ids_list = [section.id for section in blueprint.sections]
        
        prompt_parts.extend([
            "## OUTPUT FORMAT",
            "",
            "Return a JSON object with this EXACT structure.",
            f"**CRITICAL: Use these EXACT section IDs as keys: {section_ids_list}**",
            "",
            "{",
            '  "section_id": {',
            '    "title": "Section Title",',
            '    "key_points": [',
            '      "Point 1 with specific data",',
            '      "Point 2 with metrics",',
            '      "Point 3 with context"',
            '    ],',
            '    "data_to_include": ["$X amount", "Y% rate", "Z timeline"]',
            '  }',
            "}",
            "",
            "REQUIREMENTS:",
            f"- JSON must have EXACTLY these {len(section_ids_list)} keys: {', '.join(section_ids_list)}",
            "- Use SPECIFIC numbers, metrics, dollar amounts from the context",
            "- Each key_point should be concrete and actionable",
            "- Focus on high-value information for executive decision-making",
            "",
            "Return ONLY valid JSON with NO markdown formatting, no other text."
        ])
        
        prompt = "\n".join(prompt_parts)
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=16000  # Increased significantly to prevent JSON truncation for complex documents
        )
        
        # Check if response was truncated
        if response.finish_reason == "length":
            print(f"\n⚠️  WARNING: LLM response hit max_tokens limit ({response.tokens_used} tokens)")
            print(f"   Skeleton may be incomplete. Consider increasing max_tokens or simplifying the prompt.")
        
        # Parse skeleton
        try:
            content = response.content.strip()
            print(f"\n=== RAW SKELETON RESPONSE (first 1000 chars) ===")
            print(content[:1000])
            print(f"=== END (total length: {len(content)}) ===")
            
            if content.startswith("```"):
                lines = content.split("\n")
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith("```") and not in_json:
                        in_json = True
                        continue
                    elif line.strip() == "```" and in_json:
                        break
                    elif in_json:
                        json_lines.append(line)
                content = "\n".join(json_lines).strip()
            
            skeleton = json.loads(content)
            print(f"\n[OK] Successfully parsed skeleton with {len(skeleton)} sections")
            
            # Verify all required sections are present
            required_section_ids = {s.id for s in blueprint.sections}
            skeleton_section_ids = set(skeleton.keys())
            missing_sections = required_section_ids - skeleton_section_ids
            
            if missing_sections:
                print(f"[WARNING] Skeleton missing {len(missing_sections)} sections: {missing_sections}")
                print(f"   This likely means the LLM response was truncated. Adding fallback skeletons...")
                
                # Add fallback skeletons for missing sections
                for section_id in missing_sections:
                    section = next((s for s in blueprint.sections if s.id == section_id), None)
                    if section:
                        # Create detailed fallback from user inputs
                        key_points = [
                            f"Address: {section.description}",
                            "Use specific data and metrics from the provided inputs",
                            "Maintain professional tone and concrete examples"
                        ]
                        
                        # Add relevant data hints from user inputs
                        data_hints = []
                        for key, value in user_inputs.items():
                            if value and str(value).strip() and value != 'n/a':
                                val_preview = str(value)[:50].strip()
                                if val_preview:
                                    data_hints.append(val_preview)
                                if len(data_hints) >= 3:
                                    break
                        
                        skeleton[section_id] = {
                            "title": section.title,
                            "key_points": key_points,
                            "data_to_include": data_hints
                        }
                        print(f"   [OK] Added fallback skeleton for: {section_id}")
            
            return skeleton, response.tokens_used
            
        except json.JSONDecodeError as e:
            print(f"\n❌ FAILED to parse skeleton JSON")
            print(f"Error: {e}")
            print(f"\nRaw response (first 1500 chars):\n{response.content[:1500]}")
            print(f"\nRaw response (last 500 chars):\n{response.content[-500:]}")
            # Fallback: create basic skeleton from blueprint AND user inputs
            skeleton = {}
            for section in blueprint.sections:
                # Create more detailed fallback key points using section description and relevant user inputs
                key_points = [
                    f"Address: {section.description}",
                    "Use specific data and metrics from the provided inputs",
                    "Maintain professional tone and concrete examples"
                ]
                
                # Add relevant data hints from user inputs
                data_hints = []
                for key, value in user_inputs.items():
                    if value and str(value).strip() and value != 'n/a':
                        # Extract first meaningful piece of data
                        val_preview = str(value)[:50].strip()
                        if val_preview:
                            data_hints.append(val_preview)
                        if len(data_hints) >= 3:
                            break
                
                skeleton[section.id] = {
                    "title": section.title,
                    "key_points": key_points,
                    "data_to_include": data_hints
                }
            return skeleton, response.tokens_used
    
    def _expand_sections(
        self,
        skeleton: dict,
        draft_config: dict,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        step_back_result: Optional[StepBackResult],
        expansion_limits: Optional[dict] = None,
        previously_expanded: Optional[dict] = None
    ) -> tuple[dict, int]:
        """
        Expand skeleton points into full section content.
        
        Args:
            expansion_limits: Optional dict of section_id -> max_tokens for conciseness
            previously_expanded: Sections already generated (for deduplication context)
        
        Returns:
            Tuple of (expanded sections dict, tokens used)
        """
        system_message = self._build_system_message(draft_config)
        expanded = {}
        total_tokens = 0
        previously_expanded = previously_expanded or {}
        expansion_limits = expansion_limits or {}
        
        for section_id, section_skeleton in skeleton.items():
            # Build expansion prompt for this section
            prompt_parts = [
                f"# EXPAND SECTION: {section_skeleton.get('title', section_id)}",
                "",
                "## SKELETON (key points to expand)",
                ""
            ]
            
            for i, point in enumerate(section_skeleton.get("key_points", []), 1):
                prompt_parts.append(f"{i}. {point}")
            
            if section_skeleton.get("data_to_include"):
                prompt_parts.extend([
                    "",
                    "## DATA TO INCLUDE",
                    ", ".join(section_skeleton["data_to_include"])
                ])
            
            prompt_parts.extend([
                "",
                "## FACTUAL GROUNDING (use ONLY this data - DO NOT INVENT)",
                ""
            ])
            
            # Add user inputs for factual grounding
            for key, value in user_inputs.items():
                if value and str(value).strip() and value != 'n/a':
                    # Truncate long values
                    val_str = str(value)[:500] if len(str(value)) > 500 else str(value)
                    prompt_parts.append(f"**{key}**: {val_str}")
            
            prompt_parts.extend([
                "",
                "## STRATEGIC CONTEXT",
                ""
            ])
            
            if step_back_result:
                prompt_parts.append(f"{step_back_result.summary[:2000]}")
            
            if project_context:
                prompt_parts.append(f"\nProject notes: {project_context.full_context_text[:1000]}")
            
            # Add deduplication context if this isn't the first section
            if previously_expanded:
                prompt_parts.extend([
                    "",
                    "## DEDUPLICATION CRITICAL RULE",
                    "",
                    "The following sections have ALREADY been written:",
                    ""
                ])
                for prev_id, prev_content in previously_expanded.items():
                    # Show first 500 chars of previous section as reminder
                    preview = prev_content[:500] if len(prev_content) > 500 else prev_content
                    prompt_parts.append(f"### {prev_id.replace('_', ' ').title()}:")
                    prompt_parts.append(f"{preview}...\n")
                prompt_parts.extend([
                    "**🚨 DO NOT REPEAT THE ABOVE DATA/TABLES/METRICS**",
                    "- If a table was already shown, reference it by section instead of repeating",
                    "- If a calculation was done, mention the result but don't show it again",
                    "- Only include NEW analysis, interpretation, or different perspective",
                    "- Example: Use 'As shown in Executive Summary, MCS devices grew 67%' instead of repeating the table",
                    ""
                ])
            
            prompt_parts.extend([
                "",
                "## CRITICAL RULES (NEVER VIOLATE - YOU WILL BE PENALIZED FOR VIOLATIONS)",
                "",
                "**ANTI-HALLUCINATION REQUIREMENTS:**",
                "",
                "🚫 **ABSOLUTE PROHIBITIONS:**",
                "1. **NO invented names** - If a name isn't in FACTUAL GROUNDING, use generic language (e.g., 'our team' not 'Dr. Smith')",
                "2. **NO invented numbers** - If a metric/amount isn't provided, say 'significant' not '40%' or '$2M'",
                "3. **NO invented dates** - If a date isn't provided, use relative terms ('Q1 2026' not 'March 15, 2026')",
                "4. **NO invented programs/services** - Only mention programs explicitly listed in FACTUAL GROUNDING",
                "5. **NO invented credentials/titles** - Use only titles explicitly provided",
                "6. **NO assumptions** - If something isn't stated, don't fill in the gap with assumptions",
                "",
                "✅ **VERIFICATION CHECKLIST (check EVERY fact):**",
                "- [ ] Is this person's name in FACTUAL GROUNDING?",
                "- [ ] Is this number/metric explicitly stated?",
                "- [ ] Is this date specifically provided?",
                "- [ ] Is this program/service mentioned in the inputs?",
                "- [ ] Am I making ANY assumptions?",
                "",
                "**IF ANY CHECKBOX IS UNCHECKED → USE GENERIC LANGUAGE OR OMIT ENTIRELY**",
                "",
                "## FORMATTING REQUIREMENTS (CRITICAL)",
                "",
                "**This is a business proposal - use visual formatting for scannability:**",
                "",
                "1. **Short Paragraphs**: MAX 3-4 sentences each. Break up long blocks of text.",
                "2. **Bullet Lists**: Use bullets for any list of 3+ items (deliverables, benefits, requirements, activities)",
                "3. **Markdown Tables**: Use tables for structured data:",
                "   - Pricing/fee breakdowns",
                "   - Timelines and milestones",
                "   - Staffing models",
                "   - Deliverables by phase",
                "   - Quality metrics or targets",
                "   - Scope (included/excluded items)",
                "4. **Bold Key Terms**: Bold metrics, dollar amounts, dates, deliverables (e.g., **$6.9M**, **March 2026**, **24/7**)",
                "5. **Mix Formats**: Combine short paragraphs + bullets + tables (where applicable) - NOT walls of text",
                "",
                "**Example table format:**",
                "```",
                "| Component | Details | Timeline |",
                "|-----------|---------|----------|",
                "| Item 1 | Description | Date |",
                "```",
                "",
                "## INSTRUCTIONS",
                "",
                "Expand the key points into well-formatted, scannable content:",
                "- Use specific numbers, metrics, and data points FROM FACTUAL GROUNDING ONLY",
                "- Keep paragraphs SHORT (3-4 sentences maximum)",
                "- Convert any lists into bullet points",
                "- Convert structured data into markdown tables",
                "- Bold all important metrics, deliverables, and key terms",
                "- Mix paragraphs, bullets, and tables for visual variety",
                "- When in doubt about a fact, use generic language instead of inventing",
                "",
                "## FINAL STEP: FACT-CHECK YOUR OUTPUT",
                "",
                "Before returning, scan your draft and remove/replace ANY:",
                "- ❌ Names not in FACTUAL GROUNDING",
                "- ❌ Numbers/percentages you estimated or assumed",
                "- ❌ Specific dates you guessed",
                "- ❌ Programs/services not explicitly mentioned",
                "- ❌ Credentials/titles you inferred",
                "",
                "**Replace hallucinated facts with generic language or remove them.**",
                "",
                "Return ONLY the expanded section content in markdown format.",
                "Do NOT include the section title (it will be added separately)."
            ])
            
            prompt = "\n".join(prompt_parts)
            
            # Use expansion_limits if provided, otherwise default
            max_tokens = expansion_limits.get(section_id, 3000)
            if max_tokens < 300:
                max_tokens = 300  # Minimum to ensure some content
            
            response = self.llm_client.generate(
                prompt=prompt,
                system_message=system_message,
                temperature=0.5,  # Reduced for more conservative, fact-based output
                max_tokens=min(max_tokens, 3000)  # Cap at 3000 even if limit is higher
            )
            
            expanded[section_id] = response.content.strip()
            total_tokens += response.tokens_used
            print(f"\nSection '{section_id}': {len(expanded[section_id])} chars, {response.tokens_used} tokens (limit: {max_tokens})")
        
        return expanded, total_tokens
    
    def _assemble_document(
        self,
        blueprint,
        expanded_sections: dict
    ) -> str:
        """
        Assemble expanded sections into final document.
        
        Args:
            blueprint: Blueprint specification
            expanded_sections: Dict of section_id -> expanded content
            
        Returns:
            Complete markdown document
        """
        document_parts = []
        
        # Sort sections by order
        sorted_sections = sorted(blueprint.sections, key=lambda s: s.order)
        
        for section in sorted_sections:
            # Add section title
            document_parts.append(f"# {section.title}")
            document_parts.append("")
            
            # Add section content
            if section.id in expanded_sections:
                document_parts.append(expanded_sections[section.id])
            else:
                document_parts.append(f"*{section.description}*")
            
            document_parts.append("")
            document_parts.append("---")
            document_parts.append("")
        
        return "\n".join(document_parts)
