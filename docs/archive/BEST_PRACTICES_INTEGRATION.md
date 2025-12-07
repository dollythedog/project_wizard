# Best Practices Learning System Integration

## Overview

The best practices learning system enables project_wizard to learn from each document generation. By tracking what works and what doesn't, future generations benefit from accumulated knowledge.

## Architecture

### Three Core Components

1. **BestPracticesManager** (`app/services/best_practices_manager.py`)
   - Loads/saves pattern-specific learning data
   - Injects learned context into prompts
   - Updates stats after each generation

2. **SectionAgentController** (updated)
   - Accepts `pattern_name` parameter to load best practices
   - Accepts `charter` parameter for context
   - Injects best practices into section prompts before generation

3. **Generate Route** (`web/routes/generate.py`)
   - Extracts charter from user inputs
   - Passes pattern name and charter to SectionAgentController
   - (Future) Will update best practices after verification

## Data Structure

Each blueprint pattern has a `best_practices.json` file:

```
patterns/
  └── productivity_pulse/
      ├── blueprint.json
      ├── prompts.json
      ├── template.j2
      ├── README.md
      └── best_practices.json  ← NEW
```

### best_practices.json Structure

```json
{
  "pattern_name": "productivity_pulse",
  "generations_count": 0,
  "average_score": 0.0,
  "effective_phrases": {
    "phrases": [
      {
        "phrase": "across our network",
        "usage": "For neutral facility comparisons",
        "example": "ICU assignments across our network show...",
        "score_when_used": 4.0,
        "times_used": 0,
        "avoid_phrases": []
      }
    ]
  },
  "acronyms_and_conventions": {
    "standards": [
      {
        "term": "wRVU",
        "full_form": "weighted Relative Value Unit",
        "convention": "First mention: explain briefly...",
        "example": "weighted Relative Value Units (wRVU)...",
        "frequency_in_successful_emails": 0.92
      }
    ]
  },
  "topics_to_avoid": {
    "topics": [
      {
        "topic": "Direct facility-to-facility comparisons",
        "why_problematic": "Creates competitive framing...",
        "example_bad": "Facility A's wRVU/shift (14.2) significantly exceeds...",
        "example_good": "wRVU/shift ranges from 10.1 to 14.2...",
        "score_impact": -0.8,
        "times_triggered": 0
      }
    ]
  },
  "negative_patterns": {
    "patterns": [
      {
        "error_id": "vq_factual_1_hallucination",
        "verification_check": "vq_factual_1",
        "description": "Email contains numbers not in JSON source data",
        "occurrences": 0,
        "last_seen": null,
        "remediation": "Always trace every number back to JSON...",
        "prevention": "Inject JSON snapshot into draft prompt..."
      }
    ]
  }
}
```

## Usage Flow

### For Document Authors (Current)

```
1. Create Project Charter (project_charter_lite)
   ↓
2. Answer Clarification Questions
   ↓
3. Generate Document (e.g., Productivity Pulse Email)
   [During generation, best practices are loaded and injected into prompts]
   ↓
4. Document Generated with learned context applied
```

### Future: Feedback Integration

```
1. Generate Document
   ↓
2. Verification runs, score calculated
   ↓
3. [Future] Call best_practices_mgr.update_after_generation()
   - Update generation count
   - Update average score
   - Track effective phrases used
   - Record failures (for negative patterns)
   ↓
4. Next generation automatically benefits from this data
```

## Example: How It Works

### Month 1: First Productivity Pulse Email

```
User creates charter:
- Goal: "Generate concise, data-driven monthly productivity highlight emails..."
- Success Criteria: "3 paragraphs, accurate metrics, apples-to-apples comparisons..."

During generation:
- SectionAgentController loads best_practices.json for productivity_pulse
- best_practices.json is initially empty (generations_count = 0)
- Sections are generated with baseline prompts

Result: Email scores 4.2/5.0
- Verification catches 1 minor issue (tone slightly competitive)
- Email is refined and sent

[Future: update_after_generation() called]
- generations_count: 0 → 1
- average_score: 0.0 → 4.2
- negative_patterns["vq_alignment_1_competitive_tone"].occurrences: 0 → 1
```

### Month 2: Second Productivity Pulse Email

```
User provides:
- Same charter (already created)
- New JSON data for November

During generation:
- SectionAgentController loads best_practices.json
- NOW it contains:
  - generations_count: 1
  - average_score: 4.2
  - Learned that competitive tone caused -0.6 score impact
  
  ✓ EFFECTIVE PHRASES (already identified):
  - "across our network" (scored 4.0)
  - "opportunity for learning" (scored 4.5)
  
  ✗ TOPICS TO AVOID:
  - "Direct facility comparisons" (-0.8 impact)
  - "Competitive language" (-0.6 impact)

Prompts now include explicit guidance:
  "Use phrases like: 'across our network', 'opportunity for learning'
   AVOID: facility comparisons, competitive language"

Result: Email scores 4.8/5.0 (improvement!)
- No competitive tone detected
- Better neutral framing
- All 3 paragraphs concise and focused

[Future: update_after_generation() called again]
- generations_count: 1 → 2
- average_score: 4.2 → 4.5
- Effective phrases updated with usage counts
```

## API Reference

### BestPracticesManager

```python
from app.services.best_practices_manager import BestPracticesManager

# Initialize for a pattern
manager = BestPracticesManager("productivity_pulse")

# Get context to inject into prompts
context = manager.get_injection_context(charter=charter_dict)

# Update after generation completes (future)
manager.update_after_generation(
    score=4.5,
    verification_results={"vq_factual_1": True, "vq_logical_1": True},
    effective_phrases_used=["across our network", "opportunity for learning"],
    issues_caught=["vq_alignment_1_competitive_tone"]
)

# Add new patterns dynamically
manager.add_effective_phrase(
    phrase="metric shows",
    usage="For neutral metric presentation",
    example="visits/shift shows an average of 12.3",
    score=4.3
)

# Get statistics
stats = manager.get_stats()
# Returns: {
#   "pattern_name": "productivity_pulse",
#   "generations_count": 2,
#   "average_score": 4.5,
#   "effective_phrases_count": 4,
#   "acronyms_count": 4,
#   "topics_to_avoid_count": 5,
#   "negative_patterns_count": 4,
#   "last_updated": "2025-12-06T01:25:00.000Z"
# }
```

### SectionAgentController

```python
from app.services.ai_agents import SectionAgentController, LLMClient

# Initialize WITH pattern name (enables best practices)
llm = LLMClient()
controller = SectionAgentController(llm, blueprint, pattern_name="productivity_pulse")

# Generate sections WITH charter context
sections = controller.generate_all_sections(
    user_inputs=user_inputs,
    prompts=prompts,
    project_context=context,
    charter={
        "project_goal": "Generate concise emails...",
        "success_criteria": "3 paragraphs, accurate metrics...",
        "scope_out": "No rankings, no cross-category comparisons"
    }
)
```

## Next Steps

1. **Implement update_after_generation() calls**
   - After verification completes in verify_draft route
   - Track score and failed verification checks
   - Record caught issues

2. **Create verification scoring in blueprint**
   - Each verification question contributes to overall score
   - Map failing checks to negative patterns
   - Calculate improvement on re-generation

3. **Add best practices stats endpoint**
   - Dashboard showing pattern performance over time
   - Most used phrases
   - Most common issues
   - Learning curve visualization

4. **Implement feedback loop UI**
   - After generation, ask: "Did this email help?"
   - Partner feedback: "Loved the 'opportunity for learning' framing"
   - Update best practices based on human feedback

5. **Extend to other patterns**
   - Apply same system to project_charter_lite
   - Apply to clinical_services_proposal
   - Apply to data_analysis_report

## Testing

### Manual Test

```bash
# 1. Generate first productivity pulse
# - Create Pulses-Productivity project
# - Select productivity_pulse pattern
# - Fill in inputs, answer clarifications
# - Generate email
# - Note the score

# 2. Check best_practices.json was created
# - patterns/productivity_pulse/best_practices.json should exist
# - generations_count should be 0 (not updated yet)
# - effective_phrases should be empty

# 3. Generate second productivity pulse (next month)
# - Same project/pattern
# - New JSON data
# - During generation, look for "LEARNED BEST PRACTICES" section in prompts
# - Note the improved score
```

### Python Test

```python
def test_best_practices_loading():
    mgr = BestPracticesManager("productivity_pulse")
    
    # Should load successfully
    assert mgr.pattern_name == "productivity_pulse"
    
    # Should have injected context
    context = mgr.get_injection_context()
    assert "PROJECT CHARTER" in context or context == ""  # Empty on first run
    
    # Should have stats
    stats = mgr.get_stats()
    assert stats["pattern_name"] == "productivity_pulse"
    assert stats["generations_count"] >= 0

test_best_practices_loading()
```

## Known Limitations

1. **First generation**: best_practices.json will be mostly empty, so no learned context yet
2. **Manual updates**: Currently requires future implementation of update_after_generation() to populate best practices
3. **Across patterns**: Each pattern learns independently (good for specialization, but no cross-pattern learning)
4. **Static context**: Best practices are re-loaded at start of generation (not live-updated during)

## Future Enhancements

- [ ] Live best practices dashboard
- [ ] Community best practices sharing
- [ ] Pattern versioning (v1.0, v1.1)
- [ ] A/B testing different phrase alternatives
- [ ] Machine learning over longer timescales
