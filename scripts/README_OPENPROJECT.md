# OpenProject Export Utility

Export your Project Wizard work plans (ISSUES.md) to OpenProject via API.

## Setup

1. **Set your OpenProject credentials:**

```bash
export OPENPROJECT_URL="http://10.69.1.86:8080"
export OPENPROJECT_API_KEY="de7933461ff926944d6292e164d083e9104fa3145ff74225797ed0a88babfe5d"
```

2. **Install dependencies:**

```bash
pip install requests
```

## Usage

### Basic Export

```bash
python scripts/export_to_openproject.py path/to/ISSUES.md
```

### With Explicit Credentials

```bash
python scripts/export_to_openproject.py ISSUES.md \
  --url http://10.69.1.86:8080 \
  --api-key YOUR_API_KEY
```

## What Gets Exported

The script parses your ISSUES.md and creates:

1. **Project** - Main project container with name, dates, and description
2. **Phases** - Parent work packages (Phase 1, Phase 2, etc.)
3. **Tasks** - Child work packages under each phase with descriptions and dependencies
4. **Milestones** - Special work packages marking phase completions

## ISSUES.md Format Requirements

Your work plan should follow this structure:

```markdown
## 🧭 Project Structure
- Project Name
- Start Date / Due Date
- Priority

## 📋 Work Packages

### Phase 1: Phase Name
Brief description

| Task | Description | Responsible | Duration | Dependency |
|------|-------------|-------------|----------|------------|
| ... | ... | ... | ... | ... |

## 📈 Milestones

| Milestone | Target Date | Notes |
|-----------|-------------|-------|
| ... | ... | ... |
```

## Example Output

```
Parsing ISSUES.md...
Creating project in OpenProject...
✓ Created project: Patio Drainage & River Rock Project (ID: 42)

Creating work packages...
  ✓ Created phase: Planning & Design
    ✓ Created task: Define problem
    ✓ Created task: Measure grade
  ✓ Created phase: Site Preparation
    ✓ Created task: Mark area & boundaries
    ✓ Created task: Dig trench
  ✓ Created milestone: Excavation Complete

✓ Export complete! View project at: http://10.69.1.86:8080/projects/project-1234
```

## Troubleshooting

### Authentication Errors
- Verify your API key is valid
- Check that you have permissions to create projects in OpenProject

### Parsing Errors
- Ensure your ISSUES.md follows the required format
- Check that emoji section headers are present (🧭 📋 📈)
- Verify markdown tables are properly formatted

### Missing Tasks or Phases
- Check that phase headers use the format: `### Phase N: Name`
- Ensure tables have all required columns: Task, Description, Responsible, Duration, Dependency

## Future Enhancements

- [ ] Parse and assign task durations (currently not implemented)
- [ ] Map assignee names to OpenProject users
- [ ] Handle task dependencies (predecessor/successor relationships)
- [ ] Support budget allocation per work package
- [ ] Add dry-run mode to preview what would be created
