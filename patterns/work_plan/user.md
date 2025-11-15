## Project Work Plan Development

You are creating a detailed work plan for project execution following formal project management methodology. This plan will break down the work into phases, work packages, and actionable tasks with clear dependencies and timelines.

---

## User Inputs

**Project Work Description:**
{{ project_description }}

{% if key_deliverables %}
**Key Deliverables:**
{{ key_deliverables }}
{% endif %}

{% if team_resources %}
**Team & Resources:**
{{ team_resources }}
{% endif %}

{% if constraints %}
**Constraints & Dependencies:**
{{ constraints }}
{% endif %}

---

## Project Context

The following information provides context about the current project to ensure the work plan aligns with strategic goals and project scope:

### Project Charter
{{ project_charter }}

### Project README
{{ project_readme }}

### Current Issues/Tasks
{{ project_issues }}

### Recent Changes
{{ project_changelog }}

---

## Instructions

Based on the user's work description and project context above:

1. Analyze the work and break it into logical **phases**
2. For each phase, identify **work packages** and **tasks**
3. Establish **dependencies** between tasks (what must be done first)
4. Provide **realistic time estimates** for each task
5. Define **milestones** for major achievements
6. If budget/cost information is provided, create a **resource estimate**
7. Format the output as a structured work plan ready for OpenProject

Ensure the work plan:
- Covers all aspects of the user's description
- Aligns with the project charter objectives
- Has realistic, achievable timelines
- Shows clear task dependencies
- Includes measurable milestones
- Is formatted for easy import to OpenProject
