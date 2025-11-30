# Blueprint Schema Specification

**Version:** 1.0.0  
**Last Updated:** 2025-11-28  
**Status:** Draft

---

## Overview

Blueprints are JSON files that define the structure, inputs, validation rules, and quality criteria for document templates in Project Wizard. Each template (e.g., project_charter, work_plan, proposal) has a corresponding blueprint that drives:

- **Form Generation** - What inputs to collect from users
- **Validation** - What constraints to enforce on user data
- **Document Structure** - What sections the document contains
- **AI Integration** - Step-back prompts and verification questions
- **Quality Assessment** - Rubric criteria for evaluating output

Blueprints enable **template-driven document generation** where adding a new document type requires only creating a blueprint JSON file and a Jinja2 template—no code changes needed.

---

## Blueprint File Location

Blueprints are stored in the `patterns/` directory:

```
patterns/
├── project_charter/
│   ├── blueprint.json       # Blueprint specification
│   ├── template.j2          # Jinja2 template for rendering
│   └── prompts.json         # Optional: AI-specific prompts
├── work_plan/
│   ├── blueprint.json
│   └── template.j2
└── proposal/
    ├── blueprint.json
    └── template.j2
```

---

## Top-Level Schema

### Required Fields

```json
{
  "name": "string",
  "version": "string",
  "description": "string",
  "category": "string",
  "inputs": [],
  "sections": []
}
```

### Optional Fields

```json
{
  "step_back_prompts": {},
  "verification_questions": [],
  "rubric": {},
  "metadata": {}
}
```

### Complete Example Structure

```json
{
  "name": "project_charter",
  "version": "1.0.0",
  "description": "Formal project charter following PM methodology",
  "category": "project_management",
  "metadata": {
    "author": "Project Wizard Team",
    "created_date": "2025-11-28",
    "tags": ["project_management", "charter", "initiation"]
  },
  "inputs": [ /* see Inputs Schema */ ],
  "sections": [ /* see Sections Schema */ ],
  "step_back_prompts": { /* see Step-Back Prompts Schema */ },
  "verification_questions": [ /* see Verification Schema */ ],
  "rubric": { /* see Rubric Schema */ }
}
```

---

## Field Definitions

### name
- **Type:** `string`
- **Required:** Yes
- **Description:** Unique identifier for the template (matches directory name)
- **Validation:** Must be lowercase, snake_case, alphanumeric with underscores
- **Example:** `"project_charter"`, `"white_paper"`, `"executive_brief"`

### version
- **Type:** `string`
- **Required:** Yes
- **Description:** Semantic version of the blueprint
- **Format:** `MAJOR.MINOR.PATCH` (e.g., `"1.0.0"`, `"2.1.3"`)
- **Usage:** Allows tracking blueprint changes over time

### description
- **Type:** `string`
- **Required:** Yes
- **Description:** Human-readable description of the template's purpose
- **Example:** `"Formal project charter following PM methodology"`

### category
- **Type:** `string`
- **Required:** Yes
- **Description:** Document category for organization and filtering
- **Valid Values:**
  - `"project_management"` - Charters, plans, schedules
  - `"proposal"` - Business proposals, RFPs, bids
  - `"analysis"` - Reports, analyses, white papers
  - `"communication"` - Memos, briefs, summaries
  - `"technical"` - Engineering docs, specifications
  - `"policy"` - Policies, procedures, guidelines

### metadata (optional)
- **Type:** `object`
- **Description:** Additional information about the template
- **Fields:**
  - `author` (string): Template creator
  - `created_date` (string): ISO date
  - `last_modified` (string): ISO date
  - `tags` (array of strings): Search/filter tags
  - `license` (string): License information

---

## Inputs Schema

The `inputs` array defines what data to collect from users.

### Input Field Structure

```json
{
  "id": "string",
  "label": "string",
  "type": "string",
  "description": "string",
  "required": "boolean",
  "default": "any",
  "placeholder": "string",
  "options": [],
  "validation": {},
  "depends_on": "string",
  "source": "string",
  "readonly": "boolean"
}
```

### Input Field Definitions

#### id
- **Type:** `string`
- **Required:** Yes
- **Description:** Unique identifier for this input (used in templates and validation)
- **Format:** snake_case
- **Example:** `"project_title"`, `"business_need"`, `"success_criteria"`

#### label
- **Type:** `string`
- **Required:** Yes
- **Description:** User-facing label displayed in forms
- **Example:** `"Project Title"`, `"Business Need"`

#### type
- **Type:** `string`
- **Required:** Yes
- **Description:** Input field type
- **Valid Values:**
  - `"text"` - Single-line text input
  - `"textarea"` - Multi-line text input
  - `"select"` - Single selection from options
  - `"multiselect"` - Multiple selections from options
  - `"date"` - Date picker
  - `"number"` - Numeric input
  - `"boolean"` - True/false checkbox
  - `"email"` - Email address input
  - `"url"` - URL input

#### description
- **Type:** `string`
- **Required:** Yes
- **Description:** Help text explaining what to enter
- **Example:** `"A clear, concise name for your project (3-100 characters)"`

#### required
- **Type:** `boolean`
- **Required:** No (default: `false`)
- **Description:** Whether this field must be filled
- **Example:** `true` for project_title, `false` for optional notes

#### default
- **Type:** `any` (must match `type`)
- **Required:** No
- **Description:** Default value if user doesn't provide one
- **Examples:**
  - Text: `"Untitled Project"`
  - Number: `30`
  - Boolean: `true`
  - Date: `"2025-01-01"`

#### placeholder
- **Type:** `string`
- **Required:** No
- **Description:** Placeholder text shown in empty fields
- **Example:** `"Enter a brief description..."`

#### options
- **Type:** `array`
- **Required:** Yes if type is `select` or `multiselect`
- **Description:** List of selectable options
- **Format:** Array of objects with `value` and `label`
- **Example:**
  ```json
  [
    {"value": "software_mvp", "label": "Software MVP"},
    {"value": "clinical_workflow", "label": "Clinical Workflow"},
    {"value": "infrastructure", "label": "Infrastructure Project"}
  ]
  ```

#### validation (optional)
- **Type:** `object`
- **Description:** Validation rules for input
- **Fields:**
  - `min_length` (int): Minimum character length
  - `max_length` (int): Maximum character length
  - `pattern` (string): Regex pattern to match
  - `min` (number): Minimum numeric value
  - `max` (number): Maximum numeric value
  - `custom_validator` (string): Name of custom validation function

**Example:**
```json
{
  "min_length": 3,
  "max_length": 100,
  "pattern": "^[A-Za-z0-9 \\-_]+$"
}
```

#### depends_on (optional)
- **Type:** `string`
- **Description:** ID of another input field this depends on
- **Usage:** For conditional display (only show if dependency is true/filled)
- **Example:** `"has_budget"` (only show budget_amount if has_budget is checked)

#### source (optional)
- **Type:** `string`
- **Description:** Auto-populate from existing project data
- **Format:** Dot notation for nested fields
- **Examples:**
  - `"charter.project_title"` - From existing charter
  - `"project.created_date"` - From project metadata
  - `"user.name"` - From user profile

#### readonly (optional)
- **Type:** `boolean`
- **Description:** If true, field is displayed but cannot be edited
- **Usage:** When showing context from source data
- **Example:** `true` for project_title in work_plan (pulled from charter)

### Complete Input Example

```json
{
  "id": "project_title",
  "label": "Project Title",
  "type": "text",
  "description": "A clear, concise name for your project",
  "required": true,
  "placeholder": "e.g., Clinical Dashboard MVP",
  "validation": {
    "min_length": 3,
    "max_length": 100,
    "pattern": "^[A-Za-z0-9 \\-_&]+$"
  }
}
```

```json
{
  "id": "project_type",
  "label": "Project Type",
  "type": "select",
  "description": "Select the type of project",
  "required": true,
  "options": [
    {"value": "software_mvp", "label": "Software MVP"},
    {"value": "clinical_workflow", "label": "Clinical Workflow"},
    {"value": "infrastructure", "label": "Infrastructure"},
    {"value": "research_analysis", "label": "Research & Analysis"}
  ]
}
```

---

## Sections Schema

The `sections` array defines the structure of the generated document.

### Section Structure

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "required": "boolean",
  "order": "number",
  "subsections": [],
  "prompt_template": "string",
  "context_requirements": [],
  "word_count": {}
}
```

### Section Field Definitions

#### id
- **Type:** `string`
- **Required:** Yes
- **Description:** Unique identifier for this section
- **Format:** snake_case
- **Example:** `"project_overview"`, `"business_case"`, `"scope_definition"`

#### title
- **Type:** `string`
- **Required:** Yes
- **Description:** Section heading in the generated document
- **Example:** `"Project Overview"`, `"Business Case"`

#### description
- **Type:** `string`
- **Required:** Yes
- **Description:** What this section covers (for template authors)
- **Example:** `"High-level summary of project goals and strategic alignment"`

#### required
- **Type:** `boolean`
- **Required:** No (default: `true`)
- **Description:** Whether this section must be included
- **Usage:** Optional sections can be conditionally included

#### order
- **Type:** `number`
- **Required:** Yes
- **Description:** Display order (1, 2, 3, ...)
- **Usage:** Determines section sequence in document

#### subsections (optional)
- **Type:** `array` of subsection objects
- **Description:** Nested sections (max 1 level deep)
- **Structure:** Same as section, but without recursive subsections
- **Example:**
  ```json
  [
    {"id": "business_need", "title": "Business Need", "order": 1},
    {"id": "strategic_alignment", "title": "Strategic Alignment", "order": 2}
  ]
  ```

#### prompt_template (optional)
- **Type:** `string`
- **Description:** Instructions for AI to generate this section
- **Usage:** Used by DraftAgent during agentic generation
- **Example:**
  ```
  "Generate a concise project overview (2-3 paragraphs) that includes: 
   1) the business problem being addressed, 
   2) the proposed solution, and 
   3) expected benefits. 
   Use information from: {business_need}, {proposed_solution}, {measurable_benefits}"
  ```

#### context_requirements (optional)
- **Type:** `array` of strings
- **Description:** What project context is needed for this section
- **Usage:** Tells ContextBuilder what to include
- **Example:** `["charter.business_need", "charter.goals", "project.notes"]`

#### word_count (optional)
- **Type:** `object`
- **Fields:**
  - `min` (int): Minimum words
  - `target` (int): Target word count
  - `max` (int): Maximum words
- **Example:**
  ```json
  {"min": 100, "target": 200, "max": 300}
  ```

### Complete Section Example

```json
{
  "id": "business_case",
  "title": "Business Case",
  "description": "Justification for the project including need, benefits, and ROI",
  "required": true,
  "order": 2,
  "subsections": [
    {
      "id": "business_need",
      "title": "Business Need",
      "description": "Problem or opportunity being addressed",
      "order": 1
    },
    {
      "id": "expected_benefits",
      "title": "Expected Benefits",
      "description": "Quantifiable improvements from project",
      "order": 2
    }
  ],
  "prompt_template": "Synthesize a compelling business case from: {business_need}, {strategic_alignment}, and {measurable_benefits}. Emphasize ROI and strategic value.",
  "context_requirements": ["charter.business_need", "charter.measurable_benefits"],
  "word_count": {"min": 150, "target": 250, "max": 400}
}
```

---

## Step-Back Prompts Schema

Optional object defining prompts for pre-draft clarification.

### Structure

```json
{
  "restate_problem": {},
  "identify_gaps": {},
  "clarifying_questions": {},
  "confirm_scope": {}
}
```

### Prompt Item Structure

```json
{
  "prompt": "string",
  "expected_output": "string"
}
```

### Step-Back Prompt Definitions

#### restate_problem
- **Purpose:** AI restates the user's problem in clear terms
- **When:** Before generating any draft content
- **Example:**
  ```json
  {
    "prompt": "Based on the user's business need and desired outcomes, restate the core problem this project solves in 2-3 sentences. Focus on the root cause, not symptoms.",
    "expected_output": "A concise problem statement that captures the essence of the user's challenge"
  }
  ```

#### identify_gaps
- **Purpose:** AI identifies missing or unclear information
- **When:** After analyzing user inputs
- **Example:**
  ```json
  {
    "prompt": "Review the provided inputs and identify any critical information gaps. What details are missing that would improve document quality?",
    "expected_output": "A list of 3-5 specific information gaps"
  }
  ```

#### clarifying_questions
- **Purpose:** AI generates questions to fill gaps
- **Structure:**
  ```json
  {
    "prompt": "Generate clarifying questions to improve document quality",
    "max_questions": 5,
    "categories": ["scope", "constraints", "stakeholders", "success_criteria"]
  }
  ```

#### confirm_scope
- **Purpose:** AI verifies project boundaries
- **Example:**
  ```json
  {
    "prompt": "Based on the scope and deliverables provided, state what IS and IS NOT included in this project. Use bullet points.",
    "expected_output": "Two lists: In Scope (3-5 items) and Out of Scope (3-5 items)"
  }
  ```

---

## Verification Questions Schema

Array of questions for post-draft validation (Chain of Verification).

### Question Structure

```json
{
  "id": "string",
  "question": "string",
  "category": "string",
  "priority": "string",
  "expected_answer": "string",
  "context_check": [],
  "remediation_hint": "string"
}
```

### Verification Question Definitions

#### id
- **Type:** `string`
- **Required:** Yes
- **Format:** `vq_<category>_<number>` (e.g., `"vq_charter_01"`)

#### question
- **Type:** `string`
- **Required:** Yes
- **Description:** The verification question to ask
- **Example:** `"Does the charter clearly articulate the business need or opportunity?"`

#### category
- **Type:** `string`
- **Required:** Yes
- **Valid Values:**
  - `"factual"` - Check for factual accuracy
  - `"logical"` - Check for logical consistency
  - `"completeness"` - Check all required elements present
  - `"alignment"` - Check alignment with context/charter

#### priority
- **Type:** `string`
- **Required:** Yes
- **Valid Values:**
  - `"critical"` - Must be addressed
  - `"high"` - Should be addressed
  - `"medium"` - Nice to address
  - `"low"` - Optional

#### expected_answer (optional)
- **Type:** `string`
- **Description:** Expected answer for auto-verification
- **Values:** `"yes"`, `"no"`, or null for manual review
- **Example:** `"yes"` (if answer is no, flag for review)

#### context_check
- **Type:** `array` of strings
- **Description:** What to verify against
- **Example:** `["charter.business_need", "charter.strategic_alignment"]`

#### remediation_hint
- **Type:** `string`
- **Required:** Yes
- **Description:** Guidance if verification fails
- **Example:** `"Expand the business case section with specific problems or opportunities."`

### Complete Verification Example

```json
{
  "id": "vq_charter_01",
  "question": "Does the charter clearly articulate the business need or opportunity?",
  "category": "completeness",
  "priority": "critical",
  "expected_answer": "yes",
  "context_check": ["inputs.business_need", "inputs.strategic_alignment"],
  "remediation_hint": "Review the Business Need section and ensure it: 1) describes the current problem/gap, 2) explains why it matters, and 3) ties to strategic goals."
}
```

---

## Rubric Schema

Optional object defining quality assessment criteria.

### Structure

```json
{
  "criteria": [],
  "passing_score": "number",
  "feedback_template": "string"
}
```

### Criterion Structure

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "weight": "number",
  "scoring": {}
}
```

### Rubric Definitions

#### criteria
- **Type:** `array` of criterion objects
- **Description:** Assessment dimensions

**Criterion Fields:**
- `id` (string): Unique identifier (`"clarity"`, `"completeness"`)
- `name` (string): Criterion name (`"Clarity"`)
- `description` (string): What to assess
- `weight` (float 0-1): Importance (must sum to 1.0 across all criteria)
- `scoring` (object): 5-level scoring guide

**Scoring Levels:**
```json
{
  "excellent": {"score": 5, "description": "Clear, concise, professional writing"},
  "good": {"score": 4, "description": "Mostly clear with minor issues"},
  "adequate": {"score": 3, "description": "Understandable but could be clearer"},
  "needs_improvement": {"score": 2, "description": "Unclear or confusing sections"},
  "poor": {"score": 1, "description": "Very difficult to understand"}
}
```

#### passing_score
- **Type:** `number` (float)
- **Description:** Minimum acceptable score (weighted average)
- **Example:** `3.5` (on 1-5 scale)

#### feedback_template
- **Type:** `string`
- **Description:** How to present assessment results
- **Example:** `"Your document scored {score}/5.0 (passing: {passing_score}). Strengths: {strengths}. Areas for improvement: {improvements}."`

### Complete Rubric Example

```json
{
  "criteria": [
    {
      "id": "clarity",
      "name": "Clarity",
      "description": "Clear, concise, and professional writing",
      "weight": 0.25,
      "scoring": {
        "excellent": {"score": 5, "description": "Crystal clear, no ambiguity"},
        "good": {"score": 4, "description": "Mostly clear with minor issues"},
        "adequate": {"score": 3, "description": "Understandable but verbose"},
        "needs_improvement": {"score": 2, "description": "Some confusing sections"},
        "poor": {"score": 1, "description": "Very difficult to understand"}
      }
    },
    {
      "id": "completeness",
      "name": "Completeness",
      "description": "All required sections present with sufficient detail",
      "weight": 0.30,
      "scoring": {
        "excellent": {"score": 5, "description": "All sections complete and detailed"},
        "good": {"score": 4, "description": "Minor gaps in detail"},
        "adequate": {"score": 3, "description": "Some sections lack depth"},
        "needs_improvement": {"score": 2, "description": "Multiple sections incomplete"},
        "poor": {"score": 1, "description": "Major sections missing"}
      }
    },
    {
      "id": "strategic_alignment",
      "name": "Strategic Alignment",
      "description": "Clear connection to organizational goals",
      "weight": 0.25,
      "scoring": { /* ... */ }
    },
    {
      "id": "feasibility",
      "name": "Feasibility",
      "description": "Realistic scope, timeline, and resources",
      "weight": 0.20,
      "scoring": { /* ... */ }
    }
  ],
  "passing_score": 3.5,
  "feedback_template": "Document Quality: {score}/5.0 (passing: {passing_score})\n\nStrengths:\n{strengths}\n\nAreas for Improvement:\n{improvements}\n\nRecommendations:\n{recommendations}"
}
```

---

## Validation Rules

Blueprints are validated when loaded. The following rules apply:

### Top-Level Validation
- ✅ `name` must be lowercase snake_case
- ✅ `version` must match semantic versioning format (X.Y.Z)
- ✅ `category` must be from valid list
- ✅ `inputs` array must not be empty
- ✅ `sections` array must not be empty

### Input Validation
- ✅ Input `id` must be unique within blueprint
- ✅ Input `id` must be snake_case
- ✅ Input `type` must be from valid list
- ✅ If type is `select`/`multiselect`, `options` must be provided
- ✅ `validation.min_length` must be less than `max_length`
- ✅ `validation.pattern` must be valid regex
- ✅ `depends_on` must reference existing input `id`
- ✅ `default` value must match `type`

### Section Validation
- ✅ Section `id` must be unique within blueprint
- ✅ Section `order` must be positive integer
- ✅ Section `order` values must be unique
- ✅ Subsections can only be 1 level deep (no recursive nesting)
- ✅ `word_count.min` ≤ `target` ≤ `max`

### Rubric Validation
- ✅ Criterion `weight` values must sum to 1.0
- ✅ Each criterion must have all 5 scoring levels
- ✅ Scoring level scores must be 1, 2, 3, 4, 5

---

## Best Practices

### Naming Conventions
- **Blueprint names:** lowercase, snake_case (e.g., `project_charter`, `white_paper`)
- **Input IDs:** snake_case (e.g., `project_title`, `success_criteria`)
- **Section IDs:** snake_case (e.g., `business_case`, `scope_definition`)

### Input Design
- **Keep it simple:** Only collect what's necessary
- **Provide help text:** Every input should have clear `description`
- **Use validation wisely:** Enforce structure but don't over-constrain
- **Consider auto-population:** Use `source` when data exists elsewhere
- **Group related inputs:** Use logical ordering

### Section Design
- **Clear hierarchy:** Use subsections for complex sections
- **Logical flow:** Order sections to tell a story
- **Appropriate granularity:** Not too broad, not too detailed
- **Include context hints:** Use `context_requirements` for AI

### Verification Questions
- **Cover all critical aspects:** Completeness, accuracy, alignment
- **Be specific:** Vague questions get vague answers
- **Provide remediation:** Always include helpful hints
- **Prioritize wisely:** Critical issues must be addressed

### Rubric Criteria
- **Choose meaningful dimensions:** What truly matters for this document type?
- **Use standard criteria:** Clarity, completeness, alignment are universal
- **Add template-specific criteria:** E.g., "persuasiveness" for proposals
- **Balance weights:** No single criterion should dominate

---

## Common Patterns

### Pattern 1: Auto-Populate from Charter

When creating a work_plan that uses charter data:

```json
{
  "id": "project_title",
  "label": "Project Title",
  "type": "text",
  "required": true,
  "source": "charter.project_title",
  "readonly": true
}
```

### Pattern 2: Conditional Inputs

Show budget field only if project has budget:

```json
[
  {
    "id": "has_budget",
    "label": "Does this project have a budget?",
    "type": "boolean",
    "required": true
  },
  {
    "id": "budget_amount",
    "label": "Budget Amount",
    "type": "number",
    "depends_on": "has_budget",
    "validation": {"min": 0}
  }
]
```

### Pattern 3: Multi-Level Sections

Complex sections with subsections:

```json
{
  "id": "business_case",
  "title": "Business Case",
  "order": 2,
  "subsections": [
    {"id": "problem", "title": "Problem Statement", "order": 1},
    {"id": "solution", "title": "Proposed Solution", "order": 2},
    {"id": "benefits", "title": "Expected Benefits", "order": 3}
  ]
}
```

---

## Troubleshooting

### Issue: Blueprint won't load
- **Check:** JSON syntax (trailing commas, quotes)
- **Check:** Required fields present (name, version, inputs, sections)
- **Check:** Version format (must be X.Y.Z)
- **Validate:** Run `project-wizard templates validate <name>`

### Issue: Input validation failing
- **Check:** Field types match (string, number, boolean)
- **Check:** min_length < max_length
- **Check:** Pattern is valid regex
- **Check:** Options provided for select fields
- **Check:** depends_on references existing input

### Issue: Section order conflicts
- **Check:** All section `order` values are unique
- **Check:** Order values are positive integers
- **Check:** Subsection orders unique within parent

### Issue: Rubric weights don't sum to 1.0
- **Check:** Add up all criterion weights
- **Fix:** Adjust weights so sum equals 1.0 exactly
- **Tip:** Use 0.25, 0.30, 0.25, 0.20 for 4 criteria

---

## Schema Versioning

Blueprint schemas follow semantic versioning:

- **Major version (X.0.0):** Breaking changes to structure
- **Minor version (0.X.0):** New optional fields added
- **Patch version (0.0.X):** Clarifications, examples, fixes

**Current version:** 1.0.0

**Compatibility:** Blueprints specify their own version. Future versions of Project Wizard will support older blueprint versions via migration/compatibility layer.

---

## Examples

See `patterns/examples/` for complete blueprint examples:
- `sample_blueprint.json` - Fully annotated example
- `minimal_blueprint.json` - Minimal required fields only

See `patterns/project_charter/blueprint.json` for production example.

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-28  
**Status:** Complete - Ready for implementation  
**Next:** Create Pydantic models based on this schema
