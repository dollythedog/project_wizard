# Task & Purpose Framework Integration

**Date:** 2025-12-05  
**Status:** ✅ Implemented in Productivity Pulse Pattern | 🔄 Ready to apply across all blueprints  
**Inspired by:** Military mission planning methodology  

---

## Overview

**Task & Purpose** is a proven framework from military operations planning that forces clarity about **what** you're doing and **why** it matters. We're integrating it into Project Wizard as a north star for all document generation.

### The Framework

| Element | Definition | Function | Question |
|---------|-----------|----------|----------|
| **Task (What)** | The tangible output/objective | Defines what you're producing or analyzing | "What am I producing?" |
| **Purpose (Why)** | The strategic intent/impact | Explains why it matters and what decision/action it should drive | "Why does this matter, and what should my reader do with it?" |

---

## How It Works

### Step 1: Begin with Task & Purpose
Every document blueprint now starts by explicitly stating:
- **Task:** What are we generating?
- **Purpose:** Who reads this and what decision will it inform?

### Step 2: Validate Every Section
Before writing, the AI confirms:
- ✓ Does this section support the **task**?
- ✓ Does this insight advance the **purpose**?
- ✗ If not, remove it

### Step 3: End by Restating Purpose
In the conclusion, explicitly reconnect to purpose:
- "This analysis supports [stated purpose], enabling [decision-maker] to [specific action]"

---

## Implementation

### Productivity Pulse Email (v1.0 - Live)

**Task:** Summarize monthly service-line productivity metrics and highlight staffing efficiency trends across facility locations

**Purpose:** Enable facility partners to understand resource utilization, identify over/understaffed areas, and inform collaborative staffing decisions

**Validation:**
- Every metric included must support staffing decisions
- Every comparison must be apples-to-apples (no unfair facility ranking)
- Closing must restate the purpose: "These insights support our collaborative staffing planning"

---

## Blueprint Examples (Models for Other Patterns)

### Example 1: White Paper

| Element | Value |
|---------|-------|
| **Task** | Summarize and evaluate proposed policy changes affecting critical care operations |
| **Purpose** | Equip board members to make informed strategic decisions about internal adoption and resource allocation |
| **Validation** | Every section must either: (a) explain the policy, (b) show its impact, or (c) recommend action. If a section doesn't, delete it. |

### Example 2: Proposal to Hospital

| Element | Value |
|---------|-------|
| **Task** | Present a structured plan for expanding TPCCC's inpatient coverage through a contracted model |
| **Purpose** | Secure a service agreement that improves patient continuity while meeting hospital staffing and quality goals |
| **Validation** | Every benefit must be tied to the hospital's problem (staffing shortage, patient continuity, quality). If not, reframe or remove. |

### Example 3: Data Analysis Report

| Element | Value |
|---------|-------|
| **Task** | Evaluate provider productivity, payer mix, and wRVU trends from Q1 to Q3 |
| **Purpose** | Support leadership in identifying performance gaps and prioritizing operational improvements |
| **Validation** | Every metric must lead to an actionable recommendation. If data is presented without implication, rewrite it. |

### Example 4: Program Evaluation

| Element | Value |
|---------|-------|
| **Task** | Assess the first-year outcomes of the Pulmonary Embolism Response Team (PERT) program |
| **Purpose** | Determine whether the program meets accreditation readiness criteria and clinical performance benchmarks |
| **Validation** | Every finding must address accreditation or clinical benchmarks. Off-topic findings get cut. |

### Example 5: Strategic Brief

| Element | Value |
|---------|-------|
| **Task** | Outline the proposed integration of Lean management into clinical operations |
| **Purpose** | Align executive leadership around the roadmap for implementing sustainable process improvement |
| **Validation** | Every component must either explain the roadmap or justify why it's needed. Competing initiatives get removed. |

---

## Integration into Blueprints

### In `blueprint.json`
```json
{
  "task_and_purpose": {
    "task": "Summarize monthly service-line productivity metrics...",
    "purpose": "Enable facility partners to understand resource utilization...",
    "validation": "Before drafting, confirm: Does every metric support the task? Does every insight advance the purpose?"
  }
}
```

### In `prompts.json`
```json
{
  "draft_generation": {
    "task_and_purpose_guidance": {
      "task": "...",
      "purpose": "...",
      "validation": "Before drafting, confirm: Does every metric support the task? Does every insight advance the purpose?"
    }
  }
}
```

### In Verification Questions
Add verification question:
```
"Does every section support the stated task and purpose? 
Is any content off-topic or tangential?"
```

---

## Benefits of This Approach

### 1. Prevents Scope Creep
- Luxury of only 3 paragraphs? Cut anything that doesn't support the purpose
- "Interesting but irrelevant" facts get removed
- Forces discipline

### 2. Improves Document Coherence
- Readers understand why they're reading this
- Every section feels connected to the next
- Less rambling, more focused narrative

### 3. Reduces Hallucinations
- LLM knows exactly what it's supposed to generate
- Easier to catch when it goes off-topic
- Verification is straightforward: "Does this support the purpose?"

### 4. Enables Feedback
- Clear statement of intent makes critiques easier
- Reader knows what you're trying to accomplish
- "Did this achieve its purpose?" is clearer than "Is this good?"

### 5. Facilitates Learning
- If purpose-driven documents work better, store them as examples
- Next month's pulse email learns from this month's
- Memory component can focus on "what worked toward the purpose"

---

## How to Apply to Your Other Documents

### For Financial Pulse Email (Future)

**Task:** Summarize monthly revenue, collections, and payer mix trends  
**Purpose:** Enable leadership to identify revenue concentration risks and prioritize payer relationships for revenue stability

**Critical rules:**
- Every metric must relate to revenue or risk
- Comparisons only within same payer category (commercial, Medicare, etc.)
- Closing must tie to action: "These trends suggest we should focus on [specific payer relationship]"

### For Scheduling Pulse Email (Future)

**Task:** Highlight monthly coverage gaps, call burnout trends, and shift utilization  
**Purpose:** Inform staffing decisions and prevent clinician burnout through proactive scheduling adjustments

**Critical rules:**
- Every metric relates to clinician workload or coverage
- Data must be apples-to-apples (day shift to day shift, night to night)
- Closing: "These patterns suggest we should adjust [specific shifts/clinicians]"

---

## Implementation Roadmap

### Phase 1 (Done ✅)
- [x] Implement Task & Purpose in Productivity Pulse Email
- [x] Document framework in prompts.json
- [x] Create verification questions

### Phase 2 (Next)
- [ ] Apply to Clinical Services Proposal
- [ ] Apply to White Paper
- [ ] Apply to Data Analysis Report
- [ ] Apply to all existing blueprints

### Phase 3 (Future)
- [ ] Implement memory component: "Store emails that achieved purpose"
- [ ] Track: "Did this pulse email lead to staffing decision?"
- [ ] Feedback loop: Next month's email learns from this month's

---

## Practical Example: Task & Purpose in Action

### Before (Without Task & Purpose)
```
The November productivity report shows interesting trends. 
ICU assignments had an average of 18.8 visits per shift with 
wRVU ranging from 53.6–69.1. HSW saw 20.4 visits/shift while 
MCA MICU had 18.4. Also, we noticed that floor assignments are 
busy, ranging from 5.7–27.6 visits per shift. Clinic is also 
getting more volume. Telehealth had 20.4 visits/shift. Overall, 
it seems like staffing might need adjustment, but we're not sure 
where...
```

**Problems:** Rambling, compares non-equivalent things, unclear why we should care

### After (With Task & Purpose)
```
Task: Summarize monthly service-line productivity metrics
Purpose: Enable partners to understand resource utilization and 
inform collaborative staffing decisions

ICU assignments across our network averaged 18.8 visits per shift 
in November (range: 17.8–20.4), with wRVU ranging from 53.6–69.1. 
This staffing level appears well-calibrated. Floor assignments 
showed 19.2 visits per shift (range: 5.7–27.6), suggesting some 
assignments carry heavier loads—an opportunity for discussion on 
staffing calibration.

These insights support our collaborative staffing planning. 
If you see areas for adjustment, please reach out.
```

**Improvements:** Focused, apples-to-apples only, clear why this matters, reiterates purpose

---

## Key Takeaways

✅ **Task & Purpose provides a north star** for all AI-generated documents  
✅ **Validates every sentence:** "Does this support the task? Does this advance the purpose?"  
✅ **Prevents hallucinations:** Easier to catch when LLM goes off-topic  
✅ **Improves coherence:** Readers understand why they're reading this  
✅ **Enables learning:** Future versions can learn from "what worked"  

---

## Reference Documents

- `patterns/productivity_pulse/blueprint.json` - First implementation
- `patterns/productivity_pulse/prompts.json` - Prompts with Task & Purpose guidance
- `patterns/productivity_pulse/README.md` - Complete usage guide
- `PRODUCTIVITY_PULSE_SUMMARY.md` - Implementation summary

---

**Status:** Framework documented and operational. Ready to apply across all blueprints.

**Next:** Apply Task & Purpose to Clinical Services Proposal, White Paper, and other existing blueprints.
