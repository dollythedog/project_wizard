"""
Pydantic models for Blueprint specification.

Blueprints define the structure, inputs, validation rules, and quality criteria
for document templates in Project Wizard.

Based on: docs/BLUEPRINT_SCHEMA.md v1.0.0
"""

import re
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


# ============================================================================
# Enums for Fixed Values
# ============================================================================


class InputType(str, Enum):
    """Valid input field types."""

    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    MULTISELECT = "multiselect"
    DATE = "date"
    NUMBER = "number"
    BOOLEAN = "boolean"
    EMAIL = "email"
    URL = "url"


class QuestionCategory(str, Enum):
    """Verification question categories."""

    FACTUAL = "factual"
    LOGICAL = "logical"
    COMPLETENESS = "completeness"
    ALIGNMENT = "alignment"


class Priority(str, Enum):
    """Priority levels for verification questions."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DocumentCategory(str, Enum):
    """Document categories for organization and filtering."""

    PROJECT_MANAGEMENT = "project_management"
    PROPOSAL = "proposal"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    TECHNICAL = "technical"
    POLICY = "policy"


# ============================================================================
# Validation Models
# ============================================================================


class InputValidation(BaseModel):
    """Validation rules for input fields."""

    min_length: Optional[int] = Field(None, description="Minimum character length")
    max_length: Optional[int] = Field(None, description="Maximum character length")
    pattern: Optional[str] = Field(None, description="Regex pattern to match")
    min: Optional[float] = Field(None, description="Minimum numeric value")
    max: Optional[float] = Field(None, description="Maximum numeric value")
    custom_validator: Optional[str] = Field(
        None, description="Name of custom validation function"
    )

    model_config = {"extra": "forbid"}

    @field_validator("min_length", "max_length")
    @classmethod
    def validate_length_positive(cls, v):
        """Ensure length constraints are positive."""
        if v is not None and v < 0:
            raise ValueError("Length must be non-negative")
        return v

    @model_validator(mode="after")
    def validate_length_order(self):
        """Ensure min_length <= max_length."""
        if (
            self.min_length is not None
            and self.max_length is not None
            and self.min_length > self.max_length
        ):
            raise ValueError("min_length must be less than or equal to max_length")
        return self

    @field_validator("pattern")
    @classmethod
    def validate_regex_pattern(cls, v):
        """Ensure pattern is valid regex."""
        if v is not None:
            try:
                re.compile(v)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")
        return v

    @model_validator(mode="after")
    def validate_numeric_order(self):
        """Ensure min <= max for numeric values."""
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("min must be less than or equal to max")
        return self


class SelectOption(BaseModel):
    """Option for select/multiselect inputs."""

    value: str = Field(..., description="Internal value")
    label: str = Field(..., description="Display label")


# ============================================================================
# Input Models
# ============================================================================


class TemplateInput(BaseModel):
    """Input field definition for template."""

    id: str = Field(..., description="Unique identifier (snake_case)")
    label: str = Field(..., description="User-facing label")
    type: InputType = Field(..., description="Input field type")
    description: str = Field(..., description="Help text for users")
    required: bool = Field(default=False, description="Whether field is required")
    default: Optional[Any] = Field(None, description="Default value")
    placeholder: Optional[str] = Field(None, description="Placeholder text")
    options: Optional[List[SelectOption]] = Field(
        None, description="Options for select/multiselect"
    )
    validation: Optional[InputValidation] = Field(None, description="Validation rules")
    depends_on: Optional[str] = Field(
        None, description="ID of field this depends on"
    )
    source: Optional[str] = Field(
        None, description="Auto-populate from source (dot notation)"
    )
    readonly: bool = Field(
        default=False, description="If true, field cannot be edited"
    )

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        """Ensure ID is snake_case."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                "Input ID must be lowercase snake_case (start with letter, "
                "contain only lowercase letters, numbers, and underscores)"
            )
        return v

    @field_validator("label")
    @classmethod
    def validate_label_not_empty(cls, v):
        """Ensure label is not empty."""
        if not v or not v.strip():
            raise ValueError("Label cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_options_for_select(self):
        """Ensure options provided for select/multiselect types."""
        if self.type in (InputType.SELECT, InputType.MULTISELECT):
            if not self.options or len(self.options) == 0:
                raise ValueError(
                    f"Options required for type '{self.type.value}' but none provided"
                )
        return self

    @model_validator(mode="after")
    def validate_default_type(self):
        """Ensure default value matches input type."""
        if self.default is not None:
            if self.type == InputType.NUMBER and not isinstance(
                self.default, (int, float)
            ):
                raise ValueError(f"Default value must be numeric for type 'number'")
            elif self.type == InputType.BOOLEAN and not isinstance(self.default, bool):
                raise ValueError(f"Default value must be boolean for type 'boolean'")
            elif self.type in (
                InputType.TEXT,
                InputType.TEXTAREA,
                InputType.EMAIL,
                InputType.URL,
            ) and not isinstance(self.default, str):
                raise ValueError(
                    f"Default value must be string for type '{self.type.value}'"
                )
        return self


# ============================================================================
# Section Models
# ============================================================================


class WordCount(BaseModel):
    """Word count constraints for sections."""

    min: Optional[int] = Field(None, description="Minimum word count")
    target: Optional[int] = Field(None, description="Target word count")
    max: Optional[int] = Field(None, description="Maximum word count")

    @field_validator("min", "target", "max")
    @classmethod
    def validate_positive(cls, v):
        """Ensure word counts are positive."""
        if v is not None and v < 0:
            raise ValueError("Word count must be non-negative")
        return v

    @model_validator(mode="after")
    def validate_order(self):
        """Ensure min <= target <= max."""
        if self.min is not None and self.target is not None and self.min > self.target:
            raise ValueError("min must be less than or equal to target")
        if (
            self.target is not None
            and self.max is not None
            and self.target > self.max
        ):
            raise ValueError("target must be less than or equal to max")
        return self


class Subsection(BaseModel):
    """Subsection within a section (1 level deep only)."""

    id: str = Field(..., description="Unique identifier (snake_case)")
    title: str = Field(..., description="Subsection heading")
    description: str = Field(..., description="What this subsection covers")
    order: int = Field(..., description="Display order within parent section")
    required: bool = Field(default=True, description="Whether subsection is required")

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        """Ensure ID is snake_case."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError("Subsection ID must be lowercase snake_case")
        return v

    @field_validator("order")
    @classmethod
    def validate_order_positive(cls, v):
        """Ensure order is positive."""
        if v < 1:
            raise ValueError("Order must be positive (1, 2, 3, ...)")
        return v


class TemplateSection(BaseModel):
    """Section definition for generated document."""

    id: str = Field(..., description="Unique identifier (snake_case)")
    title: str = Field(..., description="Section heading in document")
    description: str = Field(..., description="What this section covers")
    required: bool = Field(default=True, description="Whether section is required")
    order: int = Field(..., description="Display order in document")
    subsections: Optional[List[Subsection]] = Field(
        None, description="Nested subsections (max 1 level)"
    )
    prompt_template: Optional[str] = Field(
        None, description="AI instructions for generating this section"
    )
    context_requirements: Optional[List[str]] = Field(
        None, description="Required project context for this section"
    )
    word_count: Optional[WordCount] = Field(None, description="Word count constraints")

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        """Ensure ID is snake_case."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError("Section ID must be lowercase snake_case")
        return v

    @field_validator("order")
    @classmethod
    def validate_order_positive(cls, v):
        """Ensure order is positive."""
        if v < 1:
            raise ValueError("Order must be positive (1, 2, 3, ...)")
        return v

    @model_validator(mode="after")
    def validate_subsection_ids_unique(self):
        """Ensure subsection IDs are unique within section."""
        if self.subsections:
            ids = [sub.id for sub in self.subsections]
            if len(ids) != len(set(ids)):
                raise ValueError(
                    f"Duplicate subsection IDs in section '{self.id}': {ids}"
                )
        return self

    @model_validator(mode="after")
    def validate_subsection_orders_unique(self):
        """Ensure subsection orders are unique within section."""
        if self.subsections:
            orders = [sub.order for sub in self.subsections]
            if len(orders) != len(set(orders)):
                raise ValueError(
                    f"Duplicate subsection orders in section '{self.id}': {orders}"
                )
        return self


# ============================================================================
# Step-Back Prompts Models
# ============================================================================


class StepBackPromptItem(BaseModel):
    """Individual step-back prompt configuration."""

    prompt: str = Field(..., description="Instruction for AI")
    expected_output: str = Field(..., description="Description of expected output")


class ClarifyingQuestionsPrompt(BaseModel):
    """Configuration for clarifying questions generation."""

    prompt: str = Field(..., description="Instruction for generating questions")
    max_questions: int = Field(
        default=5, description="Maximum number of questions to generate"
    )
    categories: List[str] = Field(
        default_factory=list, description="Categories of questions to ask"
    )

    @field_validator("max_questions")
    @classmethod
    def validate_max_questions_positive(cls, v):
        """Ensure max_questions is positive."""
        if v < 1:
            raise ValueError("max_questions must be at least 1")
        return v


class StepBackPrompts(BaseModel):
    """Step-back prompting configuration for pre-draft clarification."""

    restate_problem: Optional[StepBackPromptItem] = Field(
        None, description="Prompt to restate user's problem"
    )
    identify_gaps: Optional[StepBackPromptItem] = Field(
        None, description="Prompt to identify information gaps"
    )
    clarifying_questions: Optional[ClarifyingQuestionsPrompt] = Field(
        None, description="Configuration for generating clarifying questions"
    )
    confirm_scope: Optional[StepBackPromptItem] = Field(
        None, description="Prompt to confirm project scope"
    )


# ============================================================================
# Verification Models
# ============================================================================


class VerificationQuestion(BaseModel):
    """Post-draft verification question (Chain of Verification)."""

    id: str = Field(..., description="Unique identifier (vq_<category>_<number>)")
    question: str = Field(..., description="The verification question")
    category: QuestionCategory = Field(..., description="Question category")
    priority: Priority = Field(..., description="Question priority")
    expected_answer: Optional[str] = Field(
        None, description="Expected answer ('yes', 'no', or null)"
    )
    context_check: List[str] = Field(
        default_factory=list, description="What to verify against"
    )
    remediation_hint: str = Field(
        ..., description="Guidance if verification fails"
    )

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        """Ensure ID follows vq_<category>_<number> format."""
        if not re.match(r"^vq_[a-z]+_\d+$", v):
            raise ValueError(
                "Verification question ID must follow format: vq_<category>_<number>"
            )
        return v

    @field_validator("expected_answer")
    @classmethod
    def validate_expected_answer(cls, v):
        """Ensure expected_answer is 'yes', 'no', or None."""
        if v is not None and v.lower() not in ("yes", "no"):
            raise ValueError("expected_answer must be 'yes', 'no', or null")
        return v.lower() if v else None


# ============================================================================
# Rubric Models
# ============================================================================


class ScoringLevel(BaseModel):
    """Scoring level definition (1-5 scale)."""

    score: int = Field(..., description="Numeric score (1-5)")
    description: str = Field(..., description="What this score means")

    @field_validator("score")
    @classmethod
    def validate_score_range(cls, v):
        """Ensure score is between 1 and 5."""
        if v < 1 or v > 5:
            raise ValueError("Score must be between 1 and 5")
        return v


class RubricCriterion(BaseModel):
    """Quality assessment criterion."""

    id: str = Field(..., description="Unique identifier (snake_case)")
    name: str = Field(..., description="Criterion name")
    description: str = Field(..., description="What to assess")
    weight: float = Field(
        ..., description="Importance weight (0-1, must sum to 1.0 across all criteria)"
    )
    scoring: Dict[str, ScoringLevel] = Field(
        ..., description="5-level scoring guide"
    )

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        """Ensure ID is snake_case."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError("Criterion ID must be lowercase snake_case")
        return v

    @field_validator("weight")
    @classmethod
    def validate_weight_range(cls, v):
        """Ensure weight is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Weight must be between 0.0 and 1.0")
        return v

    @model_validator(mode="after")
    def validate_scoring_levels(self):
        """Ensure all 5 scoring levels are present with correct scores."""
        required_levels = {
            "excellent": 5,
            "good": 4,
            "adequate": 3,
            "needs_improvement": 2,
            "poor": 1,
        }

        for level_name, expected_score in required_levels.items():
            if level_name not in self.scoring:
                raise ValueError(f"Missing required scoring level: '{level_name}'")
            if self.scoring[level_name].score != expected_score:
                raise ValueError(
                    f"Scoring level '{level_name}' must have score {expected_score}, "
                    f"got {self.scoring[level_name].score}"
                )

        return self


class Rubric(BaseModel):
    """Quality assessment rubric."""

    criteria: List[RubricCriterion] = Field(
        ..., description="Assessment criteria (weights must sum to 1.0)"
    )
    passing_score: float = Field(
        ..., description="Minimum acceptable score (weighted average)"
    )
    feedback_template: str = Field(
        ..., description="Template for presenting assessment results"
    )

    @field_validator("passing_score")
    @classmethod
    def validate_passing_score_range(cls, v):
        """Ensure passing score is between 1 and 5."""
        if v < 1 or v > 5:
            raise ValueError("Passing score must be between 1.0 and 5.0")
        return v

    @model_validator(mode="after")
    def validate_weights_sum_to_one(self):
        """Ensure criterion weights sum to 1.0."""
        total_weight = sum(criterion.weight for criterion in self.criteria)
        # Allow small floating point error
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(
                f"Criterion weights must sum to 1.0, got {total_weight:.3f}"
            )
        return self

    @model_validator(mode="after")
    def validate_criterion_ids_unique(self):
        """Ensure criterion IDs are unique."""
        ids = [criterion.id for criterion in self.criteria]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate criterion IDs: {ids}")
        return self


# ============================================================================
# Metadata Model
# ============================================================================


class BlueprintMetadata(BaseModel):
    """Optional metadata about the blueprint."""

    author: Optional[str] = Field(None, description="Template creator")
    created_date: Optional[str] = Field(None, description="Creation date (ISO format)")
    last_modified: Optional[str] = Field(
        None, description="Last modification date (ISO format)"
    )
    tags: List[str] = Field(default_factory=list, description="Search/filter tags")
    license: Optional[str] = Field(None, description="License information")


# ============================================================================
# Main Blueprint Model
# ============================================================================


class GenerationStrategy(str, Enum):
    """Document generation strategies."""
    
    FIELD_ENRICHMENT = "field_enrichment"  # Enrich individual fields, then template
    SKELETON_OF_THOUGHT = "skeleton_of_thought"  # Generate outline, then expand


class BlueprintSpec(BaseModel):
    """
    Complete blueprint specification for a document template.

    Blueprints define the structure, inputs, validation rules, and quality
    criteria for document templates in Project Wizard.

    Example:
        >>> blueprint = BlueprintSpec(
        ...     name="project_charter",
        ...     version="1.0.0",
        ...     description="Formal project charter",
        ...     category=DocumentCategory.PROJECT_MANAGEMENT,
        ...     inputs=[...],
        ...     sections=[...]
        ... )
    """

    # Required fields
    name: str = Field(..., description="Unique template identifier (snake_case)")
    version: str = Field(..., description="Semantic version (X.Y.Z)")
    description: str = Field(..., description="Template purpose")
    category: DocumentCategory = Field(..., description="Document category")
    generation_strategy: GenerationStrategy = Field(
        default=GenerationStrategy.FIELD_ENRICHMENT,
        description="Strategy for generating document content"
    )
    inputs: List[TemplateInput] = Field(..., description="User input fields")
    sections: List[TemplateSection] = Field(..., description="Document sections")

    # Optional fields
    step_back_prompts: Optional[StepBackPrompts] = Field(
        None, description="Pre-draft clarification prompts"
    )
    verification_questions: List[VerificationQuestion] = Field(
        default_factory=list, description="Post-draft verification questions"
    )
    rubric: Optional[Rubric] = Field(None, description="Quality assessment rubric")
    metadata: Optional[BlueprintMetadata] = Field(
        None, description="Additional metadata"
    )

    model_config = {"use_enum_values": True}

    # Validators
    @field_validator("name")
    @classmethod
    def validate_name_format(cls, v):
        """Ensure name is snake_case."""
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError("Blueprint name must be lowercase snake_case")
        return v

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v):
        """Ensure version follows semantic versioning (X.Y.Z)."""
        if not re.match(r"^\d+\.\d+\.\d+$", v):
            raise ValueError(
                "Version must follow semantic versioning format (e.g., '1.0.0')"
            )
        return v

    @field_validator("inputs")
    @classmethod
    def validate_inputs_not_empty(cls, v):
        """Ensure at least one input is defined."""
        if not v or len(v) == 0:
            raise ValueError("Blueprint must have at least one input")
        return v

    @field_validator("sections")
    @classmethod
    def validate_sections_not_empty(cls, v):
        """Ensure at least one section is defined."""
        if not v or len(v) == 0:
            raise ValueError("Blueprint must have at least one section")
        return v

    @model_validator(mode="after")
    def validate_input_ids_unique(self):
        """Ensure input IDs are unique."""
        ids = [inp.id for inp in self.inputs]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate input IDs: {ids}")
        return self

    @model_validator(mode="after")
    def validate_section_ids_unique(self):
        """Ensure section IDs are unique."""
        ids = [section.id for section in self.sections]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate section IDs: {ids}")
        return self

    @model_validator(mode="after")
    def validate_section_orders_unique(self):
        """Ensure section orders are unique."""
        orders = [section.order for section in self.sections]
        if len(orders) != len(set(orders)):
            raise ValueError(f"Duplicate section orders: {orders}")
        return self

    @model_validator(mode="after")
    def validate_depends_on_references(self):
        """Ensure depends_on references valid input IDs."""
        input_ids = {inp.id for inp in self.inputs}
        for inp in self.inputs:
            if inp.depends_on and inp.depends_on not in input_ids:
                raise ValueError(
                    f"Input '{inp.id}' depends_on '{inp.depends_on}' "
                    f"which does not exist"
                )
        return self

    # Helper methods
    def get_input_by_id(self, input_id: str) -> Optional[TemplateInput]:
        """Get input by ID."""
        for inp in self.inputs:
            if inp.id == input_id:
                return inp
        return None

    def get_section_by_id(self, section_id: str) -> Optional[TemplateSection]:
        """Get section by ID."""
        for section in self.sections:
            if section.id == section_id:
                return section
        return None

    def get_required_inputs(self) -> List[TemplateInput]:
        """Get all required inputs."""
        return [inp for inp in self.inputs if inp.required]

    def get_required_sections(self) -> List[TemplateSection]:
        """Get all required sections."""
        return [section for section in self.sections if section.required]

    def validate_user_inputs(self, user_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate user-provided data against blueprint requirements.

        Args:
            user_data: Dictionary of user inputs (field_id -> value)

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        for inp in self.get_required_inputs():
            if inp.id not in user_data or user_data[inp.id] is None:
                errors.append(f"Required field '{inp.id}' ({inp.label}) is missing")

        # Check field-specific validation
        for inp in self.inputs:
            if inp.id in user_data and user_data[inp.id] is not None:
                value = user_data[inp.id]

                # Type checking
                if inp.type == InputType.NUMBER and not isinstance(value, (int, float)):
                    errors.append(f"Field '{inp.id}' must be a number")
                elif inp.type == InputType.BOOLEAN and not isinstance(value, bool):
                    errors.append(f"Field '{inp.id}' must be boolean")
                elif inp.type in (
                    InputType.TEXT,
                    InputType.TEXTAREA,
                    InputType.EMAIL,
                    InputType.URL,
                ) and not isinstance(value, str):
                    errors.append(f"Field '{inp.id}' must be a string")

                # Validation rules
                if inp.validation and isinstance(value, str):
                    if (
                        inp.validation.min_length
                        and len(value) < inp.validation.min_length
                    ):
                        errors.append(
                            f"Field '{inp.id}' must be at least "
                            f"{inp.validation.min_length} characters"
                        )
                    if (
                        inp.validation.max_length
                        and len(value) > inp.validation.max_length
                    ):
                        errors.append(
                            f"Field '{inp.id}' must be at most "
                            f"{inp.validation.max_length} characters"
                        )
                    if inp.validation.pattern and not re.match(
                        inp.validation.pattern, value
                    ):
                        errors.append(
                            f"Field '{inp.id}' does not match required pattern"
                        )

                if inp.validation and isinstance(value, (int, float)):
                    if inp.validation.min and value < inp.validation.min:
                        errors.append(
                            f"Field '{inp.id}' must be at least {inp.validation.min}"
                        )
                    if inp.validation.max and value > inp.validation.max:
                        errors.append(
                            f"Field '{inp.id}' must be at most {inp.validation.max}"
                        )

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert blueprint to dictionary (for JSON serialization)."""
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlueprintSpec":
        """Load blueprint from dictionary."""
        return cls(**data)
