"""Integration test for blueprint-based document generation.

Tests that DocumentGenerator can work with blueprints while maintaining
backward compatibility with legacy templates.

Author: Project Wizard Team
Created: 2025-11-28
"""

from pathlib import Path
from datetime import datetime
from app.services.document_generator import DocumentGenerator
from app.models.charter import CharterData


def test_legacy_generation():
    """Test that legacy generation still works."""
    generator = DocumentGenerator(use_blueprints=False)
    
    charter = CharterData(
        project_title="Test Project",
        project_sponsor="Test Sponsor",
        project_goal="Test goal",
        success_criteria="Test criteria",
        business_need="Test need",
        desired_outcomes="Test outcomes",
        problem_definition="Test problem",
        proposed_solution="Test solution",
        strategic_alignment="Test alignment",
        measurable_benefits="Test benefits",
        scope="Test scope",
        deliverables="Test deliverables",
        risks="Test risks",
        initial_risks_and_assumptions="Test assumptions",
        schedule_overview="Test schedule",
        high_level_requirements="Test requirements",
    )
    
    content = generator.generate_charter(charter)
    assert "Test Project" in content
    assert "Test goal" in content
    print("✓ Legacy generation works")


def test_blueprint_generation():
    """Test blueprint-based generation."""
    generator = DocumentGenerator(use_blueprints=True)
    
    # Charter data matching blueprint inputs
    charter = CharterData(
        project_title="Blueprint Test Project",
        project_sponsor="Blueprint Sponsor",
        department="Engineering",
        charter_date=datetime.now().date(),
        project_goal="Blueprint test goal",
        success_criteria="Blueprint success criteria",
        business_need="Blueprint business need",
        desired_outcomes="Blueprint outcomes",
        problem_definition="Blueprint problem",
        proposed_solution="Blueprint solution",
        strategic_alignment="Blueprint alignment",
        measurable_benefits="Blueprint benefits",
        scope="Blueprint scope",
        deliverables="Blueprint deliverables",
        risks="Blueprint risks",
        initial_risks_and_assumptions="Blueprint assumptions",
        schedule_overview="Blueprint schedule",
        high_level_requirements="Blueprint requirements",
    )
    
    content = generator.generate_charter(charter)
    assert "Blueprint Test Project" in content
    assert "Blueprint test goal" in content
    print("✓ Blueprint generation works")


def test_direct_blueprint_generation():
    """Test generating directly from blueprint with custom context."""
    generator = DocumentGenerator(use_blueprints=True)
    
    context = {
        "project_title": "Direct Blueprint Test",
        "executive_summary": "This is a test proposal generated via blueprint.",
        "problem_statement": "We need to test the blueprint system.",
        "proposed_solution": "Build automated tests.",
        "expected_benefits": "Confidence in system reliability.",
        "estimated_cost": "$0 (internal)",
        "timeline": "1 day",
        "risks": "None - low risk test",
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
    }
    
    content = generator.generate_from_blueprint("proposal", context)
    assert "Direct Blueprint Test" in content
    assert "This is a test proposal" in content
    print("✓ Direct blueprint generation works")


def test_blueprints_list():
    """Test that all blueprints are discoverable."""
    generator = DocumentGenerator(use_blueprints=True)
    blueprints = generator.blueprint_registry.list_blueprints()
    
    assert "project_charter" in blueprints
    assert "work_plan" in blueprints
    assert "proposal" in blueprints
    
    print(f"✓ Found {len(blueprints)} blueprints: {blueprints}")


def test_backward_compatibility():
    """Test that existing CLI code works unchanged."""
    # Legacy behavior (default)
    generator1 = DocumentGenerator()
    assert generator1.use_blueprints is False
    
    # Explicit legacy
    generator2 = DocumentGenerator(use_blueprints=False)
    assert generator2.use_blueprints is False
    
    # New blueprint-based
    generator3 = DocumentGenerator(use_blueprints=True)
    assert generator3.use_blueprints is True
    
    print("✓ Backward compatibility maintained")


if __name__ == "__main__":
    print("=" * 60)
    print("BLUEPRINT INTEGRATION TESTS")
    print("=" * 60)
    
    test_legacy_generation()
    test_blueprint_generation()
    test_direct_blueprint_generation()
    test_blueprints_list()
    test_backward_compatibility()
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
