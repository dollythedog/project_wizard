"""Tests for BlueprintRegistry service.

Author: Project Wizard Team
Created: 2025-11-28
"""

import json
import pytest
from pathlib import Path
from app.services.blueprint_registry import BlueprintRegistry, get_registry
from app.models.blueprint import BlueprintSpec


@pytest.fixture
def temp_patterns_dir(tmp_path):
    """Create a temporary patterns directory with test blueprints."""
    patterns = tmp_path / "patterns"
    patterns.mkdir()
    
    # Create test_blueprint_1
    bp1_dir = patterns / "test_blueprint_1"
    bp1_dir.mkdir()
    
    bp1_data = {
        "name": "test_blueprint_1",
        "version": "1.0.0",
        "description": "Test blueprint",
        "category": "test",
        "inputs": [
            {
                "id": "title",
                "label": "Title",
                "type": "text",
                "description": "Test title",
                "required": True
            }
        ],
        "sections": [
            {
                "id": "main",
                "title": "Main Section",
                "description": "Main content",
                "order": 1,
                "required": True
            }
        ]
    }
    
    with open(bp1_dir / "blueprint.json", 'w') as f:
        json.dump(bp1_data, f)
    
    with open(bp1_dir / "template.j2", 'w') as f:
        f.write("# {{ title }}")
    
    # Create test_blueprint_2
    bp2_dir = patterns / "test_blueprint_2"
    bp2_dir.mkdir()
    
    bp2_data = {
        "name": "test_blueprint_2",
        "version": "2.0.0",
        "description": "Another test",
        "category": "test",
        "inputs": [],
        "sections": []
    }
    
    with open(bp2_dir / "blueprint.json", 'w') as f:
        json.dump(bp2_data, f)
    
    with open(bp2_dir / "template.j2", 'w') as f:
        f.write("# Empty")
    
    # Create directory without blueprint (should be ignored)
    ignore_dir = patterns / "_templates"
    ignore_dir.mkdir()
    
    # Create directory with invalid JSON
    invalid_dir = patterns / "invalid_blueprint"
    invalid_dir.mkdir()
    with open(invalid_dir / "blueprint.json", 'w') as f:
        f.write("{ invalid json")
    
    return patterns


class TestBlueprintRegistry:
    """Test suite for BlueprintRegistry."""
    
    def test_init_with_custom_path(self, temp_patterns_dir):
        """Test initialization with custom patterns directory."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        assert registry.patterns_dir == temp_patterns_dir
        assert len(registry._blueprints) == 0  # Cache starts empty
    
    def test_init_with_default_path(self):
        """Test initialization with default path."""
        registry = BlueprintRegistry()
        expected_path = Path(__file__).parent.parent / "patterns"
        assert registry.patterns_dir == expected_path
    
    def test_list_blueprints(self, temp_patterns_dir):
        """Test listing available blueprints."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        blueprints = registry.list_blueprints()
        
        # Should find test_blueprint_1 and test_blueprint_2
        # Should ignore _templates and invalid_blueprint
        assert len(blueprints) == 3  # 2 valid + 1 invalid (but has file)
        assert "test_blueprint_1" in blueprints
        assert "test_blueprint_2" in blueprints
        assert "_templates" not in blueprints
    
    def test_load_blueprint(self, temp_patterns_dir):
        """Test loading a valid blueprint."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        blueprint = registry.load_blueprint("test_blueprint_1")
        
        assert isinstance(blueprint, BlueprintSpec)
        assert blueprint.name == "test_blueprint_1"
        assert blueprint.version == "1.0.0"
        assert len(blueprint.inputs) == 1
        assert blueprint.inputs[0].id == "title"
    
    def test_load_blueprint_caching(self, temp_patterns_dir):
        """Test that blueprints are cached after first load."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        # First load
        bp1 = registry.load_blueprint("test_blueprint_1")
        assert "test_blueprint_1" in registry._blueprints
        
        # Second load should return cached instance
        bp2 = registry.load_blueprint("test_blueprint_1")
        assert bp1 is bp2  # Same object reference
    
    def test_load_blueprint_not_found(self, temp_patterns_dir):
        """Test loading a non-existent blueprint."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        with pytest.raises(FileNotFoundError) as exc_info:
            registry.load_blueprint("nonexistent")
        
        assert "Blueprint not found" in str(exc_info.value)
        assert "Available blueprints:" in str(exc_info.value)
    
    def test_load_blueprint_invalid_json(self, temp_patterns_dir):
        """Test loading blueprint with invalid JSON."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        with pytest.raises(ValueError) as exc_info:
            registry.load_blueprint("invalid_blueprint")
        
        assert "Invalid JSON" in str(exc_info.value)
    
    def test_get_blueprint(self, temp_patterns_dir):
        """Test get_blueprint method (returns None on error)."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        # Valid blueprint
        bp = registry.get_blueprint("test_blueprint_1")
        assert bp is not None
        assert bp.name == "test_blueprint_1"
        
        # Invalid blueprint
        bp_none = registry.get_blueprint("nonexistent")
        assert bp_none is None
    
    def test_load_all_success(self, temp_patterns_dir):
        """Test loading all valid blueprints."""
        # Remove invalid blueprint for this test
        invalid_dir = temp_patterns_dir / "invalid_blueprint"
        (invalid_dir / "blueprint.json").unlink()
        invalid_dir.rmdir()
        
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        all_blueprints = registry.load_all()
        
        assert len(all_blueprints) == 2
        assert "test_blueprint_1" in all_blueprints
        assert "test_blueprint_2" in all_blueprints
        assert all(isinstance(bp, BlueprintSpec) for bp in all_blueprints.values())
    
    def test_load_all_with_failures(self, temp_patterns_dir):
        """Test load_all with some invalid blueprints."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        with pytest.raises(ValueError) as exc_info:
            registry.load_all()
        
        assert "Failed to load" in str(exc_info.value)
        assert "invalid_blueprint" in str(exc_info.value)
    
    def test_get_template_path(self, temp_patterns_dir):
        """Test getting template file path."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        template_path = registry.get_template_path("test_blueprint_1")
        assert template_path.exists()
        assert template_path.name == "template.j2"
        assert template_path.parent.name == "test_blueprint_1"
    
    def test_get_template_path_not_found(self, temp_patterns_dir):
        """Test get_template_path when template doesn't exist."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        # Remove template file
        (temp_patterns_dir / "test_blueprint_1" / "template.j2").unlink()
        
        with pytest.raises(FileNotFoundError) as exc_info:
            registry.get_template_path("test_blueprint_1")
        
        assert "Template file not found" in str(exc_info.value)
    
    def test_validate_user_inputs(self, temp_patterns_dir):
        """Test user input validation."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        # Valid inputs
        valid_inputs = {"title": "My Test Title"}
        errors = registry.validate_user_inputs("test_blueprint_1", valid_inputs)
        assert len(errors) == 0
        
        # Missing required field
        invalid_inputs = {}
        errors = registry.validate_user_inputs("test_blueprint_1", invalid_inputs)
        assert "title" in errors
        assert any("required" in err.lower() for err in errors["title"])
    
    def test_clear_cache(self, temp_patterns_dir):
        """Test clearing the blueprint cache."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        # Load a blueprint
        registry.load_blueprint("test_blueprint_1")
        assert len(registry._blueprints) == 1
        
        # Clear cache
        registry.clear_cache()
        assert len(registry._blueprints) == 0
    
    def test_get_blueprint_info(self, temp_patterns_dir):
        """Test getting blueprint summary information."""
        registry = BlueprintRegistry(patterns_dir=temp_patterns_dir)
        
        info = registry.get_blueprint_info("test_blueprint_1")
        
        assert info["name"] == "test_blueprint_1"
        assert info["version"] == "1.0.0"
        assert info["description"] == "Test blueprint"
        assert info["category"] == "test"
        assert info["input_count"] == 1
        assert info["section_count"] == 1
        assert info["has_verification"] is False
        assert info["has_rubric"] is False


class TestGlobalRegistry:
    """Test the global registry singleton."""
    
    def test_get_registry_singleton(self):
        """Test that get_registry returns same instance."""
        reg1 = get_registry()
        reg2 = get_registry()
        
        assert reg1 is reg2  # Same object
        assert isinstance(reg1, BlueprintRegistry)


class TestRealBlueprints:
    """Integration tests with actual project blueprints."""
    
    def test_load_project_charter(self):
        """Test loading the actual project_charter blueprint."""
        registry = BlueprintRegistry()
        
        # This will only pass if running from project root with real blueprints
        blueprints = registry.list_blueprints()
        
        if "project_charter" in blueprints:
            charter = registry.load_blueprint("project_charter")
            assert charter.name == "project_charter"
            assert len(charter.inputs) > 0
            assert len(charter.sections) > 0
            
            # Check template exists
            template_path = registry.get_template_path("project_charter")
            assert template_path.exists()
    
    def test_load_work_plan(self):
        """Test loading the actual work_plan blueprint."""
        registry = BlueprintRegistry()
        blueprints = registry.list_blueprints()
        
        if "work_plan" in blueprints:
            work_plan = registry.load_blueprint("work_plan")
            assert work_plan.name == "work_plan"
            assert work_plan.version == "1.0.0"
    
    def test_load_proposal(self):
        """Test loading the actual proposal blueprint."""
        registry = BlueprintRegistry()
        blueprints = registry.list_blueprints()
        
        if "proposal" in blueprints:
            proposal = registry.load_blueprint("proposal")
            assert proposal.name == "proposal"
            assert len(proposal.inputs) > 0
