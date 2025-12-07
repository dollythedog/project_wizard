"""
Regenerate the HFW Renegotiation proposal with all sections complete.

This script:
1. Loads the existing document run data
2. Regenerates the proposal using the fixed draft agent
3. Updates the database with complete content
"""

import json
from datetime import datetime
from app.services.database import get_db_session
from app.models.database import DocumentRun, Project
from app.services.project_registry import ProjectRegistry
from app.services.ai_agents import LLMClient, ContextBuilder, StepBackAgent, DraftAgent
from app.services.ai_agents.self_refine_agent import SelfRefineAgent

def regenerate_proposal():
    """Regenerate the proposal document."""
    
    # Get database session
    session = next(get_db_session())
    
    # Load the existing document run (ID 7)
    document_run = session.get(DocumentRun, 7)
    if not document_run:
        print("❌ Document run not found")
        return
    
    print(f"📄 Found document: {document_run.template_name}")
    print(f"   Project ID: {document_run.project_id}")
    
    # Load user inputs from the existing run
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
    
    # Initialize AI agents
    print("\n🤖 Initializing AI agents...")
    llm_client = LLMClient()
    draft_agent = DraftAgent(llm_client)
    
    # We'll use the existing step-back summary if available
    step_back_result = None
    if document_run.step_back_summary:
        from app.services.ai_agents.step_back_agent import StepBackResult
        step_back_result = StepBackResult(
            questions=[],
            summary=document_run.step_back_summary,
            context_used=""
        )
        print(f"   Using existing step-back summary")
    
    # Generate the complete draft
    print("\n📝 Generating complete proposal...")
    print("   This will take a few minutes as each section is generated...\n")
    
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
        
        # Update the document run in database
        document_run.initial_draft = draft_result.content
        document_run.completed_at = datetime.utcnow()
        session.commit()
        
        print(f"\n💾 Database updated successfully!")
        print(f"\nYou can view the complete proposal at:")
        print(f"   http://localhost:8000/generate/document/{document_run.id}")
        
        # Save to file as well
        output_file = "HFW_Renegotiation_Proposal_Complete.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(draft_result.content)
        
        print(f"\n📁 Also saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error generating draft: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("  HFW Renegotiation Proposal - Complete Regeneration")
    print("=" * 60)
    print()
    regenerate_proposal()
    print()
    print("=" * 60)
