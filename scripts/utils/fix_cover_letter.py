"""
Regenerate just the cover letter section with proper bullet format.
"""

import json
from app.services.database import get_db_session
from app.models.database import DocumentRun
from app.services.project_registry import ProjectRegistry
from app.services.ai_agents import LLMClient, ContextBuilder
from app.services.ai_agents.step_back_agent import StepBackResult
from app.services.blueprint_registry import get_registry

def regenerate_cover_letter():
    """Regenerate only the cover letter section."""
    
    # Get database session
    session = next(get_db_session())
    
    # Load the existing document run
    document_run = session.get(DocumentRun, 7)
    if not document_run:
        print("❌ Document run not found")
        return
    
    print(f"📄 Loading proposal data...")
    
    # Load user inputs
    user_inputs = json.loads(document_run.user_inputs)
    
    # Build project context
    registry = ProjectRegistry(session)
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(document_run.project_id)
    
    # Load step-back summary
    step_back_result = None
    if document_run.step_back_summary:
        step_back_result = StepBackResult(
            questions=[],
            summary=document_run.step_back_summary,
            context_used=""
        )
    
    # Initialize LLM
    llm_client = LLMClient()
    
    # Load prompts
    blueprint_registry = get_registry()
    prompts = blueprint_registry.load_prompts("proposal")
    draft_config = prompts.get("draft_generation", {})
    opening_config = draft_config.get("proposal_structure", {}).get("opening", {})
    
    # Build cover letter generation prompt
    print("\n📝 Generating new cover letter with bullet format...\n")
    
    prompt_parts = [
        "# GENERATE COVER LETTER FOR PROPOSAL",
        "",
        "## FORMAT REQUIREMENTS (CRITICAL - DO NOT IGNORE)",
        "",
        "**THE COVER LETTER MUST FIT ON ONE PAGE AND USE BULLET LISTS, NOT PARAGRAPHS**",
        "",
        "### Required Structure:",
        "",
        "```",
        "[Date]",
        "[Recipient Name], [Title]",
        "[Organization]",
        "[Address]",
        "",
        "Subject: Proposal for Critical Care Services",
        "",
        "Dear [Name]:",
        "",
        "During our [meeting/discussions] on [date/timeframe], I gained a deep understanding of the challenges currently faced by [Organization]. The primary concerns you outlined were:",
        "",
        "• [Challenge 1 - ONE LINE ONLY]",
        "• [Challenge 2 - ONE LINE ONLY]",
        "• [Challenge 3 - ONE LINE ONLY]",
        "• [Challenge 4 - ONE LINE ONLY - if applicable]",
        "",
        "At [Your Company], we are uniquely positioned to address these challenges and efficiently meet your objectives, which include:",
        "",
        "• [Objective 1 - ONE LINE ONLY]",
        "• [Objective 2 - ONE LINE ONLY]",
        "• [Objective 3 - ONE LINE ONLY]",
        "• [Objective 4 - ONE LINE ONLY - if applicable]",
        "",
        "Our unique qualifications for consulting and resolving these issues stem from our:",
        "",
        "• [Qualification 1 - ONE LINE ONLY]",
        "• [Qualification 2 - ONE LINE ONLY]",
        "• [Qualification 3 - ONE LINE ONLY]",
        "• [Qualification 4 - ONE LINE ONLY - if applicable]",
        "",
        "We are enthusiastic about the prospect of working with [Organization] and are committed to building success for your critical care operations. Our team is ready to bring our expertise and tailored solutions to enhance both patient care and operational efficiency.",
        "",
        "Sincerely,",
        "",
        "[Signature block]",
        "```",
        "",
        "## FACTUAL GROUNDING (use ONLY this data)",
        ""
    ]
    
    # Add user inputs
    for key, value in user_inputs.items():
        if value and str(value).strip() and value != 'n/a':
            val_str = str(value)[:500] if len(str(value)) > 500 else str(value)
            prompt_parts.append(f"**{key}**: {val_str}")
    
    prompt_parts.extend([
        "",
        "## STRATEGIC CONTEXT",
        ""
    ])
    
    if step_back_result:
        prompt_parts.append(f"{step_back_result.summary[:2000]}")
    
    if context:
        prompt_parts.append(f"\nProject notes: {context.full_context_text[:1000]}")
    
    prompt_parts.extend([
        "",
        "## CRITICAL INSTRUCTIONS",
        "",
        "1. **EACH BULLET MUST BE ONE LINE ONLY** - no multi-sentence bullets",
        "2. Use ONLY factual information from FACTUAL GROUNDING above",
        "3. Extract 3-4 key challenges from the provided context",
        "4. Extract 3-4 key objectives/outcomes the client wants",
        "5. Extract 3-4 unique qualifications of your company",
        "6. Keep opening and closing paragraphs to 1-2 sentences each",
        "7. Use proper business letter format with header",
        "",
        "Return ONLY the complete cover letter in markdown format."
    ])
    
    prompt = "\n".join(prompt_parts)
    
    # Generate
    response = llm_client.generate(
        prompt=prompt,
        system_message="You are an expert business proposal writer. Your cover letters are known for being concise, professional, and easy to read with clear bullet-point structure.",
        temperature=0.7,
        max_tokens=2000
    )
    
    new_cover_letter = response.content.strip()
    
    print("✅ New cover letter generated!")
    print(f"   Length: {len(new_cover_letter)} characters")
    print(f"   Tokens: {response.tokens_used}")
    
    # Replace the cover letter section in the full document
    full_content = document_run.initial_draft
    
    # Find the cover letter section
    if "# Cover Letter" in full_content:
        # Find where it ends (next section starts with #)
        parts = full_content.split("# Cover Letter", 1)
        before = parts[0]
        after = parts[1]
        
        # Find the next section
        next_section_idx = after.find("\n# ")
        if next_section_idx > 0:
            rest_of_doc = after[next_section_idx:]
            
            # Rebuild document
            updated_content = before + "# Cover Letter\n\n" + new_cover_letter + "\n" + rest_of_doc
            
            # Update database
            document_run.initial_draft = updated_content
            session.commit()
            
            print("\n💾 Document updated in database!")
            
            # Save to file
            with open("HFW_Renegotiation_Proposal_Fixed.md", 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("📁 Saved to: HFW_Renegotiation_Proposal_Fixed.md")
            
            # Show preview
            print("\n" + "="*60)
            print("COVER LETTER PREVIEW:")
            print("="*60)
            print(new_cover_letter[:800])
            if len(new_cover_letter) > 800:
                print("\n[... truncated ...]")
            print("="*60)
        else:
            print("❌ Could not find next section marker")
    else:
        print("❌ Could not find cover letter section in document")

if __name__ == "__main__":
    regenerate_cover_letter()
