"""
Tests for blueprint Pydantic models.

Tests blueprint validation logic, field validators, and helper methods.
"""

import pytest
from pydantic import ValidationError

from app.models.blueprint import (
    BlueprintSpec,
    DocumentCategory,
    InputType,
    InputValidation,
    Priority,
    QuestionCategory,
    Rubric,
    RubricCriterion,
    ScoringLevel,
    SelectOption,
    Subsection,
    TemplateInput,
    TemplateSection,
    VerificationQuestion,
    WordCount,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def minimal_valid_blueprint_data():
    """Minimal valid blueprint with required fields only."""
    return {
        "name": "test_document",
        "version": "1.0.0",
        "description": "Test document template",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Document title",
                "required": True,
            }
        ],
        "sections": [
            {
                "id": "overview",
                "title": "Overview",
                "description": "Document overview",
                "order": 1,
            }
        ],
    }


@pytest.fixture
def complete_blueprint_data(minimal_valid_blueprint_data):
    """Complete blueprint with all optional fields."""
    data = minimal_valid_blueprint_data.copy()
    data["metadata"] = {
        "author": "Test Author",
        "created_date": "2025-11-28",
        "tags": ["test", "example"],
    }
    data["verification_questions"] = [
        {
            "id": "vq_test_01",
            "question": "Is the title clear?",
            "category": "completeness",
            "priority": "high",
            "remediation_hint": "Make the title more descriptive",
        }
    ]
    return data


# ============================================================================
# InputValidation Tests
# ============================================================================


def test_input_validation_length_order():
    """Test min_length must be <= max_length."""
    with pytest.raises(ValidationError, match="min_length must be less than"):
        InputValidation(min_length=100, max_length=50)


def test_input_validation_numeric_order():
    """Test min must be <= max."""
    with pytest.raises(ValidationError, match="min must be less than"):
        InputValidation(min=100, max=50)


def test_input_validation_invalid_regex():
    """Test invalid regex pattern raises error."""
    with pytest.raises(ValidationError, match="Invalid regex pattern"):
        InputValidation(pattern="[invalid(")


def test_input_validation_valid():
    """Test valid input validation."""
    validation = InputValidation(
        min_length=3, max_length=100, pattern="^[A-Za-z]+$", min=0, max=1000
    )
    assert validation.min_length == 3
    assert validation.max_length == 100


# ============================================================================
# TemplateInput Tests
# ============================================================================


def test_template_input_id_must_be_snake_case():
    """Test input ID must be snake_case."""
    with pytest.raises(ValidationError, match="must be lowercase snake_case"):
        TemplateInput(
            id="CamelCase",
            label="Test",
            type=InputType.TEXT,
            description="Test input",
        )


def test_template_input_select_requires_options():
    """Test select/multiselect require options."""
    with pytest.raises(ValidationError, match="Options required"):
        TemplateInput(
            id="test_select",
            label="Select",
            type=InputType.SELECT,
            description="Test select",
        )


def test_template_input_select_with_options():
    """Test select with options is valid."""
    inp = TemplateInput(
        id="test_select",
        label="Select",
        type=InputType.SELECT,
        description="Test select",
        options=[
            SelectOption(value="opt1", label="Option 1"),
            SelectOption(value="opt2", label="Option 2"),
        ],
    )
    assert len(inp.options) == 2


def test_template_input_default_must_match_type():
    """Test default value must match input type."""
    with pytest.raises(ValidationError, match="must be numeric"):
        TemplateInput(
            id="test_number",
            label="Number",
            type=InputType.NUMBER,
            description="Test",
            default="not a number",
        )


def test_template_input_valid():
    """Test valid template input."""
    inp = TemplateInput(
        id="project_title",
        label="Project Title",
        type=InputType.TEXT,
        description="Enter project title",
        required=True,
        validation=InputValidation(min_length=3, max_length=100),
    )
    assert inp.id == "project_title"
    assert inp.required is True


# ============================================================================
# TemplateSection Tests
# ============================================================================


def test_template_section_order_must_be_positive():
    """Test section order must be positive."""
    with pytest.raises(ValidationError, match="must be positive"):
        TemplateSection(
            id="test_section",
            title="Test",
            description="Test section",
            order=0,
        )


def test_template_section_subsection_ids_unique():
    """Test subsection IDs must be unique."""
    with pytest.raises(ValidationError, match="Duplicate subsection IDs"):
        TemplateSection(
            id="test_section",
            title="Test",
            description="Test section",
            order=1,
            subsections=[
                Subsection(
                    id="sub1", title="Sub 1", description="Test", order=1
                ),
                Subsection(
                    id="sub1", title="Sub 1 Duplicate", description="Test", order=2
                ),
            ],
        )


def test_template_section_with_word_count():
    """Test section with word count constraints."""
    section = TemplateSection(
        id="overview",
        title="Overview",
        description="Overview section",
        order=1,
        word_count=WordCount(min=100, target=200, max=300),
    )
    assert section.word_count.target == 200


# ============================================================================
# WordCount Tests
# ============================================================================


def test_word_count_order_validation():
    """Test word count min <= target <= max."""
    with pytest.raises(ValidationError, match="min must be less than"):
        WordCount(min=300, target=200, max=400)

    with pytest.raises(ValidationError, match="target must be less than"):
        WordCount(min=100, target=400, max=300)


# ============================================================================
# VerificationQuestion Tests
# ============================================================================


def test_verification_question_id_format():
    """Test verification question ID must follow vq_<category>_<number>."""
    with pytest.raises(ValidationError, match="must follow format"):
        VerificationQuestion(
            id="invalid_id",
            question="Is this valid?",
            category=QuestionCategory.COMPLETENESS,
            priority=Priority.HIGH,
            remediation_hint="Fix it",
        )


def test_verification_question_expected_answer_validation():
    """Test expected_answer must be 'yes', 'no', or None."""
    with pytest.raises(ValidationError, match="must be 'yes', 'no', or null"):
        VerificationQuestion(
            id="vq_test_01",
            question="Is this valid?",
            category=QuestionCategory.COMPLETENESS,
            priority=Priority.HIGH,
            expected_answer="maybe",
            remediation_hint="Fix it",
        )


def test_verification_question_valid():
    """Test valid verification question."""
    vq = VerificationQuestion(
        id="vq_completeness_01",
        question="Are all sections complete?",
        category=QuestionCategory.COMPLETENESS,
        priority=Priority.CRITICAL,
        expected_answer="yes",
        context_check=["sections"],
        remediation_hint="Complete missing sections",
    )
    assert vq.id == "vq_completeness_01"
    assert vq.expected_answer == "yes"


# ============================================================================
# Rubric Tests
# ============================================================================


def test_rubric_criterion_scoring_levels():
    """Test rubric criterion must have all 5 scoring levels."""
    with pytest.raises(ValidationError, match="Missing required scoring level"):
        RubricCriterion(
            id="clarity",
            name="Clarity",
            description="Test",
            weight=1.0,
            scoring={
                "excellent": ScoringLevel(score=5, description="Great"),
                # Missing other levels
            },
        )


def test_rubric_weights_must_sum_to_one():
    """Test rubric criterion weights must sum to 1.0."""
    with pytest.raises(ValidationError, match="must sum to 1.0"):
        Rubric(
            criteria=[
                RubricCriterion(
                    id="clarity",
                    name="Clarity",
                    description="Test",
                    weight=0.6,
                    scoring={
                        "excellent": ScoringLevel(score=5, description="Great"),
                        "good": ScoringLevel(score=4, description="Good"),
                        "adequate": ScoringLevel(score=3, description="OK"),
                        "needs_improvement": ScoringLevel(score=2, description="Meh"),
                        "poor": ScoringLevel(score=1, description="Bad"),
                    },
                ),
                RubricCriterion(
                    id="completeness",
                    name="Completeness",
                    description="Test",
                    weight=0.3,  # Total is 0.9, not 1.0
                    scoring={
                        "excellent": ScoringLevel(score=5, description="Great"),
                        "good": ScoringLevel(score=4, description="Good"),
                        "adequate": ScoringLevel(score=3, description="OK"),
                        "needs_improvement": ScoringLevel(score=2, description="Meh"),
                        "poor": ScoringLevel(score=1, description="Bad"),
                    },
                ),
            ],
            passing_score=3.5,
            feedback_template="Score: {score}",
        )


# ============================================================================
# BlueprintSpec Tests
# ============================================================================


def test_blueprint_minimal_valid(minimal_valid_blueprint_data):
    """Test loading minimal valid blueprint."""
    blueprint = BlueprintSpec(**minimal_valid_blueprint_data)
    assert blueprint.name == "test_document"
    assert len(blueprint.inputs) == 1
    assert len(blueprint.sections) == 1


def test_blueprint_complete_valid(complete_blueprint_data):
    """Test loading complete blueprint with optional fields."""
    blueprint = BlueprintSpec(**complete_blueprint_data)
    assert blueprint.name == "test_document"
    assert blueprint.metadata.author == "Test Author"
    assert len(blueprint.verification_questions) == 1


def test_blueprint_name_must_be_snake_case():
    """Test blueprint name must be snake_case."""
    data = {
        "name": "InvalidName",  # Should be snake_case
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
            }
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    with pytest.raises(ValidationError, match="must be lowercase snake_case"):
        BlueprintSpec(**data)


def test_blueprint_version_must_be_semantic():
    """Test blueprint version must follow semantic versioning."""
    data = {
        "name": "test",
        "version": "1.0",  # Should be X.Y.Z
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
            }
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    with pytest.raises(ValidationError, match="semantic versioning"):
        BlueprintSpec(**data)


def test_blueprint_duplicate_input_ids():
    """Test blueprint rejects duplicate input IDs."""
    data = {
        "name": "test",
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
            },
            {
                "id": "title",  # Duplicate
                "label": "Title 2",
                "type": "text",
                "description": "Test",
            },
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    with pytest.raises(ValidationError, match="Duplicate input IDs"):
        BlueprintSpec(**data)


def test_blueprint_duplicate_section_orders():
    """Test blueprint rejects duplicate section orders."""
    data = {
        "name": "test",
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
            }
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1},
            {
                "id": "background",
                "title": "Background",
                "description": "Test",
                "order": 1,  # Duplicate order
            },
        ],
    }
    with pytest.raises(ValidationError, match="Duplicate section orders"):
        BlueprintSpec(**data)


def test_blueprint_depends_on_invalid_reference():
    """Test blueprint rejects depends_on with non-existent field."""
    data = {
        "name": "test",
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
                "depends_on": "nonexistent_field",
            }
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    with pytest.raises(ValidationError, match="does not exist"):
        BlueprintSpec(**data)


# ============================================================================
# Helper Method Tests
# ============================================================================


def test_blueprint_get_input_by_id(minimal_valid_blueprint_data):
    """Test getting input by ID."""
    blueprint = BlueprintSpec(**minimal_valid_blueprint_data)
    inp = blueprint.get_input_by_id("title")
    assert inp is not None
    assert inp.label == "Title"

    inp_missing = blueprint.get_input_by_id("nonexistent")
    assert inp_missing is None


def test_blueprint_get_required_inputs():
    """Test getting all required inputs."""
    data = {
        "name": "test",
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "required1",
                "label": "Required 1",
                "type": "text",
                "description": "Test",
                "required": True,
            },
            {
                "id": "optional1",
                "label": "Optional 1",
                "type": "text",
                "description": "Test",
                "required": False,
            },
            {
                "id": "required2",
                "label": "Required 2",
                "type": "text",
                "description": "Test",
                "required": True,
            },
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    blueprint = BlueprintSpec(**data)
    required = blueprint.get_required_inputs()
    assert len(required) == 2
    assert all(inp.required for inp in required)


def test_blueprint_validate_user_inputs():
    """Test validating user inputs against blueprint."""
    data = {
        "name": "test",
        "version": "1.0.0",
        "description": "Test",
        "category": "project_management",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test",
                "required": True,
                "validation": {"min_length": 3, "max_length": 50},
            },
            {
                "id": "count",
                "label": "Count",
                "type": "number",
                "description": "Test",
                "required": False,
                "validation": {"min": 0, "max": 100},
            },
        ],
        "sections": [
            {"id": "overview", "title": "Overview", "description": "Test", "order": 1}
        ],
    }
    blueprint = BlueprintSpec(**data)

    # Valid data
    valid, errors = blueprint.validate_user_inputs(
        {"title": "Test Document", "count": 50}
    )
    assert valid is True
    assert len(errors) == 0

    # Missing required field
    valid, errors = blueprint.validate_user_inputs({"count": 50})
    assert valid is False
    assert any("title" in error.lower() for error in errors)

    # String too short
    valid, errors = blueprint.validate_user_inputs({"title": "AB", "count": 50})
    assert valid is False
    assert any("at least 3 characters" in error for error in errors)

    # Number out of range
    valid, errors = blueprint.validate_user_inputs({"title": "Valid Title", "count": 150})
    assert valid is False
    assert any("at most 100" in error for error in errors)


def test_blueprint_to_dict_from_dict(minimal_valid_blueprint_data):
    """Test serialization roundtrip."""
    blueprint1 = BlueprintSpec(**minimal_valid_blueprint_data)
    data_dict = blueprint1.to_dict()
    blueprint2 = BlueprintSpec.from_dict(data_dict)

    assert blueprint1.name == blueprint2.name
    assert blueprint1.version == blueprint2.version
    assert len(blueprint1.inputs) == len(blueprint2.inputs)
