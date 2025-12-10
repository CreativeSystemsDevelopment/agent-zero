"""Caching mechanism for API responses."""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class Cache:
    """Simple file-based cache for API responses."""
    
    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600):
        """Initialize cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time-to-live for cache entries in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self.cache_file = self.cache_dir / "models_cache.json"
    
    def get(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached models if valid.
        
        Returns:
            Cached models or None if cache is invalid/expired
        """
        if not self.cache_file.exists():
            logger.debug("Cache file does not exist")
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
            now = datetime.now()
            
            if now - cached_time > timedelta(seconds=self.ttl_seconds):
                logger.info("Cache expired")
                return None
            
            logger.info(f"Using cached data from {cached_time}")
            return cache_data.get("models")
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning(f"Invalid cache file: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def set(self, models: List[Dict[str, Any]]):
        """Cache models data.
        
        Args:
            models: Models data to cache
        """
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "models": models
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Cached {len(models)} models")
            
        except Exception as e:
            logger.error(f"Error writing cache: {e}")
    
    def clear(self):
        """Clear the cache."""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
                logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def is_valid(self) -> bool:
        """Check if cache exists and is valid.
        
        Returns:
            True if cache is valid, False otherwise
        """
        return self.get() is not None
