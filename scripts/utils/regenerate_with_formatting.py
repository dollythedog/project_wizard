"""
Regenerate the HFW Renegotiation proposal with improved formatting:
- Bullet lists
- Tables for structured data
- Bold highlights for key terms
- Short paragraphs
"""

import json
from datetime import datetime
from app.services.database import get_db_session
from app.models.database import DocumentRun
from app.services.project_registry import ProjectRegistry
from app.services.ai_agents import LLMClient, ContextBuilder, DraftAgent
from app.services.ai_agents.step_back_agent import StepBackResult

def regenerate_with_formatting():
    """Regenerate the proposal with better formatting."""
    
    # Get database session
    session = next(get_db_session())
    
    # Load the existing document run
    document_run = session.get(DocumentRun, 7)
    if not document_run:
        print("❌ Document run not found")
        return
    
    print("=" * 70)
    print("  HFW Renegotiation Proposal - Formatting Enhancement")
    print("=" * 70)
    print()
    print(f"📄 Found document: {document_run.template_name}")
    print(f"   Project ID: {document_run.project_id}")
    
    # Load user inputs
    user_inputs = json.loads(document_run.user_inputs)
    print(f"   User inputs loaded: {len(user_inputs)} fields")
    
    # Build project context
    registry = ProjectRegistry(session)
    project = registry.get_project(document_run.project_id)
    
    if not project:
        print("❌ Project not found")
        return
    
    print(f"   Project: {project.title}")
    
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(document_run.project_id)
    print(f"   Context: {context.notes_count} notes, {context.files_count} files")
    
    # Load step-back summary
    step_back_result = None
    if document_run.step_back_summary:
        step_back_result = StepBackResult(
            questions=[],
            summary=document_run.step_back_summary,
            context_used=""
        )
        print(f"   Using existing step-back summary")
    
    # Initialize AI agents
    print("\n🤖 Initializing AI agents with enhanced formatting rules...")
    llm_client = LLMClient()
    draft_agent = DraftAgent(llm_client)
    
    # Generate the complete draft
    print("\n📝 Regenerating proposal with improved formatting...")
    print("   ✨ Applying: bullets, tables, bold highlights, short paragraphs")
    print("   This will take a few minutes...\n")
    
    try:
        draft_result = draft_agent.generate_draft(
            template_name=document_run.template_name,
            user_inputs=user_inputs,
            project_context=context,
            step_back_result=step_back_result
        )
        
        print(f"\n✅ Draft generation complete!")
        print(f"   Content length: {len(draft_result.content)} characters")
        print(f"   Sections: {', '.join(draft_result.sections_generated)}")
        print(f"   Tokens used: {draft_result.tokens_used}")
        print(f"   Model: {draft_result.model_used}")
        
        # Count formatting elements
        bullet_count = draft_result.content.count('\n•') + draft_result.content.count('\n-')
        table_count = draft_result.content.count('|')
        bold_count = draft_result.content.count('**') // 2
        
        print(f"\n📊 Formatting stats:")
        print(f"   Bullets: ~{bullet_count}")
        print(f"   Tables: ~{table_count // 3} (estimated)")  # Approximate
        print(f"   Bold terms: ~{bold_count}")
        
        # Update the document run in database
        document_run.initial_draft = draft_result.content
        document_run.completed_at = datetime.utcnow()
        session.commit()
        
        print(f"\n💾 Database updated successfully!")
        print(f"\nView the formatted proposal at:")
        print(f"   http://localhost:8000/generate/document/{document_run.id}")
        
        # Save to file
        output_file = "HFW_Renegotiation_Proposal_Formatted.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(draft_result.content)
        
        print(f"\n📁 Also saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error generating draft: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerate_with_formatting()
    print()
    print("=" * 70)
