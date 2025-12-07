#!/usr/bin/env python3
"""
Test script to validate data_analysis blueprint produces concise 2-3 page output.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ai_agents import LLMClient, DraftAgent, ContextBuilder
from app.services.blueprint_registry import get_registry

# Sample user inputs that would come from the web form
test_inputs = {
    "business_context": "Requesting additional CVICU staffing to handle increased critical care volume",
    "data_scope": "MCS devices, ECMO, Code Blue events",
    "key_metrics": "Device volumes, monthly trends, growth rates"
}

# Sample project context (minimal for testing)
class MockContext:
    def __init__(self):
        self.notes_count = 1
        self.files_count = 0
        self.full_context_text = """
## Source Data

### MCS Device Usage
- Jan 2024: 9 devices
- Feb 2024: 10 devices
- Mar 2024: 11 devices
- Apr 2024: 12 devices
- May 2024: 13 devices
- Jun 2024: 14 devices
- Oct 2025: 15 devices

### ECMO Device Usage
- Jan 2024: 2-3 devices/month
- Mar 2024: 3-4 devices/month
- Jun 2024: 4-5 devices/month
- Oct 2025: 5-6 devices/month

### Code Blue Events
- Monthly average: 45-75 events
- Consistent throughout 2024-2025
- No significant trend
"""

def test_data_analysis_generation():
    """Test the data_analysis blueprint generation."""
    print("\n" + "="*80)
    print("Testing data_analysis blueprint (should be 2-3 pages max)")
    print("="*80 + "\n")
    
    try:
        # Initialize AI client
        llm_client = LLMClient()
        draft_agent = DraftAgent(llm_client)
        
        # Mock context
        context = MockContext()
        
        # Generate draft
        print("Generating data_analysis document...")
        print("=" * 40)
        
        draft_result = draft_agent.generate_draft(
            template_name="data_analysis",
            user_inputs=test_inputs,
            project_context=context,
            step_back_result=None  # Optional, for this test
        )
        
        # Analyze output
        content = draft_result.content
        word_count = len(content.split())
        line_count = len(content.split('\n'))
        
        # Better page estimate: tables take ~2 words per line, prose ~10 words per line
        # Average ~40 lines per page in markdown
        page_estimate = line_count / 40
        table_count = content.count('|')  # Rough count of markdown tables
        bullet_count = content.count('•') + content.count('-')  # Bullet points
        
        print(f"\n{'DOCUMENT ANALYSIS':^40}")
        print("-" * 40)
        print(f"Word count: {word_count}")
        print(f"Line count: {line_count}")
        print(f"Estimated pages: {page_estimate:.1f}")
        print(f"Table separators (|): {table_count}")
        print(f"Bullet/list items: ~{bullet_count}")
        print(f"Model used: {draft_result.model_used}")
        print(f"Tokens used: {draft_result.tokens_used}")
        print("-" * 40)
        
        # Validation checks
        print(f"\n{'VALIDATION CHECKS':^40}")
        print("-" * 40)
        
        checks = {
            "Under 1500 words": word_count < 1500,
            "Estimated 2-4 pages (line-based)": 2 <= page_estimate <= 4,
            "Not excessive length": word_count < 2000,
        }
        
        for check, result in checks.items():
            status = "PASS" if result else "FAIL"
            symbol = "[OK]" if result else "[!!]"
            print(f"{symbol} {check}: {status}")
        
        # Save full output to file for inspection and print preview
        with open('test_output.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n{'FULL DOCUMENT':^40}")
        print("-" * 40)
        print("Full document saved to test_output.md")
        print("\nFirst 2000 characters:")
        print(content[:2000] if content else "[EMPTY]")
        print("...\n")
        
        # Summary
        all_passed = all(checks.values())
        if all_passed:
            print("[SUCCESS] Document meets all conciseness criteria!")
        else:
            print("[WARNING] Some criteria not met. Review output above.")
        
        return all_passed
        
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_analysis_generation()
    sys.exit(0 if success else 1)
