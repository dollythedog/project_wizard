# Project Management System Upgrade - v2.5

## Date: November 9, 2025

## Summary
Complete overhaul of project management in Project Wizard v2.5, replacing the broken "Recent Projects" system with a proper project registry and visual project gallery.

## Changes Made

### 1. Hermes Project Relocated
- **From:** `/home/ivesjl/project_wizard/PROJECT_CHARTER.md`
- **To:** `/home/ivesjl/Projects/Hermes/PROJECT_CHARTER.md`
- Created proper project directory structure at `/home/ivesjl/Projects/`

### 2. New Project Registry System
- **File:** `app/services/project_registry.py`
- **Registry Data:** `~/.project_wizard_projects.json`
- Tracks project metadata:
  - Name, path, description
  - Project type and icon
  - Created date, last modified, last accessed
- Methods: register, update, remove, list, touch projects

### 3. Redesigned UI

#### Welcome Screen
- Shows when no project is loaded
- Two main actions: "Browse My Projects" or "Create New Project"

#### Project Gallery (📚 My Projects button)
- Visual grid of project cards (3 columns)
- Shows icon, name, type, description, created date
- Actions: Open project, Remove from list
- Replaces non-functional "Recent Projects" sidebar

#### New Project Dialog (➕ New Project button)
- Guided project creation workflow
- Fields:
  - Project name (required)
  - Icon selection (20 emoji options)
  - Project type dropdown
  - Description (optional)
  - Base directory (defaults to `~/Projects`)
- Automatically creates project directory
- Sanitizes project name for folder structure
- Shows preview of where project will be created

#### Sidebar Improvements
- Shows current project with icon and name
- Quick access buttons: "My Projects" and "New Project"
- Recent Projects list (5 most recent)
- Clickable folder icons to quickly load projects

### 4. Enhanced Project Workflow
- Projects are now properly tracked and organized
- Each project gets its own directory
- Charter files stay in project directories
- Last accessed tracking for "Recent Projects"
- Projects directory structure matches Windows setup (`~/Projects` like `C:\Projects`)

### 5. Files Modified
- `app_v2_5.py` - Complete rewrite of project management
- `app_v2_5.py.backup` - Backup of original version
- Created `app/services/project_registry.py` - New registry system

### 6. Data Migration
- Hermes project registered in new system
- Old `.project_wizard_recent.json` removed
- New `.project_wizard_projects.json` created

## How to Use

### Start the App
```bash
./run_v2_5.sh
# or
streamlit run app_v2_5.py
```

### Create New Project
1. Click "➕ New Project" in sidebar
2. Enter project details
3. Choose icon
4. Select project type
5. Set base directory (default: ~/Projects)
6. Click "🚀 Create Project"

### Open Existing Project
1. Click "📚 My Projects" in sidebar
2. Browse project gallery
3. Click "📂 Open" on desired project

### Quick Access
- Use sidebar "Recent Projects" for fast switching
- Click folder icon (📂) next to project name

## Benefits
✅ Visual project organization with icons
✅ Proper project directory structure
✅ No more confusion about current project
✅ Easy project switching
✅ Metadata tracking (dates, types, descriptions)
✅ Consistent with Windows workflow
✅ Scalable to many projects

## Next Steps
- Test creating a new project through the UI
- Verify Hermes loads correctly
- Consider adding project templates
- Consider adding project archiving feature
