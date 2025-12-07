# Clinical Services Proposal Template

**Version:** 1.0.0  
**Category:** Clinical Partnership  
**Purpose:** Staffing and clinical coverage proposals for hospital partnerships  

---

## Overview

This blueprint generates **structured, data-driven clinical services proposals** for hospital physician/APP staffing partnerships.

**Best for:**
- Pulmonary & Critical Care coverage agreements
- Emergency Medicine staffing
- Cardiology/Specialty consult coverage
- ICU hospitalist partnerships
- PERT/ELSO program formalization (see `programmatic_proposal` for that type)

**Output:** 5–7 page professional proposal with clear sections, metrics tables, staffing details, and financial transparency.

---

## Key Features

✅ **Fixed 8-section structure** (prevents rambling)  
✅ **Metrics-driven** (baseline → target outcomes)  
✅ **Operationally specific** (exact staffing, schedule, procedures)  
✅ **Data-grounded** (no hallucinated names or invented metrics)  
✅ **Table-based** (metrics, staffing, financial terms all tabular for scannability)  
✅ **No repetition** (each section has unique purpose)

---

## Files

- **`blueprint.json`** - Schema with inputs, sections, verification questions, rubric
- **`template.j2`** - Jinja2 markdown template (8-section structure)
- **`prompts.json`** - AI agent instructions (step-back, skeleton, draft, verification)
- **`README.md`** - This file

---

## Inputs (15 Total)

### Required Inputs

| Input ID | Label | Type | Description |
|----------|-------|------|-------------|
| `specialty` | Specialty/Service Line | text | E.g., "Pulmonary and Critical Care", "Cardiology" |
| `current_challenges` | Current Challenges | textarea | Specific problems (e.g., "variable ICU coverage, 35% locum dependency") |
| `clinical_impact` | Clinical Impact | textarea | How challenges affect patient care (e.g., "0.7-day longer LOS") |
| `scope_of_services` | Scope of Services | textarea | Services included (bullets: admissions, consultations, rounding, code participation) |
| `staffing_model` | Staffing Model | textarea | Detailed roles & schedule (e.g., "1 Physician 24/7 rotation, 1 APP weekday") |
| `baseline_metrics` | Current Baseline Metrics | textarea | Measured data (e.g., "ICU LOS: 4.2 days, Mortality Index: 1.15") |
| `target_metrics` | Target/Goal Metrics | textarea | Desired state (e.g., "ICU LOS: 3.8 days, Mortality Index: 0.95") |
| `financial_proposal` | Financial Terms & Pricing | textarea | Detailed pricing (e.g., "Base stipend: $X/month, includes APP, optional clinic at $Y/half-day") |
| `contract_term` | Contract Term | text | E.g., "One (1) year with annual renewal" or "3-year initial term" |

### Optional Inputs

| Input ID | Label | Type | Description |
|----------|-------|------|-------------|
| `operational_impact` | Operational Impact | textarea | Staffing/workflow issues |
| `financial_impact` | Financial Impact | textarea | Cost pressures (e.g., locum costs, budget volatility) |
| `procedures` | Procedures Included | textarea | E.g., "Bronchoscopy, thoracentesis, central line, mechanical ventilation" |
| `emr_system` | EMR System | text | E.g., "Epic", "Cerner" |
| `compliance_requirements` | Compliance & Insurance | textarea | E.g., "Malpractice $1M/$3M, active privileges, HIPAA" |
| `governance_structure` | Governance & Communication | textarea | E.g., "Weekly calls with CNO, monthly QI meetings, quarterly reviews" |

---

## Sections (8 Fixed)

| # | Section | Purpose | Length | Format |
|---|---------|---------|--------|--------|
| 1 | Executive Summary | Hook with partnership overview | 150–200 words | Brief paragraphs + bullets |
| 2 | Background & Need | Establish credibility via understanding | 200–250 words | Challenges + impacts |
| 3 | Proposed Coverage Model | Detail staffing, procedures, integration | 350–400 words | Tables + procedures bullets |
| 4 | Quality & Performance Metrics | Set measurable expectations | 200–250 words | Baseline vs. Target table |
| 5 | Financial Proposal | Transparent pricing and assumptions | 200–250 words | Fee structure table |
| 6 | Governance & Communication | Define leadership alignment | 150–200 words | Coordination + reporting bullets |
| 7 | Compliance & Risk Management | Reassure on credentials/standards | 150–200 words | Insurance + licensure bullets |
| 8 | Conclusion & Next Steps | Partnership value + actions | 150–200 words | Summary + 3–4 next steps |

**Total:** ~2,500–3,500 words (5–7 pages)

---

## Verification Questions (6 Critical)

The VerifierAgent will check:

1. **Baseline/Target Metrics** - Are they specific numbers from data (not estimates)?
2. **Coverage Model Clarity** - Does it specify staffing numbers, schedule, and procedures?
3. **Challenge-to-Solution Mapping** - How does staffing address specific baseline challenges?
4. **No Hallucinations** - Are all team names/credentials verifiable (not invented)?
5. **Financial Grounding** - Are financial claims documented assumptions or explicit data?
6. **Deduplication & Length** - Does document fit 5–7 pages with no section repetition?

---

## Rubric (Quality Scoring)

Weighted criteria:

- **Clinical Specificity (0.25)** - Metrics are data-grounded, clinical impacts concrete
- **Staffing Model Clarity (0.25)** - Clear roles, schedule, procedures; operationally feasible
- **Value Alignment (0.25)** - Challenges clearly mapped to solutions; ROI evident
- **Professionalism & Completeness (0.25)** - Professional tone, well-organized, no hallucinations

**Passing score:** 3.8/5.0

---

## Generation Strategy

**Skeleton-of-Thought** approach:

1. **Step-Back Agent** asks clarifying questions about hospital's baseline metrics, staffing model, governance preferences
2. **Draft Agent** generates unified skeleton showing how each section fits
3. **Draft Agent** expands sections in parallel, enforcing deduplication rules
4. **Verifier Agent** checks 6 critical questions (metrics, hallucinations, length, deduplication)
5. **RefinementAgent** condenses if >8 pages or if needed

---

## Anti-Hallucination Rules

**CRITICAL:** This template emphasizes DATA-DRIVEN proposals. Violations will fail verification:

❌ **NEVER invent:**
- Team member names (e.g., "Dr. Sarah Mitchell" if not provided)
- Credentials or experience (e.g., "15 years ICU experience" if not stated)
- Baseline/target metrics (e.g., "4.2 days LOS" if not in data)
- Financial savings (e.g., "40% cost reduction" without calculation)

✅ **DO this instead:**
- Use generic language: "Our team of board-certified intensivists"
- Use only provided metrics: "Baseline: 4.2 days (from hospital records)"
- Document assumptions: "If 35% of coverage is locums at $5K/shift, annual spend ≈ $2.5M"

---

## Example Usage

**User Input Summary:**
```
Specialty: Pulmonary and Critical Care
Current Challenges: Variable ICU coverage (35% locum dependent), slow consult response (45+ min avg)
Clinical Impact: Inconsistent protocols, higher handoff errors (23%), longer LOS
Staffing Model: 1 Physician (24/7), 1 APP (weekdays), backup redundancy
Baseline Metrics: LOS 4.2d, Mortality Index 1.15, Consult turnaround 45 min
Target Metrics: LOS 3.8d, Mortality Index 0.95, Consult turnaround <30 min
Financial: $X/month for 24/7 + APP
```

**Output:** 
- 5–7 page proposal with Executive Summary, clear staffing table, baseline→target metrics table, transparent pricing
- Zero hallucinations
- Each section has unique purpose (no repetition)
- Professional, data-driven tone suitable for CFO/CMO review

---

## Best Practices

**DO:**
- Use specific numbers (not "many", "robust", "excellent")
- Link staffing model to baseline challenges (e.g., "45-min consult delay → dedicated ICU physician")
- Present metrics in tables for scannability
- Document financial assumptions clearly
- Be honest about baseline data gaps ("Baseline to be established via data analysis")

**DON'T:**
- Invent team member names or credentials
- Estimate metrics you don't have
- Repeat information across sections
- Use vague language like "comprehensive coverage" without specifics
- Make financial claims without basis

---

## Related Templates

- **`proposal`** - Generic business proposal (more flexible, less structured)
- **`programmatic_proposal`** - For program development (PERT, ELSO, rapid response teams)

---

## Support

For questions about this template or generation process, see `PROPOSAL_QUALITY_GUIDE.md` and `IMPROVEMENTS_2025-12-03.md` in the parent `patterns/proposal/` directory.

---

**Last Updated:** 2025-12-03  
**Status:** Active  
**Next Review:** After first 3 generated proposals
