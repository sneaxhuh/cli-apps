"""Command-line interface for the weather app."""
import click
from typing import Optional
from .config import Config
from .api import WeatherAPI
from .display import WeatherDisplay

class WeatherCLI:
    """Command-line interface for the weather app."""
    
    def __init__(self):
        self.display = WeatherDisplay()
        self.api = None
    
    def _init_api(self):
        """Initialize API client with validation."""
        try:
            Config.validate()
            self.api = WeatherAPI()
        except ValueError as e:
            self.display.show_error(str(e))
            raise click.ClickException("Configuration error")
    
    def get_current_weather(self, city: str, units: str):
        """Get and display current weather."""
        self._init_api()
        
        try:
            self.display.show_loading(f"Getting current weather for {city}...")
            data = self.api.get_current_weather(city, units)
            self.display.display_current_weather(data, units)
        
        except Exception as e:
            self.display.show_error(str(e))
            raise click.ClickException("Failed to get weather data")
    
    def get_forecast(self, city: str, days: int, units: str):
        """Get and display weather forecast."""
        self._init_api()
        
        try:
            self.display.show_loading(f"Getting {days}-day forecast for {city}...")
            data = self.api.get_forecast(city, days, units)
            self.display.display_forecast(data, days, units)
        
        except Exception as e:
            self.display.show_error(str(e))
            raise click.ClickException("Failed to get forecast data")

# CLI instance
weather_cli = WeatherCLI()

@click.command()
@click.argument('city', required=False)
@click.option('--units', '-u', 
              type=click.Choice(['metric', 'imperial']), 
              default='metric',
              help='Temperature units (metric=Celsius, imperial=Fahrenheit)')
@click.option('--forecast', '-f', 
              type=int, 
              metavar='DAYS',
              help='Show forecast for specified number of days (1-5)')
@click.option('--clear-cache', 
              is_flag=True,
              help='Clear cached weather data')
@click.version_option(version='1.0.0', prog_name='Weather CLI')
def main(city: Optional[str], units: str, forecast: Optional[int], clear_cache: bool):
    """
    🌤️  Beautiful command-line weather app for Ubuntu
    
    Get current weather or forecast for any city with colorful, formatted output.
    
    Examples:
    
        weather "New York"              # Current weather for New York
        
        weather London --units imperial # Weather in Fahrenheit
        
        weather Paris --forecast 3      # 3-day forecast for Paris
        
        weather --clear-cache           # Clear cached data
    
    """
    display = WeatherDisplay()
    
    # Handle cache clearing
    if clear_cache:
        try:
            from .cache import WeatherCache
            cache = WeatherCache()
            cache.clear()
            display.show_success("Weather cache cleared successfully!")
            return
        except Exception as e:
            display.show_error(f"Failed to clear cache: {e}")
            return
    
    # Get city name
    if not city:
        city = click.prompt("Enter city name", type=str)
    
    # Validate forecast days
    if forecast is not None:
        if forecast < 1 or forecast > 5:
            display.show_error("Forecast days must be between 1 and 5")
            return
    
    try:
        if forecast:
            weather_cli.get_forecast(city, forecast, units)
        else:
            weather_cli.get_current_weather(city, units)
    
    except click.ClickException:
        # Error already displayed by the CLI methods
        pass
    except KeyboardInterrupt:
        display.console.print("\n👋 Goodbye!", style="bold yellow")
    except Exception as e:
        display.show_error(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()