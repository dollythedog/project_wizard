# OpenProject Integration

Project Wizard can automatically export your WORK_PLAN.md files to OpenProject, creating a structured project with work packages for each task.

## Setup

### 1. Get Your OpenProject API Key

1. Log into your OpenProject instance at `http://10.69.1.86:8080`
2. Go to **My Account** (top-right menu)
3. Click **Access tokens** in the left sidebar
4. Click **+ API token**
5. Give it a name (e.g., "Project Wizard Integration")
6. Copy the generated API key

### 2. Configure Environment Variables

Add your OpenProject credentials to the `.env` file:

```bash
# OpenProject Integration
OPENPROJECT_URL=http://10.69.1.86:8080
OPENPROJECT_API_KEY=your-api-key-here
```

## Usage

### From the Streamlit UI

1. Open project_wizard: `streamlit run app.py`
2. Navigate to a project with a WORK_PLAN.md
3. Go to the **Deliverables** tab
4. Select **Work Plan (ISSUES)** from the dropdown
5. Click the **📤 Upload to OpenProject** button

The exporter will:
- Create or find the project in OpenProject
- Create a parent work package for each phase
- Create child work packages for each task
- Include all task metadata (responsible party, duration, dependencies)
- Set estimated effort based on duration

### From Command Line (Alternative)

You can also use the exporter directly:

```bash
python3 -m app.services.openproject_exporter \
  /path/to/project/WORK_PLAN.md \
  --url http://10.69.1.86:8080 \
  --api-key your-api-key
```

Or using environment variables:

```bash
export OPENPROJECT_API_KEY="your-api-key"
python3 -m app.services.openproject_exporter /path/to/project/WORK_PLAN.md
```

## Work Plan Structure

The exporter expects WORK_PLAN.md to follow this structure:

```markdown
## 🧭 Project Structure
- **Project Name**: Your Project Name
- **Project Type**: Project Type
- **Start Date**: YYYY-MM-DD
- **End Date**: YYYY-MM-DD

## 📋 Work Packages (Phases, Tasks & Subtasks)

### Phase 1: Phase Name
**Objective**: Phase description

| Task | Description | Responsible | Duration | Dependency |
|------|-------------|-------------|----------|------------|
| 1.1 | Task description | Team | 5 days | None |
| 1.2 | Task description | Team | 3 days | 1.1 |
```

## Features

- ✅ Creates hierarchical work packages (phases → tasks)
- ✅ Parses task IDs, descriptions, and responsibilities
- ✅ Converts duration to estimated effort hours
- ✅ Preserves dependency information
- ✅ Creates or reuses existing projects
- ✅ Provides direct link to view results in OpenProject

## Troubleshooting

### "OPENPROJECT_API_KEY not set"
Make sure you've added the API key to your `.env` file and restarted the Streamlit app.

### "Failed to create project"
Check that your API key has permissions to create projects in OpenProject.

### "No tasks found in work plan"
Verify your WORK_PLAN.md follows the expected format with proper markdown tables.

### API Authentication Errors
OpenProject uses HTTP Basic Auth with the API key. Make sure there are no extra spaces or characters in your API key.
