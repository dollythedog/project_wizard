"""
Application configuration management.

Loads configuration from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Application configuration."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Anthropic Configuration (optional)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/project_wizard.db")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> list[str]:
        """
        Validate configuration and return list of errors.
        
        Returns:
            List of error messages. Empty list if all valid.
        """
        errors = []
        
        # Check if at least one AI provider is configured
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append(
                "No AI provider configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY "
                "in environment or .env file."
            )
        
        # Validate OpenAI configuration if key is present
        if cls.OPENAI_API_KEY:
            if not cls.OPENAI_API_KEY.startswith("sk-"):
                errors.append(
                    "OPENAI_API_KEY appears invalid (should start with 'sk-')"
                )
        
        return errors
    
    @classmethod
    def get_llm_provider(cls) -> str:
        """
        Get the preferred LLM provider based on configuration.
        
        Returns:
            "openai" or "anthropic"
        """
        if cls.OPENAI_API_KEY:
            return "openai"
        elif cls.ANTHROPIC_API_KEY:
            return "anthropic"
        else:
            return "none"


# Validate configuration on import
config_errors = Config.validate()
if config_errors and not Config.DEBUG:
    # Only warn in production, don't crash
    import warnings
    for error in config_errors:
        warnings.warn(f"Configuration warning: {error}")
