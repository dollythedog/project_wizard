# Quick Start: Guided Refinement 🎯

## 2-Minute Overview

**Goal:** Take your long/repetitive document and refine it with AI guidance

**Flow:**
```
1. Generate document
2. Click "Review Quality" → Get feedback
3. Click "🎯 Guided Refinement" → Edit recommendations
4. Click "Apply Guided Refinement" → Get refined document
```

---

## Step-by-Step for Project 2

### Step 1: Generate Your Data Analysis Document

Go to your Project 2
1. Click "Generate Document"
2. Select: **data_analysis** template
3. Fill in the form (data range, metrics, audience, etc.)
4. Answer the clarifying questions
5. Get your analysis document (probably 8-12 pages)

### Step 2: Review Quality

From the document view:
1. Click **"Review Quality"** button
2. Wait for AI assessment (20-30 seconds)
3. See:
   - Score (1.0-5.0)
   - Strengths (what's working)
   - Weaknesses (what needs work)
   - Specific recommendations (how to improve)

**If score ≥ 4.0:** Document is good! Skip to Step 5.
**If score < 4.0:** Continue to Step 3.

### Step 3: Enter Guided Refinement

From the review page:
1. Click **"🎯 Guided Refinement"** button
2. See refinement interface with:
   - Editable improvement recommendations (3-5 boxes)
   - Identified issues with checkboxes
   - Focus areas selector
   - Strengths panel
   - Detailed scores

### Step 4: Edit Recommendations

In the "Improvement Recommendations" section:

**Option A: Keep recommendations as-is**
- Just click "Apply Guided Refinement"

**Option B: Edit recommendations** (RECOMMENDED)
```
Example edits for your data_analysis:

BEFORE (AI suggested):
  "Remove repetition"

AFTER (you specify):
  "Remove repetition: Mention each key metric once, then use 
   cross-references like 'As shown in Table 1' instead of repeating"

---

BEFORE:
  "Condense document"

AFTER:
  "Reduce document from 8,500 to 5,000 words by consolidating 
   similar findings and moving detailed analysis to appendix"

---

BEFORE:
  "Improve data presentation"

AFTER:
  "Convert the Metrics section from paragraphs to a clean 
   table with columns: Category, Q1, Q2, Q3, Q4, YTD Change"
```

**Option C: Add custom improvements**
```
Click "+ Add Custom Improvement" and add:
  - "Add year-over-year comparison for trending metrics"
  - "Bold all percentages and dollar amounts"
  - "Create summary table of key findings (top 5 metrics)"
```

**Option D: Use issues checkboxes**
- If any weaknesses are shown, click checkboxes to add them
- They'll automatically add to improvements list

### Step 5: Select Focus Areas (Optional)

Check boxes for sections to prioritize:
- ☑ Executive Summary
- ☑ Key Findings / Results
- ☐ Recommendations
- ☐ Clarity & Conciseness
- ☑ Data Quality & Accuracy

(This tells AI: "Pay extra attention to these areas")

### Step 6: Apply Refinement

1. Click **"✨ Apply Guided Refinement"** button
2. **Wait** (30-45 seconds for AI to process)
3. See refined document appear
4. Refined version will show:
   - Summary of improvements applied
   - Model used (GPT-4 or Claude)
   - Tokens consumed
   - Updated document

### Step 7: Check Results

Compare original vs. refined:

**Original:**
- 8,500 words
- Metrics repeated throughout
- Long paragraphs
- Data embedded in text

**Refined:**
- 5,500 words (35% shorter)
- Metrics mentioned once + cross-referenced
- Shorter paragraphs (3-4 sentences max)
- Metrics in table format
- Bold amounts and percentages

### Step 8: Export or Refine Again

**Export:**
```
Click "Download" → Get refined.md file
```

**Refine Again:**
```
Click "Review Quality" on refined document
→ Check new score (should be higher!)
→ Click "Guided Refinement" again for second pass
→ Make more specific edits
→ Apply refinement again
```

**Edit Manually:**
```
Click "Edit" on markdown source
→ Make manual tweaks
→ Save changes
```

---

## Common Edits to Try

### Edit 1: Condensing
```
ORIGINAL: "Condense document"
REFINED:  "Reduce word count from X to Y by removing 
           repetitive sections and condensing paragraphs 
           to 2-3 sentences each"
```

### Edit 2: Data Quality
```
ORIGINAL: "Fix data inconsistencies"
REFINED:  "Verify all numbers and percentages against 
           source data in project notes. Flag any 
           calculations that don't match and recalculate"
```

### Edit 3: Clarity
```
ORIGINAL: "Improve clarity"
REFINED:  "Replace technical jargon with plain language. 
           Add 1-2 sentence explanation for each key metric 
           explaining what it means to business"
```

### Edit 4: Structure
```
ORIGINAL: "Improve organization"
REFINED:  "Add Executive Summary as first section (2-3 
           sentences). Reorganize findings: start with 
           biggest opportunities, end with risks"
```

### Edit 5: Formatting
```
ORIGINAL: "Improve formatting"
REFINED:  "Convert Metrics section to table format. 
           Bold all dollar amounts, percentages, and 
           timeline dates. Add bullet lists for 
           recommendations"
```

---

## Pro Tips

### Tip 1: Be Specific
❌ "Make it better" 
✅ "Reduce from 8500 to 5500 words"

### Tip 2: Show Examples
❌ "Improve clarity"
✅ "Replace '5% increase' with '6% increase (specific metric)'"

### Tip 3: Reference Sections
❌ "Use tables"
✅ "Convert the Metrics Analysis section to a table with columns: Category, Value, Change %"

### Tip 4: Focus on Top Issues
❌ Add 10 improvements
✅ Add 3-5 most important improvements

### Tip 5: Iterate
1. First pass: 2-3 edits → Review → Check score
2. Second pass: More specific edits → Review → Check score
3. Final pass: Polish formatting → Done

---

## Expected Results

### For Long Documents (8+ pages)
- **Before:** 8,500 words, repetitive, long paragraphs
- **After:** 5,500 words, concise, tables, cross-references
- **Score improvement:** 3.2/5 → 4.0/5

### For Repetitive Documents
- **Before:** Key metrics mentioned 5+ times each
- **After:** Each metric mentioned once, then cross-referenced
- **Score improvement:** 2.8/5 → 3.8/5

### For Data-Heavy Documents
- **Before:** Metrics embedded in text paragraphs
- **After:** Metrics in tables, summaries in text
- **Score improvement:** 3.0/5 → 4.2/5

---

## Troubleshooting

### Problem: Document still too long
**Solution:** 
- Be more aggressive: "Reduce to 4000 words" (not 5500)
- Add: "Move all detailed analysis to appendix"
- Focus on: "Executive Summary"

### Problem: Not condensed enough
**Solution:**
- Check: Did you specify a target word count?
- Add: "Remove all repetitive sections"
- Add: "Use cross-references instead of repeating data"

### Problem: Data disappeared
**Solution:**
- This shouldn't happen (AI preserves data)
- Try again with edit: "Preserve all data and numbers"
- Check your improvements for "remove" language

### Problem: Format didn't change
**Solution:**
- Be specific: "Create a markdown table with columns..."
- Add: "Convert paragraphs to bullet lists"
- Use focus area: "Data Quality & Accuracy"

---

## Full Example: Step by Step

### Scenario: You have a 12-page data_analysis document that's repetitive

**Step 1: Review Quality**
```
Score: 3.1/5 (needs improvement)
Weaknesses: "Repetitive data mentions", "Verbose paragraphs", "Unclear focus"
Recommendations:
  1. "Remove repetition"
  2. "Condense to 40% shorter"
  3. "Improve data clarity"
```

**Step 2: Edit Recommendations**
```
Change 1:
  FROM: "Remove repetition"
  TO:   "Remove repetition - mention each metric once in text, 
         then use cross-references like 'As described in Table 2'"

Change 2:
  FROM: "Condense to 40% shorter"
  TO:   "Reduce from 10,000 words to 6,000 words by tightening 
         paragraphs and moving methodology to appendix"

Change 3:
  FROM: "Improve data clarity"
  TO:   "Create table for key metrics showing: 
         Name, Current Value, Previous Value, Change %"
```

**Step 3: Add Custom Improvements**
```
New 1: "Add 1-sentence business impact summary for top 3 findings"
New 2: "Bold all dollar amounts and percentages"
New 3: "Create executive summary section (2-3 sentences) at top"
```

**Step 4: Select Focus Areas**
```
☑ Executive Summary
☑ Key Findings
☑ Clarity & Conciseness
```

**Step 5: Apply Refinement**
```
Click "✨ Apply Guided Refinement"
Wait 30-45 seconds...
```

**Step 6: Check Result**
```
✓ Reduced from 10,000 to 6,200 words
✓ Executive summary at top
✓ Key metrics in table
✓ No repetition (cross-references used)
✓ Formatting improved (bold amounts)
```

**Step 7: Review Score**
```
Click "Review Quality" again
Score: 4.1/5 ✅ READY FOR APPROVAL!
```

**Step 8: Export**
```
Click "Download"
Get: Project2_data_analysis_20251203.md
Ready to share with stakeholders!
```

---

## Next Steps

1. **Try It:** Generate a document and use guided refinement
2. **Iterate:** Review → Refine → Review → Repeat until satisfied
3. **Export:** Download the refined document
4. **Learn More:** Read `GUIDED_REFINEMENT_GUIDE.md` for advanced techniques

---

**Happy refining! 🎯**

Questions? Check the full guide: `GUIDED_REFINEMENT_GUIDE.md`
