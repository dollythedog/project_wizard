# Root Folder Cleanup Plan

## Current Issues
1. **Multiple app versions**: `app_v2_5.py` and `app_v2_5_refactored.py` causing confusion
2. **Session/phase tracking docs scattered**: PHASE1, PHASE2, PHASE3, SESSION_SUMMARY, etc.
3. **Proposal/planning docs in root**: Should be in docs/archive or docs/planning
4. **Multiple fix summaries**: CHARTER_FIX_SUMMARY, FIXES_NEEDED, FIX_SUMMARY, etc.

## Proposed Structure

### Keep in Root (Production Files)
- `app_v2_5_refactored.py` → **rename to** → `app.py` (main app)
- `setup.py` (installation)
- `README.md` (project overview)
- `PROJECT_CHARTER.md` (this project's charter)
- `PROJECT_PLAN.md` (this project's plan)
- `CHANGELOG.md` (version history)
- `ISSUES.md` (current issues)

### Move to docs/archive/
- `app_v2_5.py` (old version, keep as backup)
- All PHASE*.md files
- SESSION_SUMMARY.md
- DEPLOYMENT_COMPLETE.md
- REFACTORING_SUMMARY.md
- All proposal docs (PROPOSAL_*.md)
- All fix summaries (CHARTER_FIX_SUMMARY.md, TESTING_CHARTER_FIX.md, FIXES_NEEDED.md)
- PROJECT_MANAGEMENT_UPGRADE.md
- WORK_PLAN_PATTERN.md

### Actions
1. Create docs/archive/old_sessions/ if not exists
2. Move archived files
3. Rename app_v2_5_refactored.py → app.py
4. Update systemd service to use app.py
5. Remove .backup files created during fix

## Benefits
- Single source of truth for the app (`app.py`)
- Clean root directory
- Historical docs preserved but out of the way
- Easier for new contributors to understand structure
