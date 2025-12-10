"""OpenRouter API client with comprehensive error handling and retry logic."""

import time
import logging
from typing import Dict, List, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import Config


logger = logging.getLogger(__name__)


class OpenRouterAPIError(Exception):
    """Custom exception for OpenRouter API errors."""
    pass


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(self, config: Config):
        """Initialize the OpenRouter client.
        
        Args:
            config: Configuration object with API settings
        """
        self.config = config
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic.
        
        Returns:
            Configured requests Session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "HTTP-Referer": self.config.app_url,
            "X-Title": self.config.app_name,
            "Content-Type": "application/json"
        })
        
        return session
    
    def fetch_models(self) -> List[Dict[str, Any]]:
        """Fetch all available models from OpenRouter.
        
        Returns:
            List of model dictionaries
            
        Raises:
            OpenRouterAPIError: If API request fails
        """
        url = f"{self.config.api_base_url}/models"
        
        try:
            logger.info(f"Fetching models from {url}")
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if "data" not in data:
                raise OpenRouterAPIError("Invalid response format: 'data' field missing")
            
            models = data["data"]
            logger.info(f"Successfully fetched {len(models)} models")
            
            return models
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "unknown"
            error_msg = f"HTTP error {status_code}: {str(e)}"
            
            if status_code == 401:
                error_msg += " - Invalid API key"
            elif status_code == 429:
                error_msg += " - Rate limit exceeded"
            elif status_code == 403:
                error_msg += " - Access forbidden"
            
            logger.error(error_msg)
            raise OpenRouterAPIError(error_msg) from e
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            logger.error(error_msg)
            raise OpenRouterAPIError(error_msg) from e
            
        except requests.exceptions.Timeout as e:
            error_msg = f"Request timeout after {self.config.timeout} seconds"
            logger.error(error_msg)
            raise OpenRouterAPIError(error_msg) from e
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            raise OpenRouterAPIError(error_msg) from e
            
        except ValueError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            logger.error(error_msg)
            raise OpenRouterAPIError(error_msg) from e
    
    def get_model_details(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific model.
        
        Args:
            model_id: The model identifier
            
        Returns:
            Model details dictionary or None if not found
        """
        try:
            models = self.fetch_models()
            for model in models:
                if model.get("id") == model_id:
                    return model
            
            logger.warning(f"Model {model_id} not found")
            return None
            
        except OpenRouterAPIError as e:
            logger.error(f"Failed to fetch model details: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
