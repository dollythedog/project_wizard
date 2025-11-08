"""
Pattern Registry Service
Fabric-inspired pattern management system
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)


class PatternRegistry:
    """Manages LEAN/PM document patterns (Fabric-inspired)"""
    
    def __init__(self, patterns_dir: Path = None):
        """
        Initialize pattern registry
        
        Args:
            patterns_dir: Path to patterns directory. If None, uses project_root/patterns
        """
        if patterns_dir is None:
            # Default to project_root/patterns
            base_dir = Path(__file__).parent.parent.parent
            patterns_dir = base_dir / "patterns"
        
        self.patterns_dir = Path(patterns_dir)
        self._patterns = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load all patterns from patterns directory"""
        if not self.patterns_dir.exists():
            logger.warning(f"Patterns directory not found: {self.patterns_dir}")
            return
        
        for pattern_dir in self.patterns_dir.iterdir():
            if not pattern_dir.is_dir():
                continue
            
            pattern_name = pattern_dir.name
            
            try:
                pattern_data = {
                    'name': pattern_name,
                    'path': pattern_dir,
                    'system': self._load_file(pattern_dir / 'system.md'),
                    'user_template': self._load_template(pattern_dir / 'user.md'),
                    'output_template': self._load_template(pattern_dir / 'template.md.j2'),
                    'variables': self._load_json(pattern_dir / 'variables.json'),
                    'rubric': self._load_json(pattern_dir / 'rubric.json'),
                }
                
                # Validate required files
                if not pattern_data['system']:
                    logger.warning(f"Pattern {pattern_name}: missing system.md")
                    continue
                
                self._patterns[pattern_name] = pattern_data
                logger.info(f"Loaded pattern: {pattern_name}")
                
            except Exception as e:
                logger.error(f"Failed to load pattern {pattern_name}: {e}")
    
    def _load_file(self, path: Path) -> Optional[str]:
        """Load text file"""
        if not path.exists():
            return None
        try:
            return path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read {path}: {e}")
            return None
    
    def _load_template(self, path: Path) -> Optional[Template]:
        """Load Jinja2 template"""
        content = self._load_file(path)
        if content:
            try:
                return Template(content)
            except Exception as e:
                logger.error(f"Failed to parse template {path}: {e}")
        return None
    
    def _load_json(self, path: Path) -> Optional[Dict]:
        """Load JSON file"""
        content = self._load_file(path)
        if content:
            try:
                return json.loads(content)
            except Exception as e:
                logger.error(f"Failed to parse JSON {path}: {e}")
        return None
    
    def get_pattern(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a pattern by name
        
        Args:
            name: Pattern name (directory name)
        
        Returns:
            Pattern dictionary or None if not found
        """
        return self._patterns.get(name)
    
    def list_patterns(self) -> list[str]:
        """Get all available pattern names"""
        return list(self._patterns.keys())
    
    def get_pattern_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get pattern metadata without loading full content
        
        Returns:
            Dict with name, variables, rubric info
        """
        pattern = self.get_pattern(name)
        if not pattern:
            return None
        
        return {
            'name': pattern['name'],
            'variables': pattern['variables'],
            'has_rubric': pattern['rubric'] is not None,
            'rubric_threshold': pattern['rubric'].get('threshold') if pattern['rubric'] else None,
        }
    
    def render_user_prompt(self, pattern_name: str, **variables) -> str:
        """
        Render user.md template with provided variables
        
        Args:
            pattern_name: Name of pattern
            **variables: Variables to inject into template
        
        Returns:
            Rendered user prompt string
        """
        pattern = self.get_pattern(pattern_name)
        if not pattern or not pattern['user_template']:
            raise ValueError(f"Pattern {pattern_name} not found or has no user template")
        
        try:
            return pattern['user_template'].render(**variables)
        except Exception as e:
            logger.error(f"Failed to render user prompt for {pattern_name}: {e}")
            raise
    
    def render_output(self, pattern_name: str, content: str, **metadata) -> str:
        """
        Render final output document using template.md.j2
        
        Args:
            pattern_name: Name of pattern
            content: Main document content (from AI)
            **metadata: Additional metadata (project_name, created_date, etc.)
        
        Returns:
            Rendered output document
        """
        pattern = self.get_pattern(pattern_name)
        if not pattern or not pattern['output_template']:
            # Fallback: return content as-is
            logger.warning(f"Pattern {pattern_name} has no output template, returning raw content")
            return content
        
        try:
            return pattern['output_template'].render(content=content, **metadata)
        except Exception as e:
            logger.error(f"Failed to render output for {pattern_name}: {e}")
            return content  # Fallback to raw content
    
    def reload_patterns(self):
        """Reload all patterns from disk"""
        self._patterns = {}
        self._load_patterns()
