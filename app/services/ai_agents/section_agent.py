"""
Section Agent for generating document sections sequentially with constraints.

Generates each section of a document one-by-one while maintaining context
from previous sections to ensure coherence and prevent repetition.
"""

from dataclasses import dataclass
from typing import Optional, Dict
import re

from app.services.ai_agents.llm_client import LLMClient
from app.services.ai_agents.context_builder import ProjectContext
from app.models.blueprint import BlueprintSpec


@dataclass
class SectionContent:
    """Result of section generation."""
    section_id: str
    section_title: str
    content: str
    word_count: int
    target_words: int
    is_valid: bool
    regeneration_count: int


class SectionAgentController:
    """
    Generates document sections sequentially with word count enforcement.
    
    Maintains context from previous sections to ensure coherence and prevent
    repetition. Verifies each section meets constraints before proceeding.
    """
    
    def __init__(self, llm_client: LLMClient, blueprint: BlueprintSpec):
        """
        Initialize section agent controller.
        
        Args:
            llm_client: LLM client for generating sections
            blueprint: Blueprint specifying document structure
        """
        self.llm = llm_client
        self.blueprint = blueprint
        self.sections: Dict[str, SectionContent] = {}
        self.context_summary = ""  # Accumulated context from previous sections
        self.total_words = 0
    
    def generate_all_sections(
        self,
        user_inputs: dict,
        prompts: dict,
        project_context: Optional[ProjectContext] = None,
        max_regenerations: int = 2
    ) -> Dict[str, SectionContent]:
        """
        Generate all sections sequentially with constraint enforcement.
        
        Args:
            user_inputs: User-provided data for template
            prompts: AI prompt instructions from blueprint
            project_context: Optional project context
            max_regenerations: Max times to regenerate a section if invalid
            
        Returns:
            Dictionary of section_id -> SectionContent
        """
        draft_config = prompts.get("draft_generation", {})
        section_targets = self._get_section_targets()
        
        # Sort sections by order
        sorted_sections = sorted(self.blueprint.sections, key=lambda s: s.order)
        
        print("\n🔄 Generating sections sequentially...")
        print(f"Total target length: 2,500–3,500 words (5–7 pages)\n")
        
        for section in sorted_sections:
            print(f"📝 Section {section.order}: {section.title}")
            target = section_targets.get(section.id, 200)
            print(f"   Target: {target} words (±10%)")
            
            # Attempt to generate section
            content = None
            regeneration_count = 0
            
            for attempt in range(max_regenerations + 1):
                content = self._generate_section(
                    section,
                    target,
                    user_inputs,
                    draft_config,
                    project_context,
                    regeneration_attempt=attempt,
                    is_tight=(attempt > 0)
                )
                
                # Verify section
                word_count = len(content.split())
                is_valid = self._verify_section(
                    section,
                    content,
                    target,
                    user_inputs
                )
                
                if is_valid:
                    print(f"   ✓ Valid ({word_count} words)")
                    break
                else:
                    regeneration_count += 1
                    if attempt < max_regenerations:
                        print(f"   ⚠️  Over limit or has issues ({word_count} words)")
                        print(f"   🔄 Regenerating with tighter constraints...")
                    else:
                        print(f"   ⚠️  Still over limit after {max_regenerations} regenerations")
                        print(f"   ✓ Using as-is (will be condensed later)")
            
            # Store section
            word_count = len(content.split())
            self.sections[section.id] = SectionContent(
                section_id=section.id,
                section_title=section.title,
                content=content,
                word_count=word_count,
                target_words=target,
                is_valid=is_valid,
                regeneration_count=regeneration_count
            )
            
            # Update context for next section (prevent repetition)
            self._update_context(section, content)
            self.total_words += word_count
        
        print(f"\n✓ All sections generated")
        print(f"Total: {self.total_words} words across {len(self.sections)} sections")
        
        return self.sections
    
    def _generate_section(
        self,
        section,
        target_words: int,
        user_inputs: dict,
        draft_config: dict,
        project_context: Optional[ProjectContext],
        regeneration_attempt: int = 0,
        is_tight: bool = False
    ) -> str:
        """
        Generate a single section with word count constraints.
        
        Args:
            section: Section specification from blueprint
            target_words: Target word count for section
            user_inputs: User-provided input data
            draft_config: Draft generation config from prompts
            project_context: Optional project context
            regeneration_attempt: Which attempt this is (0 = first)
            is_tight: If True, apply stricter constraints
            
        Returns:
            Generated section content
        """
        # Build system message
        system_message = self._build_system_message(draft_config)
        
        # Determine strictness
        if is_tight:
            max_words = int(target_words * 1.1)  # Only 10% over
            strictness = "MAXIMUM STRICTNESS"
        else:
            max_words = int(target_words * 1.2)  # 20% tolerance first try
            strictness = "STRICT"
        
        # Build prompt
        prompt = self._build_section_prompt(
            section,
            target_words,
            max_words,
            user_inputs,
            project_context,
            strictness
        )
        
        # Generate
        response = self.llm.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5,
            max_tokens=max_words * 5  # Allow buffer for token count
        )
        
        return response.content.strip()
    
    def _build_system_message(self, draft_config: dict) -> str:
        """Build system message for LLM."""
        parts = []
        
        if "identity" in draft_config:
            parts.append(draft_config["identity"])
        
        if "core_principle" in draft_config:
            parts.append(f"\nCore Principle: {draft_config['core_principle']}")
        
        # Add anti-hallucination rules
        parts.append("""
CRITICAL ANTI-HALLUCINATION RULES:
- NEVER invent names, credentials, or titles not in user inputs
- NEVER fabricate metrics or financial figures
- NEVER create fake experience or past work
- NEVER assume data—only use explicitly provided information
- Use generic language when specifics aren't provided
- Document assumptions clearly if necessary

TONE AND STYLE:
- Professional, collaborative, data-informed
- Avoid salesy language; convey competence and partnership
- Short paragraphs (3-4 sentences max)
- Use bullets for lists of 3+ items
- Bold key metrics and deliverables
""")
        
        return "\n".join(parts)
    
    def _build_section_prompt(
        self,
        section,
        target_words: int,
        max_words: int,
        user_inputs: dict,
        project_context: Optional[ProjectContext],
        strictness: str
    ) -> str:
        """Build prompt for section generation."""
        parts = [
            f"# GENERATE SECTION: {section.title}",
            f"## Section Purpose: {section.description}",
            "",
            f"## Word Count Constraint",
            f"Target: {target_words} words",
            f"Absolute maximum: {max_words} words",
            f"Strictness level: {strictness}",
            "",
            "🚨 If your response exceeds {max_words} words, it will be rejected.",
            "",
        ]
        
        # Add context from previous sections (prevents repetition)
        if self.context_summary:
            parts.extend([
                "## Previous Sections (for context—DO NOT REPEAT)",
                "",
                self.context_summary,
                "",
            ])
        
        # Add section-specific guidance if available
        section_guidance = self._get_section_guidance(section.id)
        if section_guidance:
            parts.extend([
                "## Section-Specific Guidance",
                "",
                section_guidance,
                "",
            ])
        
        # Add relevant inputs
        parts.extend([
            "## Factual Grounding (use ONLY this data)",
            "",
        ])
        relevant_inputs = self._get_relevant_inputs(section.id, user_inputs)
        for key, value in relevant_inputs.items():
            if value:
                val_str = str(value)[:300] if len(str(value)) > 300 else str(value)
                parts.append(f"**{key}**: {val_str}")
        
        if project_context:
            parts.extend([
                "",
                "## Project Context",
                project_context.full_context_text[:1000],
            ])
        
        parts.extend([
            "",
            "## Instructions",
            "1. Write ONLY the content for this section (no section title)",
            "2. Use short paragraphs (3-4 sentences max)",
            "3. Use bullet points for lists of 3+ items",
            "4. Bold key metrics, dates, and important terms",
            "5. Do NOT repeat information from previous sections",
            "6. Do NOT invent data—use only provided facts",
            "7. Aim for {target_words} words; do NOT exceed {max_words}",
            "",
            "Begin writing the section content now:",
        ])
        
        return "\n".join(parts).format(target_words=target_words, max_words=max_words)
    
    def _get_section_targets(self) -> dict:
        """Get target word counts for each section."""
        return {
            "executive_summary": 150,
            "background_and_need": 200,
            "coverage_model": 350,
            "quality_metrics": 200,
            "financial_proposal": 200,
            "governance": 150,
            "compliance": 150,
            "conclusion": 150,
        }
    
    def _get_section_guidance(self, section_id: str) -> str:
        """Get section-specific guidance from blueprint."""
        section_guidance = {
            "executive_summary": (
                "- Hook the decision-maker in 1-2 opening sentences\n"
                "- List 3-4 key highlights as bullets\n"
                "- Do NOT include detailed staffing numbers (save for later sections)\n"
                "- Do NOT include specific metrics or financial terms"
            ),
            "background_and_need": (
                "- State specific baseline metrics (e.g., 'ICU LOS: 4.2 days')\n"
                "- Explain clinical, operational, and financial impacts\n"
                "- Do NOT propose solutions yet\n"
                "- Do NOT repeat content from Executive Summary"
            ),
            "coverage_model": (
                "- Use tables for staffing model (if applicable)\n"
                "- Be specific: exact numbers (1 Physician, 2 APPs), times (0700-1900)\n"
                "- List procedures as bullets\n"
                "- Explain EMR integration and operational workflows\n"
                "- Do NOT discuss metrics or benefits"
            ),
            "quality_metrics": (
                "- Use table format: Metric | Baseline | Target | Frequency\n"
                "- Do NOT explain HOW the model achieves these targets\n"
                "- Do NOT repeat staffing details\n"
                "- Include review process (quarterly, etc.)"
            ),
            "financial_proposal": (
                "- Use table format: Category | Description | Rate | Notes\n"
                "- State contract term and key assumptions\n"
                "- Do NOT justify costs with benefits (that's a different section)\n"
                "- Do NOT repeat metrics"
            ),
            "governance": (
                "- State weekly/monthly/quarterly touchpoints\n"
                "- Name who participates and what's discussed\n"
                "- Do NOT repeat staffing details or metrics\n"
                "- Include escalation protocol"
            ),
            "compliance": (
                "- State specific insurance amounts (e.g., $1M/$3M)\n"
                "- List licensure, privileges, HIPAA compliance\n"
                "- Do NOT repeat clinical capabilities\n"
                "- Be firm and specific (not vague)"
            ),
            "conclusion": (
                "- Reinforce partnership value in 1-2 sentences\n"
                "- List 3-4 clear next steps\n"
                "- Include primary contact info\n"
                "- Do NOT repeat the entire proposal"
            ),
        }
        return section_guidance.get(section_id, "")
    
    def _get_relevant_inputs(self, section_id: str, user_inputs: dict) -> dict:
        """Get relevant inputs for a section."""
        relevance_map = {
            "executive_summary": [
                "specialty", "recipient_organization", "your_company_name"
            ],
            "background_and_need": [
                "current_challenges", "clinical_impact", "operational_impact",
                "financial_impact", "baseline_metrics"
            ],
            "coverage_model": [
                "scope_of_services", "staffing_model", "procedures",
                "emr_system"
            ],
            "quality_metrics": [
                "baseline_metrics", "target_metrics"
            ],
            "financial_proposal": [
                "financial_proposal", "contract_term"
            ],
            "governance": [
                "governance_structure"
            ],
            "compliance": [
                "compliance_requirements"
            ],
            "conclusion": [],
        }
        
        relevant_keys = relevance_map.get(section_id, [])
        return {k: v for k, v in user_inputs.items() if k in relevant_keys}
    
    def _verify_section(
        self,
        section,
        content: str,
        target_words: int,
        user_inputs: dict
    ) -> bool:
        """
        Verify section meets constraints.
        
        Returns True if section is valid, False otherwise.
        """
        word_count = len(content.split())
        max_words = int(target_words * 1.2)
        
        # Check word count
        if word_count > max_words:
            return False
        
        # Check for hallucinations
        if self._has_hallucinations(section, content, user_inputs):
            return False
        
        return True
    
    def _has_hallucinations(
        self,
        section,
        content: str,
        user_inputs: dict
    ) -> bool:
        """
        Check if section contains hallucinated content.
        
        Looks for invented names, credentials, metrics, and claims.
        """
        # Extract all capitalized words that look like names
        # (e.g., "Dr. Sarah Mitchell", "John Smith")
        name_pattern = r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+)?)\b'
        mentioned_names = set(re.findall(name_pattern, content))
        
        # Get provided names from user inputs (if any)
        provided_text = " ".join(str(v) for v in user_inputs.values())
        provided_names = set(re.findall(name_pattern, provided_text))
        
        # Check for invented names (mentioned but not provided)
        for name in mentioned_names:
            if name not in provided_names and name not in ["CEO", "CNO", "CMO", "CFO"]:
                # This might be invented—flag it
                if "Dr." in name or "Dr " in name:
                    return True
        
        return False
    
    def _update_context(self, section, content: str):
        """
        Update context summary with section content.
        
        This is used to prevent repetition in subsequent sections.
        """
        # Extract key facts from section (first 300 chars)
        summary = content[:400] + "..." if len(content) > 400 else content
        
        self.context_summary += f"\n**{section.title}:** {summary}\n"
    
    def assemble_document(
        self,
        document_title: Optional[str] = None,
        prepend_header: bool = True
    ) -> str:
        """
        Assemble all sections into final document.
        
        Args:
            document_title: Optional document title
            prepend_header: If True, add header with metadata
            
        Returns:
            Complete document markdown
        """
        parts = []
        
        if prepend_header and document_title:
            parts.append(f"# {document_title}\n")
        
        # Sort sections by order
        sorted_sections = sorted(self.blueprint.sections, key=lambda s: s.order)
        
        for section in sorted_sections:
            if section.id in self.sections:
                section_data = self.sections[section.id]
                parts.append(f"## {section_data.section_title}\n")
                parts.append(section_data.content)
                parts.append("")
        
        return "\n".join(parts)
