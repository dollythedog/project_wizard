# Template Patterns Directory

This directory contains blueprint-driven document templates for Project Wizard.

## Structure

Each template lives in its own directory:

```
patterns/
├── _templates/              # Shared Jinja2 includes
├── examples/                # Example blueprints
├── project_charter/
│   ├── blueprint.json       # Blueprint specification
│   ├── template.j2          # Jinja2 document template
│   └── README.md           # Template documentation
├── work_plan/
│   ├── blueprint.json
│   ├── template.j2
│   └── README.md
└── proposal/
    ├── blueprint.json
    ├── template.j2
    └── README.md
```

## File Naming Conventions

- **blueprint.json** - Blueprint specification (required)
- **template.j2** - Jinja2 template for rendering document (required)
- **README.md** - Template documentation (optional)
- **prompts.json** - Additional AI prompts (optional, future use)

## Creating a New Template

1. Create directory: `patterns/my_template/`
2. Create `blueprint.json` following schema in `docs/BLUEPRINT_SCHEMA.md`
3. Create `template.j2` with Jinja2 template for document
4. Test with: `project-wizard templates validate my_template`

## Blueprint Schema

See `docs/BLUEPRINT_SCHEMA.md` for complete specification.

Required fields:
- `name` - Template identifier (snake_case)
- `version` - Semantic version (X.Y.Z)
- `description` - Template purpose
- `category` - Document category
- `inputs` - User input fields
- `sections` - Document sections

Optional fields:
- `step_back_prompts` - Pre-draft clarification
- `verification_questions` - Post-draft validation
- `rubric` - Quality assessment criteria
- `metadata` - Author, tags, etc.

## Examples

See `patterns/examples/sample_blueprint.json` for a complete example with all fields.

## Validation

Validate a blueprint:
```bash
project-wizard templates validate <template_name>
```

Validate all blueprints:
```bash
project-wizard templates validate --all
```

## Loading

Blueprints are automatically loaded by BlueprintRegistry on startup.
Invalid blueprints are logged but don't prevent the app from starting.
