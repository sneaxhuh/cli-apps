#!/usr/bin/env python3
"""
🌤️ Beautiful Weather CLI - Main Entry Point

A beautiful command-line weather application for Ubuntu with colorful output,
caching, and advanced features.

Usage:
    python weather.py "New York"
    python weather.py London --units imperial
    python weather.py Paris --forecast 3
"""

from weather_app.cli import main

if __name__ == '__main__':
    main()