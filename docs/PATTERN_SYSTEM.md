# Project Wizard Pattern System - Complete Explanation

## Overview

Yes, you are **absolutely correct**! The Project Wizard uses a **modular, pattern-based AI system** inspired by the Fabric framework. This allows you to add new document types (deliverables) without modifying core code - just by adding new pattern folders.

## How the Pattern System Works

### 1. **Pattern Registry** (`PatternRegistry`)
- Automatically discovers and loads all patterns from the `patterns/` directory
- Each subdirectory (e.g., `patterns/5w1h_analysis/`) represents one pattern
- Validates pattern structure and loads all required files
- Provides a registry of available patterns for the UI

### 2. **Pattern Pipeline** (`PatternPipeline`)  
- Orchestrates the AI document generation process
- Takes user inputs + pattern definition → generates structured document
- Handles the complete flow:
  1. Load pattern from registry
  2. Build context from project files
  3. Generate user prompt from `user.md` template
  4. Call LLM with `system.md` prompt + user prompt
  5. Wrap AI output in `template.md.j2` template
  6. Return formatted document

### 3. **Pattern Structure** (5 Required Files)

Each pattern folder must contain:

#### **`variables.json`** - Input Collection Schema
Defines what information to collect from the user before generation.

```json
{
  "variable_name": {
    "type": "textarea",           // or "text_input"
    "label": "Display Label *",   // Shown to user
    "help": "Helper text",        // Tooltip/guidance
    "placeholder": "Example...",  // Input placeholder
    "required": true,             // Validation flag
    "height": 120                 // For textarea only
  }
}
```

**Purpose:** Drives the dynamic form generation in the UI. The wizard automatically creates input fields based on this schema.

---

#### **`system.md`** - AI System Prompt
The **identity, instructions, and constraints** for the AI agent.

**Structure:**
```markdown
# IDENTITY and PURPOSE
[Who the AI is and what it does]

# CONTEXT  
[What information it will receive]

# STEPS
[How to process the inputs]

# QUALITY CRITERIA
[What makes a good output]

# CONSTRAINTS
[What NOT to do - anti-hallucination rules]

# OUTPUT INSTRUCTIONS
[Exact format to generate]
```

**Purpose:** This is the "agent configuration" - it defines the AI's role, methodology, and output format. This is where you encode expertise (e.g., LEAN Six Sigma methodology for 5W1H).

---

#### **`user.md`** - User Prompt Template
A Jinja2 template that assembles the **user's input + project context** into the actual prompt sent to the AI.

**Variables available:**
- User inputs (from `variables.json`): `{{what}}`, `{{when}}`, etc.
- Project context (auto-injected by `ProjectContext`):
  - `{{project_charter}}`
  - `{{project_readme}}`
  - `{{project_issues}}`
  - `{{project_changelog}}`

**Purpose:** Combines user-provided data with project context to create a complete, contextually-aware prompt for the AI.

---

#### **`template.md.j2`** - Document Wrapper Template
A Jinja2 template for the **final document structure** (header, footer, metadata).

**Variables available:**
- `{{content}}` - The AI-generated content
- `{{project_name}}`, `{{created_date}}`, `{{author}}`, etc.
- Any custom metadata you define

**Purpose:** Wraps the AI output in a professional document format with metadata, version control, and navigation links.

---

#### **`rubric.json`** - Quality Critique Schema
Defines the **evaluation criteria** for the CriticAgent to assess document quality.

```json
{
  "criteria": [
    {
      "name": "Criterion Name",
      "weight": 0.20,
      "description": "What to evaluate"
    }
  ],
  "threshold": 0.75
}
```

**Purpose:** Enables automated quality assessment. The CriticAgent uses this to provide structured feedback (like we built for the Charter critique).

---

## How to Add a New Deliverable

### Example: Adding a "Project Plan" Pattern

1. **Create the pattern directory:**
   ```bash
   mkdir -p patterns/project_plan
   ```

2. **Define `variables.json`** - What inputs do you need?
   ```json
   {
     "project_goals": {
       "type": "textarea",
       "label": "Project Goals *",
       "help": "What are the primary objectives?",
       "required": true,
       "height": 150
     },
     "scope": {
       "type": "textarea",
       "label": "Scope & Deliverables *",
       "help": "What's included/excluded?",
       "required": true,
       "height": 150
     },
     "timeline": {
       "type": "textarea",
       "label": "Timeline & Milestones",
       "help": "Key dates and phases",
       "required": false,
       "height": 120
     }
   }
   ```

3. **Write `system.md`** - Configure the AI agent
   ```markdown
   # IDENTITY and PURPOSE
   You are a project management expert specializing in creating comprehensive project plans following PMI standards.
   
   # STEPS
   1. Review project goals and scope
   2. Identify key deliverables and phases
   3. Structure a logical project plan
   4. Include risk management and success criteria
   
   # CONSTRAINTS
   - Never fabricate timelines if not provided
   - Keep scope realistic
   - Flag any gaps in information
   
   # OUTPUT INSTRUCTIONS
   Generate an ISSUES.md file in markdown format with:
   - Project Overview section
   - Phases and Milestones
   - Task breakdown (Phase/Work Package format)
   - Dependencies and Risks
   ```

4. **Create `user.md`** - Assemble the prompt
   ```markdown
   ## Project Planning Inputs
   
   **Project Goals:**
   {{project_goals}}
   
   **Scope:**
   {{scope}}
   
   **Timeline:**
   {{timeline}}
   
   ## Project Context
   {{project_charter}}
   {{project_readme}}
   ```

5. **Design `template.md.j2`** - Wrap the output
   ```markdown
   # Project Plan - ISSUES.md
   
   **Created:** {{created_date}}
   **Status:** {{status | default('Active')}}
   
   ---
   
   {{content}}
   
   ---
   
   *Generated by Project Wizard*
   ```

6. **Define `rubric.json`** - Quality criteria
   ```json
   {
     "criteria": [
       {"name": "Clear Objectives", "weight": 0.25},
       {"name": "Logical Task Structure", "weight": 0.25},
       {"name": "Risk Management", "weight": 0.20},
       {"name": "Success Metrics", "weight": 0.15},
       {"name": "Timeline Realism", "weight": 0.15}
     ],
     "threshold": 0.75
   }
   ```

7. **Add to the UI options** in `app_v2_5.py` tab4:
   ```python
   deliverable_options = {
       "📊 Project Plan": "project_plan",  # Add this line
       "❓ 5W1H Analysis": "5w1h_analysis",
       # ... rest
   }
   ```

**That's it!** The system will automatically:
- Discover the new pattern
- Generate the wizard form from `variables.json`
- Use your AI prompts to generate the document
- Apply your quality rubric for critique
- Save to `PROJECT_PLAN.md` (or whatever filename you configure)

---

## Key Advantages

1. **No Code Changes Needed** - Just add files to `patterns/` directory
2. **AI Agent Configuration as Code** - System prompts are versioned and reusable
3. **Context-Aware** - Automatically injects project context (charter, README, etc.)
4. **Quality Built-In** - Each pattern includes its own quality rubric
5. **Consistent UX** - The UI automatically adapts to any pattern
6. **Portable** - Patterns can be shared between projects

## Current Implementation Status

✅ **Working:**
- PatternRegistry discovers patterns
- PatternPipeline executes generation
- Tab 4 (Deliverables) uses the system
- 5W1H Analysis pattern is fully configured

⚠️ **Needs Implementation:**
- Other patterns (Project Plan, SIPOC, Fishbone, VOC) - just need the 5 files created
- CriticAgent integration for deliverables (currently only used for Charter)

---

## Next Steps for You

To add a Planning Agent (for ISSUES.md generation):

1. Create `patterns/project_plan/` with the 5 files
2. Focus on the `system.md` - this is where you encode project planning expertise
3. In `user.md`, leverage the project context variables heavily
4. Test by selecting "📊 Project Plan" in Tab 4

The system will handle the rest automatically!

---

## Auto-Discovery in UI

As of v2.5.2, Tab 4 (Deliverables) **automatically discovers** new patterns from the registry!

### How It Works

1. **PatternRegistry scans** `patterns/` directory on startup
2. **Tab 4 builds the radio selector** dynamically from discovered patterns
3. **Custom display names** are defined in `pattern_display_names` dict
4. **Fallback formatting**: If no custom name exists, auto-formats pattern key (e.g., `my_new_pattern` → "📄 My New Pattern")

### Adding a New Pattern - Complete Workflow

1. **Create pattern folder:** `patterns/my_pattern/`
2. **Add 5 required files:** variables.json, system.md, user.md, template.md.j2, rubric.json
3. **(Optional) Add custom emoji/name** in `app_v2_5.py`:
   ```python
   pattern_display_names = {
       # ...existing patterns...
       "my_pattern": "🎯 My Custom Name"
   }
   ```
4. **Restart the app** - Pattern appears automatically in Tab 4!

If you skip step 3, it still works - just shows as "📄 My Pattern" with auto-formatting.

### Benefits

✅ No code changes required (unless you want custom emoji/name)  
✅ Patterns appear immediately when added to `patterns/` folder  
✅ Clean separation: pattern config vs UI display  
✅ Easy to share patterns between projects
