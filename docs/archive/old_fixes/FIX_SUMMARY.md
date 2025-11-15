# Fix Summary: Re-open Wizard Button Issue

## Problem
The "♻️ Re-open Wizard" button in the Deliverables tab was not working. When clicked, nothing happened.

## Root Cause
The deliverable selector used an `st.radio()` widget without a `key` parameter. This caused the radio button selection to **reset to the first option** on every page rerun.

### What was happening:
1. User selected "5W1H Analysis" (pattern_key = "5w1h_analysis")
2. User clicked "♻️ Re-open Wizard"  
3. Session state was set: `st.session_state.show_wizard_5w1h_analysis = True`
4. Page reran
5. **Radio button reset to first option** (e.g., "Project Charter", pattern_key = "project_charter")
6. Code checked: `st.session_state.show_wizard_project_charter` (False ❌)
7. Wizard didn't open because it was looking for the wrong pattern_key

## Solution
Added `key="selected_deliverable"` parameter to the `st.radio()` widget to persist the selection across reruns.

## Files Modified

### 1. `app/ui/tabs/deliverables_tab.py`
- Added session state initialization for `selected_deliverable`
- Added `key="selected_deliverable"` to radio button
- Backup: `app/ui/tabs/deliverables_tab.py.backup`

### 2. `app_v2_5.py`  
- Applied same fix to inline deliverables code
- Backup: `app_v2_5.py.backup`

## Changes Made

```python
# BEFORE
selected_deliverable = st.radio(
    "Select Deliverable:", 
    options=deliverable_options, 
    horizontal=True
)

# AFTER  
# Initialize session state for selected deliverable if not exists
if "selected_deliverable" not in st.session_state:
    st.session_state.selected_deliverable = deliverable_options[0]

selected_deliverable = st.radio(
    "Select Deliverable:", 
    options=deliverable_options, 
    horizontal=True,
    key="selected_deliverable"  # Add key to preserve selection across reruns
)
```

## Testing Instructions

1. **Restart the Streamlit app** (if not using auto-reload):
   ```bash
   pkill -f "streamlit run app_v2_5.py"
   cd /home/ivesjl/project_wizard
   nohup venv/bin/streamlit run app_v2_5.py --server.port 8502 --server.address 0.0.0.0 > /tmp/v2_output.log 2>&1 &
   ```

2. **Test the fix**:
   - Open the Project Wizard in your browser
   - Load or create a project
   - Go to the **📦 Deliverables** tab
   - Select any deliverable that exists (e.g., "5W1H Analysis")
   - Click **♻️ Re-open Wizard** button
   - **Expected**: The wizard form should open
   - **Before fix**: Nothing happened

3. **Test multiple deliverables**:
   - Switch between different deliverable types using the radio buttons
   - Verify the selection persists after clicking "Re-open Wizard"
   - Verify the correct wizard opens for each deliverable type

## Rollback
If needed, restore from backups:
```bash
cp app/ui/tabs/deliverables_tab.py.backup app/ui/tabs/deliverables_tab.py
cp app_v2_5.py.backup app_v2_5.py
```

## Status
✅ Fix applied successfully
✅ Python syntax validated
⏳ Awaiting user testing
