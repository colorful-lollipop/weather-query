#!/usr/bin/env python3
"""
Weather Query Script using Open-Meteo API
Free weather API with no authentication required
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime


def get_coordinates(city_name):
    """Get latitude and longitude for a city name"""
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=zh&format=json"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        if not data.get('results'):
            print(f"Error: Could not find location '{city_name}'")
            return None
            
        result = data['results'][0]
        return {
            'latitude': result['latitude'],
            'longitude': result['longitude'],
            'name': result.get('name', city_name),
            'country': result.get('country', ''),
            'admin1': result.get('admin1', '')  # State/Province
        }
    except Exception as e:
        print(f"Error fetching location data: {e}")
        return None


def get_weather(lat, lon, days=1, hourly=False, aqi=False):
    """Fetch weather data from Open-Meteo"""
    
    # Build URL based on requested data
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = [
        f"latitude={lat}",
        f"longitude={lon}",
        "current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,is_day",
        "daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum",
        f"forecast_days={days}",
        "timezone=auto"
    ]
    
    if hourly:
        params.append("hourly=temperature_2m,weather_code,relative_humidity_2m")
    
    url = f"{base_url}?{'&'.join(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            weather_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
    
    # Fetch air quality if requested
    aqi_data = None
    if aqi:
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm10,pm2_5"
        try:
            with urllib.request.urlopen(aqi_url, timeout=10) as response:
                aqi_data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            pass  # AQI not available for all locations
    
    return {'weather': weather_data, 'aqi': aqi_data}


def weather_code_to_emoji(code):
    """Convert WMO weather code to emoji"""
    codes = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌧️",
        61: "🌧️",
        63: "🌧️",
        65: "🌧️",
        71: "🌨️",
        73: "🌨️",
        75: "🌨️",
        77: "🌨️",
        80: "🌦️",
        81: "🌧️",
        82: "🌧️",
        85: "🌨️",
        86: "🌨️",
        95: "⛈️",
        96: "⛈️",
        99: "⛈️",
    }
    return codes.get(code, "🌡️")


def weather_code_to_text(code):
    """Convert WMO weather code to text description"""
    codes = {
        0: "晴朗",
        1: "主要晴朗",
        2: "多云",
        3: "阴天",
        45: "雾",
        48: "雾凇",
        51: "毛毛雨",
        53: "中度毛毛雨",
        55: "大毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中阵雨",
        82: "大阵雨",
        85: "小阵雪",
        86: "大阵雪",
        95: "雷雨",
        96: "雷雨伴有冰雹",
        99: "大雷雨伴有冰雹",
    }
    return codes.get(code, "未知")


def get_aqi_description(aqi):
    """Get air quality description based on US AQI"""
    if aqi <= 50:
        return "🟢 优"
    elif aqi <= 100:
        return "🟡 良"
    elif aqi <= 150:
        return "🟠 轻度污染"
    elif aqi <= 200:
        return "🔴 中度污染"
    elif aqi <= 300:
        return "🟣 重度污染"
    else:
        return "🟤 严重污染"


def format_weather(location, data, days=1, aqi=False):
    """Format weather data for display"""
    weather = data['weather']
    aqi_data = data.get('aqi')
    current = weather['current']
    daily = weather['daily']
    
    city_name = location['name']
    if location.get('admin1'):
        city_name += f", {location['admin1']}"
    if location.get('country'):
        city_name += f", {location['country']}"
    
    # Current weather
    code = current['weather_code']
    emoji = weather_code_to_emoji(code)
    condition = weather_code_to_text(code)
    
    output = []
    output.append(f"\n{emoji} {location['name']} 当前天气")
    output.append("━━━━━━━━━━━━━━━━━━━")
    output.append(f"🌡️  温度: {current['temperature_2m']}°C (体感 {current['apparent_temperature']}°C)")
    output.append(f"☁️  天气: {condition}")
    output.append(f"💧 湿度: {current['relative_humidity_2m']}%")
    output.append(f"💨 风速: {current['wind_speed_10m']} km/h")
    
    # Air quality
    if aqi and aqi_data and 'current' in aqi_data:
        aqi_value = aqi_data['current'].get('us_aqi', 'N/A')
        if aqi_value != 'N/A':
            aqi_desc = get_aqi_description(aqi_value)
            output.append(f"🌬️  空气质量: {aqi_desc} (AQI: {aqi_value})")
            pm25 = aqi_data['current'].get('pm2_5')
            if pm25:
                output.append(f"   PM2.5: {pm25} μg/m³")
    
    output.append("━━━━━━━━━━━━━━━━━━━")
    
    # Daily forecast
    if days > 1:
        output.append(f"\n📅 未来 {days} 天预报:")
        output.append("─" * 30)
        
        for i in range(days):
            date_str = daily['time'][i]
            date_obj = datetime.fromisoformat(date_str)
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
            
            day_code = daily['weather_code'][i]
            day_emoji = weather_code_to_emoji(day_code)
            day_condition = weather_code_to_text(day_code)
            
            max_temp = daily['temperature_2m_max'][i]
            min_temp = daily['temperature_2m_min'][i]
            precip = daily['precipitation_sum'][i]
            
            output.append(f"{day_emoji} {date_obj.strftime('%m-%d')} {weekday}")
            output.append(f"   {day_condition}")
            output.append(f"   🌡️  {min_temp}°C ~ {max_temp}°C")
            if precip > 0:
                output.append(f"   🌧️  降水: {precip}mm")
            output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='查询天气信息')
    parser.add_argument('--city', '-c', required=True, help='城市名称')
    parser.add_argument('--days', '-d', type=int, default=1, help='预报天数 (1-16)')
    parser.add_argument('--hourly', action='store_true', help='获取小时级预报')
    parser.add_argument('--aqi', '-a', action='store_true', help='包含空气质量信息')
    parser.add_argument('--json', '-j', action='store_true', help='以JSON格式输出')
    
    args = parser.parse_args()
    
    # Validate days
    if args.days < 1 or args.days > 16:
        print("Error: days must be between 1 and 16")
        sys.exit(1)
    
    # Get coordinates
    location = get_coordinates(args.city)
    if not location:
        sys.exit(1)
    
    # Get weather data
    data = get_weather(
        location['latitude'], 
        location['longitude'],
        days=args.days,
        hourly=args.hourly,
        aqi=args.aqi
    )
    
    if not data:
        sys.exit(1)
    
    # Output
    if args.json:
        result = {
            'location': location,
            'weather': data['weather'],
            'aqi': data.get('aqi')
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_weather(location, data, days=args.days, aqi=args.aqi))


if __name__ == '__main__':
    main()
