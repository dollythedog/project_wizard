#!/usr/bin/env python3
"""
Test script for 5W1H pattern pipeline
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.pattern_pipeline import PatternPipeline

def main():
    print("=== 5W1H Pattern Pipeline Test ===\n")
    
    # Initialize components
    print("1. Loading pattern registry...")
    registry = PatternRegistry()
    patterns = registry.list_patterns()
    print(f"   Found patterns: {patterns}\n")
    
    if '5w1h_analysis' not in patterns:
        print("ERROR: 5w1h_analysis pattern not found!")
        return
    
    # Initialize project context (using this project as test)
    print("2. Loading project context...")
    project_path = Path(__file__).parent
    context = ProjectContext(project_path)
    print(f"   Project: {context.get_project_name()}")
    print(f"   Context summary: {context.get_summary()}\n")
    
    # Initialize pipeline
    print("3. Initializing pipeline...")
    pipeline = PatternPipeline(registry, context)
    print("   Pipeline ready\n")
    
    # Test inputs
    print("4. Preparing test inputs...")
    test_inputs = {
        'problem_statement': 'AI enhancement requests are timing out during charter generation, causing user frustration and incomplete documents.',
        'what': 'OpenAI API calls fail with timeout errors after 30 seconds when processing enhancement requests for long charter sections.',
        'when': 'Occurs intermittently, more frequent during peak hours (9am-5pm EST). Happens about 20% of the time.',
        'where': 'In the CharterAgent.enhance_section() method when calling llm.complete() with sections over 500 words.',
        'who': 'Affects: Users trying to generate charters. Discovered by: Beta testers. Can solve: Development team, possibly need to optimize prompts or implement retry logic.',
        'why': 'Leads to incomplete charters, forces users to manually retry, degrades user experience, and reduces trust in the AI features.',
        'how': 'Users click "Enhance" button, see loading spinner for 30+ seconds, then get error message. Logs show OpenAI API timeout exceptions. Pattern correlates with longer input text.'
    }
    
    for key, value in test_inputs.items():
        print(f"   {key}: {value[:80]}...")
    print()
    
    # Execute pipeline
    print("5. Executing pipeline...")
    print("   [This will make API calls - may take 30-60 seconds]\n")
    
    try:
        result = pipeline.execute(
            pattern_name='5w1h_analysis',
            user_inputs=test_inputs,
            enable_editing=True,
            enable_critique=True,
            max_revision_iterations=1,
            project_path=project_path
        )
        
        print("=== PIPELINE COMPLETE ===\n")
        
        # Display results
        print(f"Final Score: {result['final_score']:.2f}" if result['final_score'] else "No critique")
        print(f"Iterations: {result['iterations']}")
        print(f"Document Length: {len(result['document'])} characters\n")
        
        # Show pipeline log
        print("Pipeline Log:")
        for log_entry in result['pipeline_log']:
            stage = log_entry.get('stage', 'unknown')
            if 'length' in log_entry:
                print(f"  - {stage}: {log_entry['length']} chars")
            if 'score' in log_entry:
                print(f"    Score: {log_entry['score']:.2f}")
        print()
        
        # Save document
        output_file = Path("test_5w1h_output.md")
        output_file.write_text(result['document'])
        print(f"✓ Document saved to: {output_file}")
        
        # Show critique summary if available
        if result['critique']:
            print("\nCritique Summary:")
            for score in result['critique'].get('scores', []):
                print(f"  - {score['criterion']}: {score['score']}/100")
        
        print("\n=== TEST SUCCESSFUL ===")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
