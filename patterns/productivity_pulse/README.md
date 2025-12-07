# Productivity Pulse Email Pattern

**Purpose:** Generate monthly productivity highlight emails for facility partners

**Audience:** Facility leadership, partners  
**Format:** Email (3 paragraphs, ~200-300 words)  
**Update Frequency:** Monthly  
**Created:** 2025-12-05

---

## Overview

The Productivity Pulse email provides facility partners with a data-driven, neutral summary of service-line productivity trends. It enables partners to understand resource utilization without creating unfair facility comparisons.

### Task & Purpose
- **Task:** Summarize monthly service-line productivity metrics and highlight staffing efficiency trends across facility locations
- **Purpose:** Enable facility partners to understand resource utilization, identify over/understaffed areas, and inform collaborative staffing decisions

---

## Key Design Principles

### 1. Apples-to-Apples Comparison
- ICU assignments only compared to other ICU assignments
- Floor assignments only compared to other floor assignments
- Clinic to Clinic, Telehealth to Telehealth, etc.
- **Never** compare across service line categories

### 2. Neutral, Partnership-Focused Language
- Avoid "winning" vs "losing" facilities
- Use phrases like "trending at X visits/shift across our network"
- Frame variance as "opportunities for learning" not failures
- No competitive framing

### 3. Data-Driven, Not Subjective
- Every metric comes directly from JSON source data
- No hallucinated numbers or facilities
- Calculations verified before publication
- Clear attribution: "November 2025 service line breakdown shows..."

### 4. Strict Format Discipline
- **Exactly 3 paragraphs** (no more, no less)
- Subject line + opening + metrics + closing
- 3-4 specific metrics referenced (visits/shift, wRVU/shift, procedures/shift, etc.)
- Actionable insights for staffing planning

---

## Input Requirements

### Required Inputs

1. **json_data** (textarea)
   - Full service-line-breakdown JSON array
   - Format: `[{"assignment_name": "...", "facility_class": "...", ...}, ...]`
   - Must be valid JSON

2. **reporting_month** (text)
   - Example: "November 2025"
   - Used in opening paragraph and subject line

3. **high_profile_service_lines** (text, comma-separated)
   - Example: "ICU, Floor"
   - Which service line categories to emphasize

4. **comparison_metrics** (text, comma-separated)
   - Example: "avg_visits_per_shift, wrvu_per_shift, avg_procedures_per_shift"
   - Which metrics drive the narrative

### Optional Inputs

5. **key_trends** (textarea)
   - Business context: seasonal shifts, new assignments, staffing changes
   - Woven into narrative naturally

6. **chart_descriptions** (textarea)
   - Which charts user is including
   - Example: "Chart 1: Service Line Efficiency - wRVU per Shift by Facility"
   - Referenced in closing: "See Chart 1 for detailed breakdown"

---

## Email Structure

### Section 1: Subject Line
- Professional, clear, data-focused
- Example: "November 2025 Productivity Report" or "Monthly Service Line Update – November"

### Section 2: Opening Paragraph (1 paragraph)
- Context-setting for reporting period
- Data source attribution
- Example opening: "Attached is our November 2025 service line productivity analysis. These data aggregate performance across all facilities and assignments, comparing like-with-like by service category (ICU, floor, clinic, etc.)."

### Section 3: Metrics & Highlights (1 paragraph, ~2-3 key findings)
- Organized by service line
- Use format: "[Service Line] assignments show [metric] of X across our network, ranging from Y to Z. This suggests [interpretation for staffing]."
- Include 3-4 specific metrics with ranges
- No facility-specific rankings
- Example: "ICU assignments across our network averaged 18.8 visits per shift in November (range: 17.8–20.4), with wRVU per shift ranging from 53.6–69.1. This staffing level appears well-calibrated for current patient acuity."

### Section 4: Closing Paragraph (1 paragraph)
- Restate purpose: staffing planning support
- Invite questions
- Reference charts if applicable
- Professional close
- Example: "These insights support our collaborative staffing planning discussions. If you see areas for discussion or adjustment based on your on-the-ground experience, please reach out. I'm happy to dive deeper into any service line."

---

## Verification Checklist

Before sending, verify:

### Data Accuracy (30% weight)
- [ ] Every metric matches JSON source data
- [ ] Calculations verified (e.g., visits/shift = total_visits / shift_count)
- [ ] No hallucinated numbers or assignments
- [ ] Numbers formatted consistently (commas, decimals)

### Fair Comparison (25% weight)
- [ ] Service lines only compared to peer service lines
- [ ] No facility rankings or "winner/loser" framing
- [ ] Interpretations align with data (e.g., "high wRVU/shift" only if actually high relative to peers)
- [ ] Trends support staffing implications mentioned

### Clarity & Focus (25% weight)
- [ ] Email is exactly 3 paragraphs
- [ ] Subject line is clear and professional
- [ ] All high-profile service lines mentioned
- [ ] Key trends from user input incorporated
- [ ] Chart descriptions referenced appropriately
- [ ] Easy to scan, no overwhelming detail

### Professional Tone (20% weight)
- [ ] Neutral, partnership-focused language throughout
- [ ] No competitive framing between facilities
- [ ] Purpose restated in closing (staffing decisions support)
- [ ] Professional tone maintained
- [ ] Actionable insights for leadership

---

## Example Usage

### Input Data

```json
[
  {"assignment_name": "HSW ICU SW", "facility_class": "HSW", "service_line": "ICU", "shift_count": "30", "total_visits": "613", "avg_visits_per_shift": "20.43", "total_wrvus": "1,737.64", "wrvu_per_shift": "57.92"},
  {"assignment_name": "MCA CSTN ICU", "facility_class": "MCA", "service_line": "ICU", "shift_count": "30", "total_visits": "578", "avg_visits_per_shift": "19.27", "total_wrvus": "1,779.60", "wrvu_per_shift": "59.32"},
  ...
]
```

### Example Output Email

```
Subject: November 2025 Productivity Report

Our November 2025 service line productivity analysis is attached. These data aggregate performance across all facilities and assignments, comparing like-with-like by service category (ICU, floor, clinic, etc.).

ICU assignments across our network averaged 18.8 visits per shift in November (range: 17.8–20.4 among our primary sites), with wRVU productivity per shift ranging from 53.6–69.1. This variation reflects differences in patient acuity and case mix across locations. Floor assignments showed an average of 19.2 visits per shift (range: 5.7–27.6), suggesting some assignments carry heavier patient loads than others—an opportunity for discussion on staffing calibration.

These insights support our collaborative staffing planning discussions. If you see areas for discussion or adjustment based on your on-the-ground experience, please reach out. I'm happy to dive deeper into any service line or facility.
```

---

## Common Pitfalls to Avoid

❌ **Comparing non-equivalent service lines** (e.g., ICU to Floor)  
✅ Service lines only compared to peer service lines (ICU to ICU, Floor to Floor)

❌ **Too much detail** (more than 3 paragraphs)  
✅ Exactly 3 paragraphs, highlights only

❌ **Judgmental language** ("underperforming", "lagging", "struggling")  
✅ Neutral framing: "trending at X", "shows opportunity for learning"

❌ **Hallucinating assignments** not in the data  
✅ Only mention assignments present in JSON input

❌ **Forgetting the purpose** (just reporting numbers)  
✅ Always tie metrics to staffing implications: "suggests adequate coverage" or "indicates opportunity for optimization"

---

## Future Enhancements (v2.0+)

- [ ] Automate JSON parsing to extract and calculate metrics
- [ ] Store sent emails as "good examples" for learning
- [ ] Track which emails drive staffing decisions (success metrics)
- [ ] Add seasonal trend detection ("compared to same month last year")
- [ ] Multi-month comparison mode (e.g., Q3 vs. Q2)
- [ ] Facility-specific variants (same data, tailored narrative per facility)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial pulse email template with Task & Purpose |

---

**Questions?** Reach out to your Project Wizard team.
