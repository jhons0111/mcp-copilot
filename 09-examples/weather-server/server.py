"""
Weather MCP Server
Provides current weather and forecasts using the free Open-Meteo API.
No API key required.
"""

import json
import sys
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

# ─── Helpers ──────────────────────────────────────────────────────────────────

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


async def _geocode(city: str) -> tuple[float, float]:
    """Return (latitude, longitude) for a city name."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(GEOCODING_URL, params={"name": city, "count": 1, "language": "en", "format": "json"})
        resp.raise_for_status()
        data = resp.json()

    results = data.get("results")
    if not results:
        raise ValueError(f"City not found: {city!r}")

    return results[0]["latitude"], results[0]["longitude"]


async def _fetch_forecast(lat: float, lon: float) -> dict[str, Any]:
    """Fetch forecast data from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weathercode",
        "hourly": "temperature_2m,wind_speed_10m,weathercode",
        "forecast_days": 1,
        "timezone": "auto",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(FORECAST_URL, params=params)
        resp.raise_for_status()
        return resp.json()


# ─── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """
    Return the current temperature, wind speed, and weather condition for a city.

    Args:
        city: Name of the city (e.g. 'Tokyo', 'New York', 'London').
    """
    try:
        lat, lon = await _geocode(city)
        data = await _fetch_forecast(lat, lon)
        current = data["current"]
        code = current.get("weathercode", -1)
        condition = WMO_CODES.get(code, f"Unknown (code {code})")

        result = {
            "city": city,
            "temperature_celsius": current["temperature_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "condition": condition,
        }
        return json.dumps(result, indent=2)
    except ValueError as exc:
        return f"Error: {exc}"
    except httpx.HTTPError as exc:
        return f"HTTP error fetching weather: {exc}"


@mcp.tool()
async def get_forecast(city: str, hours: int = 6) -> str:
    """
    Return an hourly weather forecast for a city.

    Args:
        city:  Name of the city.
        hours: Number of hours to forecast (1–24, default 6).
    """
    if not 1 <= hours <= 24:
        return "Error: hours must be between 1 and 24"

    try:
        lat, lon = await _geocode(city)
        data = await _fetch_forecast(lat, lon)
        hourly = data["hourly"]
        times = hourly["time"][:hours]
        temps = hourly["temperature_2m"][:hours]
        winds = hourly["wind_speed_10m"][:hours]
        codes = hourly["weathercode"][:hours]

        forecast = [
            {
                "time": t,
                "temperature_celsius": temp,
                "wind_speed_kmh": wind,
                "condition": WMO_CODES.get(code, f"code {code}"),
            }
            for t, temp, wind, code in zip(times, temps, winds, codes)
        ]

        return json.dumps({"city": city, "forecast": forecast}, indent=2)
    except ValueError as exc:
        return f"Error: {exc}"
    except httpx.HTTPError as exc:
        return f"HTTP error fetching forecast: {exc}"


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
