"""Configuration management for OpenRouter application."""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple
from dotenv import load_dotenv


class Config:
    """Configuration class for managing OpenRouter application settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load .env from parent directory (project root)
        parent_dir = Path(__file__).parent.parent
        env_path = parent_dir / ".env"
        
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # Try to load from current directory or environment
        
        self.api_key = self._get_api_key()
        self.api_base_url = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
        self.timeout = int(os.getenv("OPENROUTER_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("OPENROUTER_MAX_RETRIES", "3"))
        self.cache_ttl = int(os.getenv("OPENROUTER_CACHE_TTL", "3600"))  # 1 hour default
        
        # Application settings
        self.app_name = "Agent Zero - OpenRouter Model Fetcher"
        self.app_url = "https://agent-zero.ai/"
        
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables.
        
        Returns:
            str: API key if found, None otherwise
        """
        return os.getenv("OPENROUTER_API_KEY")
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate configuration.
        
        Returns:
            Tuple: (is_valid, error_message)
        """
        if not self.api_key:
            return False, (
                "OpenRouter API key not found. Please set OPENROUTER_API_KEY "
                "environment variable or add it to .env file in the project root."
            )
        
        if len(self.api_key) < 10:
            return False, "Invalid API key format. API key seems too short."
        
        if self.timeout < 1:
            return False, "Timeout must be at least 1 second."
        
        if self.max_retries < 0:
            return False, "Max retries must be non-negative."
        
        return True, None
    
    def __repr__(self) -> str:
        """String representation of configuration (without exposing API key)."""
        return (
            f"Config(api_base_url={self.api_base_url}, "
            f"timeout={self.timeout}, "
            f"max_retries={self.max_retries}, "
            f"cache_ttl={self.cache_ttl})"
        )
