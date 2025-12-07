# Guided Refinement Workflow - Project Wizard

## 🎯 Overview

The **Guided Refinement** feature allows you to:

1. **Review** a document with AI quality feedback
2. **Edit** specific improvement recommendations
3. **Customize** the refinement strategy
4. **Send** guided instructions back to AI for targeted improvements

This workflow is perfect for documents that are "mostly good" but need specific refinements like condensing, removing repetition, or fixing particular issues.

---

## 🔄 Workflow Steps

### Step 1: Generate Document
```
Create project → Add context notes → Fill blueprint form 
→ Answer clarifying questions → Get draft
```

### Step 2: Review Quality
```
Document view → Click "Review Quality" 
→ VerifierAgent scores document against rubric
→ See: Overall score, criterion-by-criterion breakdown, strengths, weaknesses
```

### Step 3: Guided Refinement (NEW)
```
Review page → Click "🎯 Guided Refinement"
→ Edit AI recommendations
→ Select focus areas
→ Click "Apply Guided Refinement"
→ RefinementAgent applies YOUR specific instructions
```

### Step 4: Compare & Export
```
View refined document
→ Download, edit further, or regenerate
```

---

## 📋 What Happens in Each Phase

### Phase 1: Quality Review (VerifierAgent)

**Input:**
- Original document
- Project context (notes, files, charter)
- Blueprint rubric (clarity, completeness, alignment, feasibility)

**Process:**
1. VerifierAgent reads full document
2. Scores each criterion on 1-5 scale
3. Identifies strengths and weaknesses
4. Generates specific improvement recommendations

**Output:**
- Overall score (1.0-5.0)
- Individual criterion scores with feedback
- 3-5 strengths (what's working)
- 3-5 weaknesses (what needs work)
- 3-5 specific recommendations (how to improve)

### Phase 2: Guided Refinement (NEW - RefinementAgent)

**What You Do:**
1. Review AI recommendations (from Phase 1)
2. **Edit each recommendation** to be more specific or adjusted
3. **Add custom improvements** if needed
4. **Select focus areas** (Executive Summary, Key Findings, etc.)
5. Click "Apply Guided Refinement"

**What AI Does:**
1. Takes your **custom instructions**
2. Reads full document
3. Applies improvements while:
   - Preserving all data and structure
   - Removing repetition
   - Improving clarity
   - Fixing identified issues
4. Returns refined document

**Output:**
- Refined markdown document
- Summary of improvements applied
- Token count and model used

---

## 💡 Example Use Cases

### Use Case 1: Long & Repetitive Data Analysis

**Situation:**
- Generated 12-page data analysis
- Very long, repetitive data points mentioned multiple times
- VerifierAgent recommends: "Remove repetition", "Condense by 40%", "Improve data presentation"

**Your Process:**
1. Go to Guided Refinement
2. Edit recommendations:
   - Keep: "Remove repetition" ✓
   - Change: "Condense by 40%" → "Reduce from 6000 words to 3500 words (aggressive condensing)"
   - Add: "Create tables instead of paragraphs for metrics"
   - Add: "Use cross-references like 'As shown in Table 1' instead of repeating data"
3. Select focus area: "Executive Summary"
4. Click "Apply Guided Refinement"
5. AI returns condensed version with tables and cross-references

### Use Case 2: Missing Data Points

**Situation:**
- VerifierAgent flags: "Incomplete analysis in trends section"
- You know what's missing

**Your Process:**
1. Go to Guided Refinement
2. Edit the recommendation:
   - Original: "Incomplete analysis in trends section"
   - Change to: "Complete the Trends Analysis section with year-over-year growth rates and seasonal patterns"
3. Select focus area: "Key Findings"
4. Click "Apply Guided Refinement"
5. AI returns with completed section

### Use Case 3: Custom Refinement Strategy

**Situation:**
- Document is okay but you want specific changes
- VerifierAgent gave general recommendations

**Your Process:**
1. Go to Guided Refinement
2. Clear default recommendations
3. Add your custom instructions:
   - "Reorganize sections: move Recommendations to top"
   - "Add executive summary as first section (2-3 sentences)"
   - "Bold all dollar amounts and percentages"
   - "Create a summary table of key metrics"
4. Select focus areas: "Executive Summary", "Clarity & Conciseness"
5. Click "Apply Guided Refinement"
6. AI applies your exact refinement strategy

---

## 🛠️ How RefinementAgent Works

### Architecture

```
Your Custom Instructions (editable recommendations + focus areas)
        ↓
RefinementAgent._build_refinement_prompt()
        ↓
Prompt Includes:
  - Each improvement instruction (numbered list)
  - Focus areas (prioritize these sections)
  - Project context (for grounding)
  - Full current document
  - Quality checklist (preserve data, apply improvements, etc.)
        ↓
LLMClient.generate()
        ↓
AI Review & Refinement:
  1. Read all improvements
  2. Apply each one systematically
  3. Preserve structure and data
  4. Check quality checklist before returning
        ↓
Refined Document (saved to database)
```

### System Message

```
You are an expert document editor and refiner.

Your role:
- Apply specific improvements while maintaining document structure
- Preserve all critical information and data
- Improve clarity, conciseness, and flow
- Fix identified issues and weaknesses
- Maintain professional tone and formatting

Standards:
- Never remove important data or analysis
- Cross-reference instead of repeating information
- Use active voice and clear language
- Keep bold formatting for key metrics
- Maintain markdown formatting (headings, tables, lists)
```

### Quality Checklist

Before returning refined document, AI verifies:
- ✅ All critical data and analysis preserved
- ✅ Specific improvements applied
- ✅ No unnecessary repetition
- ✅ Clear, concise language
- ✅ Professional formatting
- ✅ Tables and lists properly formatted

---

## 📊 Key Improvements Across Phases

| Phase | Agent | Input | Output | Time | Cost |
|-------|-------|-------|--------|------|------|
| Generation | DraftAgent | User inputs + context | Full document (5000+ words) | ~30-60s | $0.15-0.30 |
| Review | VerifierAgent | Document + rubric | Scores + feedback | ~20-30s | $0.05-0.10 |
| Refinement | RefinementAgent | Doc + custom instructions | Improved document | ~20-40s | $0.05-0.15 |

---

## 🔧 Editing Recommendations Guide

### Types of Improvements You Can Make

#### 1. **Clarify Vague Recommendations**

**Original (vague):**
- "Improve clarity in Executive Summary"

**Refined (specific):**
- "Executive Summary: Add 2-3 specific metrics for each claim (e.g., '30% increase in engagement' instead of 'significant increase')"

#### 2. **Add Quantified Goals**

**Original:**
- "Remove repetition"

**Refined:**
- "Remove repetition: Reduce document from 6200 to 3500 words by mentioning each key data point once and using cross-references"

#### 3. **Specify Format Changes**

**Original:**
- "Improve data presentation"

**Refined:**
- "Create a table for Appendix A with columns: Metric, Q1, Q2, Q3, Q4, YTD Growth. Summarize in text with only top 3 metrics"

#### 4. **Combine Multiple Improvements**

**Original (separate):**
- "Fix calculation errors"
- "Add missing analysis"

**Refined (combined):**
- "Verify all calculations in Trend Analysis section and add missing seasonal pattern analysis with 3-year comparison"

#### 5. **Add Custom Instructions**

**Original (none - add new):**
- (empty)

**Refined (new):**
- "Add new section: 'Key Risks & Mitigations' (3-4 bullet points) after Recommendations"

---

## ✅ Best Practices

### DO ✓

- **Be specific**: Instead of "improve", say "reduce from X to Y" or "add X detail"
- **Focus on outcomes**: What should the refined document look like?
- **Reference sections**: Mention specific sections by name
- **Use examples**: Show what you want (e.g., "Create a table with...")
- **Prioritize**: Use focus areas to guide AI attention
- **Preserve data**: All recommendations should maintain facts and analysis

### DON'T ✗

- **Don't be vague**: "Make it better" → Use specific instructions
- **Don't remove data**: AI will preserve data, but you guide HOW to present it
- **Don't change recommendations without reason**: Explain your refinement
- **Don't add too many improvements**: Focus on top 3-5 (AI works better with clear priorities)

---

## 🚀 Advanced Techniques

### Technique 1: Condensing with Purpose

**Scenario:** Document is too long
**Strategy:**
```
1. Keep original: "Remove repetition"
2. Add: "Reduce from [X] words to [Y] words"
3. Add: "Use cross-references for data already mentioned"
4. Add: "Create summary table for metrics"
5. Focus on: "Executive Summary"
```

### Technique 2: Restructuring for Impact

**Scenario:** Information is in wrong order
**Strategy:**
```
1. Add: "Move Recommendations section to position 2 (right after Executive Summary)"
2. Add: "Create 'Key Metrics Dashboard' section with 5-7 critical numbers"
3. Add: "Reorganize narrative to flow: Problem → Solution → Results → Recommendations"
4. Focus on: "Recommendations", "Executive Summary"
```

### Technique 3: Data Quality Focus

**Scenario:** Verifier flagged data inconsistencies
**Strategy:**
```
1. Add: "Verify all numbers against source data in Project Notes"
2. Add: "Flag any calculations that don't match source data and recalculate"
3. Add: "Add data source citations for each statistic"
4. Focus on: "Data Quality & Accuracy"
```

### Technique 4: Executive Readability

**Scenario:** Document is too technical
**Strategy:**
```
1. Add: "Rewrite Executive Summary for C-suite audience (non-technical language)"
2. Add: "Replace jargon: use plain language equivalents"
3. Add: "Add business impact statement for each finding"
4. Add: "Reduce Findings section to 1-2 paragraphs summary + table"
5. Focus on: "Executive Summary", "Clarity & Conciseness"
```

---

## 📈 Iteration Strategy

### First Pass: Quick Improvements
1. Review quality feedback
2. Adjust 2-3 most important recommendations
3. Apply refinement
4. Evaluate

### Second Pass: Fine-Tuning
1. Look at refined document
2. Identify remaining issues
3. Review again (click "Review Quality")
4. Make more targeted adjustments
5. Apply refinement

### Third Pass: Polish
1. Focus on formatting and readability
2. Check cross-references and structure
3. Final review
4. Export

---

## 🔗 Related Features

### Other Refinement Options

**Automatic Condensing:**
- Review page → "Apply Improvements & Condense"
- Auto-applies verifier feedback + 40% condensing
- Less control, faster

**Manual Editing:**
- Draft view → Click "Edit" on markdown
- Direct text editing
- Maximum control, manual work

**Guided Refinement (NEW):**
- Review page → "Guided Refinement"
- Edit recommendations + send to AI
- Balance of control and automation

### Workflow Integration

```
Generate Document
    ↓
Review Quality ← Manual Edit (alternative)
    ↓
Guided Refinement ← Auto Condense (alternative)
    ↓
Refined Document
    ↓
Export/Download
```

---

## 📝 Example: Complete Workflow

### Scenario: Long, Repetitive Data Analysis

**Step 1: Generate**
```
Create "Q4 Analytics"
Add notes: raw data CSV, business context, goals
Fill form: date range, metrics, target audience
Answer clarifying questions
→ 12-page analysis generated
```

**Step 2: Review Quality**
```
Click "Review Quality"
→ Score: 3.2/5 (needs improvement)
→ Weaknesses: "Repetitive data mentions", "Paragraphs too long"
→ Recommendations: "Remove repetition", "Condense", "Use tables"
```

**Step 3: Guided Refinement**
```
Click "Guided Refinement"

Edit Recommendations:
  1. "Remove repetition" → KEEP
  2. "Condense" → "Reduce from 6200 words to 3800 words"
  3. "Use tables" → "Convert Metrics section to table format"
  4. NEW: "Add year-over-year comparison"

Focus Areas:
  ☑ Executive Summary
  ☑ Key Findings
  ☐ Recommendations

Click "Apply Guided Refinement"
→ Waiting for AI...
→ Refined document: 3800 words with tables and YoY comparison
```

**Step 4: Review Result**
```
New document shows:
- Condensed from 12 pages to 8 pages
- Executive summary tightened to 150 words
- Metrics in table format
- Cross-references instead of repetition
- New YoY comparison section

Try: "Review Quality" again
→ Score: 4.1/5 (ready for approval!)
```

**Step 5: Export**
```
Click "Download"
→ Q4_Analytics_data_analysis_20251203.md
Ready to share with stakeholders!
```

---

## 🐛 Troubleshooting

### Issue: "Refinement applied but not what I expected"

**Solution:**
- Be more specific in your instructions
- Use examples: "Create a table with columns: X, Y, Z"
- Reduce number of improvements (focus on top 3)
- Try again with clearer language

### Issue: "Data got removed during refinement"

**Solution:**
- This shouldn't happen - RefinementAgent has explicit preservation rules
- If it does, check your instructions for any "remove" language
- Try: "Keep all data, but summarize in table format instead of paragraphs"

### Issue: "Still too long after condensing"

**Solution:**
- Refinement applies YOUR instructions (not automatic 40% cut)
- Be explicit: "Reduce to [exact word count]"
- Add: "Eliminate any redundant sections"
- Specify what to remove: "Remove 'Methodology' section if non-essential"

### Issue: "Need to try refinement again"

**Solution:**
1. Go back to document view
2. Click "Review Quality" again
3. Go back to "Guided Refinement"
4. Edit recommendations differently
5. Apply again

---

## 🎓 Learning Resources

- See `SYSTEM_OVERVIEW.md` for architecture details
- Check `PROJECT_PLAN.md` for roadmap
- View `verifier_agent.py` for quality scoring logic
- Check `refinement_agent.py` for refinement implementation

---

**Happy refining! 🎯**

Questions? Check the main documentation or try the workflow yourself on a test document first.
