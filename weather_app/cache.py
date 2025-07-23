"""Simple file-based caching system for weather data."""
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from .config import Config

class WeatherCache:
    """Simple file-based cache for weather data."""
    
    def __init__(self):
        self.cache_dir = Config.CACHE_DIR
        self.cache_duration = Config.CACHE_DURATION
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists."""
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for a given key."""
        safe_key = key.lower().replace(' ', '_').replace(',', '').replace('/', '_')
        return self.cache_dir / f"{safe_key}.json"
    
    def get(self, key: str) -> Optional[Dict[Any, Any]]:
        """Get cached data if it exists and is not expired."""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            if time.time() - cached_data.get('timestamp', 0) > self.cache_duration:
                cache_file.unlink()  # Remove expired cache
                return None
            
            return cached_data.get('data')
        
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            # If cache file is corrupted, remove it
            if cache_file.exists():
                cache_file.unlink()
            return None
    
    def set(self, key: str, data: Dict[Any, Any]):
        """Cache data with current timestamp."""
        cache_file = self._get_cache_file(key)
        
        cached_data = {
            'timestamp': time.time(),
            'data': data
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cached_data, f, indent=2)
        except Exception as e:
            # If we can't write to cache, just continue without caching
            pass
    
    def clear(self):
        """Clear all cached data."""
        if self.cache_dir.exists():
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()