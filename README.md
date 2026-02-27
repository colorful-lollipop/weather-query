# Weather Query Skill

一个用于 Kimi Code CLI 的天气查询 Skill，支持全球城市天气查询和预报。

## 功能特点

- 🌍 **全球覆盖** - 支持世界任何城市的天气查询
- 🆓 **完全免费** - 使用 Open-Meteo API，无需 API Key
- 📅 **多日预报** - 支持最多 16 天的天气预报
- 🌬️ **空气质量** - 支持查询空气质量指数 (AQI)
- 🕐 **小时预报** - 支持小时级天气数据
- 🌐 **多语言** - 支持中英文城市名称查询

## 安装

将此 skill 目录复制到 Kimi CLI 的 skills 目录：

```bash
# 默认 skills 目录位置
~/.local/share/uv/tools/kimi-cli/lib/python3.13/site-packages/kimi_cli/skills/
```

## 使用方法

### 作为 Kimi CLI Skill 使用

安装后，Kimi 会自动识别天气相关的查询请求：

- "北京今天天气怎么样？"
- "查询上海的天气预报"
- "纽约未来一周天气"

### 直接使用脚本

```bash
# 当前天气
python scripts/weather.py --city "北京"

# 7天预报
python scripts/weather.py --city "上海" --days 7

# 带空气质量
python scripts/weather.py --city "广州" --aqi

# JSON 输出
python scripts/weather.py --city "深圳" --days 3 --json
```

## 技术说明

### API 来源

- **天气数据**: [Open-Meteo](https://open-meteo.com/) - 免费开源天气 API
- **地理编码**: Open-Meteo Geocoding API
- **空气质量**: Open-Meteo Air Quality API

### 天气代码对照

| 代码 | 天气状况 |
|------|----------|
| 0 | 晴朗 ☀️ |
| 1-3 | 多云 ⛅ |
| 45, 48 | 雾 🌫️ |
| 51-55 | 毛毛雨 🌦️ |
| 61-65 | 雨 🌧️ |
| 71-77 | 雪 🌨️ |
| 80-82 | 阵雨 🌧️ |
| 95-99 | 雷雨 ⛈️ |

## 示例输出

```
🌤️ 北京当前天气
━━━━━━━━━━━━━━━━━━━
🌡️ 温度: 22°C (体感 24°C)
☁️ 天气: 多云
💧 湿度: 65%
💨 风速: 12 km/h
🌬️ 空气质量: 🟡 良 (AQI: 85)
   PM2.5: 35 μg/m³
━━━━━━━━━━━━━━━━━━━

📅 未来 7 天预报:
──────────────────────────────
🌤️ 02-27 周四
   多云
   🌡️  8°C ~ 18°C

☀️ 02-28 周五
   晴朗
   🌡️  10°C ~ 20°C
```

## 许可证

MIT License
