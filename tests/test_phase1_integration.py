"""Phase 1 Integration Tests - Blueprint System End-to-End

Tests the complete blueprint system including:
- Blueprint loading and validation
- Template rendering with blueprints
- Prompts.json loading and structure
- CLI commands
- Backward compatibility

Author: Project Wizard Team
Created: 2025-11-30
"""

import json
from pathlib import Path
from datetime import date

from app.models.blueprint import BlueprintSpec
from app.services.blueprint_registry import BlueprintRegistry, get_registry
from app.services.document_generator import DocumentGenerator
from app.models.charter import CharterData


class TestBlueprintSystemIntegration:
    """Integration tests for complete blueprint system."""
    
    def test_all_blueprints_load_successfully(self):
        """Verify all blueprints load without errors."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        assert len(blueprints) >= 3, "Should have at least 3 blueprints"
        
        for name in blueprints:
            blueprint = registry.load_blueprint(name)
            assert isinstance(blueprint, BlueprintSpec)
            assert blueprint.name == name
            assert len(blueprint.inputs) > 0
            assert len(blueprint.sections) > 0
            print(f"✓ {name} loaded successfully")
    
    def test_all_templates_exist(self):
        """Verify all blueprints have corresponding templates."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        for name in blueprints:
            template_path = registry.get_template_path(name)
            assert template_path.exists(), f"Template missing for {name}"
            assert template_path.suffix == ".j2", f"Template should be .j2 for {name}"
            print(f"✓ {name} template exists at {template_path}")
    
    def test_all_prompts_files_exist(self):
        """Verify all blueprints have prompts.json files."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        for name in blueprints:
            prompts_path = registry.patterns_dir / name / "prompts.json"
            assert prompts_path.exists(), f"prompts.json missing for {name}"
            
            # Verify it's valid JSON
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            
            # Verify required sections exist
            assert "step_back_prompts" in prompts, f"{name} missing step_back_prompts"
            assert "draft_generation" in prompts, f"{name} missing draft_generation"
            assert "verification" in prompts, f"{name} missing verification"
            assert "memory_logging" in prompts, f"{name} missing memory_logging"
            
            print(f"✓ {name} prompts.json valid with all sections")
    
    def test_prompts_structure_is_consistent(self):
        """Verify all prompts.json follow the same structure."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        required_sections = ["step_back_prompts", "draft_generation", "verification", "memory_logging"]
        
        for name in blueprints:
            prompts_path = registry.patterns_dir / name / "prompts.json"
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            
            for section in required_sections:
                assert section in prompts, f"{name} missing {section}"
            
            # Verify step_back_prompts structure
            assert "identity" in prompts["step_back_prompts"]
            assert "goals" in prompts["step_back_prompts"]
            assert "questions" in prompts["step_back_prompts"]
            
            # Verify draft_generation structure
            assert "identity" in prompts["draft_generation"]
            assert "goals" in prompts["draft_generation"]
            assert "steps" in prompts["draft_generation"]
            
            # Verify verification structure
            assert "identity" in prompts["verification"]
            assert "checks" in prompts["verification"]
            
            print(f"✓ {name} prompts structure is consistent")
    
    def test_blueprint_inputs_match_template_variables(self):
        """Verify blueprint inputs align with template variables (spot check)."""
        registry = get_registry()
        
        # Test project_charter
        charter_bp = registry.load_blueprint("project_charter")
        charter_template_path = registry.get_template_path("project_charter")
        
        with open(charter_template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check that some key inputs appear in template
        key_inputs = ["project_title", "project_goal", "scope"]
        for input_id in key_inputs:
            assert f"{{{{{input_id}}}}}" in template_content or f"{{{{ {input_id}" in template_content, \
                f"Input {input_id} not found in template"
        
        print("✓ project_charter inputs align with template")
    
    def test_document_generation_with_blueprints(self):
        """Test end-to-end document generation using blueprints."""
        # Create test charter data
        charter_data = CharterData(
            project_title="Test Integration Project",
            project_sponsor="Test Sponsor",
            department="Engineering",
            charter_date=date.today(),
            project_goal="Test the blueprint system integration",
            success_criteria="All tests pass successfully",
            business_need="Validate blueprint-based generation",
            desired_outcomes="Working document generation",
            problem_definition="Need to verify system works end-to-end",
            proposed_solution="Create comprehensive integration tests",
            strategic_alignment="Aligns with v3.0 roadmap",
            measurable_benefits="Confidence in system reliability",
            scope="Blueprint system validation",
            deliverables="Test suite and documentation",
            risks="Integration issues between components",
            initial_risks_and_assumptions="Assuming all components are in place",
            schedule_overview="Complete in Phase 1",
            high_level_requirements="Blueprint loading, template rendering, validation"
        )
        
        # Test with blueprint mode
        generator = DocumentGenerator(use_blueprints=True)
        content = generator.generate_charter(charter_data)
        
        assert "Test Integration Project" in content
        assert "Test the blueprint system integration" in content
        assert len(content) > 500, "Generated content should be substantial"
        
        print("✓ Document generation with blueprints works")
    
    def test_legacy_generation_still_works(self):
        """Verify backward compatibility - legacy generation unchanged."""
        charter_data = CharterData(
            project_title="Legacy Test Project",
            project_sponsor="Legacy Sponsor",
            project_goal="Test backward compatibility",
            success_criteria="Legacy mode works",
            business_need="Maintain compatibility",
            desired_outcomes="No breaking changes",
            problem_definition="Must support existing users",
            proposed_solution="Keep legacy path intact",
            strategic_alignment="User continuity",
            measurable_benefits="Zero migration issues",
            scope="Legacy generation",
            deliverables="Working legacy path",
            risks="Breaking changes",
            initial_risks_and_assumptions="Legacy templates unchanged",
            schedule_overview="Ongoing",
            high_level_requirements="Backward compatibility"
        )
        
        # Test without blueprint mode (legacy)
        generator = DocumentGenerator(use_blueprints=False)
        content = generator.generate_charter(charter_data)
        
        assert "Legacy Test Project" in content
        assert len(content) > 500
        
        print("✓ Legacy generation still works")
    
    def test_blueprint_validation_catches_errors(self):
        """Test that blueprint validation works correctly."""
        registry = get_registry()
        
        # Valid inputs
        charter_bp = registry.load_blueprint("project_charter")
        valid_inputs = {
            "project_title": "Test",
            "project_sponsor": "Sponsor",
            "charter_date": "2025-01-01",
            "project_goal": "This is a project goal that meets the minimum 20 character requirement",
            "success_criteria": "Criteria",
            "business_need": "This is a business need that is at least 50 characters long",
            "desired_outcomes": "Outcomes",
            "problem_definition": "Problem",
            "proposed_solution": "Solution",
            "strategic_alignment": "Alignment",
            "measurable_benefits": "Benefits",
            "scope": "This is a scope that is at least 50 characters long for validation",
            "deliverables": "Deliverables",
            "risks": "Risks",
            "initial_risks_and_assumptions": "Assumptions",
            "schedule_overview": "Schedule",
            "high_level_requirements": "Requirements"
        }
        
        is_valid, errors = charter_bp.validate_user_inputs(valid_inputs)
        assert is_valid and len(errors) == 0, f"Valid inputs should pass: {errors}"
        
        # Invalid inputs (missing required)
        invalid_inputs = {"project_title": "Test"}
        is_valid, errors = charter_bp.validate_user_inputs(invalid_inputs)
        assert not is_valid and len(errors) > 0, "Should have validation errors for missing fields"
        
        print("✓ Blueprint validation works correctly")
    
    def test_all_blueprints_have_verification_questions(self):
        """Verify all blueprints include verification questions."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        for name in blueprints:
            blueprint = registry.load_blueprint(name)
            assert blueprint.verification_questions is not None
            assert len(blueprint.verification_questions) > 0
            
            # Check structure of verification questions
            for vq in blueprint.verification_questions:
                assert vq.id is not None
                assert vq.question is not None
                assert vq.category is not None
                assert vq.priority is not None
            
            print(f"✓ {name} has {len(blueprint.verification_questions)} verification questions")
    
    def test_all_blueprints_have_rubrics(self):
        """Verify all blueprints include quality rubrics."""
        registry = get_registry()
        blueprints = registry.list_blueprints()
        
        for name in blueprints:
            blueprint = registry.load_blueprint(name)
            assert blueprint.rubric is not None
            assert len(blueprint.rubric.criteria) > 0
            assert blueprint.rubric.passing_score > 0
            
            # Check criteria structure
            for criterion in blueprint.rubric.criteria:
                assert criterion.id is not None
                assert criterion.name is not None
                assert 0 <= criterion.weight <= 1
                assert criterion.scoring is not None
            
            print(f"✓ {name} has rubric with {len(blueprint.rubric.criteria)} criteria")
    
    def test_registry_caching_works(self):
        """Test that blueprint caching functions properly."""
        registry = BlueprintRegistry()  # Fresh instance
        
        # First load
        bp1 = registry.load_blueprint("project_charter")
        assert "project_charter" in registry._blueprints
        
        # Second load should be cached
        bp2 = registry.load_blueprint("project_charter")
        assert bp1 is bp2, "Should return cached instance"
        
        # Clear cache
        registry.clear_cache()
        assert len(registry._blueprints) == 0
        
        # Load again
        bp3 = registry.load_blueprint("project_charter")
        assert bp3 is not bp1, "Should be new instance after cache clear"
        
        print("✓ Registry caching works correctly")
    
    def test_complete_workflow_project_charter(self):
        """Test complete workflow: load blueprint -> validate -> generate."""
        registry = get_registry()
        
        # 1. Load blueprint
        blueprint = registry.load_blueprint("project_charter")
        
        # 2. Prepare inputs
        inputs = {inp.id: f"Test {inp.label} with enough characters to meet requirements" for inp in blueprint.inputs if inp.required}
        inputs["project_title"] = "Complete Workflow Test"
        inputs["charter_date"] = "2025-01-01"
        inputs["project_goal"] = "This is a comprehensive project goal that meets all minimum length requirements for validation"
        inputs["business_need"] = "This is a business need that meets the 50 character minimum requirement"
        inputs["scope"] = "This is a detailed scope statement that meets the 50 character minimum"
        
        # 3. Validate inputs
        is_valid, errors = blueprint.validate_user_inputs(inputs)
        assert is_valid and len(errors) == 0, f"Validation should pass: {errors}"
        
        # 4. Generate document
        charter_data = CharterData(**inputs)
        generator = DocumentGenerator(use_blueprints=True)
        content = generator.generate_charter(charter_data)
        
        # 5. Verify output
        assert "Complete Workflow Test" in content
        assert len(content) > 1000
        
        print("✓ Complete workflow test passed")


class TestPromptsIntegration:
    """Test prompts.json integration with blueprint system."""
    
    def test_prompts_can_be_loaded_programmatically(self):
        """Verify prompts.json files can be loaded alongside blueprints."""
        registry = get_registry()
        
        for blueprint_name in registry.list_blueprints():
            prompts_path = registry.patterns_dir / blueprint_name / "prompts.json"
            
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            
            # Verify we can access step-back questions
            assert isinstance(prompts["step_back_prompts"]["questions"], list)
            assert len(prompts["step_back_prompts"]["questions"]) > 0
            
            # Verify draft generation steps
            assert isinstance(prompts["draft_generation"]["steps"], list)
            assert len(prompts["draft_generation"]["steps"]) > 0
            
            print(f"✓ {blueprint_name} prompts loaded successfully")
    
    def test_proposal_has_anti_hallucination_rules(self):
        """Verify proposal prompts include critical anti-hallucination safeguards."""
        registry = get_registry()
        prompts_path = registry.patterns_dir / "proposal" / "prompts.json"
        
        with open(prompts_path, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        # Check for anti-hallucination rules
        assert "critical_rules" in prompts["draft_generation"]
        assert "ABSOLUTE_PROHIBITIONS" in prompts["draft_generation"]["critical_rules"]
        
        prohibitions = prompts["draft_generation"]["critical_rules"]["ABSOLUTE_PROHIBITIONS"]
        assert any("NEVER invent names" in p for p in prohibitions)
        assert any("NEVER fabricate credentials" in p for p in prohibitions)
        
        print("✓ Proposal has anti-hallucination safeguards")


if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 1 INTEGRATION TESTS")
    print("=" * 70)
    print()
    
    # Run tests
    test_suite = TestBlueprintSystemIntegration()
    prompts_suite = TestPromptsIntegration()
    
    tests = [
        ("All blueprints load", test_suite.test_all_blueprints_load_successfully),
        ("All templates exist", test_suite.test_all_templates_exist),
        ("All prompts files exist", test_suite.test_all_prompts_files_exist),
        ("Prompts structure consistent", test_suite.test_prompts_structure_is_consistent),
        ("Blueprint inputs match templates", test_suite.test_blueprint_inputs_match_template_variables),
        ("Document generation with blueprints", test_suite.test_document_generation_with_blueprints),
        ("Legacy generation works", test_suite.test_legacy_generation_still_works),
        ("Blueprint validation works", test_suite.test_blueprint_validation_catches_errors),
        ("All have verification questions", test_suite.test_all_blueprints_have_verification_questions),
        ("All have rubrics", test_suite.test_all_blueprints_have_rubrics),
        ("Registry caching works", test_suite.test_registry_caching_works),
        ("Complete workflow test", test_suite.test_complete_workflow_project_charter),
        ("Prompts load programmatically", prompts_suite.test_prompts_can_be_loaded_programmatically),
        ("Proposal anti-hallucination", prompts_suite.test_proposal_has_anti_hallucination_rules),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {name} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    if failed == 0:
        print(f"✅ ALL {passed} TESTS PASSED")
    else:
        print(f"❌ {failed} TESTS FAILED, {passed} PASSED")
    print("=" * 70)
