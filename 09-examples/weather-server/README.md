# Example 1 — Weather Server (Python)

A simple MCP server that provides current weather information by calling the free [Open-Meteo API](https://open-meteo.com/) (no API key required).

---

## Features

| Tool | Description |
|------|-------------|
| `get_current_weather` | Returns temperature, wind speed, and weather condition for a city |
| `get_forecast` | Returns an hourly forecast for the next N hours |

---

## Setup

```bash
cd 09-examples/weather-server

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### `requirements.txt`

```
mcp>=1.0.0
httpx>=0.27.0
```

---

## Running

```bash
# Start with the MCP Inspector
mcp-inspector python server.py

# Or run directly
python server.py
```

---

## Claude Desktop Config

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/09-examples/weather-server/server.py"]
    }
  }
}
```

---

## Usage in Claude

Once connected, try asking Claude:

> "What is the current weather in Tokyo?"

> "Give me the 12-hour forecast for New York."

---

## How It Works

1. `get_current_weather` uses the Open-Meteo **geocoding API** to convert the city name to latitude/longitude, then calls the **forecast API** to get the current conditions.
2. Weather codes are mapped to human-readable descriptions (e.g., code `61` → "Slight rain").
