# AI Critique Display Fix

## Problem
The AI Quality Critique showed a score of 0% even though the API call was working correctly.

## Root Cause
**Data structure mismatch** between `critic_agent.py` output and `app_streamlit_v2.py` display code.

### What critic_agent Returns:
```json
{
  "scores": [
    {"criterion": "Clarity of Goal", "score": 85, "strengths": "...", "weaknesses": "...", "improvements": "..."},
    ...
  ],
  "weighted_score": 0.82,           // 0.0-1.0 scale
  "approved": true,                 // boolean
  "overall_assessment": "...",       // summary text
  "critical_gaps": ["..."],
  "recommended_next_steps": ["..."]
}
```

### What v2.0 App Expected (incorrectly):
```json
{
  "overall_score": 82,              // percentage
  "passed": true,                   // boolean
  "criteria_scores": {              // dict, not array
    "criterion_name": {"score": 8, "feedback": "..."}
  },
  "summary": "..."                  // different field name
}
```

## Solution
Updated Tab 5 (Quality Review) in `app_streamlit_v2.py` to:

1. **Convert weighted_score to percentage:**
   ```python
   weighted_score = result.get('weighted_score', 0.0)
   overall_score = int(weighted_score * 100)  # 0.82 → 82%
   ```

2. **Use correct boolean field:**
   ```python
   passed = result.get('approved', False)  # was looking for 'passed'
   ```

3. **Iterate scores array correctly:**
   ```python
   scores = result.get('scores', [])  # array, not dict
   for item in scores:
       criterion = item.get('criterion')
       score = item.get('score')  # already 0-100 scale
       strengths = item.get('strengths')
       weaknesses = item.get('weaknesses')
       improvements = item.get('improvements')
   ```

4. **Display all critique components:**
   - Overall score (converted to %)
   - Detailed scores per criterion (with strengths/weaknesses/improvements)
   - Overall assessment (was 'summary')
   - Critical gaps (new)
   - Recommended next steps (new)

## Testing
1. Go to Tab 4 and generate a charter
2. Go to Tab 5 and click "Run Quality Critique"
3. Should now see:
   - Overall score (e.g., 82%)
   - ✅ PASS or ⚠️ NEEDS WORK status
   - 6 expandable criterion sections with detailed feedback
   - Overall assessment summary
   - Critical gaps (if any)
   - Recommended next steps (if any)

## Files Modified
- `app_streamlit_v2.py` - Lines 443-505 (critique display section)
- Backup created: `app_streamlit_v2.py.backup`

## Result
✅ AI Critique now displays correctly with proper scores, feedback, and recommendations!
