"""Blueprint Registry Service.

This service manages the loading, caching, and retrieval of document blueprints.
Blueprints define the structure, inputs, and validation rules for document templates.

Author: Project Wizard Team
Created: 2025-11-28
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from app.models.blueprint import BlueprintSpec


class BlueprintRegistry:
    """Registry for managing document template blueprints.
    
    This service:
    - Loads blueprints from the patterns/ directory
    - Validates blueprints on load using Pydantic models
    - Caches loaded blueprints in memory
    - Provides lookup by name
    - Lists available blueprints
    
    Attributes:
        patterns_dir: Root directory containing blueprint patterns
        _blueprints: Cache of loaded blueprints keyed by name
    """
    
    def __init__(self, patterns_dir: Optional[Path] = None):
        """Initialize the blueprint registry.
        
        Args:
            patterns_dir: Optional path to patterns directory. 
                         Defaults to <project_root>/patterns/
        """
        if patterns_dir is None:
            # Default to patterns/ directory relative to this file's location
            project_root = Path(__file__).parent.parent.parent
            patterns_dir = project_root / "patterns"
        
        self.patterns_dir = Path(patterns_dir)
        self._blueprints: Dict[str, BlueprintSpec] = {}
        
    def load_blueprint(self, name: str) -> BlueprintSpec:
        """Load a specific blueprint by name.
        
        Args:
            name: Blueprint name (e.g., 'project_charter')
            
        Returns:
            Validated BlueprintSpec instance
            
        Raises:
            FileNotFoundError: If blueprint.json not found
            ValueError: If blueprint fails validation
        """
        # Check cache first
        if name in self._blueprints:
            return self._blueprints[name]
        
        # Load from filesystem
        blueprint_path = self.patterns_dir / name / "blueprint.json"
        
        if not blueprint_path.exists():
            raise FileNotFoundError(
                f"Blueprint not found: {blueprint_path}\n"
                f"Available blueprints: {', '.join(self.list_blueprints())}"
            )
        
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate using Pydantic model
            blueprint = BlueprintSpec.model_validate(data)
            
            # Cache it
            self._blueprints[name] = blueprint
            
            return blueprint
            
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in blueprint {name}: {e}"
            ) from e
        except Exception as e:
            raise ValueError(
                f"Failed to load blueprint {name}: {e}"
            ) from e
    
    def get_blueprint(self, name: str) -> Optional[BlueprintSpec]:
        """Get a blueprint by name, returning None if not found.
        
        Args:
            name: Blueprint name
            
        Returns:
            BlueprintSpec instance or None if not found
        """
        try:
            return self.load_blueprint(name)
        except (FileNotFoundError, ValueError):
            return None
    
    def list_blueprints(self) -> List[str]:
        """List all available blueprint names.
        
        Returns:
            List of blueprint names (directories containing blueprint.json)
        """
        if not self.patterns_dir.exists():
            return []
        
        blueprints = []
        for item in self.patterns_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                blueprint_file = item / "blueprint.json"
                if blueprint_file.exists():
                    blueprints.append(item.name)
        
        return sorted(blueprints)
    
    def load_all(self) -> Dict[str, BlueprintSpec]:
        """Load all available blueprints into cache.
        
        Returns:
            Dictionary mapping blueprint names to BlueprintSpec instances
            
        Raises:
            ValueError: If any blueprint fails to load
        """
        names = self.list_blueprints()
        failed = []
        
        for name in names:
            try:
                self.load_blueprint(name)
            except Exception as e:
                failed.append((name, str(e)))
        
        if failed:
            error_msg = "\n".join([f"  - {name}: {err}" for name, err in failed])
            raise ValueError(
                f"Failed to load {len(failed)} blueprint(s):\n{error_msg}"
            )
        
        return self._blueprints.copy()
    
    def get_template_path(self, name: str) -> Path:
        """Get the template file path for a blueprint.
        
        Args:
            name: Blueprint name
            
        Returns:
            Path to template.j2 file
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_path = self.patterns_dir / name / "template.j2"
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"Template file not found: {template_path}"
            )
        
        return template_path
    
    def validate_user_inputs(
        self, 
        blueprint_name: str, 
        user_inputs: Dict[str, any]
    ) -> Dict[str, List[str]]:
        """Validate user inputs against blueprint requirements.
        
        Args:
            blueprint_name: Name of the blueprint
            user_inputs: Dictionary of user-provided input values
            
        Returns:
            Dictionary of validation errors keyed by input ID.
            Empty dict means validation passed.
            
        Raises:
            FileNotFoundError: If blueprint not found
        """
        blueprint = self.load_blueprint(blueprint_name)
        return blueprint.validate_user_inputs(user_inputs)
    
    def clear_cache(self):
        """Clear the blueprint cache, forcing reload on next access."""
        self._blueprints.clear()
    
    def get_blueprint_info(self, name: str) -> Dict[str, any]:
        """Get summary information about a blueprint.
        
        Args:
            name: Blueprint name
            
        Returns:
            Dictionary with blueprint metadata
        """
        blueprint = self.load_blueprint(name)
        
        return {
            "name": blueprint.name,
            "version": blueprint.version,
            "description": blueprint.description,
            "category": blueprint.category,
            "input_count": len(blueprint.inputs),
            "section_count": len(blueprint.sections),
            "has_verification": len(blueprint.verification_questions or []) > 0,
            "has_rubric": blueprint.rubric is not None,
            "metadata": blueprint.metadata
        }


# Global singleton instance
_registry: Optional[BlueprintRegistry] = None


def get_registry() -> BlueprintRegistry:
    """Get the global blueprint registry instance.
    
    Returns:
        BlueprintRegistry singleton
    """
    global _registry
    if _registry is None:
        _registry = BlueprintRegistry()
    return _registry
