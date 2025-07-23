"""Rich-based display formatting for weather data."""
from typing import Dict, Any, List
from datetime import datetime
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich import box

class WeatherDisplay:
    """Weather data display using Rich."""
    
    def __init__(self):
        self.console = Console()
        self.weather_icons = {
            'clear sky': '☀️',
            'few clouds': '🌤️',
            'scattered clouds': '⛅',
            'broken clouds': '☁️',
            'overcast clouds': '☁️',
            'shower rain': '🌦️',
            'rain': '🌧️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️',
            'haze': '🌫️',
            'dust': '🌪️',
            'sand': '🌪️',
            'ash': '🌋',
            'squall': '💨',
            'tornado': '🌪️'
        }
    
    def get_weather_icon(self, description: str) -> str:
        """Get weather icon for description."""
        description = description.lower()
        for key, icon in self.weather_icons.items():
            if key in description:
                return icon
        return '🌡️'  # Default icon
    
    def get_temperature_color(self, temp: float, units: str) -> str:
        """Get color for temperature based on value."""
        if units == 'imperial':
            # Fahrenheit thresholds
            if temp >= 85: return 'red'
            elif temp >= 70: return 'yellow'
            elif temp >= 50: return 'green'
            elif temp >= 32: return 'cyan'
            else: return 'blue'
        else:
            # Celsius thresholds
            if temp >= 30: return 'red'
            elif temp >= 20: return 'yellow'
            elif temp >= 10: return 'green'
            elif temp >= 0: return 'cyan'
            else: return 'blue'
    
    def format_units(self, units: str) -> Dict[str, str]:
        """Get unit symbols for display."""
        if units == 'imperial':
            return {
                'temp': '°F',
                'speed': 'mph',
                'pressure': 'in'
            }
        else:
            return {
                'temp': '°C',
                'speed': 'm/s',
                'pressure': 'hPa'
            }
    
    def display_current_weather(self, data: Dict[str, Any], units: str = 'metric'):
        """Display current weather data."""
        unit_symbols = self.format_units(units)
        
        # Extract data
        city = data['name']
        country = data['sys']['country']
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data.get('wind', {}).get('speed', 0)
        wind_dir = data.get('wind', {}).get('deg', 0)
        
        # Get weather icon and temperature color
        icon = self.get_weather_icon(description)
        temp_color = self.get_temperature_color(temp, units)
        
        # Create main weather panel
        weather_info = Text()
        weather_info.append(f"{icon} ", style="bold")
        weather_info.append(f"{description.title()}\n", style="bold white")
        weather_info.append(f"{temp:.1f}{unit_symbols['temp']}", style=f"bold {temp_color}")
        weather_info.append(f" (feels like {feels_like:.1f}{unit_symbols['temp']})", style="dim")
        
        main_panel = Panel(
            Align.center(weather_info),
            title=f"[bold cyan]{city}, {country}[/bold cyan]",
            title_align="center",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        # Create details table
        details_table = Table(show_header=False, box=None, padding=(0, 1))
        details_table.add_column(style="bold cyan", justify="right")
        details_table.add_column(style="white")
        
        details_table.add_row("💧 Humidity:", f"{humidity}%")
        details_table.add_row("🌬️  Wind:", f"{wind_speed:.1f} {unit_symbols['speed']}")
        details_table.add_row("📊 Pressure:", f"{pressure:.0f} {unit_symbols['pressure']}")
        
        # Wind direction
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind_direction = directions[int((wind_dir + 22.5) // 45) % 8] if wind_speed > 0 else 'N/A'
        details_table.add_row("🧭 Direction:", wind_direction)
        
        details_panel = Panel(
            details_table,
            title="[bold yellow]Details[/bold yellow]",
            box=box.ROUNDED
        )
        
        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_panel = Panel(
            Align.center(Text(f"🕐 {current_time}", style="dim")),
            box=box.ROUNDED
        )
        
        # Display all panels
        self.console.print()
        self.console.print(main_panel)
        self.console.print()
        self.console.print(Columns([details_panel, time_panel], equal=True))
        self.console.print()
    
    def display_forecast(self, data: Dict[str, Any], days: int, units: str = 'metric'):
        """Display weather forecast."""
        unit_symbols = self.format_units(units)
        
        city = data['city']['name']
        country = data['city']['country']
        forecast_list = data['list']
        
        # Group forecast by day
        daily_forecasts = {}
        for item in forecast_list[:days * 8]:  # Limit to requested days
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Create forecast table
        forecast_table = Table(box=box.ROUNDED, show_lines=True)
        forecast_table.add_column("Date", style="bold cyan", justify="center")
        forecast_table.add_column("Weather", justify="center")
        forecast_table.add_column("High/Low", style="bold", justify="center")
        forecast_table.add_column("Details", justify="left")
        
        for date, day_data in list(daily_forecasts.items())[:days]:
            # Get min/max temperatures for the day
            temps = [item['main']['temp'] for item in day_data]
            min_temp = min(temps)
            max_temp = max(temps)
            
            # Get most common weather condition
            weather_desc = day_data[len(day_data)//2]['weather'][0]['description']
            icon = self.get_weather_icon(weather_desc)
            
            # Get average humidity and wind
            avg_humidity = sum(item['main']['humidity'] for item in day_data) // len(day_data)
            avg_wind = sum(item.get('wind', {}).get('speed', 0) for item in day_data) / len(day_data)
            
            # Format date
            if date == datetime.now().date():
                date_str = "Today"
            elif date == datetime.now().date().replace(day=datetime.now().date().day + 1):
                date_str = "Tomorrow"
            else:
                date_str = date.strftime("%m/%d")
            
            # Temperature colors
            high_color = self.get_temperature_color(max_temp, units)
            low_color = self.get_temperature_color(min_temp, units)
            
            high_low = Text()
            high_low.append(f"{max_temp:.0f}°", style=f"bold {high_color}")
            high_low.append(" / ", style="dim")
            high_low.append(f"{min_temp:.0f}°", style=f"bold {low_color}")
            
            weather_col = Text()
            weather_col.append(f"{icon} ", style="bold")
            weather_col.append(weather_desc.title())
            
            details_col = Text()
            details_col.append(f"💧 {avg_humidity}%  ", style="dim")
            details_col.append(f"🌬️ {avg_wind:.1f}{unit_symbols['speed']}", style="dim")
            
            forecast_table.add_row(
                date_str,
                weather_col,
                high_low,
                details_col
            )
        
        # Display forecast
        forecast_panel = Panel(
            forecast_table,
            title=f"[bold cyan]{days}-Day Forecast for {city}, {country}[/bold cyan]",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(forecast_panel)
        self.console.print()
    
    def show_loading(self, message: str = "Fetching weather data..."):
        """Show loading spinner."""
        import time
        from rich.spinner import Spinner
        
        with self.console.status(f"[bold cyan]{message}[/bold cyan]", spinner="dots"):
            time.sleep(0.5)  # Brief pause for visual feedback
    
    def show_error(self, error_message: str):
        """Display error message."""
        error_panel = Panel(
            Text(f"❌ {error_message}", style="bold red"),
            title="[bold red]Error[/bold red]",
            box=box.ROUNDED
        )
        self.console.print()
        self.console.print(error_panel)
        self.console.print()
    
    def show_success(self, message: str):
        """Display success message."""
        success_panel = Panel(
            Text(f"✅ {message}", style="bold green"),
            title="[bold green]Success[/bold green]",
            box=box.ROUNDED
        )
        self.console.print()
        self.console.print(success_panel)
        self.console.print()