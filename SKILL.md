---
name: weather-query
description: Query weather information for cities worldwide. Use this skill when users ask about weather, temperature, forecasts, or climate conditions for any location. This skill supports current weather, multi-day forecasts, and air quality data. Activate whenever the user mentions weather, forecast, temperature, rain, snow, or asks about conditions in a specific city or location.
---

# Weather Query Skill

A skill for fetching weather information using the free Open-Meteo API (no API key required).

## Capabilities

- Get current weather for any city worldwide
- Get multi-day weather forecasts (up to 16 days)
- Get hourly weather data
- Get air quality information
- Support for both Celsius and Fahrenheit

## Supported Weather Data

- Temperature (current, feels-like, min/max)
- Weather conditions (sunny, cloudy, rain, snow, etc.)
- Humidity and precipitation
- Wind speed and direction
- Air quality index (AQI)
- UV index
- Sunrise/sunset times

## Usage

### Basic Usage

When the user asks for weather information:

1. Identify the location (city name)
2. Determine what data they need:
   - Current weather only
   - Multi-day forecast
   - Specific metrics (temperature, rain, etc.)
3. Use the provided scripts or API calls to fetch data
4. Present the information in a clear, human-readable format

### Available Scripts

The skill includes helper scripts in the `scripts/` directory:

- `weather.py` - Main weather query script with full functionality

### Using the Script Directly

```bash
# Current weather for a city
python scripts/weather.py --city "Beijing"

# 7-day forecast
python scripts/weather.py --city "Shanghai" --days 7

# Weather with air quality
python scripts/weather.py --city "Guangzhou" --aqi

# Hourly forecast for today
python scripts/weather.py --city "Shenzhen" --hourly
```

### Direct API Usage

If you need to make custom API calls:

**Geocoding (convert city name to coordinates):**
```
https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json
```

**Weather data:**
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto
```

## Weather Code Reference

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1-3 | Partly cloudy |
| 45, 48 | Foggy |
| 51-55 | Drizzle |
| 61-65 | Rain |
| 71-77 | Snow |
| 80-82 | Rain showers |
| 85-86 | Snow showers |
| 95-99 | Thunderstorm |

## Output Format

Always present weather information in a friendly format:

```
🌤️ 北京当前天气
━━━━━━━━━━━━━━━━━━━
🌡️ 温度: 22°C (体感 24°C)
☁️ 天气: 多云
💧 湿度: 65%
💨 风速: 12 km/h
━━━━━━━━━━━━━━━━━━━
```

## Examples

**User:** "北京今天天气怎么样？"
→ Fetch current weather for Beijing and display temperature, conditions, and humidity.

**User:** "纽约未来一周的天气预报"
→ Fetch 7-day forecast for New York City with daily highs/lows and conditions.

**User:** "Tokyo weather with air quality"
→ Fetch current weather + air quality index for Tokyo.

## Notes

- Open-Meteo API is free and requires no authentication
- Data is sourced from national weather services worldwide
- Forecast accuracy varies by region but is generally reliable
- Air quality data may not be available for all locations
