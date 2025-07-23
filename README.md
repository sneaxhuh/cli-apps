# 🌤️ Beautiful Weather CLI

A stunning command-line weather application for Ubuntu with colorful output, intelligent caching, and advanced features.

![Weather CLI Demo](https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=800&h=200&fit=crop)

## ✨ Features

- 🎨 **Beautiful Output**: Rich, colorful terminal interface with weather icons
- ⚡ **Smart Caching**: Fast performance with intelligent data caching
- 🌡️ **Multiple Units**: Support for Celsius and Fahrenheit
- 📅 **Forecasts**: Up to 5-day weather forecasts
- 🔒 **Secure**: API keys stored in environment files
- 💫 **Loading Animations**: Smooth loading spinners
- 🚀 **Easy Setup**: Simple installation and configuration

## 📦 Installation

1. **Clone or download** the weather app files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get an API key**:
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## 🚀 Usage

### Basic Weather
```bash
# Get current weather for a city
python weather.py "New York"

# Interactive mode (prompts for city)
python weather.py
```

### Advanced Options
```bash
# Imperial units (Fahrenheit)
python weather.py London --units imperial

# 3-day forecast
python weather.py Paris --forecast 3

# 5-day forecast with imperial units
python weather.py Tokyo --forecast 5 --units imperial
```

### Cache Management
```bash
# Clear cached data
python weather.py --clear-cache
```

### Help
```bash
python weather.py --help
```

## 🎯 Examples

### Current Weather
```bash
$ python weather.py "San Francisco"

┌─────────── San Francisco, US ───────────┐
│                                         │
│              🌫️ Foggy Mist              │
│             15.2°C (feels like 14.8°C)  │
│                                         │
└─────────────────────────────────────────┘

┌───── Details ─────┐  ┌────── Time ──────┐
│  💧 Humidity: 78% │  │  🕐 2025-01-28   │
│  🌬️ Wind: 3.2 m/s │  │     14:30:22     │
│  📊 Pressure: 1013│  │                  │
│  🧭 Direction: NW │  │                  │
└───────────────────┘  └──────────────────┘
```

### 3-Day Forecast
```bash
$ python weather.py "London" --forecast 3

┌────────────── 3-Day Forecast for London, GB ──────────────┐
│  Date    │    Weather     │ High/Low │      Details       │
├──────────┼────────────────┼──────────┼────────────────────┤
│  Today   │ ☁️ Overcast    │   8° / 3°│ 💧 85%  🌬️ 4.1m/s │
│ Tomorrow │ 🌧️ Light Rain  │   7° / 2°│ 💧 92%  🌬️ 5.2m/s │
│  01/30   │ ⛅ Few Clouds  │  10° / 4°│ 💧 73%  🌬️ 3.8m/s │
└──────────┴────────────────┴──────────┴────────────────────┘
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Cache Settings
- **Location**: `~/.weather_cache/`
- **Duration**: 10 minutes
- **Auto-cleanup**: Expired cache files are automatically removed

## 🛠️ Development

### Project Structure
```
weather_app/
├── __init__.py          # Package initialization
├── api.py               # Weather API client
├── cache.py             # Caching system
├── cli.py               # Command-line interface
├── config.py            # Configuration management
└── display.py           # Rich-based display formatting

weather.py               # Main entry point
requirements.txt         # Dependencies
.env.example            # Example environment file
README.md               # This file
```

### Dependencies
- **requests**: HTTP client for API calls
- **rich**: Beautiful terminal output
- **python-dotenv**: Environment variable management
- **click**: Command-line interface framework

## 🔧 Troubleshooting

### Common Issues

**"API key not found"**
- Make sure your `.env` file exists and contains `OPENWEATHER_API_KEY`
- Verify your API key is valid at OpenWeatherMap

**"City not found"**
- Check spelling of city name
- Try including country code: "Paris, FR"
- Use quotes around city names with spaces

**"Connection error"**
- Check your internet connection
- Verify firewall isn't blocking requests

**Permission errors (cache)**
- Cache directory: `~/.weather_cache/`
- Ensure write permissions to home directory

### Clear Cache
If you encounter cache-related issues:
```bash
python weather.py --clear-cache
```

## 📋 Requirements

- **Python 3.7+**
- **Ubuntu** (tested on GNOME Terminal, xterm)
- **Internet connection**
- **Free OpenWeatherMap API key**

## 🌟 Features in Detail

### Weather Icons
- ☀️ Clear skies
- 🌤️ Partly cloudy
- ⛅ Scattered clouds
- ☁️ Overcast
- 🌦️ Showers
- 🌧️ Rain
- ⛈️ Thunderstorms
- ❄️ Snow
- 🌫️ Fog/Mist

### Temperature Colors
- 🔴 Hot (30°C+ / 85°F+)
- 🟡 Warm (20-29°C / 70-84°F)
- 🟢 Mild (10-19°C / 50-69°F)
- 🔵 Cool (0-9°C / 32-49°F)
- 🟦 Cold (below 0°C / 32°F)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

*Made with ❤️ for Ubuntu terminal users*