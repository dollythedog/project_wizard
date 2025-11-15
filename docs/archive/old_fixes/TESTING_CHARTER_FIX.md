# Testing Guide: Charter Generation Fixes

## Overview
This guide walks through testing the charter generation fixes implemented in version 2.5.3.

## Prerequisites
- Project Wizard application running (`./run_v2_5.sh` or `streamlit run app_v2_5.py`)
- A test project created or selected
- OpenAI API key configured in `.env`

## Test Case 1: Create New Charter with User Inputs

### Steps:
1. **Start the application** and navigate to Tab 2: "Charter Wizard"
2. **Complete Step 1: Project Initiation**
   - Enter a unique project title (e.g., "Test Patient Portal v2")
   - Select a project type
   - Enter executive sponsor name
   - Enter project manager name
   - Write a specific problem statement (be detailed!)
   - Set start and end dates
   - Click "Save & Continue →"
   - Verify success message appears

3. **Complete Step 2: Business Case**
   - Enter strategic alignment (specific to your test case)
   - Enter potential solutions considered
   - Enter preferred solution with rationale
   - Enter measurable benefits (include specific metrics)
   - Enter high-level requirements
   - Enter budget estimate
   - Enter resource needs
   - Click "Save & Continue →"
   - Verify success message appears

4. **Generate Charter (Step 3)**
   - Click "🎯 Generate Charter" button
   - Wait for generation (may take 10-20 seconds)
   - Verify success message: "✓ Charter generated and saved!"

5. **Verify User Inputs Are Included**
   - Navigate to Tab 4: "Deliverables"
   - Select "PROJECT_CHARTER" from radio buttons
   - Read through the generated charter
   - **CHECK:** Does the charter include your specific:
     - Project title?
     - Problem statement details?
     - Strategic alignment points?
     - Measurable benefits with your metrics?
     - Solution approach?
     - Budget and resource estimates?

### Expected Result:
✅ Charter should be a complete, well-formatted document that incorporates ALL your specific inputs, not generic boilerplate text.

### If Test Fails:
- Check browser console for errors
- Check terminal/logs for Python exceptions
- Verify `patterns/project_charter/template.md.j2` contains `{{ content }}`
- Verify `patterns/project_charter/system.md` has been updated
- Check DEBUG output in Step 3 to see what data was passed

---

## Test Case 2: Recreate Existing Charter

### Steps:
1. **Ensure you have an existing charter** (from Test Case 1 or previous work)

2. **Navigate to Tab 4: Deliverables**
   - Select "PROJECT_CHARTER" from radio buttons
   - Verify existing charter loads in the editor
   - Note some specific details from the charter

3. **Access the Wizard for Existing Charter**
   - Look for a "wizard" button or action in the document editor
   - OR: If there's a "✨ Create PROJECT_CHARTER" button, click it
   - The wizard form should appear

4. **Verify Form Pre-population**
   - **CHECK:** Are the form fields pre-populated with data from the existing charter?
   - **CHECK:** Do you see your project title?
   - **CHECK:** Do you see your problem statement?
   - **CHECK:** Do you see your strategic alignment?
   - **CHECK:** Do you see your other inputs?

5. **Modify and Regenerate**
   - Change one field (e.g., update the problem statement)
   - Click "✨ Generate" button
   - Wait for generation
   - Verify success message appears

6. **Verify Changes Applied**
   - Check that the regenerated charter reflects your modification
   - Check that other fields remained consistent

### Expected Result:
✅ Wizard form loads with existing charter data pre-populated  
✅ You can modify fields and regenerate  
✅ New charter reflects your changes

### If Test Fails:
- Check if `parse_charter_to_form_data()` is working correctly
- Look for warnings in the UI about parsing failures
- Check browser console for JavaScript errors
- Verify `existing_form_data` is being populated (add debug prints if needed)

---

## Test Case 3: Charter as Context for Other Deliverables

### Steps:
1. **Ensure you have a charter** with specific project details

2. **Generate a Work Plan**
   - Navigate to Tab 4: Deliverables
   - Select "WORK_PLAN" from radio buttons
   - Click "✨ Create WORK_PLAN" if it doesn't exist
   - Fill in the wizard fields
   - Click "✨ Generate"

3. **Verify Charter Context Used**
   - Review the generated work plan
   - **CHECK:** Does it reference your charter's:
     - Project goals?
     - Deliverables?
     - Timeline?
     - Constraints?

4. **Generate a Proposal**
   - Select "PROJECT_PROPOSAL" from radio buttons
   - Create if needed
   - **CHECK:** Does it align with charter content?

### Expected Result:
✅ Other deliverables should reference and align with charter content  
✅ ProjectContext should load charter for use in pattern generation

### If Test Fails:
- Check `app/services/project_context.py` - is it loading PROJECT_CHARTER.md?
- Verify charter file exists and is readable
- Check pattern pipeline logs for context loading

---

## Regression Testing

### Quick Checks:
- [ ] Other deliverables still generate correctly (Work Plan, 5W1H, Proposal)
- [ ] Document editor save functionality still works
- [ ] AI enhancements still work (Wording, Tone, Simplify)
- [ ] Critique system still functions
- [ ] Project selection/creation still works
- [ ] No Python syntax errors on startup
- [ ] No JavaScript console errors

---

## Troubleshooting

### Charter is still generic/missing inputs
1. Check DEBUG output in Step 3 of charter wizard
2. Verify `st.session_state.form_data` contains your inputs
3. Check `patterns/project_charter/user.md` - does it include all variable placeholders?
4. Check AI agent logs - what prompt was sent to OpenAI?

### Wizard doesn't pre-populate
1. Verify `deliverable_file.exists()` returns True
2. Check for warning message about parsing failure
3. Manually check `parse_charter_to_form_data()` output
4. Verify charter format matches what the parser expects

### Generation takes too long
1. Check OpenAI API status
2. Verify API key is valid and has credits
3. Check network connectivity
4. Consider adding timeout handling

---

## Success Criteria

All tests pass when:
- ✅ New charters include all user-provided details
- ✅ Wizard pre-populates when recreating existing charters  
- ✅ Updated charters reflect modifications
- ✅ Charter serves as context for other deliverables
- ✅ No regression in existing functionality

---

**Testing Date:** _____________  
**Tester Name:** _____________  
**Results:** ☐ Pass  ☐ Fail  ☐ Partial  
**Notes:** ___________________________________________________
