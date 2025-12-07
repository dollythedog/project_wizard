# Productivity Pulse Email Pattern - Implementation Summary

**Date:** 2025-12-05  
**Status:** ✅ COMPLETE - Ready to integrate and test  
**Location:** `patterns/productivity_pulse/`

---

## What Was Built

A complete blueprint for generating monthly productivity highlight emails for facility partners, with **Task & Purpose** as the north star.

### Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `blueprint.json` | Pattern definition: inputs, sections, verification questions, rubric | 150 |
| `prompts.json` | AI instructions with Task & Purpose guidance, critical rules, email structure | 138 |
| `template.j2` | Jinja2 email template | 8 |
| `README.md` | Complete usage documentation with examples and pitfalls | 208 |

**Total:** 504 lines of new pattern documentation

---

## Key Features

### 1. Task & Purpose as North Star ⭐
- **Task:** Summarize monthly service-line productivity metrics and highlight staffing efficiency trends
- **Purpose:** Enable facility partners to understand resource utilization and inform collaborative staffing decisions
- Built into every agent instruction
- Validated at every verification step
- Restated in email closing

### 2. Apples-to-Apples Comparison
- ICU assignments only compared to ICU assignments
- Floor to Floor, Clinic to Clinic, etc.
- No facility "winners" or "losers"
- Critical rule: enforced throughout

### 3. Strict Format Discipline
- **Exactly 3 paragraphs:** no more, no less
- Subject line + opening context + metrics & highlights + closing with next steps
- 3-4 specific metrics per email (visits/shift, wRVU/shift, procedures/shift)
- ~200-300 words total

### 4. Neutral, Partnership-Focused Language
- No competitive framing
- Frame variance as "opportunities for learning"
- Use phrases like "trending at X visits/shift across our network"
- Professional, clinical tone

### 5. Data-Driven, Not Subjective
- Every number from JSON source
- Calculations verified
- No hallucinated assignments or metrics
- Clear attribution: "November 2025 service line breakdown shows..."

---

## Input Parameters

### Required
1. **json_data** - Full service-line-breakdown JSON array
2. **reporting_month** - e.g., "November 2025"
3. **high_profile_service_lines** - e.g., "ICU, Floor"
4. **comparison_metrics** - e.g., "avg_visits_per_shift, wrvu_per_shift"

### Optional
5. **key_trends** - Business context (seasonal shifts, staffing changes)
6. **chart_descriptions** - Which charts user is including

---

## Email Structure

```
Subject: [November 2025 Productivity Report]

[Opening Paragraph]
Context-setting for reporting period + data source attribution

[Metrics & Highlights Paragraph]
2-3 key findings organized by service line
Format: "[Service Line] assignments show [metric] of X across our network, 
ranging from Y to Z. This suggests [interpretation for staffing]."

[Closing Paragraph]
Restate purpose + invite questions + reference charts + professional close
```

---

## Verification Checklist (4 criteria)

1. **Data Accuracy (30%)** - Every metric verified from JSON
2. **Fair Comparison (25%)** - Only peer comparisons, no rankings
3. **Clarity & Focus (25%)** - Exactly 3 paragraphs, highlights only
4. **Professional Tone (20%)** - Neutral, partnership-focused, actionable

**Passing score:** 3.8/5.0

---

## Workflow Integration

### Current Status
✅ Blueprint created and documented  
⏳ Ready for integration into Project Wizard web UI

### Integration Steps (Not yet done)
1. Add "productivity_pulse" to available blueprints in web UI
2. Update project to add notes about productivity trends (context)
3. User selects "Productivity Pulse Email" template
4. Answers step-back questions (4 key questions about priorities)
5. Pastes JSON data + chart descriptions
6. AI generates 3-paragraph email
7. Verify against rubric
8. Send or refine

---

## Example Usage

### Input
- **json_data:** Full service-line-breakdown JSON (32 assignments)
- **reporting_month:** "November 2025"
- **high_profile_service_lines:** "ICU, Floor"
- **comparison_metrics:** "avg_visits_per_shift, wrvu_per_shift"
- **key_trends:** "New MCA MICU night shift staffed, seasonal clinic volume increase"

### Example Output
```
Subject: November 2025 Productivity Report

Our November 2025 service line productivity analysis is attached. 
These data aggregate performance across all facilities and assignments, 
comparing like-with-like by service category (ICU, floor, clinic, etc.).

ICU assignments across our network averaged 18.8 visits per shift in November 
(range: 17.8–20.4 among primary sites), with wRVU productivity per shift 
ranging from 53.6–69.1. This staffing level appears well-calibrated for 
current patient acuity. We've successfully staffed the new MCA MICU night 
shift, which contributed to network capacity. Floor assignments showed an 
average of 19.2 visits per shift (range: 5.7–27.6), suggesting some 
assignments carry heavier patient loads than others—an opportunity for 
discussion on staffing calibration.

These insights support our collaborative staffing planning discussions. 
If you see areas for discussion or adjustment based on your on-the-ground 
experience, please reach out. I'm happy to dive deeper into any service 
line or facility.
```

---

## Critical Design Decisions

### 1. Why "Task & Purpose"?
- Military planning proven framework
- Keeps every sentence accountable to strategic intent
- Prevents scope creep in emails (3 paragraphs only)
- Helps LLM avoid unfair comparisons

### 2. Why "Exactly 3 Paragraphs"?
- Respects busy executive schedules
- Forces discipline: only highlights, not details
- Easy to scan and act on
- Fits email format (not report format)

### 3. Why "Apples-to-Apples Only"?
- Prevents unhealthy facility competition
- Fair to different patient populations
- Educates partners on complexity (not all ICUs are the same)
- Data-driven, not judgment-driven

### 4. Why Emphasis on "Partnership"?
- These are facility partners, not competitors
- Email should invite collaboration, not defensiveness
- Tone and language matter for relationship management
- Neutral framing = trusted data source

---

## Lessons Applied (From SectionAgentController)

This pattern borrows successful strategies from the proposal generation work:

✅ **Task & Purpose as north star** (from military planning framework)  
✅ **Word count enforcement** (3 paragraphs max, like section targets)  
✅ **Verification questions** (same rubric-based approach)  
✅ **Hallucination prevention** (anti-fabrication rules)  
✅ **Neutral tone throughout** (partnership-focused language)  
✅ **Context passing** (prompts inform section generation)

---

## Next Steps

### To Use This Pattern

1. **Copy to project:** Files are in `patterns/productivity_pulse/`
2. **Create a "Pulses" project** in Project Wizard
3. **Add context notes:** e.g., "What makes a good productivity pulse?" 
4. **Generate pulse email:** Select template → paste JSON → answer questions
5. **Review & send:** Email appears in 3 paragraphs, ready to send

### To Extend This Pattern

- [ ] Add "Financial Pulse Email" (revenue, collections, payer mix)
- [ ] Add "Scheduling Pulse Email" (coverage gaps, call patterns)
- [ ] Implement memory/learning (store sent emails as examples)
- [ ] Add trend detection (compare month-over-month or year-over-year)
- [ ] Create dashboard showing pulse history

---

## Files Location

```
patterns/productivity_pulse/
├── blueprint.json          # Pattern definition
├── prompts.json            # AI instructions with Task & Purpose
├── template.j2             # Email template
└── README.md               # Full documentation + examples
```

---

## Quick Reference

**Pattern Name:** Productivity Pulse Email  
**Type:** Email  
**Audience:** Facility partners  
**Format:** 3 paragraphs, ~200-300 words  
**Frequency:** Monthly  
**Key Principle:** Task & Purpose-driven, data-accurate, neutral, partnership-focused  
**Status:** Ready to integrate  

---

**Ready to test?** The pattern is complete and documented. Next step: integrate into web UI or test via CLI.
