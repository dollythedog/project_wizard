"""
Best Practices Manager - Load, inject, and update pattern-specific learned context.

This module manages the best_practices.json file for each blueprint pattern,
allowing the system to learn from each generation and improve future outputs.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any


class BestPracticesManager:
    """Manages best practices registry for a blueprint pattern."""
    
    def __init__(self, pattern_name: str, patterns_dir: str = "patterns"):
        """
        Initialize best practices manager for a pattern.
        
        Args:
            pattern_name: Name of the blueprint pattern (e.g., 'productivity_pulse')
            patterns_dir: Directory where patterns are stored
        """
        self.pattern_name = pattern_name
        self.bp_path = Path(patterns_dir) / pattern_name / "best_practices.json"
        self.best_practices = self._load_best_practices()
    
    def _load_best_practices(self) -> Dict[str, Any]:
        """Load best practices from file, or return empty structure if not found."""
        if self.bp_path.exists():
            try:
                with open(self.bp_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._create_empty_best_practices()
        return self._create_empty_best_practices()
    
    def _create_empty_best_practices(self) -> Dict[str, Any]:
        """Create empty best practices structure if file doesn't exist."""
        return {
            "pattern_name": self.pattern_name,
            "last_updated": datetime.now().isoformat(),
            "generations_count": 0,
            "average_score": 0.0,
            "effective_phrases": {"phrases": []},
            "acronyms_and_conventions": {"standards": []},
            "topics_to_avoid": {"topics": []},
            "negative_patterns": {"patterns": []},
            "charter_context_integration": {"charter_fields_used": []},
            "generation_workflow": {"steps": []},
            "feedback_integration": {"feedback_types": []},
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "version": "1.0.0",
                "purpose": f"Centralized learning library for {self.pattern_name} pattern"
            }
        }
    
    def get_injection_context(self, charter: Optional[Dict] = None) -> str:
        """
        Build context string to inject into prompts.
        
        Args:
            charter: Optional charter dict for context
            
        Returns:
            Formatted context string ready for injection into prompts
        """
        parts = []
        
        # Add charter context if provided
        if charter:
            parts.append("🎯 PROJECT CHARTER (Your Foundation):")
            if "project_goal" in charter:
                parts.append(f"Goal: {charter['project_goal']}")
            if "success_criteria" in charter:
                parts.append(f"Success Criteria: {charter['success_criteria']}")
            if "scope_out" in charter:
                parts.append(f"Out of Scope: {charter['scope_out']}")
            parts.append("")
        
        # Add learned best practices
        parts.append("📚 LEARNED BEST PRACTICES:")
        parts.append("")
        
        # Effective phrases
        if self.best_practices.get("effective_phrases", {}).get("phrases"):
            parts.append("✓ EFFECTIVE PHRASES (Use These):")
            for phrase_obj in self.best_practices["effective_phrases"]["phrases"]:
                parts.append(f"  • \"{phrase_obj['phrase']}\"")
                parts.append(f"    Usage: {phrase_obj['usage']}")
                parts.append(f"    Example: {phrase_obj['example']}")
                parts.append(f"    Score: {phrase_obj.get('score_when_used', 'N/A')}/5.0 (Used {phrase_obj.get('times_used', 0)} times)")
            parts.append("")
        
        # Acronyms and conventions
        if self.best_practices.get("acronyms_and_conventions", {}).get("standards"):
            parts.append("📝 CONVENTIONS (Follow These):")
            for standard in self.best_practices["acronyms_and_conventions"]["standards"]:
                parts.append(f"  • {standard['term']}: {standard['convention']}")
                parts.append(f"    Example: {standard.get('example', 'N/A')}")
            parts.append("")
        
        # Topics to avoid
        if self.best_practices.get("topics_to_avoid", {}).get("topics"):
            parts.append("✗ TOPICS TO AVOID (Don't Do This):")
            for topic in self.best_practices["topics_to_avoid"]["topics"]:
                parts.append(f"  • {topic['topic']}: {topic['why_problematic']}")
                parts.append(f"    ❌ Bad: {topic['example_bad']}")
                parts.append(f"    ✓ Good: {topic['example_good']}")
            parts.append("")
        
        # Negative patterns
        if self.best_practices.get("negative_patterns", {}).get("patterns"):
            parts.append("⚠️  KNOWN PITFALLS (Learn From Past):")
            for pattern in self.best_practices["negative_patterns"]["patterns"]:
                if pattern.get("occurrences", 0) > 0:
                    parts.append(f"  • {pattern['error_id']} (occurred {pattern['occurrences']} time(s))")
                    parts.append(f"    Prevention: {pattern.get('prevention', 'N/A')}")
            parts.append("")
        
        return "\n".join(parts)
    
    def update_after_generation(
        self,
        score: float,
        verification_results: Dict[str, bool],
        effective_phrases_used: Optional[list] = None,
        issues_caught: Optional[list] = None
    ):
        """
        Update best practices after a generation completes.
        
        Args:
            score: Overall score for the generation (0-5.0)
            verification_results: Dict of verification check -> passed (bool)
            effective_phrases_used: List of phrase IDs that were used
            issues_caught: List of error pattern IDs that were caught
        """
        # Update generation count and average score
        old_count = self.best_practices.get("generations_count", 0)
        old_avg = self.best_practices.get("average_score", 0.0)
        new_count = old_count + 1
        new_avg = (old_avg * old_count + score) / new_count if new_count > 0 else score
        
        self.best_practices["generations_count"] = new_count
        self.best_practices["average_score"] = round(new_avg, 2)
        self.best_practices["last_updated"] = datetime.now().isoformat()
        
        # Track effective phrases if used
        if effective_phrases_used:
            phrases = self.best_practices.get("effective_phrases", {}).get("phrases", [])
            for phrase_id in effective_phrases_used:
                for phrase in phrases:
                    # Match by phrase text or index
                    if phrase.get("id") == phrase_id or str(phrase_id) in phrase.get("phrase", ""):
                        phrase["times_used"] = phrase.get("times_used", 0) + 1
        
        # Track errors/patterns that failed verification
        for check_id, passed in verification_results.items():
            if not passed:
                # Find matching negative pattern
                patterns = self.best_practices.get("negative_patterns", {}).get("patterns", [])
                for pattern in patterns:
                    if pattern.get("verification_check") == check_id:
                        pattern["occurrences"] = pattern.get("occurrences", 0) + 1
                        pattern["last_seen"] = datetime.now().isoformat()
        
        # Track issues that were caught/prevented
        if issues_caught:
            patterns = self.best_practices.get("negative_patterns", {}).get("patterns", [])
            for issue_id in issues_caught:
                for pattern in patterns:
                    if pattern.get("error_id") == issue_id:
                        # Just record it was caught; this info helps track prevention effectiveness
                        pattern["last_caught_timestamp"] = datetime.now().isoformat()
        
        self._save_best_practices()
    
    def add_effective_phrase(self, phrase: str, usage: str, example: str, score: float = 4.0):
        """Add a new effective phrase to best practices."""
        phrases = self.best_practices.get("effective_phrases", {}).get("phrases", [])
        
        # Check if phrase already exists
        for p in phrases:
            if p["phrase"].lower() == phrase.lower():
                # Update existing
                p["usage"] = usage
                p["example"] = example
                p["score_when_used"] = score
                self._save_best_practices()
                return
        
        # Add new phrase
        phrases.append({
            "phrase": phrase,
            "usage": usage,
            "example": example,
            "score_when_used": score,
            "times_used": 0,
            "avoid_phrases": []
        })
        
        self.best_practices["effective_phrases"]["phrases"] = phrases
        self._save_best_practices()
    
    def add_negative_pattern(self, error_id: str, description: str, verification_check: str, remediation: str):
        """Add a new negative pattern to track."""
        patterns = self.best_practices.get("negative_patterns", {}).get("patterns", [])
        
        # Check if pattern already exists
        for p in patterns:
            if p["error_id"] == error_id:
                return  # Already exists
        
        # Add new pattern
        patterns.append({
            "error_id": error_id,
            "verification_check": verification_check,
            "description": description,
            "occurrences": 0,
            "last_seen": None,
            "remediation": remediation,
            "prevention": f"Monitor for: {description}"
        })
        
        self.best_practices["negative_patterns"]["patterns"] = patterns
        self._save_best_practices()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about pattern performance."""
        return {
            "pattern_name": self.pattern_name,
            "generations_count": self.best_practices.get("generations_count", 0),
            "average_score": self.best_practices.get("average_score", 0.0),
            "effective_phrases_count": len(self.best_practices.get("effective_phrases", {}).get("phrases", [])),
            "acronyms_count": len(self.best_practices.get("acronyms_and_conventions", {}).get("standards", [])),
            "topics_to_avoid_count": len(self.best_practices.get("topics_to_avoid", {}).get("topics", [])),
            "negative_patterns_count": len(self.best_practices.get("negative_patterns", {}).get("patterns", [])),
            "last_updated": self.best_practices.get("last_updated", "Never")
        }
    
    def _save_best_practices(self):
        """Save best practices to file."""
        self.bp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.bp_path, 'w') as f:
            json.dump(self.best_practices, f, indent=2)
