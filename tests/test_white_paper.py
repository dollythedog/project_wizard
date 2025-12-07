#!/usr/bin/env python
"""Test script to generate white paper draft with clarified focus."""

from app.services.ai_agents.draft_agent import DraftAgent
from app.services.ai_agents.llm_client import LLMClient
from app.services.blueprint_registry import get_registry

# Setup
llm_client = LLMClient()
registry = get_registry()
blueprint = registry.load_blueprint('white_paper')
prompts = registry.load_prompts('white_paper')

# User inputs from form
user_inputs = {
    'paper_title': 'Staffing Proposal',
    'paper_topic': 'This will serve as an explanation of the current staffing model and a new enhanced staffing model to be used by TPCCC. TPCCC provides critical care coverage in the form of physicians and APPs. Currently only two of the physician positions are subsidized and 1 of the APPs and this plan will revamp that.',
    'target_audience': 'Hospital Executives reading a proposal requesting additional staffing',
    'key_argument': 'This plan formalizes an arrangement already in place, clarifying the staffing structure that has enabled TPCCC to support hospital growth.',
    'supporting_evidence': 'Program activity shows increased volumes of high-acuity patients and complexity shifts. TPCCC supports ECMO, interventional pulmonary, GME training, PERT, and Code Blue responses.',
    'desired_action': 'Approve the enhanced staffing plan that formalizes the current partnership',
    'constraints': 'Focus on clearly comparing current staffing model vs. enhanced model. Use tables/diagrams for clarity.'
}

# Step-back responses (from user clarifications)
step_back_answers = """
SCOPE: Current staffing includes 5 daytime physicians (2 subsidized, 3 unsubsidized covering costs) and multiple APPs. Enhanced model formalizes this arrangement with clear role definitions.

HOSPITAL PERSPECTIVE: Hospital executives want to see this as a partnership formalization, not a threat. This is about clarity and continued collaboration on what's already working.

SUCCESS METRIC: Clear side-by-side comparison of current vs. enhanced staffing model showing how the partnership works.

KEY SERVICES: TPCCC supports ECMO, interventional pulmonary, GME training, PERT, Code Blue, and Shock Team operations—integrated services that are central to hospital operations.

TIMELINE: Not urgent/threatening. Both parties are satisfied. This is about formalizing to prevent future instability and clarify roles.
"""

# Mock notes
notes_text = """
CURRENT STAFFING MODEL
- 5 Daytime Physicians: 2 subsidized positions, 3 positions covered by group
- APP Coverage: 1 subsidized APP, additional APPs supporting clinical work
- Services: MCS management, ECMO cases, interventional procedures, Shock Team, PERT, Code Blue responses, hospital committee participation

VOLUME INDICATORS (supporting need for formalization)
- MCS device volume: 80% growth Jan 2024 - Oct 2025
- High-acuity cases: 33% of device portfolio now (vs 10% baseline)
- Shock Team: 75% growth
- PERT: 150-200% growth
- Code Blue: Sustained 50-60/month demand

ENHANCED MODEL (formalization)
- Clearly defined physician roles and responsibilities
- Formalized APP positions and coverage expectations
- Explicit recognition of institutional services provided
- Structured partnership framework
"""

# Generate draft
draft_agent = DraftAgent(llm_client=llm_client)

try:
    result = draft_agent.generate_draft(
        blueprint=blueprint,
        prompts=prompts,
        user_inputs=user_inputs,
        selected_notes=[{'id': 'mock', 'content': notes_text}],
        step_back_summary=step_back_answers,
        project_context=None
    )
    
    print('=== DRAFT GENERATED ===\n')
    print(result)
    
    # Save to file
    with open('white_paper_draft.md', 'w') as f:
        f.write(result)
    print('\n\n=== Saved to white_paper_draft.md ===')
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
