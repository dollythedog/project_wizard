# Project Wizard v3.0 - Testing Rubric

**Date:** 2025-12-01  
**Version:** 3.0.0-beta  
**Tester:** _______________________

---

## Configuration Review ✅

Before testing, verify your `.env` file:

### Expected Configuration
```bash
# Required (check ONE)
OPENAI_API_KEY=sk-proj-...        # ✅ Should start with "sk-"
# OR
ANTHROPIC_API_KEY=sk-ant-...      # ✅ Should start with "sk-ant-"

# OpenAI Settings (if using OpenAI)
OPENAI_MODEL=gpt-4                 # Options: gpt-4, gpt-4o, gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4000             # Recommended: 4000-8000
OPENAI_TEMPERATURE=0.7             # Recommended: 0.7 (creative) or 0.3 (focused)

# Anthropic Settings (if using Anthropic)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Latest model
```

### Configuration Checklist
- [ ] API key starts with correct prefix (sk- or sk-ant-)
- [ ] Model name is valid
- [ ] Temperature is between 0.0-2.0 (recommend 0.3-0.9)
- [ ] Max tokens is reasonable (2000-8000)

**Notes:** _________________________________________________________________

---

## Test Scenario: Healthcare Monitoring MVP

We'll create a realistic healthcare project to test all features.

### Project Details
- **Title:** Post-Discharge Patient Monitoring System
- **Type:** software_mvp
- **Description:** SMS-based check-in system for post-discharge patients using Twilio

---

## Phase 1: System Startup (5 points)

### 1.1 Server Start
**Command:** `python run_web.py`

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| Server starts without errors | ✅ | ☐ Pass / ☐ Fail | 1 |
| Port 8000 accessible | ✅ | ☐ Pass / ☐ Fail | 1 |
| Database initialized message shown | ✅ | ☐ Pass / ☐ Fail | 1 |
| No API key warnings | ✅ | ☐ Pass / ☐ Fail | 1 |
| Navigate to http://localhost:8000 | ✅ Works | ☐ Pass / ☐ Fail | 1 |

**Score: ___5__ / 5**

**Issues/Notes:** Nothing really to note here, it started up very well. I do see there is an error in the error log that some favicon.ico HTTP/1.1 had a 404 error but the actual app itself looks gorgeous.
---

## Phase 2: Project Creation (10 points)

### 2.1 Create Project via Web UI

**Steps:**
1. Click "+ New Project"
2. Fill in form with test data
3. Submit

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| "New Project" button visible and clickable | ✅ | x Pass / ☐ Fail | 1 |
| Form displays correctly | ✅ | x Pass / ☐ Fail | 1 |
| Project type dropdown has options | ✅ | x Pass / ☐ Fail | 1 |
| Form validation works | ✅ | x Pass / ☐ Fail | 1 |
| Project created successfully | ✅ | x Pass / ☐ Fail | 2 |
| Redirected to project detail page | ✅ | x Pass / ☐ Fail | 2 |
| Project details display correctly | ✅ | x Pass / ☐ Fail | 2 |

**Score: __10___ / 10**

**Issues/Notes:** 
The Project type dropdown has fixed options and I need the ability to add new project types

---

## Phase 3: Add Project Context (15 points)

### 3.1 Add Note #1: System Requirements

**Content:**
```
- SMS-based patient check-ins via Twilio
- Daily automated messages to patients
- Yes/No response pattern
- Weekly CSV imports for patient list
- HIPAA compliance required
- No PHI in SMS messages
- PostgreSQL database with encryption
```

### 3.2 Add Note #2: Technical Stack

**Content:**
```
- Backend: Python FastAPI
- Database: PostgreSQL 15+
- SMS: Twilio API
- Frontend: Simple web dashboard (Streamlit or basic HTML)
- Hosting: Local MiniPC (Ubuntu 22.04)
- Authentication: Basic username/password
```

### 3.3 Add Note #3: User Workflow

**Content:**
```
1. System sends daily check-in SMS at 9 AM
2. Patient receives: "How are you feeling today? Reply 1 (Good) or 2 (Not well)"
3. Patient responds with number
4. System triages response:
   - Good: Log and continue monitoring
   - Not well: Alert care team via email/Slack
5. Weekly CSV updates patient roster
6. Dashboard shows patient status and alert history
```

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| "Add Note" button visible | ✅ | x Pass / ☐ Fail | 1 |
| Note form appears | ✅ | x Pass / ☐ Fail | 1 |
| Can enter title and content | ✅ | x Pass / ☐ Fail | 2 |
| Note #1 saves successfully | ✅ | x Pass / ☐ Fail | 2 |
| Note #1 displays on project page | ✅ | x Pass / ☐ Fail | 1 |
| Note #2 saves successfully | ✅ | x Pass / ☐ Fail | 2 |
| Note #3 saves successfully | ✅ | x Pass / ☐ Fail | 2 |
| All 3 notes visible on project page | ✅ | x Pass / ☐ Fail | 2 |
| Notes display in correct order | ✅ | x Pass / ☐ Fail | 1 |
| Markdown formatting works | ✅ | x Pass / ☐ Fail | 1 |

**Score: __15___ / 15**

**Issues/Notes:** 
This looks like it worked very well. I love this concept of adding notes that grows the context to send to the agents and that I can grow it over time. 

---

## Phase 4: Generate Project Charter (30 points)

### 4.1 Initiate Generation

**Steps:**
1. Click "📄 Generate Document" button
2. Select "Project Charter"

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| "Generate Document" button visible | ✅ | x Pass / ☐ Fail | 1 |
| Template selection page loads | ✅ | x Pass / ☐ Fail | 2 |
| 3 templates displayed (charter, work_plan, proposal) | ✅ | x Pass / ☐ Fail | 2 |
| Template descriptions are clear | ✅ | xPass / ☐ Fail | 1 |
| Can click "Project Charter" | ✅ | x Pass /  Fail | 1 |

**Score: __7___ / 7**


### 4.2 Step-Back Questions

> ! The order was switched to first collect the inputs and then to do the step-back questions, but I will include the responses below, just note that the order changed. 

This step 

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| Questions page loads (3-10 sec) | ✅ | x Pass / ☐ Fail | 2 |
| Displays 5-7 questions | ✅ 5-7 questions | x Pass / ☐ Fail | 2 |
| Questions are numbered | ✅ | x Pass / ☐ Fail | 1 |
| Questions are relevant to healthcare/MVP | ✅ | x Pass / ☐ Fail | 3 |
| Questions reference project context (notes) | ✅ | x Pass / ☐ Fail | 3 |
| Textareas provided for answers | ✅ | x Pass / ☐ Fail | 1 |
| Form is usable and clear | ✅ | x Pass / ☐ Fail | 1 |

**Score: __13___ / 13**

**Question Quality (1-5 scale):**
- Relevance to project: __5___ / 5
- Clarity of questions: ___5__ / 5
- Usefulness for charter: __5___ / 5

**Example questions received:**
1. What specific criteria will be used to flag high-risk patients in the text responses?
2.  How will the system ensure HIPAA compliance, considering the sensitive nature of patient health information?
3. What specific features are required for the web dashboard?
4. What measures will be put in place to handle false flags or patients who may accidentally input incorrect information?
5. What is the estimated budget for this project, including Twilio costs and server maintenance?
6. Are there any existing systems or technologies in place that the new system needs to integrate or collaborate with, besides the stated exclusion of EHR?
7. What kind of support is expected from the hospital staff in the implementation and operation of this system?

### 4.3 Draft Generation

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| Submit answers successfully | ✅ | x Pass / ☐ Fail | 1 |
| Loading spinner appears | ✅ | x Pass / ☐ Fail | 1 |
| Generation completes (30-90 sec) | ✅ | x Pass / ☐ Fail | 2 |
| Draft page loads | ✅ | x Pass / ☐ Fail | 2 |
| Document is substantial (3-5 pages) | ✅ | x Pass / ☐ Fail | 2 |
| Rendered HTML view works | ✅ | x Pass / ☐ Fail | 1 |
| Markdown source view works | ✅ | x Pass / ☐ Fail | 1 |
| Tab switching works | ✅ | x Pass / ☐ Fail | 1 |
| Analysis summary displayed | ✅ | x Pass / ☐ Fail | 1 |

**Score: ___12__ / 12**

- Having suggested inputs for the fields would be helpful (like from the ones we approve at the end?). In fact, this sort of functionality is already built-in with the checkboxes that are offered to the user under the label section "Selection Criteria". It was rendered from the following in the blueprint.json for the charter
   - For example:
      "```json
      "options": [
            {"value": "cost_effective", "label": "Cost Effective"},
            {"value": "quick_wins", "label": "Quick Wins Possible"},
            {"value": "strategic_importance", "label": "Strategic Importance"},
            {"value": "stakeholder_support", "label": "Strong Stakeholder Support"},
            {"value": "technical_feasibility", "label": "Technical Feasibility"}
            ]
      ```
   - This sort of thing is probably true for a lot of areas of the fields, where I can learn the types of inputs that work well for those variables. It would seem this json formatting could incorporate some sort of feature like this dynamically to learn over time? IDK how much sense this makes
- Business need and problem/opportunity definition are overlapping
- The selection criteria with checkboxes is a great idea but they are not vertically aligned properly and the checkboxes appear to be at the top of that row and the text appears at the bottom?

**Performance Metrics:**
- Questions generation time: _______ seconds
- Draft generation time: _______ seconds
- Total time: _______ seconds
- I didn't see any timing outputs. 

---

## Phase 5: Document Quality Assessment (25 points)

### 5.1 Content Completeness

Review the generated charter. Does it include:

| Section | Present | Quality (1-5) | Notes |
|---------|---------|---------------|-------|
| Executive Summary | ☐ | _____ | _______No executive summary was provided. __________ |
| Business Case | ☐ | _____ | _________________ |
| Project Objectives | ☐ | _____ | _________________ |
| Scope & Deliverables | ☐ | _____ | _________________ |
| Stakeholders | ☐ | _____ | _________________ |
| Success Criteria | ☐ | _____ | _________________ |
| Risks & Mitigation | ☐ | _____ | _________________ |
| Timeline/Milestones | ☐ | _____ | _________________ |
| Budget/Resources | ☐ | _____ | _________________ |

**Sections present: ___0__ / 9** (2 points)

It looks like the format of in the template was not followed at all. It looks like it basically just added more text to the input variables (like it cleaned up what I put in there)

It might just be easiest for me to share it with you:
```md
# Aether Bot Project Charter

## 1. Project Goal
The primary goal of the Aether Bot project is to create a secure, SMS-based chatbot system, using Twilio, for post-discharge patient monitoring. This system will automate daily check-ins with a series of structured questions and simple flowcharts.
The success of this project will be measured based on the following criteria:
- Patients receive daily check-in messages in line with the established schedule
- No Protected Health Information (PHI) is transmitted in violation of HIPAA regulations

## 2. Business Need & Opportunity
Chronic Obstructive Pulmonary Disease (COPD) exacerbation patients have high re-admission rates, placing significant financial and manpower burdens on hospitals. The Aether Bot project presents an opportunity to alleviate this issue by providing a structured, automated system for post-discharge patient monitoring and triage.

## 3. Problem/Opportunity Definition
The project aims to address the high re-admission rates among COPD exacerbation patients by effectively monitoring their health status post-discharge and flagging high-risk patients for further action such as phone calls, tele-visits, or clinic visits.

## 4. Proposed Solution
The proposed solution is the Aether Bot, an SMS chatbot that sends out scheduled messages with structured questions to patients post-discharge. High-risk patients, based on their responses, will be flagged for further follow-up actions.

## 5. Alignment with Strategic Goals
The Aether Bot aligns with the organizational goals of providing high-quality and cost-effective care. By reducing the readmission rates, the project contributes to the efficient allocation of resources while maintaining a high standard of patient care.

## 6. Selection Criteria
The Aether Bot was selected for its strategic importance in addressing the critical issue of high re-admission rates and its potential to improve patient care while easing the hospital's financial and manpower burdens.

## 7. Cost/Benefit Analysis
A detailed cost/benefit analysis will be completed during the planning phase of the project. However, the anticipated benefits include decreased readmission rates, more efficient use of hospital resources, and improved patient care.

## 8. Scope
The project scope includes the development and implementation of an SMS-based chatbot for post-discharge patient monitoring. The scope does not extend to the integration of the chatbot with the Electronic Health Record (EHR) system.

## 9. Major Deliverables
- A functional SMS chatbot system using Twilio
- A dashboard for monitoring and tracking patient responses
- A presentation for executives detailing the project's implementation and benefits

## 10. Risks & Mitigation
One major risk identified is the potential for an increased workload due to unnecessary flags. This risk will be mitigated through careful refinement of the patient triage criteria to minimize false positives. 

## 11. Schedule Overview
The project will be implemented over an estimated duration of six weeks. Detailed scheduling will be established during the planning phase.

## 12. High-Level Requirements
The project requires a server to run the system and a Twilio account for the SMS functionality. Additionally, the system must ensure HIPAA compliance by not transmitting PHI in the SMS messages.

## 13. Collaboration Needs 
Collaboration will be required with hospital staff for the implementation and operation of the system. The extent of this collaboration will be defined during the planning phase.
```

And I might as well just share the summary provided at the top of the document:
```md
📊 Analysis Summary

            The core problem identified is the need for a post-discharge patient monitoring system that can effectively track the health status of patients and triage them based on their responses. The opportunity lies in developing an SMS-based check-in system that uses Twilio, enabling daily automated messages to patients and allowing them to respond with a simple yes/no pattern. The system will also need to import a weekly CSV file for the patient list and maintain HIPAA compliance. 

The key requirements for this system include a backend developed in Python FastAPI, a PostgreSQL database, and a frontend with a simple web dashboard. The system should be hosted on a local MiniPC running Ubuntu 22.04 and should provide basic username/password authentication. It is crucial to ensure that no PHI is included in the SMS messages for HIPAA compliance. A manual review of the flagged patients will be conducted weekly, and daily emails will be sent out for patients requiring a phone call. 

However, there are certain gaps and areas that require clarification. The project's budget appears to be limited at $250, and it is unclear whether this includes server maintenance and Twilio costs. Moreover, the criteria for flagging high-risk patients need to be clearly defined. Finally, the support expected from the hospital staff during the implementation and operation of this system is not specified. 

In light of these findings, the project charter should focus on defining the technical specifications, establishing clear criteria for patient triage, ensuring HIPAA compliance, and detailing the review and reporting process. It should also address budgeting concerns and clarify roles and responsibilities during the project's implementation.
```


### 5.2 Context Integration

| Criteria | Score (1-5) | Comments |
|----------|-------------|----------|
| Used information from Note #1 (Requirements) | _____ | _________________ |
| Used information from Note #2 (Tech Stack) | _____ | _________________ |
| Used information from Note #3 (Workflow) | _____ | _________________ |
| Information is accurate and relevant | _____ | _________________ |
| Context is well-integrated, not just copied | _____ | _________________ |

**Context Score: _____ / 25** (5 points)

### 5.3 Writing Quality

| Criteria | Score (1-5) | Comments |
|----------|-------------|----------|
| Professional tone | _____ | _________________ |
| Grammar and spelling | _____ | _________________ |
| Clear and concise | _____ | _________________ |
| Logical organization | _____ | _________________ |
| Appropriate level of detail | _____ | _________________ |

**Writing Score: _____ / 25** (5 points)

### 5.4 Healthcare/Compliance Awareness

| Criteria | Present | Score (1-5) | Comments |
|----------|---------|-------------|----------|
| Mentions HIPAA compliance | ☐ | _____ | _________________ |
| Addresses PHI handling | ☐ | _____ | _________________ |
| Security/encryption mentioned | ☐ | _____ | _________________ |
| Patient privacy considerations | ☐ | _____ | _________________ |

**Compliance Score: _____ / 20** (4 points)

### 5.5 Actionability

| Criteria | Score (1-5) | Comments |
|----------|-------------|----------|
| Clear next steps | _____ | _________________ |
| Realistic and achievable | _____ | _________________ |
| Could hand this to a developer | _____ | _________________ |

**Actionability Score: _____ / 15** (3 points)

### 5.6 Overall Document Assessment

**Would you use this charter as-is? (circle one)**
- YES, ready to use
- YES, with minor edits (< 15 minutes)
- MAYBE, needs moderate edits (15-30 minutes)
- NO, needs substantial rework (> 30 minutes)

**Estimated time saved vs. manual creation:** _______ minutes

**Score: _____ / 25**

---

## Phase 6: User Experience (10 points)

| Criteria | Score (1-5) | Comments |
|----------|-------------|----------|
| UI is intuitive and easy to navigate | _____ | _________________ |
| Forms are clear and well-labeled | _____ | _________________ |
| Visual design is professional | _____ | _________________ |
| Loading states are clear | _____ | _________________ |
| Error messages are helpful (if any) | _____ | _________________ |
| Copy/download functionality works | _____ | _________________ |

**Score: _____ / 30** (normalize to 10 points)

---

## Phase 7: Generate Additional Document (10 points)

### Test: Generate Work Plan for Same Project

| Criteria | Expected | Actual | Points |
|----------|----------|--------|--------|
| Can navigate back to project | ✅ | ☐ Pass / ☐ Fail | 1 |
| Generate another document | ✅ | ☐ Pass / ☐ Fail | 1 |
| Select "Work Plan" template | ✅ | ☐ Pass / ☐ Fail | 1 |
| Questions are different from charter | ✅ | ☐ Pass / ☐ Fail | 2 |
| Work plan generates successfully | ✅ | ☐ Pass / ☐ Fail | 2 |
| Work plan has different structure | ✅ | ☐ Pass / ☐ Fail | 2 |
| Uses same project context | ✅ | ☐ Pass / ☐ Fail | 1 |

**Score: _____ / 10**

**Work Plan Quality (brief notes):** _____________________________________________

---

## Bonus Tests (5 points)

### Copy to Clipboard
- [ ] Copy button works
- [ ] Content is properly formatted

### Download Markdown
- [ ] Download button works
- [ ] File has correct name (includes project title)
- [ ] Markdown is valid

### Token Usage Display
- [ ] Token usage shown
- [ ] Numbers seem reasonable (~3000-6000 total)

**Bonus Score: _____ / 5**

---

## Bug Tracking

### Bugs Found

| Severity | Description | Steps to Reproduce | Workaround |
|----------|-------------|-------------------|------------|
| ☐ Critical ☐ Major ☐ Minor | | | |
| ☐ Critical ☐ Major ☐ Minor | | | |
| ☐ Critical ☐ Major ☐ Minor | | | |

---

## Final Scoring

| Phase | Points Possible | Points Earned | % |
|-------|----------------|---------------|---|
| 1. System Startup | 5 | _____ | _____ % |
| 2. Project Creation | 10 | _____ | _____ % |
| 3. Add Context (Notes) | 15 | _____ | _____ % |
| 4. Generate Charter | 30 | _____ | _____ % |
| 5. Document Quality | 25 | _____ | _____ % |
| 6. User Experience | 10 | _____ | _____ % |
| 7. Additional Document | 10 | _____ | _____ % |
| Bonus | 5 | _____ | _____ % |
| **TOTAL** | **110** | **_____** | **_____ %** |

### Grade Scale
- **95-110%**: Exceeds Expectations (MVP+ ready for production)
- **85-94%**: Meets Expectations (MVP ready, minor polish needed)
- **70-84%**: Partially Meets (Functional but needs improvement)
- **Below 70%**: Does Not Meet (Significant work needed)

---

## Qualitative Feedback

### What worked really well?
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

### What needs improvement?
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

### Unexpected issues?
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

### Would you use this tool for real projects?
☐ YES, definitely  
☐ YES, with improvements: ________________________________________________  
☐ MAYBE, needs: __________________________________________________________  
☐ NO, because: ___________________________________________________________

### Most valuable feature?
_________________________________________________________________________

### Least valuable feature?
_________________________________________________________________________

### Recommended next priority?
☐ VerifierAgent (quality checks)  
☐ File upload support  
☐ Memory system (learning)  
☐ More templates  
☐ Better UI/UX  
☐ Other: _________________________________________________________________

---

## API Cost Analysis

**Estimated costs for this test session:**

| Action | Tokens Used | Estimated Cost |
|--------|-------------|----------------|
| Questions (Charter) | _______ | $_______ |
| Draft (Charter) | _______ | $_______ |
| Questions (Work Plan) | _______ | $_______ |
| Draft (Work Plan) | _______ | $_______ |
| **Total** | **_______** | **$_______** |

**Notes:** _________________________________________________________________

---

**Tester Signature:** _______________________ **Date:** _________________
