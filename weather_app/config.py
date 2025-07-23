"""Configuration management for the weather app."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the weather app."""
    
    # API Configuration
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    BASE_URL = 'http://api.openweathermap.org/data/2.5'
    
    # Cache Configuration
    CACHE_DIR = Path.home() / '.weather_cache'
    CACHE_DURATION = 600  # 10 minutes in seconds
    
    # Default Settings
    DEFAULT_UNITS = 'metric'
    DEFAULT_CITY = None
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.API_KEY:
            raise ValueError(
                "API key not found. Please set OPENWEATHER_API_KEY in your .env file.\n"
                "Get a free API key from: https://openweathermap.org/api"
            )
        return True