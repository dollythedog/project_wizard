"""
LLM Client for AI provider integration.

Supports OpenAI and Anthropic APIs with error handling, retry logic, and token tracking.
"""

import time
from typing import Optional, Any
from dataclasses import dataclass

from app.config import Config


@dataclass
class LLMResponse:
    """Response from LLM API call."""
    content: str
    model: str
    tokens_used: int
    finish_reason: str
    latency_ms: int


class LLMClient:
    """
    Client for LLM API calls with error handling and retry logic.
    
    Supports OpenAI and Anthropic APIs.
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize LLM client.
        
        Args:
            provider: "openai" or "anthropic". Auto-detected if None.
            model: Model name. Uses config default if None.
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
        """
        self.provider = provider or Config.get_llm_provider()
        
        if self.provider == "openai":
            self.model = model or Config.OPENAI_MODEL
            self.temperature = temperature or Config.OPENAI_TEMPERATURE
            self.max_tokens = max_tokens or Config.OPENAI_MAX_TOKENS
            self._init_openai()
        elif self.provider == "anthropic":
            self.model = model or Config.ANTHROPIC_MODEL
            self.temperature = temperature or 0.7
            self.max_tokens = max_tokens or 4000
            self._init_anthropic()
        else:
            raise ValueError(
                "No AI provider configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY."
            )
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Run: pip install openai"
            )
    
    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Run: pip install anthropic"
            )
    
    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3
    ) -> LLMResponse:
        """
        Generate text from prompt with retry logic.
        
        Args:
            prompt: User prompt/message
            system_message: System message (role instruction)
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            max_retries: Number of retries on failure
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            Exception: If all retries fail
        """
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                if self.provider == "openai":
                    response = self._generate_openai(prompt, system_message, temp, max_tok)
                elif self.provider == "anthropic":
                    response = self._generate_anthropic(prompt, system_message, temp, max_tok)
                else:
                    raise ValueError(f"Unknown provider: {self.provider}")
                
                latency_ms = int((time.time() - start_time) * 1000)
                
                return LLMResponse(
                    content=response["content"],
                    model=response["model"],
                    tokens_used=response["tokens"],
                    finish_reason=response["finish_reason"],
                    latency_ms=latency_ms
                )
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"LLM API error (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> dict[str, Any]:
        """Generate using OpenAI API."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "tokens": response.usage.total_tokens,
            "finish_reason": response.choices[0].finish_reason
        }
    
    def _generate_anthropic(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> dict[str, Any]:
        """Generate using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "content": response.content[0].text,
            "model": response.model,
            "tokens": response.usage.input_tokens + response.usage.output_tokens,
            "finish_reason": response.stop_reason
        }
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Note: This is a rough estimate. Actual tokens may vary.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        # Rough estimate: ~4 characters per token
        return len(text) // 4
