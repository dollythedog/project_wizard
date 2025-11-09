# Project Issues Tracker

This document tracks known issues, bugs, and their resolutions for the Project Wizard.

**Last Updated:** 2024-11-06  
**Current Version:** 2.0.0

---

## Active Issues

*No active issues at this time* ✅

---

## Resolved Issues

### Issue #1: AI Critique Shows 0% Score
**Status:** ✅ RESOLVED  
**Severity:** High  
**Reported:** 2024-11-06  
**Resolved:** 2024-11-06  
**Version Fixed:** 2.0.0

**Description:**  
When running Quality Critique in Tab 5, the overall score displayed as 0% even though the API call was successful and the AI was returning valid scores.

**Root Cause:**  
Data structure mismatch between `critic_agent.py` output format and `app_streamlit_v2.py` display code expectations.

Critic returns:
```json
{
  "weighted_score": 0.82,        // 0.0-1.0 scale
  "approved": true,              // boolean
  "scores": [...],               // array
  "overall_assessment": "..."    // string
}
```

App expected:
```json
{
  "overall_score": 82,           // percentage
  "passed": true,                // different field
  "criteria_scores": {...},      // dict
  "summary": "..."               // different field
}
```

**Solution:**  
Updated Tab 5 display code (lines 443-505) to properly transform critic_agent output:
1. Convert `weighted_score` from 0.0-1.0 to percentage: `int(weighted_score * 100)`
2. Use `approved` instead of `passed`
3. Iterate `scores` array instead of `criteria_scores` dict
4. Display `overall_assessment` instead of `summary`
5. Added display of `critical_gaps` and `recommended_next_steps`

**Files Modified:**
- `app_streamlit_v2.py` (lines 443-505)

**Documentation:**
- Created `CRITIQUE_FIX.md` with detailed technical analysis

**Testing:**
- Verified scores now display correctly (e.g., 78%, 85%)
- Confirmed all 6 criteria show detailed feedback
- Validated strengths/weaknesses/improvements display

---

### Issue #2: OpenAI API Key Not Found on v2.0 Launch
**Status:** ✅ RESOLVED  
**Severity:** Critical  
**Reported:** 2024-11-06  
**Resolved:** 2024-11-06  
**Version Fixed:** 2.0.0

**Description:**  
v2.0 app crashed on startup with error:
```
ValueError: OpenAI API key not found. Set OPENAI_API_KEY environment variable.
```

**Root Cause:**  
Missing `load_dotenv()` call in `app_streamlit_v2.py`. The v1.0 app had this import, but it was omitted when creating v2.0.

**Solution:**  
Added to top of `app_streamlit_v2.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # Loads OPENAI_API_KEY from .env file
```

**Files Modified:**
- `app_streamlit_v2.py` (lines 1-10)

**Testing:**
- Verified v2.0 starts without errors
- Confirmed AI Enhancement works
- Validated Quality Critique functions properly

---

### Issue #3: "Edit Manually" Button Not Editable
**Status:** ✅ RESOLVED  
**Severity:** Medium  
**Reported:** 2024-11-06 (during development)  
**Resolved:** 2024-11-06  
**Version Fixed:** 2.0.0

**Description:**  
Clicking "Edit Manually" button in Tab 3 didn't provide an editable text area to modify AI-enhanced text.

**Root Cause:**  
Initial implementation didn't include state management for manual editing workflow.

**Solution:**  
Implemented state-based editing system:
1. Added `st.session_state.manual_edits` dictionary
2. On "Edit Manually" click: store enhanced text in manual_edits
3. Display editable `st.text_area` with the content
4. "Save Manual Edit" button updates `form_data` and clears temporary states
5. Integrated with Accept/Reject workflow

**User Flow:**
1. Click "✨ Enhance" → see AI suggestion
2. Click "✏️ Edit Manually" → get editable text area
3. Modify text → Click "💾 Save Manual Edit"
4. Changes saved and used in charter generation

**Files Modified:**
- `app_streamlit_v2.py` (Tab 3 section, lines 250-320)

---

### Issue #4: AI Hallucination - Fabricating Metrics
**Status:** ✅ RESOLVED  
**Severity:** Critical  
**Reported:** 2024-11-06 (during testing)  
**Resolved:** 2024-11-06  
**Version Fixed:** 2.0.0

**Description:**  
User reported that when inputting "The current website for Texas Pulmonary is outdated," the AI added fabricated metrics like:
- "website traffic has decreased by 30%"
- "session duration dropped to under two minutes"
- "25% increase in bounce rates"

None of these were provided by the user.

**Root Cause:**  
AI was using generic prompts without explicit constraints against inventing data. Temperature setting (0.7) was too high, allowing creative generation.

**Solution:**  
Multi-layered approach:

1. **Structured Prompt Library** (`configs/enhancement_prompts.json`):
   - Meta-level constraints: "NEVER invent metrics, preserve all user facts"
   - Per-field forbidden actions list
   - Explicit examples showing what NOT to do

2. **Updated charter_agent.py**:
   - `enhance_section()` method loads structured prompts
   - System prompt includes CRITICAL CONSTRAINTS
   - User prompt includes explicit "PRESERVE ALL USER FACTS" instruction
   - Reduced temperature from 0.7 → 0.3 (conservative)

3. **Charter Generation Strategy Change**:
   - Moved from AI-generated to template-based
   - Charter built directly from user's form_data
   - AI only used for text enhancement, not content creation

**Prevention Measures:**
- Structured prompt library with meta-constraints
- Conservative temperature (0.3)
- Template-based generation
- Multiple layers of "do not fabricate" instructions

**Testing:**
- Verified enhancement preserves user facts exactly
- Confirmed no metrics added unless user provided them
- Validated with multiple test cases

**Files Modified:**
- `app/services/ai_agents/charter_agent.py`
- `configs/enhancement_prompts.json` (created)
- `app_streamlit_v2.py` (Tab 4 generation logic)

---

## Known Limitations

### L1: Tab 6 (Create Project) Not Implemented
**Status:** 🚧 PLANNED  
**Severity:** Medium  
**Target:** v2.1.0

**Description:**  
Tab 6 shows placeholder text. Project scaffolding and OpenProject API integration not yet implemented.

**Workaround:**  
Download charter from Tab 4 and manually create project structure. User already has OpenProject API integration working separately.

**Planned Solution:**
- Implement folder structure generation
- Add file generation (README, CHANGELOG, LICENSE, .gitignore)
- Integrate with user's existing OpenProject API code
- Create tasks automatically from charter sections

---

### L2: No Session Persistence Across Days
**Status:** 🚧 PLANNED  
**Severity:** Low  
**Target:** v2.1.0

**Description:**  
Session state clears when browser is closed or service is restarted. Users lose in-progress charter data.

**Workaround:**  
Complete charter in one session or copy text to external document.

**Planned Solution:**
- Add auto-save to browser localStorage
- Implement draft management system
- Allow saving and loading charter drafts
- Session recovery on page refresh

---

### L3: Single User Only
**Status:** 🚧 PLANNED  
**Severity:** Low  
**Target:** v2.2.0

**Description:**  
No authentication or multi-user support. All users share same session state on server.

**Workaround:**  
Run on local network, coordinate usage with team members.

**Planned Solution:**
- Add authentication (OAuth, username/password)
- User-specific session management
- Charter ownership and permissions
- Collaboration features (comments, approvals)

---

## Issue Templates

### Bug Report Template
```markdown
**Title:** Brief description of the issue

**Status:** 🐛 ACTIVE / ✅ RESOLVED  
**Severity:** Critical / High / Medium / Low  
**Reported:** YYYY-MM-DD  
**Resolved:** YYYY-MM-DD (if applicable)

**Description:**  
Detailed description of the bug and its symptoms.

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**  
What should happen.

**Actual Behavior:**  
What actually happens.

**Root Cause:**  
Technical explanation of why it happens.

**Solution:**  
How it was fixed.

**Files Modified:**
- file1.py
- file2.yaml

**Testing:**
- Verification steps performed
```

### Feature Request Template
```markdown
**Title:** Feature name

**Status:** 💡 PROPOSED / 🚧 PLANNED / ✅ IMPLEMENTED  
**Priority:** High / Medium / Low  
**Target Version:** X.X.X

**Description:**  
What the feature should do.

**User Story:**  
As a [user type], I want [goal] so that [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Technical Notes:**  
Implementation approach and considerations.
```

---

## Issue Workflow

### Lifecycle States
1. **🐛 ACTIVE** - Known bug, not yet resolved
2. **🔍 INVESTIGATING** - Under investigation
3. **🚧 IN PROGRESS** - Fix in development
4. **✅ RESOLVED** - Fixed and deployed
5. **🗄️ ARCHIVED** - Closed without fix (wontfix, duplicate, etc.)

### Severity Levels
- **Critical** - Service down, data loss, security vulnerability
- **High** - Major feature broken, significant user impact
- **Medium** - Feature partially broken, workaround available
- **Low** - Minor cosmetic issue, minimal impact

---

## GitHub Issues Integration

This local ISSUES.md file mirrors GitHub Issues for offline tracking.

**Sync Strategy:**
1. Create issue in GitHub when discovered
2. Update ISSUES.md when resolved
3. Keep both in sync on each commit

**GitHub Labels:**
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `v2.0` - Related to v2.0 release
- `v2.1` - Planned for v2.1
- `critical` - Needs immediate attention
- `wontfix` - Will not be fixed

---

## Contact & Reporting

**Project Owner:** dollythedog  
**Repository:** github.com/dollythedog/project_wizard

To report a new issue:
1. Check this file for existing issues
2. Create GitHub Issue with appropriate template
3. Update this file in next commit

---

**Document Version:** 2.0.0  
**Last Review:** 2024-11-06  
**Next Review:** When v2.1 development begins

### Issue #2: Non-Functional Recent Projects Sidebar
**Status:** ✅ RESOLVED  
**Severity:** High  
**Reported:** 2024-11-09  
**Resolved:** 2024-11-09  
**Version Fixed:** 2.5.1

**Description:**  
The "Recent Projects" sidebar showed "project_wizard" (the app directory itself) instead of actual user projects. Clicking on entries did nothing, making project navigation broken.

**Root Cause:**  
- Charter was being saved to app root directory instead of dedicated project folders
- Recent projects tracked directory paths without proper project metadata
- No proper project registration system

**Solution:**  
Complete project management system overhaul:
- Created `ProjectRegistry` service for metadata tracking
- Implemented visual Project Gallery with project cards
- Added New Project wizard with proper directory creation
- Created `~/Projects/` directory structure
- Migrated Hermes project to proper location
- Replaced simple path list with full registry system (`.project_wizard_projects.json`)

**Files Changed:**  
- `app_v2_5.py` - Complete rewrite of project management UI
- `app/services/project_registry.py` - New project registry service

