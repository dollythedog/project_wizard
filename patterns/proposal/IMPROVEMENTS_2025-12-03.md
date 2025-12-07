# Proposal Pattern Improvements (2025-12-03)

## Summary

Updated the proposal blueprint and prompts to address two critical issues:
1. **Hallucination prevention** - Stop inventing team members, credentials, and metrics
2. **Length control** - Keep proposals concise (5–7 pages, not 16+) through word count targets and deduplication rules

---

## Changes Made

### 1. Added Hallucination Verification Questions to `blueprint.json`

Added two new critical verification questions (VQ_PROP_06 and VQ_PROP_07) that the VerifierAgent will check against:

**VQ_PROP_06: Team/Credentials Hallucination Check**
```json
{
  "id": "vq_prop_06",
  "question": "Are all team member names, credentials, and experience claims verifiable in the provided inputs? (No hallucinated people or credentials)",
  "category": "factual",
  "priority": "critical"
}
```
- Will catch invented names like "Dr. Sarah Mitchell" when not provided
- Will catch fabricated credentials or false experience claims

**VQ_PROP_07: Numbers/Metrics Hallucination Check**
```json
{
  "id": "vq_prop_07",
  "question": "Are all numerical claims (costs, metrics, percentages, timelines) grounded in the provided inputs or explicit in your organization's known data?",
  "category": "factual",
  "priority": "critical"
}
```
- Will catch invented metrics like "40% cost reduction" if not stated
- Will catch unsourced dollar amounts or percentages

### 2. Enhanced `prompts.json` with Comprehensive Guidance

#### Added `general_guidance` section
- **Tone of Voice**: Professional, collaborative, data-informed; avoid salesy language
- **Perspective**: Use "We" for partnership; use company name for organization capabilities
- **Target Length**: 5–7 pages; every paragraph must earn its place
- **Formatting**: Clear headings, bullets, white space, tables for data
- **Key Principle**: Show understanding of THEIR problem first → YOUR solution → YOUR capability → cost

#### Added `section_length_targets` section
Strict word count limits to prevent bloat:
- Cover Letter: 200–300 words (1 page max)
- Executive Summary: 150–200 words
- Key Benefits: 250–300 words
- Experience Snapshot: 200–250 words
- Statement of Work: 400–500 words
- Terms & Pricing: 300–350 words
- **Total: 2,500–3,500 words (5–7 pages)**

Critical rule: If document exceeds 8 pages or 4,500 words, condense immediately. Prioritize client pain points and solution over everything else.

#### Added `section_by_section_guidance` section
Detailed guidance for each section showing:
- **Purpose** (what problem it solves)
- **Tone** (how to sound)
- **Focus** (what goes in)
- **Must include** (critical elements)
- **Avoid** (common mistakes)

Key insight: Each section has a **unique purpose**. Cover letter = prove you understand THEIR problem. Executive Summary = propose YOUR solution. Benefits = outcomes ONLY. Experience = credibility building. SOW = show the work. Terms = define scope.

#### Added `deduplication_critical_rules` section
Six explicit rules to prevent repetition across sections:
1. Cover Letter = Understand THEIR problem (no solution, no benefits, no team pitching)
2. Executive Summary = Propose YOUR solution (don't repeat client problem, don't list benefits)
3. Key Benefits = Outcomes ONLY (don't repeat solution methods, don't list deliverables)
4. Experience = Build confidence (don't repeat value prop, don't describe solution)
5. Statement of Work = Show the work (don't repeat benefits, don't describe outcomes)
6. Terms & Pricing = Business framework ONLY (no sales messaging, no benefits)

### 3. Updated `draft_generation` section in `prompts.json`

Added core principle and enhanced goals:
- **Core Principle**: "Proposals that work are CLIENT-FOCUSED, not VENDOR-FOCUSED. Show you understand THEIR problem first, then propose YOUR solution. Keep it concise."
- **Goals now include**: 
  - Generate proposals 5–7 pages max (2,500–3,500 words)
  - Enforce word count limits per section to prevent bloat
  - Use section-by-section guidance to ensure unique purposes

Enhanced critical_rules to emphasize anti-hallucination violations:
- NEVER invent names, credentials, experience, data, or metrics
- WHEN TEAM EMPTY: Use generic language only
- VERIFICATION_CHECKLIST: Verify every person, credential, number before finalizing

---

## New Documentation

### PROPOSAL_QUALITY_GUIDE.md

Comprehensive 370+ line guide covering:

**Section 1: Target Lengths**
- Table with word count targets for each section
- Critical rule: If >8 pages or 4,500 words, condense immediately

**Section 2: Anti-Hallucination Checklist**
- Absolute prohibitions (never invent names, credentials, metrics, experience)
- Verification checklist (5 boxes to check before finalizing)
- Quick fixes (Problem → Solution table for common hallucinations)

**Section 3: Section Deduplication Rules**
- Table showing unique purpose of each section
- Examples of violations vs. correct approaches
- Real proposal excerpts showing what to do/avoid

**Section 4: Section-by-Section Guidance**
- Detailed subsections for: Cover Letter, Executive Summary, Key Benefits, Experience Snapshot, SOW, Terms & Pricing
- Each includes: Purpose, Tone, Length, Structure, ✅ Examples, ❌ Avoid

**Section 5: Verification Checklists**
- Hallucination check (fictional people, invented metrics, etc.)
- Length check (word counts per section and total)
- Deduplication check (no section repeats another)
- Quality check (formatting, tone, specificity)

---

## How These Changes Work Together

### User Journey Before:
1. User fills in proposal inputs
2. StepBackAgent asks clarifying questions
3. DraftAgent generates proposal using field enrichment or skeleton-of-thought
4. VerifierAgent checks basic quality
5. **Output: 16+ page bloated, repetitive proposal with hallucinated team members** ❌

### User Journey After:
1. User fills in proposal inputs
2. StepBackAgent asks clarifying questions
3. DraftAgent uses enhanced guidance:
   - Enforces 200–300 word cover letter (not 800+ word rambling)
   - Separate section purposes prevent repetition
   - Deduplication rules stop same benefits appearing in SOW
   - Word count targets keep total to 5–7 pages
4. VerifierAgent checks 7 questions including **two new hallucination checks**:
   - VQ_PROP_06: Are all names/credentials verifiable?
   - VQ_PROP_07: Are all numbers grounded in provided data?
5. RefinementAgent condenses if needed
6. **Output: Concise 5–7 page proposal with zero hallucinations** ✅

---

## Expected Improvements

| Problem | Solution | Result |
|---------|----------|--------|
| 16+ page proposals | Word count targets (2,500–3,500) | 5–7 page proposals |
| Repetitive sections | Deduplication rules + section purposes | Each section has unique role |
| Hallucinated team members | VQ_PROP_06 verification | Generic language when names unavailable |
| Invented metrics | VQ_PROP_07 verification | Only grounded, verifiable numbers |
| Bloated SOW | Statement of Work guidance | Clear activities, timeline, deliverables |
| Vague language | Specific tone + section guidance | Data-driven, professional tone |

---

## Testing Recommendations

Before using updated pattern in production, test:

1. **Hallucination Test**: Create inputs with NO team members provided. Verify proposal uses only generic language ("Our team of board-certified...") instead of invented Dr. names.

2. **Length Test**: Generate proposal from typical inputs. Verify:
   - Cover letter is ~250 words (not 600)
   - Total document is 2,500–3,500 words (not 5,000+)
   - No section exceeds target word count by >20%

3. **Deduplication Test**: Generate proposal with detailed benefits input. Verify:
   - Benefits section lists outcomes ONLY
   - Statement of Work does NOT repeat benefits
   - No section repeats information from another section

4. **Verification Test**: Generate intentionally bad proposal (invented data, fake names, repetitive). Verify:
   - VQ_PROP_06 catches fictional people
   - VQ_PROP_07 catches made-up numbers
   - RefinementAgent can condense if needed

---

## Files Updated

1. **`patterns/proposal/blueprint.json`**
   - Added VQ_PROP_06 and VQ_PROP_07 verification questions
   - 8 new lines of critical verification logic

2. **`patterns/proposal/prompts.json`**
   - Added `general_guidance` section (5 keys)
   - Added `section_length_targets` section (7 keys)
   - Added `section_by_section_guidance` section (6 subsections)
   - Added `deduplication_critical_rules` section (6 rules + consequence)
   - Enhanced `draft_generation` core_principle and goals

3. **`patterns/proposal/PROPOSAL_QUALITY_GUIDE.md`** (NEW)
   - 370+ line comprehensive quality guide
   - Target lengths, anti-hallucination rules, deduplication rules
   - Section-by-section detailed guidance with examples
   - Verification checklists

4. **`patterns/proposal/IMPROVEMENTS_2025-12-03.md`** (NEW)
   - This document; summary of all changes made

---

## Next Steps

1. **Immediate**: Test proposals with updated blueprint + prompts
2. **Short-term**: Iterate on word count targets if needed (adjust targets based on real proposals)
3. **Medium-term**: Create similar improvements for work_plan and project_charter blueprints
4. **Long-term**: Add rubric weighting by client type (financial vs. clinical decision-makers)

---

## Questions to Address

1. **Are 5–7 pages always enough?** For most hospital proposals, yes. If needed, can increase to 8 pages and mark as "expanded" format.

2. **What if the user provides very detailed team info?** Keep it but still enforce word limits. Focus on most relevant credentials.

3. **What if client is large/complex?** Section guidance allows multiple levels (e.g., "Clinical Benefits: Intensive Care, Pulmonary Care, Emergency Department"). Keep each concise.

4. **Should we auto-condense?** Yes—RefinementAgent should have a "condense_and_improve" method that reduces document by 30–40% while preserving critical content.

---

**Updated:** 2025-12-03  
**Status:** Ready for testing  
**Maintenance Owner:** [Your Name]
