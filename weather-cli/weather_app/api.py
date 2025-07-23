"""Weather API client for fetching weather data."""
import requests
from typing import Dict, Any, Optional
from .config import Config
from .cache import WeatherCache

class WeatherAPI:
    """Weather API client."""
    
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.cache = WeatherCache()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request with error handling."""
        url = f"{self.base_url}/{endpoint}"
        params['appid'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please check your internet connection.")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Unable to connect to weather service. Please check your internet connection.")
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Invalid API key. Please check your OPENWEATHER_API_KEY.")
            elif response.status_code == 404:
                raise Exception("City not found. Please check the city name and try again.")
            else:
                raise Exception(f"Weather service error: {e}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {e}")
    
    def get_current_weather(self, city: str, units: str = 'metric') -> Dict[str, Any]:
        """Get current weather for a city."""
        cache_key = f"current_{city}_{units}"
        
        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Fetch from API
        params = {
            'q': city,
            'units': units
        }
        
        data = self._make_request('weather', params)
        
        # Cache the result
        self.cache.set(cache_key, data)
        
        return data
    
    def get_forecast(self, city: str, days: int = 5, units: str = 'metric') -> Dict[str, Any]:
        """Get weather forecast for a city."""
        cache_key = f"forecast_{city}_{days}_{units}"
        
        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Fetch from API
        params = {
            'q': city,
            'units': units,
            'cnt': days * 8  # API returns 3-hour intervals, so 8 per day
        }
        
        data = self._make_request('forecast', params)
        
        # Cache the result
        self.cache.set(cache_key, data)
        
        return data