# Blueprint System Implementation Guide

**Version:** 1.0.0  
**Created:** 2025-11-28  
**Phase:** 1 - Blueprint System Foundation  
**Status:** Implementation in Progress

---

## Overview

This document provides atomic-level, step-by-step instructions for implementing the Blueprint System (Phase 1 of v3.0 AI Project OS). Each task is broken down to its most granular level so implementation can be paused and resumed at any point.

---

## Phase 1 Implementation Plan

### Total Duration: 1-2 weeks (40-60 hours)
### Current Status: Task 1.1.1 - In Progress

---

## Sprint 1.1: Blueprint Schema Design (2-3 days / 12-16 hours)

### Task 1.1.1: Design blueprint.json Schema Specification ✨ **STARTING HERE**
**Duration:** 4-6 hours  
**Priority:** Critical  
**Dependencies:** None

#### Atomic Steps:

**Step 1: Define Core Blueprint Structure** (30 min)
- [ ] Create `docs/BLUEPRINT_SCHEMA.md` file
- [ ] Document high-level blueprint purpose
- [ ] Define required top-level fields:
  - `name` (string): template identifier
  - `version` (string): semantic version
  - `description` (string): template purpose
  - `category` (string): document category
  - `inputs` (array): user input fields
  - `sections` (array): document sections
  - `step_back_prompts` (object): pre-draft prompts
  - `verification_questions` (array): post-draft validation
  - `rubric` (object): quality criteria

**Step 2: Design Input Field Schema** (45 min)
- [ ] Define `TemplateInput` structure:
  ```json
  {
    "id": "string (unique within template)",
    "label": "string (user-facing label)",
    "type": "string (text|textarea|select|multiselect|date|number|boolean)",
    "description": "string (help text)",
    "required": "boolean",
    "default": "any (optional)",
    "options": "array (for select/multiselect)",
    "validation": {
      "min_length": "int (optional)",
      "max_length": "int (optional)",
      "pattern": "string (regex, optional)",
      "custom_validator": "string (function name, optional)"
    },
    "depends_on": "string (field_id, optional - conditional display)",
    "source": "string (charter_field, optional - auto-populate from charter)"
  }
  ```
- [ ] Document each field with examples
- [ ] Add validation rules

**Step 3: Design Section Schema** (45 min)
- [ ] Define `TemplateSection` structure:
  ```json
  {
    "id": "string (unique within template)",
    "title": "string (section heading)",
    "description": "string (what this section covers)",
    "required": "boolean",
    "order": "int (display order)",
    "subsections": "array of subsection objects (optional)",
    "prompt_template": "string (AI generation instructions)",
    "context_requirements": "array of strings (what context needed)",
    "word_count": {
      "min": "int (optional)",
      "target": "int (optional)",
      "max": "int (optional)"
    }
  }
  ```
- [ ] Document nesting rules for subsections
- [ ] Add examples for different section types

**Step 4: Design Step-Back Prompts Schema** (30 min)
- [ ] Define `StepBackPrompts` structure:
  ```json
  {
    "restate_problem": {
      "prompt": "string (AI instruction to restate)",
      "expected_output": "string (format description)"
    },
    "identify_gaps": {
      "prompt": "string (AI instruction to find missing info)",
      "expected_output": "string"
    },
    "clarifying_questions": {
      "prompt": "string (generate questions for user)",
      "max_questions": "int (default 5)",
      "categories": "array of strings (question types)"
    },
    "confirm_scope": {
      "prompt": "string (verify boundaries)",
      "expected_output": "string"
    }
  }
  ```
- [ ] Document how these feed into DraftAgent
- [ ] Add examples

**Step 5: Design Verification Questions Schema** (30 min)
- [ ] Define `VerificationQuestion` structure:
  ```json
  {
    "id": "string (unique)",
    "question": "string (the question text)",
    "category": "string (factual|logical|alignment|completeness)",
    "priority": "string (critical|high|medium|low)",
    "expected_answer": "string (optional - for auto-check)",
    "context_check": "array of strings (what to verify against)",
    "remediation_hint": "string (if answer is 'no', what to do)"
  }
  ```
- [ ] Document question categories
- [ ] Add examples for each priority level

**Step 6: Design Rubric Schema** (30 min)
- [ ] Define `Rubric` structure:
  ```json
  {
    "criteria": [
      {
        "id": "string",
        "name": "string (criterion name)",
        "description": "string (what to assess)",
        "weight": "float (0-1, sum to 1.0)",
        "scoring": {
          "excellent": {"score": 5, "description": "string"},
          "good": {"score": 4, "description": "string"},
          "adequate": {"score": 3, "description": "string"},
          "needs_improvement": {"score": 2, "description": "string"},
          "poor": {"score": 1, "description": "string"}
        }
      }
    ],
    "passing_score": "float (minimum acceptable score)",
    "feedback_template": "string (how to present scores)"
  }
  ```
- [ ] Document standard rubric criteria (clarity, completeness, evidence, alignment)
- [ ] Add template-specific example

**Step 7: Create Complete Example Blueprint** (1 hour)
- [ ] Create `patterns/examples/sample_blueprint.json`
- [ ] Fill in every field with realistic data
- [ ] Add inline comments (in separate .md file) explaining each section
- [ ] Validate JSON syntax

**Step 8: Document Blueprint Best Practices** (30 min)
- [ ] Add "Creating Blueprints" section to `BLUEPRINT_SCHEMA.md`
- [ ] Document naming conventions
- [ ] Document file organization in `patterns/` directory
- [ ] Add troubleshooting section

**Deliverables for Task 1.1.1:**
- [ ] `docs/BLUEPRINT_SCHEMA.md` (complete specification)
- [ ] `patterns/examples/sample_blueprint.json` (working example)
- [ ] Schema versioning strategy documented

---

### Task 1.1.2: Create Blueprint Pydantic Models
**Duration:** 3-4 hours  
**Priority:** Critical  
**Dependencies:** Task 1.1.1 complete

#### Atomic Steps:

**Step 1: Create Blueprint Models File** (15 min)
- [ ] Create `app/models/blueprint.py`
- [ ] Add file docstring
- [ ] Import required modules:
  ```python
  from pydantic import BaseModel, Field, validator
  from typing import Optional, List, Dict, Any, Literal
  from enum import Enum
  ```

**Step 2: Create Enums for Fixed Values** (20 min)
- [ ] Create `InputType` enum:
  ```python
  class InputType(str, Enum):
      TEXT = "text"
      TEXTAREA = "textarea"
      SELECT = "select"
      MULTISELECT = "multiselect"
      DATE = "date"
      NUMBER = "number"
      BOOLEAN = "boolean"
  ```
- [ ] Create `QuestionCategory` enum
- [ ] Create `Priority` enum
- [ ] Create `DocumentCategory` enum

**Step 3: Create Validation Model** (30 min)
- [ ] Create `InputValidation` model:
  ```python
  class InputValidation(BaseModel):
      min_length: Optional[int] = None
      max_length: Optional[int] = None
      pattern: Optional[str] = None
      custom_validator: Optional[str] = None
      
      class Config:
          extra = "forbid"  # No extra fields allowed
  ```
- [ ] Add validators for min_length < max_length
- [ ] Add validator for regex pattern syntax

**Step 4: Create TemplateInput Model** (45 min)
- [ ] Create `TemplateInput` model with all fields from schema
- [ ] Add field validators:
  - id must be snake_case
  - label must not be empty
  - options required if type is select/multiselect
  - default value must match type
- [ ] Add custom validator for depends_on (must reference existing field)
- [ ] Add docstrings for each field

**Step 5: Create TemplateSection Model** (45 min)
- [ ] Create `Subsection` model (simplified version of Section)
- [ ] Create `WordCount` model
- [ ] Create `TemplateSection` model with all fields
- [ ] Add validators:
  - order must be positive
  - subsections can only be 1 level deep (no recursive nesting)
- [ ] Add docstrings

**Step 6: Create Step-Back Prompts Models** (30 min)
- [ ] Create `StepBackPromptItem` model
- [ ] Create `StepBackPrompts` model
- [ ] Add default values for common prompts
- [ ] Add docstrings

**Step 7: Create Verification Models** (30 min)
- [ ] Create `VerificationQuestion` model
- [ ] Add validators for categories and priorities
- [ ] Add docstrings

**Step 8: Create Rubric Models** (30 min)
- [ ] Create `ScoringLevel` model
- [ ] Create `RubricCriterion` model
- [ ] Create `Rubric` model
- [ ] Add validator: criterion weights must sum to 1.0
- [ ] Add docstrings

**Step 9: Create Main BlueprintSpec Model** (30 min)
- [ ] Create `BlueprintSpec` model combining all above
- [ ] Add top-level validators:
  - version must be semantic (e.g., "1.0.0")
  - input ids must be unique
  - section ids must be unique
  - section orders must be unique
- [ ] Add `model_config` for JSON schema generation
- [ ] Add comprehensive docstring with example

**Step 10: Add Helper Methods** (20 min)
- [ ] Add `BlueprintSpec.get_input_by_id()` method
- [ ] Add `BlueprintSpec.get_section_by_id()` method
- [ ] Add `BlueprintSpec.validate_input_data()` method for runtime validation
- [ ] Add `BlueprintSpec.to_json_schema()` for form generation

**Deliverables for Task 1.1.2:**
- [ ] `app/models/blueprint.py` (complete with all models)
- [ ] Type hints for all fields
- [ ] Comprehensive validation logic
- [ ] Helper methods for common operations

---

### Task 1.1.3: Write Blueprint Validation Tests
**Duration:** 2-3 hours  
**Priority:** High  
**Dependencies:** Task 1.1.2 complete

#### Atomic Steps:

**Step 1: Create Test File** (10 min)
- [ ] Create `tests/test_blueprint_models.py`
- [ ] Import pytest, BlueprintSpec, and example data
- [ ] Create fixtures for valid/invalid blueprints

**Step 2: Test Valid Blueprint Loading** (30 min)
- [ ] Test loading minimal valid blueprint
- [ ] Test loading complete blueprint with all optional fields
- [ ] Test all input types load correctly
- [ ] Test nested subsections load correctly
- [ ] Assert no validation errors

**Step 3: Test Invalid Blueprints** (45 min)
- [ ] Test missing required fields (name, version, inputs, sections)
- [ ] Test invalid semantic version format
- [ ] Test duplicate input ids
- [ ] Test duplicate section ids
- [ ] Test invalid input type
- [ ] Test select field without options
- [ ] Test weights not summing to 1.0
- [ ] Test negative order values
- [ ] Test depends_on referencing non-existent field
- [ ] Assert appropriate validation errors raised

**Step 4: Test Field Validators** (30 min)
- [ ] Test min_length < max_length validation
- [ ] Test regex pattern syntax validation
- [ ] Test word count min < target < max
- [ ] Test priority enum values
- [ ] Test category enum values

**Step 5: Test Helper Methods** (30 min)
- [ ] Test `get_input_by_id()` with valid/invalid ids
- [ ] Test `get_section_by_id()` with valid/invalid ids
- [ ] Test `validate_input_data()` with valid/invalid user data
- [ ] Test `to_json_schema()` output structure

**Step 6: Test JSON Serialization** (15 min)
- [ ] Test blueprint → JSON → blueprint roundtrip
- [ ] Test JSON output matches schema
- [ ] Test pretty-printing option

**Deliverables for Task 1.1.3:**
- [ ] `tests/test_blueprint_models.py` (complete test suite)
- [ ] 20+ test cases covering edge cases
- [ ] All tests passing
- [ ] Test coverage > 90% for blueprint.py

---

## Sprint 1.2: Convert Existing Templates (3-4 days / 16-20 hours)

### Task 1.2.1: Create patterns/ Directory Structure
**Duration:** 1 hour  
**Priority:** Critical  
**Dependencies:** Task 1.1.1 complete

#### Atomic Steps:

**Step 1: Create Directory Structure** (15 min)
- [ ] Create directories:
  ```
  patterns/
  ├── _templates/             # For shared includes
  ├── examples/               # Example blueprints
  ├── project_charter/
  │   └── .gitkeep
  ├── work_plan/
  │   └── .gitkeep
  ├── proposal/
  │   └── .gitkeep
  ├── white_paper/           # New template
  │   └── .gitkeep
  └── executive_brief/       # New template
      └── .gitkeep
  ```

**Step 2: Create README for patterns/** (20 min)
- [ ] Create `patterns/README.md`
- [ ] Document structure purpose
- [ ] Document file naming conventions:
  - `blueprint.json` - Blueprint specification
  - `template.j2` - Jinja2 template for final document
  - `prompts.json` - AI prompts for generation (optional)
- [ ] Add instructions for creating new templates
- [ ] Link to `BLUEPRINT_SCHEMA.md`

**Step 3: Move Existing Templates** (15 min)
- [ ] Copy `app/templates/documents/PROJECT_CHARTER.md.j2` → `patterns/project_charter/template.j2`
- [ ] Copy `app/templates/documents/PROJECT_PLAN.md.j2` → `patterns/work_plan/template.j2`
- [ ] Keep originals for now (delete after migration complete)

**Step 4: Create Template Metadata** (10 min)
- [ ] Add `patterns/project_charter/README.md` with template description
- [ ] Add `patterns/work_plan/README.md` with template description
- [ ] Document required inputs for each

**Deliverables for Task 1.2.1:**
- [ ] Complete `patterns/` directory structure
- [ ] Documentation in place
- [ ] Existing templates copied to new location

---

### Task 1.2.2: Migrate PROJECT_CHARTER.md.j2 to Blueprint Format
**Duration:** 3-4 hours  
**Priority:** Critical  
**Dependencies:** Task 1.2.1 complete, phase1_initiation.py analysis

#### Atomic Steps:

**Step 1: Analyze Current Charter Wizard** (30 min)
- [ ] Read `app/wizard/phase1_initiation.py`
- [ ] List all prompted fields (20+ fields)
- [ ] Document field types and validations
- [ ] Note which fields are required vs optional
- [ ] Identify fields that map to CharterData model

**Step 2: Create Input Definitions** (1 hour)
- [ ] For each wizard field, create `TemplateInput` entry in JSON
- [ ] Example for `project_title`:
  ```json
  {
    "id": "project_title",
    "label": "Project Title",
    "type": "text",
    "description": "A clear, concise name for your project",
    "required": true,
    "validation": {
      "min_length": 3,
      "max_length": 100
    },
    "source": "charter.project_title"
  }
  ```
- [ ] Repeat for all fields:
  - project_sponsor
  - department
  - business_need
  - desired_outcomes
  - success_criteria
  - initial_risks_and_assumptions
  - strategic_alignment
  - measurable_benefits
  - high_level_requirements
  - project_goal
  - problem_definition
  - proposed_solution
  - selection_criteria
  - cost_benefit_analysis
  - scope
  - deliverables
  - major_obstacles
  - risks
  - schedule_overview
  - collaboration_needs
  - project_type

**Step 3: Define Section Structure** (45 min)
- [ ] Analyze existing `PROJECT_CHARTER.md.j2` template
- [ ] Identify main sections:
  1. Project Overview
  2. Business Case
  3. Goals & Objectives
  4. Scope
  5. Deliverables
  6. Risks & Assumptions
  7. Resources & Schedule
  8. Approval
- [ ] For each section, create `TemplateSection` entry
- [ ] Define prompt_template for AI enhancement (if applicable)
- [ ] Define context_requirements (what project context needed)

**Step 4: Create Step-Back Prompts** (30 min)
- [ ] Write restate_problem prompt:
  ```json
  {
    "restate_problem": {
      "prompt": "Based on the user's business need and desired outcomes, restate the core problem this project solves in 2-3 sentences.",
      "expected_output": "A clear, concise problem statement"
    }
  }
  ```
- [ ] Write identify_gaps prompt (check for missing charter elements)
- [ ] Write clarifying_questions prompt
- [ ] Write confirm_scope prompt

**Step 5: Create Verification Questions** (45 min)
- [ ] Create 8-10 verification questions for charter quality
- [ ] Example:
  ```json
  {
    "id": "vq_charter_01",
    "question": "Does the charter clearly articulate the business need or opportunity?",
    "category": "completeness",
    "priority": "critical",
    "context_check": ["business_need", "strategic_alignment"],
    "remediation_hint": "Expand the business case section with specific problems or opportunities."
  }
  ```
- [ ] Cover all critical charter elements
- [ ] Include factual, logical, and alignment checks

**Step 6: Define Quality Rubric** (30 min)
- [ ] Create rubric criteria:
  - Clarity (weight: 0.25) - Clear, concise language
  - Completeness (weight: 0.30) - All required sections present
  - Strategic Alignment (weight: 0.25) - Ties to org goals
  - Feasibility (weight: 0.20) - Realistic scope and resources
- [ ] Define 5-point scoring for each
- [ ] Set passing_score = 3.5

**Step 7: Assemble Complete Blueprint** (30 min)
- [ ] Create `patterns/project_charter/blueprint.json`
- [ ] Combine all above pieces into valid JSON
- [ ] Add metadata:
  ```json
  {
    "name": "project_charter",
    "version": "1.0.0",
    "description": "Formal project charter following PM methodology",
    "category": "project_management",
    ...
  }
  ```
- [ ] Validate JSON syntax
- [ ] Test loading with BlueprintSpec model

**Step 8: Update Jinja2 Template** (15 min)
- [ ] Review `template.j2` to ensure variable names match blueprint input ids
- [ ] Add comments indicating which inputs feed each section
- [ ] Keep template logic minimal (blueprints handle structure)

**Deliverables for Task 1.2.2:**
- [ ] `patterns/project_charter/blueprint.json` (complete, valid)
- [ ] `patterns/project_charter/template.j2` (updated)
- [ ] Blueprint loads successfully with BlueprintSpec model

---

### Task 1.2.3: Migrate PROJECT_PLAN.md.j2 to Blueprint Format
**Duration:** 2-3 hours  
**Priority:** High  
**Dependencies:** Task 1.2.2 complete (use as template)

#### Atomic Steps:

**Step 1: Analyze Current Planning Wizard** (20 min)
- [ ] Read `app/wizard/phase2_planning.py`
- [ ] List inputs (simpler than charter - uses AI for most)
- [ ] Document AI-generated vs user-provided fields

**Step 2: Create Input Definitions** (45 min)
- [ ] Create inputs for:
  - milestones (multiselect or textarea)
  - tasks (textarea or structured)
  - dependencies (textarea)
  - timeline (number - weeks or days)
  - resources (textarea)
  - critical_path (textarea, optional)
- [ ] Some fields auto-populated from charter:
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

**Step 3: Define Section Structure** (30 min)
- [ ] Sections:
  1. Executive Summary (from charter)
  2. Milestones
  3. Work Breakdown Structure (tasks)
  4. Dependencies
  5. Timeline
  6. Resource Requirements
  7. Critical Path
- [ ] Define prompt_templates for AI-enhanced sections

**Step 4: Create Step-Back Prompts** (20 min)
- [ ] Restate project goals
- [ ] Identify missing milestones
- [ ] Check task granularity

**Step 5: Create Verification Questions** (30 min)
- [ ] Does plan cover all deliverables from charter?
- [ ] Are dependencies clearly stated?
- [ ] Is timeline realistic given scope?
- [ ] Are resources identified?
- [ ] Is critical path identified?

**Step 6: Define Rubric** (20 min)
- [ ] Completeness (0.30)
- [ ] Clarity (0.25)
- [ ] Feasibility (0.25)
- [ ] Traceability to Charter (0.20)

**Step 7: Assemble Blueprint** (20 min)
- [ ] Create `patterns/work_plan/blueprint.json`
- [ ] Validate with BlueprintSpec

**Step 8: Update Template** (15 min)
- [ ] Update `patterns/work_plan/template.j2`
- [ ] Ensure variable names match

**Deliverables for Task 1.2.3:**
- [ ] `patterns/work_plan/blueprint.json`
- [ ] `patterns/work_plan/template.j2`
- [ ] Blueprint loads successfully

---

### Task 1.2.4: Create Proposal Blueprint (New Template)
**Duration:** 2-3 hours  
**Priority:** Medium  
**Dependencies:** Tasks 1.2.2 and 1.2.3 as examples

#### Atomic Steps:

**Step 1: Define Proposal Inputs** (45 min)
- [ ] Common proposal fields:
  - proposal_title
  - client/audience
  - problem_statement
  - proposed_solution
  - methodology
  - timeline
  - budget
  - team/qualifications
  - expected_outcomes
  - success_metrics
  - next_steps
- [ ] Some auto-populate from charter if project exists

**Step 2: Define Proposal Sections** (30 min)
- [ ] Standard proposal structure:
  1. Executive Summary
  2. Problem Statement
  3. Proposed Solution
  4. Methodology/Approach
  5. Timeline & Deliverables
  6. Budget
  7. Team Qualifications
  8. Success Metrics
  9. Next Steps

**Step 3: Create Step-Back Prompts** (20 min)
- [ ] Restate problem from client perspective
- [ ] Identify value proposition
- [ ] Check for compelling narrative

**Step 4: Create Verification Questions** (30 min)
- [ ] Does proposal clearly address client's problem?
- [ ] Is solution feasible and well-explained?
- [ ] Are costs justified?
- [ ] Are success metrics measurable?
- [ ] Is the call-to-action clear?

**Step 5: Define Rubric** (20 min)
- [ ] Clarity (0.30)
- [ ] Persuasiveness (0.25)
- [ ] Feasibility (0.25)
- [ ] Professionalism (0.20)

**Step 6: Create Jinja2 Template** (45 min)
- [ ] Write `patterns/proposal/template.j2`
- [ ] Professional proposal format
- [ ] Include all sections
- [ ] Add styling placeholders (for future PDF export)

**Step 7: Assemble Blueprint** (20 min)
- [ ] Create `patterns/proposal/blueprint.json`
- [ ] Validate

**Deliverables for Task 1.2.4:**
- [ ] `patterns/proposal/blueprint.json`
- [ ] `patterns/proposal/template.j2`
- [ ] Blueprint loads successfully

---

## Sprint 1.3: BlueprintRegistry Service (2-3 days / 12-16 hours)

### Task 1.3.1: Create BlueprintRegistry Service
**Duration:** 3-4 hours  
**Priority:** Critical  
**Dependencies:** All Sprint 1.2 tasks complete

#### Atomic Steps:

**Step 1: Create Service File** (10 min)
- [ ] Create `app/services/blueprint_registry.py`
- [ ] Add file docstring
- [ ] Import required modules:
  ```python
  from pathlib import Path
  import json
  from typing import Dict, List, Optional
  from app.models.blueprint import BlueprintSpec
  import logging
  ```

**Step 2: Create BlueprintRegistry Class** (20 min)
- [ ] Create class skeleton:
  ```python
  class BlueprintRegistry:
      """
      Manages loading, validation, and access to template blueprints.
      
      Blueprints are stored in patterns/<template_name>/blueprint.json
      """
      
      def __init__(self, patterns_dir: Optional[Path] = None):
          self.patterns_dir = patterns_dir or self._default_patterns_dir()
          self._blueprints: Dict[str, BlueprintSpec] = {}
          self._load_all_blueprints()
      
      @staticmethod
      def _default_patterns_dir() -> Path:
          """Get default patterns directory (project_root/patterns)"""
          # Implementation
          
      def _load_all_blueprints(self) -> None:
          """Load all blueprints from patterns directory"""
          # Implementation
  ```
- [ ] Add logger setup

**Step 3: Implement _load_all_blueprints() Method** (45 min)
- [ ] Scan patterns_dir for subdirectories
- [ ] For each directory, look for `blueprint.json`
- [ ] Try to load and validate each blueprint
- [ ] Log errors for invalid blueprints (don't crash)
- [ ] Store valid blueprints in `_blueprints` dict
- [ ] Log summary (X blueprints loaded, Y errors)

**Step 4: Implement load_blueprint() Method** (30 min)
- [ ] Method signature:
  ```python
  def load_blueprint(self, template_name: str) -> BlueprintSpec:
      """
      Load a specific blueprint by name.
      
      Args:
          template_name: Name of template (matches directory name)
          
      Returns:
          BlueprintSpec instance
          
      Raises:
          FileNotFoundError: If blueprint doesn't exist
          ValidationError: If blueprint is invalid
      """
  ```
- [ ] Check if already loaded (return cached)
- [ ] If not, load from file
- [ ] Validate with Pydantic
- [ ] Cache and return

**Step 5: Implement list_blueprints() Method** (20 min)
- [ ] Return list of available template names
- [ ] Include metadata (name, description, category)
- [ ] Option to filter by category
- [ ] Option to sort by name/category

**Step 6: Implement get_blueprint() Method** (15 min)
- [ ] Simpler version of load_blueprint for cached access
- [ ] Returns None if not found (doesn't try to load)

**Step 7: Implement validate_blueprint() Static Method** (30 min)
- [ ] Method signature:
  ```python
  @staticmethod
  def validate_blueprint(blueprint_path: Path) -> tuple[bool, List[str]]:
      """
      Validate a blueprint file without loading it into registry.
      
      Returns:
          (is_valid, list_of_errors)
      """
  ```
- [ ] Load JSON
- [ ] Try to parse with BlueprintSpec
- [ ] Return validation result and any error messages

**Step 8: Implement Hot-Reload (Dev Mode)** (45 min)
- [ ] Add `watch_mode` parameter to __init__
- [ ] Use watchdog library to monitor patterns_dir for changes
- [ ] On file change:
  - Reload affected blueprint
  - Validate
  - Update cache if valid
  - Log result
- [ ] Only enable in dev mode (not production)

**Step 9: Add Helper Methods** (30 min)
- [ ] `get_template_path(template_name: str) -> Path` - Get path to template.j2
- [ ] `get_inputs_for_template(template_name: str) -> List[TemplateInput]`
- [ ] `get_sections_for_template(template_name: str) -> List[TemplateSection]`
- [ ] `validate_user_inputs(template_name: str, user_data: dict) -> tuple[bool, List[str]]`

**Step 10: Add Error Handling** (15 min)
- [ ] Define custom exceptions:
  - `BlueprintNotFoundError`
  - `BlueprintValidationError`
- [ ] Wrap file I/O in try/except
- [ ] Provide helpful error messages

**Deliverables for Task 1.3.1:**
- [ ] `app/services/blueprint_registry.py` (complete)
- [ ] All methods implemented and documented
- [ ] Error handling in place
- [ ] Hot-reload functional (dev mode)

---

### Task 1.3.2: Implement Blueprint Caching
**Duration:** 1-2 hours  
**Priority:** Medium  
**Dependencies:** Task 1.3.1 complete

#### Atomic Steps:

**Step 1: Add Cache Invalidation Logic** (30 min)
- [ ] Add `reload_blueprint(template_name: str)` method
- [ ] Add `reload_all()` method
- [ ] Add `clear_cache()` method

**Step 2: Add Cache Statistics** (20 min)
- [ ] Track cache hits/misses
- [ ] Track load times
- [ ] Add `get_cache_stats()` method for debugging

**Step 3: Add LRU Cache (Optional)** (30 min)
- [ ] If many blueprints, use LRU cache to limit memory
- [ ] Use functools.lru_cache decorator
- [ ] Make cache size configurable

**Deliverables for Task 1.3.2:**
- [ ] Cache invalidation methods
- [ ] Cache statistics
- [ ] Optional LRU cache

---

### Task 1.3.3: Create CLI Command for Templates
**Duration:** 2-3 hours  
**Priority:** High  
**Dependencies:** Task 1.3.1 complete

#### Atomic Steps:

**Step 1: Add Templates Command to CLI** (30 min)
- [ ] Open `app/main.py`
- [ ] Add new command group:
  ```python
  @cli.group()
  def templates():
      """Manage document templates and blueprints"""
      pass
  ```

**Step 2: Implement `templates list` Subcommand** (45 min)
- [ ] Command:
  ```python
  @templates.command()
  def list():
      """List all available document templates"""
      # Load registry
      # Get list of blueprints
      # Display in table with rich.table
  ```
- [ ] Show: name, description, category, version
- [ ] Color-code by category
- [ ] Show count at bottom

**Step 3: Implement `templates show <name>` Subcommand** (1 hour)
- [ ] Command:
  ```python
  @templates.command()
  @click.argument("template_name")
  def show(template_name):
      """Show detailed information about a template"""
  ```
- [ ] Display:
  - Full description
  - Required inputs (list)
  - Optional inputs (list)
  - Sections (hierarchical)
  - Verification questions count
  - Rubric criteria
- [ ] Use rich.panel for formatting

**Step 4: Implement `templates validate` Subcommand** (30 min)
- [ ] Command:
  ```python
  @templates.command()
  @click.option("--all", is_flag=True, help="Validate all templates")
  @click.argument("template_name", required=False)
  def validate(template_name, all):
      """Validate blueprint file(s)"""
  ```
- [ ] If --all, validate all blueprints
- [ ] If template_name, validate specific one
- [ ] Show errors in red, success in green
- [ ] Return exit code 0 if all valid, 1 if any errors

**Step 5: Add to Makefile** (15 min)
- [ ] Add command: `make templates` → `project-wizard templates list`
- [ ] Add command: `make validate-templates` → `project-wizard templates validate --all`

**Deliverables for Task 1.3.3:**
- [ ] `project-wizard templates` command group
- [ ] `list`, `show`, `validate` subcommands
- [ ] Rich formatting for output
- [ ] Integration with Makefile

---

## Sprint 1.4: Integration & Testing (1-2 days / 8-12 hours)

### Task 1.4.1: Update DocumentGenerator to Use Blueprints
**Duration:** 3-4 hours  
**Priority:** Critical  
**Dependencies:** All Sprint 1.3 tasks complete

#### Atomic Steps:

**Step 1: Analyze Current DocumentGenerator** (30 min)
- [ ] Read `app/services/document_generator.py`
- [ ] Identify where templates are loaded
- [ ] Identify where data is passed to templates
- [ ] Note any hardcoded logic that should move to blueprints

**Step 2: Add BlueprintRegistry Integration** (30 min)
- [ ] Add BlueprintRegistry as dependency in __init__:
  ```python
  def __init__(self):
      self.template_env = ...  # existing Jinja2 env
      self.blueprint_registry = BlueprintRegistry()
  ```
- [ ] Update template loading to use registry

**Step 3: Update generate_document() Method** (1 hour)
- [ ] Change signature to:
  ```python
  def generate_document(
      self,
      template_name: str,
      user_data: dict,
      project_context: Optional[dict] = None
  ) -> tuple[str, dict]:
      """
      Generate document from blueprint and user data.
      
      Returns:
          (rendered_document, metadata)
      """
  ```
- [ ] Load blueprint from registry
- [ ] Validate user_data against blueprint inputs
- [ ] Merge user_data with project_context
- [ ] Render template with merged data
- [ ] Return document + metadata (blueprint version, timestamp, etc.)

**Step 4: Add Input Validation Method** (30 min)
- [ ] Create `validate_inputs()` method:
  ```python
  def validate_inputs(self, template_name: str, user_data: dict) -> tuple[bool, List[str]]:
      """Validate user inputs against blueprint requirements"""
  ```
- [ ] Check required fields present
- [ ] Check types match
- [ ] Check validation rules (min_length, pattern, etc.)
- [ ] Return errors list

**Step 5: Update Existing Document Generation Calls** (1 hour)
- [ ] Find all places DocumentGenerator is used
- [ ] Update calls to use new signature
- [ ] Update to use template_name instead of hardcoded template paths
- [ ] Ensure backward compatibility (old code still works)

**Step 6: Add Blueprint Metadata to Generated Docs** (20 min)
- [ ] Add YAML frontmatter to generated documents:
  ```yaml
  ---
  generated_by: project_wizard
  template: project_charter
  template_version: 1.0.0
  generated_at: 2025-11-28T12:00:00Z
  blueprint_checksum: abc123def456
  ---
  ```
- [ ] Useful for tracking document provenance

**Deliverables for Task 1.4.1:**
- [ ] DocumentGenerator updated to use blueprints
- [ ] Input validation functional
- [ ] Backward compatibility maintained
- [ ] Metadata added to generated documents

---

### Task 1.4.2: Create Integration Tests
**Duration:** 3-4 hours  
**Priority:** High  
**Dependencies:** Task 1.4.1 complete

#### Atomic Steps:

**Step 1: Create Test File** (10 min)
- [ ] Create `tests/test_blueprint_integration.py`
- [ ] Import required modules
- [ ] Create fixtures for test blueprints and data

**Step 2: Test Blueprint Loading** (30 min)
- [ ] Test BlueprintRegistry loads all patterns
- [ ] Test load_blueprint() for each template
- [ ] Test error handling for missing/invalid blueprints

**Step 3: Test Document Generation with Blueprints** (1 hour)
- [ ] Test generating charter from blueprint + data
- [ ] Test generating work_plan from blueprint + data
- [ ] Test generating proposal from blueprint + data
- [ ] Assert documents contain expected sections
- [ ] Assert metadata is present

**Step 4: Test Input Validation** (45 min)
- [ ] Test validation with valid inputs (all pass)
- [ ] Test validation with missing required fields
- [ ] Test validation with invalid types
- [ ] Test validation with values outside constraints
- [ ] Assert error messages are helpful

**Step 5: Test Template Rendering** (30 min)
- [ ] Test Jinja2 template can access all input fields
- [ ] Test conditional sections render correctly
- [ ] Test loops work (for lists like deliverables)

**Step 6: Test End-to-End Workflow** (45 min)
- [ ] Simulate full charter creation:
  1. Load blueprint
  2. Collect user inputs (mock)
  3. Validate inputs
  4. Generate document
  5. Verify output quality
- [ ] Repeat for work_plan and proposal

**Deliverables for Task 1.4.2:**
- [ ] `tests/test_blueprint_integration.py` (complete)
- [ ] 15+ integration test cases
- [ ] All tests passing
- [ ] Test coverage > 85% for blueprint system

---

### Task 1.4.3: Update Documentation
**Duration:** 2-3 hours  
**Priority:** High  
**Dependencies:** All Phase 1 tasks complete

#### Atomic Steps:

**Step 1: Create BLUEPRINT_GUIDE.md** (1 hour)
- [ ] Create `docs/BLUEPRINT_GUIDE.md`
- [ ] Sections:
  - "What are Blueprints?"
  - "Creating a New Blueprint"
  - "Blueprint File Structure"
  - "Input Types Reference"
  - "Section Configuration"
  - "Verification Questions"
  - "Quality Rubrics"
  - "Best Practices"
  - "Examples"
  - "Troubleshooting"
- [ ] Include screenshots of CLI commands
- [ ] Include full example blueprint

**Step 2: Update README.md** (30 min)
- [ ] Add "Blueprint System" section
- [ ] Document new `project-wizard templates` commands
- [ ] Update architecture diagram to show blueprints
- [ ] Update feature list

**Step 3: Update WARP.md** (20 min)
- [ ] Document new files (blueprint.py, blueprint_registry.py)
- [ ] Document patterns/ directory structure
- [ ] Add blueprint validation to testing section

**Step 4: Create CHANGELOG Entry** (15 min)
- [ ] Add Phase 1 completion to CHANGELOG.md:
  ```markdown
  ## [3.0.0-alpha.1] - 2025-11-XX
  
  ### Added
  - Blueprint system for template-driven document generation
  - BlueprintRegistry service for managing templates
  - `project-wizard templates` CLI commands
  - Migrated charter, work_plan, and proposal to blueprint format
  
  ### Changed
  - DocumentGenerator now uses blueprints instead of hardcoded logic
  
  ### Deprecated
  - Direct template loading (will be removed in v3.1.0)
  ```

**Step 5: Update PROJECT_PLAN.md** (10 min)
- [ ] Check off Phase 1 tasks
- [ ] Update status to "Phase 1 Complete ✅"
- [ ] Add lessons learned section

**Deliverables for Task 1.4.3:**
- [ ] `docs/BLUEPRINT_GUIDE.md` (comprehensive)
- [ ] Updated README.md, WARP.md, CHANGELOG.md
- [ ] PROJECT_PLAN.md updated
- [ ] All documentation accurate and helpful

---

## Phase 1 Success Checklist

Before marking Phase 1 complete, verify:

- [ ] All 3 blueprints (charter, work_plan, proposal) are valid and load successfully
- [ ] BlueprintRegistry service is fully functional
- [ ] `project-wizard templates` CLI commands work
- [ ] DocumentGenerator uses blueprints for generation
- [ ] All existing CLI commands still work (backward compatibility)
- [ ] All tests pass (unit + integration)
- [ ] Test coverage > 85% for new code
- [ ] Documentation is complete and accurate
- [ ] No breaking changes introduced
- [ ] Can generate a charter using new system successfully

---

## Next Phase Preview

### Phase 2: Database Migration & Enhanced Project Model

**First Steps:**
1. Design SQLModel schema for Project, ProjectNote, SupportingFile
2. Create migration script from JSON → SQLite
3. Test migration with sample data

**Estimated Duration:** 2-3 weeks

---

## Resumption Guide

**If you need to pause and resume later:**

1. **Check current status:**
   - Run: `git status` to see what files changed
   - Review this document to see which tasks are completed
   - Check PROJECT_PLAN.md for high-level progress

2. **Find your place:**
   - Each task has clear atomic steps
   - Check boxes [ ] indicate completion state
   - Read "Deliverables" section to see what should exist

3. **Continue from next uncompleted step:**
   - Start with the first unchecked [ ] item
   - Follow atomic steps exactly
   - Update checkboxes as you complete each step

4. **Validate before continuing:**
   - After each task, run tests
   - Verify deliverables exist and are correct
   - Commit work with descriptive message

---

## Appendix: Quick Reference

### File Locations
- Blueprint models: `app/models/blueprint.py`
- Blueprint service: `app/services/blueprint_registry.py`
- Blueprint tests: `tests/test_blueprint_models.py`, `tests/test_blueprint_integration.py`
- Templates: `patterns/<template_name>/`
- Documentation: `docs/BLUEPRINT_SCHEMA.md`, `docs/BLUEPRINT_GUIDE.md`

### Key Commands
```bash
# List templates
project-wizard templates list

# Show template details
project-wizard templates show project_charter

# Validate blueprints
project-wizard templates validate --all

# Run tests
pytest tests/test_blueprint_models.py -v
pytest tests/test_blueprint_integration.py -v

# Check coverage
pytest --cov=app.models.blueprint --cov=app.services.blueprint_registry tests/
```

### Common Issues

**Issue:** Blueprint won't load  
**Solution:** Validate JSON syntax, check required fields, run `project-wizard templates validate <name>`

**Issue:** Input validation fails  
**Solution:** Check `validation` rules in blueprint, ensure user_data types match input types

**Issue:** Template rendering error  
**Solution:** Verify variable names in template.j2 match input ids in blueprint

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-28  
**Status:** Ready for Implementation  
**Next Review:** After Sprint 1.1 completion
