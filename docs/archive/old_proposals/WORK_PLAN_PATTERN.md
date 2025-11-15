# Work Plan Pattern - Implementation Summary

## Overview

Created a new pattern for the Project Wizard that generates detailed Project Work Plans (ISSUES.md) following formal project management methodology. The pattern integrates with OpenProject for automated export.

## Files Created

### Pattern Files (`patterns/work_plan/`)

1. **variables.json** - User input form definition
   - `project_description` - Free-text work description (required)
   - `key_deliverables` - Main outputs (optional)
   - `team_resources` - Available people/equipment (optional)
   - `constraints` - Limitations and dependencies (optional)

2. **system.md** - AI agent instructions
   - Identity: Project Management expert
   - Task: Create detailed Work Breakdown Structure (WBS)
   - Output: Phases → Work Packages → Tasks with dependencies, timelines, milestones

3. **user.md** - Jinja2 prompt template
   - Injects user variables
   - Auto-includes project context (charter, README, issues, changelog)
   - Provides instructions for comprehensive work plan generation

4. **template.md.j2** - Document wrapper
   - Formats as ISSUES.md
   - Includes document control metadata
   - Links to related project docs
   - Instructions for OpenProject export

5. **rubric.json** - Quality criteria for CriticAgent
   - Work Breakdown Completeness (25%)
   - Dependency & Sequencing (20%)
   - Realistic Estimates (20%)
   - Clear Milestones (15%)
   - Strategic Alignment (10%)
   - OpenProject Readiness (10%)
   - Threshold: 75%

### Export Utility (`scripts/`)

1. **export_to_openproject.py** - Python script for API integration
   - Parses ISSUES.md structure
   - Extracts project metadata, phases, tasks, milestones
   - Creates project in OpenProject via REST API
   - Creates hierarchical work packages (phases as parents, tasks as children)
   - Creates milestone work packages
   - Handles authentication, error reporting

2. **README_OPENPROJECT.md** - Documentation
   - Setup instructions
   - Usage examples
   - Format requirements
   - Troubleshooting guide

## How It Works

### 1. User Workflow

```
User clicks "Deliverables" tab 
  → Selects "Work Plan" 
  → Fills form with project description 
  → AI generates detailed ISSUES.md with phases, tasks, milestones 
  → CriticAgent evaluates against rubric 
  → User refines if needed 
  → Saves to project root as ISSUES.md 
  → (Optional) Exports to OpenProject
```

### 2. Pattern System Integration

The pattern automatically injects:
- `{{project_charter}}` - Project objectives and scope
- `{{project_readme}}` - Project overview
- `{{project_issues}}` - Current tasks
- `{{project_changelog}}` - Recent changes

This ensures the work plan aligns with existing project context.

### 3. Generated Work Plan Structure

```markdown
## 🧭 Project Structure
- Project Name, Type, Status
- Start/End Dates
- Priority

## 📋 Work Packages (Phases, Tasks & Subtasks)

### Phase 1: Phase Name
Description of phase objectives

| Task | Description | Responsible | Duration | Dependency |
|------|-------------|-------------|----------|------------|
| ... | ... | ... | ... | ... |

### Phase 2: Phase Name
...

## 📈 Milestones

| Milestone | Target Date | Notes |
|-----------|-------------|-------|
| ... | ... | ... |

## 💰 Resources & Budget (if applicable)

| Item | Unit | Qty | Unit Cost | Total |
|------|------|-----|-----------|-------|
| ... | ... | ... | ... | ... |

## 📝 Assumptions & Notes
- Assumptions made
- Areas needing clarification
- Critical path highlights
```

### 4. OpenProject Export

```bash
# Set credentials
export OPENPROJECT_URL="http://10.69.1.86:8080"
export OPENPROJECT_API_KEY="your_key_here"

# Export
python scripts/export_to_openproject.py ISSUES.md
```

Creates:
- Project with metadata
- Parent work packages for each phase
- Child work packages for each task
- Milestone work packages

## Example Usage

### Input:
```
Project Description: "I will be digging out 12" from my concrete patio 
and filling with drainage rock and river rock to solve standing water 
issues. Timeline is 2 weeks, budget around $500."

Team: "Just me on weekends"
Constraints: "Must complete before winter, weather dependent"
```

### Output:
Detailed work plan with 5-6 phases:
1. Planning & Design (measurements, materials, budget)
2. Site Preparation (excavation, soil compaction)
3. Drainage Layer Installation (fabric, drainage rock)
4. Finish Layer Installation (edging, river rock)
5. Quality Check & Maintenance (rain test, adjustments)

Each phase includes:
- Specific tasks with descriptions
- Duration estimates
- Dependencies (what must happen first)
- Responsible party
- Milestones for phase completion
- Budget breakdown (if provided)

## Testing

To test the pattern:

1. **Generate Work Plan**
   - Run Project Wizard app
   - Navigate to Deliverables tab
   - Select "Work Plan" pattern
   - Enter the patio project description
   - Review generated ISSUES.md

2. **Run Critique**
   - Use CriticAgent to evaluate against rubric
   - Refine based on feedback
   - Save final version

3. **Export to OpenProject** (when ready)
   ```bash
   python scripts/export_to_openproject.py ISSUES.md \
     --url http://10.69.1.86:8080 \
     --api-key de7933461ff926944d6292e164d083e9104fa3145ff74225797ed0a88babfe5d
   ```

## Future Enhancements

1. **Export Improvements**
   - Parse and assign task durations (ISO 8601 format)
   - Map assignee names to OpenProject user IDs
   - Create dependency links between work packages
   - Support budget allocation per work package
   - Add dry-run mode to preview without creating

2. **Pattern Enhancements**
   - Support for Gantt chart generation
   - Risk register integration
   - Resource allocation optimization
   - Template library for common project types

3. **UI Integration**
   - Add "Export to OpenProject" button in Deliverables tab
   - Show preview before export
   - Track export status and provide OpenProject link

## Notes

- Pattern follows the Planning Phase methodology from project management guide
- AI generates realistic estimates based on work description
- Format is optimized for both human reading and OpenProject import
- ISSUES.md serves as both documentation and sync point with GitHub Issues
