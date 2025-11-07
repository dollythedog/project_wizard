"""OpenAI LLM client with retry logic and error handling."""

import os
from typing import Optional, Dict, List
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """Wrapper for OpenAI API with retry logic and configuration."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name (defaults to OPENAI_MODEL env var or gpt-4o-mini)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"Initialized LLM client with model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate completion with retry logic.
        
        Args:
            system_prompt: System message defining AI behavior
            user_prompt: User message with the actual request
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            
        Returns:
            Generated text completion
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temp,
                max_tokens=tokens
            )
            
            content = response.choices[0].message.content
            logger.info(f"Completion generated: {response.usage.total_tokens} tokens used")
            return content
            
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            raise
    
    def complete_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        examples: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate structured completion with optional few-shot examples.
        
        Args:
            system_prompt: System message
            user_prompt: User request
            examples: List of {"user": "...", "assistant": "..."} examples
            temperature: Override temperature
            
        Returns:
            Generated completion
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        if examples:
            for ex in examples:
                messages.append({"role": "user", "content": ex["user"]})
                messages.append({"role": "assistant", "content": ex["assistant"]})
        
        messages.append({"role": "user", "content": user_prompt})
        
        temp = temperature if temperature is not None else self.temperature
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in structured completion: {e}")
            raise
