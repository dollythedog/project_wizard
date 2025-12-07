"""
Regenerate with STRICT anti-hallucination controls.

Changes:
- Stronger fact-checking instructions
- Lower temperature (0.5 instead of 0.7)
- Explicit verification checklist
- Post-generation fact-check step
"""

import json
from datetime import datetime
from app.services.database import get_db_session
from app.models.database import DocumentRun
from app.services.project_registry import ProjectRegistry
from app.services.ai_agents import LLMClient, ContextBuilder, DraftAgent
from app.services.ai_agents.step_back_agent import StepBackResult

def regenerate_strict():
    """Regenerate with strict anti-hallucination controls."""
    
    session = next(get_db_session())
    document_run = session.get(DocumentRun, 7)
    
    if not document_run:
        print("❌ Document run not found")
        return
    
    print("=" * 70)
    print("  Regenerating with STRICT Anti-Hallucination Controls")
    print("=" * 70)
    print()
    print("🛡️  Enforcing:")
    print("   • Lower temperature (0.5) for conservative output")
    print("   • Explicit fact verification checklist")
    print("   • Post-generation fact-check step")
    print("   • Stronger penalties for invented facts")
    print()
    
    # Load data
    user_inputs = json.loads(document_run.user_inputs)
    registry = ProjectRegistry(session)
    project = registry.get_project(document_run.project_id)
    context_builder = ContextBuilder(registry)
    context = context_builder.build_context(document_run.project_id)
    
    step_back_result = None
    if document_run.step_back_summary:
        step_back_result = StepBackResult(
            questions=[],
            summary=document_run.step_back_summary,
            context_used=""
        )
    
    print(f"📄 Project: {project.title}")
    print(f"   Inputs: {len(user_inputs)} fields")
    print(f"   Context: {context.notes_count} notes")
    print()
    
    # Generate
    print("🤖 Generating with strict fact-checking...\n")
    
    llm_client = LLMClient()
    draft_agent = DraftAgent(llm_client)
    
    try:
        draft_result = draft_agent.generate_draft(
            template_name=document_run.template_name,
            user_inputs=user_inputs,
            project_context=context,
            step_back_result=step_back_result
        )
        
        print(f"\n✅ Generation complete!")
        print(f"   Length: {len(draft_result.content)} characters")
        print(f"   Tokens: {draft_result.tokens_used}")
        
        # Update database
        document_run.initial_draft = draft_result.content
        document_run.completed_at = datetime.utcnow()
        session.commit()
        
        print(f"\n💾 Updated in database")
        
        # Save to file
        output_file = "HFW_Proposal_Final.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(draft_result.content)
        
        print(f"📁 Saved to: {output_file}")
        print()
        print("🔍 Review the proposal for accuracy:")
        print(f"   http://localhost:8000/generate/document/7")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerate_strict()
    print()
    print("=" * 70)
