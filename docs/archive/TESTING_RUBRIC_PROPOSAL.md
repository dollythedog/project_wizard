# Proposal Generation Testing Rubric

**Date:** 2025-12-01  
**Project:** HFW Renegotiation  
**Document Type:** Contract Proposal  
**Tester:** _____________

---

## Test Flow Overview

```
User fills form → StepBackAgent questions → DraftAgent generates → User reviews → VerifierAgent scores
```

---

## Phase 1: Input Form (24 Fields)

### Expected Behavior:
- [ ] Form displays all 24 input fields from blueprint.json
- [ ] Required fields are marked with asterisk or indicator
- [ ] Field descriptions are helpful and clear
- [ ] Textarea fields have adequate space
- [ ] Form submission works without errors

### Actual Behavior:
```
[Fill in observations]


```

### Issues Found:
```


```

---

## Phase 2: StepBack Questions

### Expected Behavior:
- [ ] Agent asks 5-8 clarifying questions
- [ ] Questions are relevant to contract proposals (not generic)
- [ ] Questions reference the charter/project context
- [ ] Questions help identify gaps or clarify scope
- [ ] Questions use information from project notes

### Actual Behavior:
**Questions Asked:**
1. 
2. 
3. 
4. 
5. 

**Quality Assessment:**
```
Were questions specific? Y/N
Did they reference charter? Y/N
Did they use project notes? Y/N
Were they helpful? Y/N
```

### Issues Found:
```


```

---

## Phase 3: Draft Generation

### Expected Behavior - Structure:
- [ ] Cover letter with recipient name/address
- [ ] Executive summary (3 paragraphs)
- [ ] Key benefits (4-5 bullets)
- [ ] Experience snapshot
- [ ] Statement of Work (Phases 1-3)
- [ ] Deliverables section
- [ ] Client responsibilities section
- [ ] Terms table with pricing
- [ ] Signature block
- [ ] Attachment A (legal boilerplate)

### Expected Behavior - Content Quality:
- [ ] Uses SPECIFIC numbers from notes ($350K, 5 physicians, $175/hr, etc.)
- [ ] References charter context throughout
- [ ] Professional, business-appropriate tone
- [ ] No hallucinated names/credentials
- [ ] No vague language ("substantial", "significant")
- [ ] Client-focused (addresses their pain points)
- [ ] Benefits are measurable/concrete

### Actual Behavior - Structure Check:
```
✓/✗ Cover letter format correct?
✓/✗ All sections present?
✓/✗ Proper markdown formatting?
✓/✗ Table renders correctly?
✓/✗ Signature block formatted?
✓/✗ Attachment A included?
```

### Actual Behavior - Content Analysis:
**Specific Numbers Used:**
```
$350K loss: Y/N - Where?
5 physicians: Y/N - Where?
$175/hr rate: Y/N - Where?
$90/hr APP rate: Y/N - Where?
$6.9M target: Y/N - Where?
```

**Charter Integration:**
```
Problem statement referenced: Y/N
Solution approach mentioned: Y/N
Strategic alignment: Y/N
```

**Tone & Quality:**
```
Professional: 1-5 (5=excellent)
Client-focused: 1-5
Specificity: 1-5
No hallucinations: Y/N
```

### Issues Found:
```


```

---

## Phase 4: Document Review/Edit

### Expected Behavior:
- [ ] "View" button works
- [ ] Three tabs: Rendered, Markdown Source, Edit
- [ ] Edit tab allows direct markdown editing
- [ ] Save button persists changes to database
- [ ] Changes reflect in rendered view after save

### Actual Behavior:
```
✓/✗ All tabs functional?
✓/✗ Editing works?
✓/✗ Save successful?
✓/✗ Changes persisted?
```

### Issues Found:
```


```

---

## Phase 5: Verification (AI Review)

### Expected Behavior:
- [ ] "Review Quality" button works
- [ ] Overall score displayed (1-5 scale)
- [ ] Individual criterion scores shown:
  - Client Focus (30% weight)
  - Persuasiveness (35% weight)
  - Clarity & Professionalism (20% weight)
  - Completeness (15% weight)
- [ ] Strengths listed (3-5 items)
- [ ] Weaknesses listed (3-5 items)
- [ ] Specific improvements listed (5-10 actionable items)
- [ ] Ready for approval indicator

### Actual Behavior:
**Scores:**
```
Overall: ___/5.0
Client Focus: ___/5
Persuasiveness: ___/5
Clarity: ___/5
Completeness: ___/5
```

**Feedback Quality:**
```
Strengths are specific: Y/N
Weaknesses cite sections: Y/N
Improvements are actionable: Y/N
```

### Issues Found:
```


```

---

## Overall System Assessment

### What Worked Well:
```
1. 
2. 
3. 
```

### What Needs Improvement:
```
1. 
2. 
3. 
```

### Critical Bugs:
```
1. 
2. 
3. 
```

### Performance:
```
Form load time: _____ seconds
StepBack generation: _____ seconds
Draft generation: _____ seconds
Verification: _____ seconds

Total workflow time: _____ minutes
```

---

## Comparison to Real-World Example

### Structural Match:
```
Cover letter format: Similar / Different - Notes:
Executive summary: Similar / Different - Notes:
Statement of work: Similar / Different - Notes:
Terms section: Similar / Different - Notes:
Legal boilerplate: Similar / Different - Notes:
```

### Content Match:
```
Professional tone: Match / Don't Match - Notes:
Specificity level: Match / Don't Match - Notes:
Client focus: Match / Don't Match - Notes:
```

---

## Recommendations

### Priority 1 (Critical):
```


```

### Priority 2 (Important):
```


```

### Priority 3 (Nice to Have):
```


```

---

## Sign-off

**Tested By:** _______________  
**Date:** _______________  
**Overall Pass/Fail:** _______  
**Ready for Production:** Y/N

---

## Notes & Observations

```
[Free-form notes about the testing experience]




```
