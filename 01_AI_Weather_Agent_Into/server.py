"""MCP server for the live weather and location tools.

Stdio is the default transport, which is what MCP Inspector launches:

    python server.py

Streamable HTTP listens on http://127.0.0.1:8000/mcp:

    python server.py --transport streamable-http
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from tools.tools_live import get_location as fetch_location
from tools.tools_live import get_weather as fetch_weather

logger = logging.getLogger("weather_mcp")

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=True)

mcp = MCPServer(
    "Weather Agent",
    instructions=(
        "Live weather and location tools. Call get_location when the user "
        "does not name a city, then pass that city to get_weather. "
        "get_weather needs OPENWEATHER_API_KEY in the project .env file. "
        "Read location://current, weather://{city}, weather://units, "
        "prompt://weather-assistant, and doc://mcp-inspector for context."
    ),
    # mcp dev installs these into a fresh uv env, then runs `mcp run`.
    # That command needs typer, which ships only with the mcp[cli] extra.
    dependencies=["requests", "python-dotenv", "typer"],
)


def _weather_payload(city: str) -> dict[str, Any]:
    weather, converted = fetch_weather(city)
    if not isinstance(weather, dict) or "main" not in weather:
        message = "Weather lookup failed."
        if isinstance(weather, dict) and weather.get("message"):
            message = str(weather["message"])
        raise RuntimeError(message)
    return {
        "city": city,
        "weather": weather,
        "temperature_fahrenheit": converted["temperature_fahrenheit"],
    }


@mcp.tool(
    title="Get weather",
    annotations=READ_ONLY,
)
def get_weather(city: str) -> str:
    """Fetch live weather for a city from OpenWeatherMap.

    The raw temperatures are Celsius. The result also includes
    temperature_fahrenheit for locations that use Fahrenheit, such as
    the US, Liberia, and Burma. Requires OPENWEATHER_API_KEY.
    """
    city = city.strip()
    if not city:
        raise ValueError("city is required")

    try:
        payload = _weather_payload(city)
    except KeyError as exc:
        raise RuntimeError(
            f"OpenWeatherMap did not return weather for {city!r}. "
            "The city may be unknown to that API, or OPENWEATHER_API_KEY may be invalid."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Weather request failed: {exc}") from exc

    logger.info("Fetched weather for %s", city)
    return json.dumps(payload, indent=2)


@mcp.tool(
    title="Get location",
    annotations=READ_ONLY,
)
def get_location() -> str:
    """Detect the current city and country from this machine's public IP address."""
    try:
        location = fetch_location()
    except KeyError as exc:
        raise RuntimeError("Location lookup failed. The IP geolocation service did not return a city.") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Location request failed: {exc}") from exc

    logger.info("Resolved location to %s", location)
    return location


UNITS_TEXT = """\
Temperatures in the OpenWeatherMap payload are Celsius because the live tool requests units=metric.
main.temp, main.feels_like, main.temp_min, and main.temp_max are all Celsius.
temperature_fahrenheit is the converted value of main.temp, for places that use Fahrenheit such as the US, Liberia, and Burma.
Conversion: fahrenheit = (celsius * 9/5) + 32.
"""


def _read_project_file(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Missing project file: {relative_path}")
    return path.read_text(encoding="utf-8")


@mcp.resource(
    "location://current",
    name="current_location",
    title="Current location",
    description="City and country detected from this machine's public IP address.",
    mime_type="text/plain",
)
def current_location() -> str:
    """Read the current city and country."""
    return get_location()


@mcp.resource(
    "weather://{city}",
    name="city_weather",
    title="City weather",
    description="Live OpenWeatherMap payload for a city, plus temperature_fahrenheit.",
    mime_type="application/json",
)
def city_weather(city: str) -> str:
    """Read live weather for one city. Prayagraj is listed as Allahabad."""
    return get_weather(city)


@mcp.resource(
    "weather://units",
    name="weather_units",
    title="Weather units",
    description="How to read Celsius fields and temperature_fahrenheit in a weather payload.",
    mime_type="text/plain",
)
def weather_units() -> str:
    """Explain the temperature units returned by the weather tool."""
    return UNITS_TEXT


@mcp.resource(
    "prompt://weather-assistant",
    name="weather_assistant_prompt",
    title="Weather assistant workflow",
    description="System prompt that decides when to call get_location and get_weather.",
    mime_type="text/plain",
)
def weather_assistant_prompt() -> str:
    """Read prompts/system_prompt.txt."""
    return _read_project_file("prompts/system_prompt.txt")


@mcp.resource(
    "doc://mcp-inspector",
    name="mcp_inspector_guide",
    title="MCP Inspector guide",
    description="How to connect MCP Inspector to this server and use its tools and resources.",
    mime_type="text/markdown",
)
def mcp_inspector_guide() -> str:
    """Read doc/mcp-inspector.md."""
    return _read_project_file("doc/mcp-inspector.md")


def init() -> None:
    parser = argparse.ArgumentParser(description="Run the weather MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="MCP transport. Use stdio for MCP Inspector's command launch.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address for HTTP transports.")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transports.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(name)s: %(message)s")

    logger.info("🌤️ Weather MCP Server started")
    logger.info("🛠️ Tools: get_weather, get_location")
    logger.info("🗺️ Resources: location://current, weather://units, prompt://weather-assistant, doc://mcp-inspector")
    logger.info("🏙️ Resource template: weather://{city} for any city OpenWeatherMap recognizes")
    if args.transport == "stdio":
        logger.info("🔌 Transport: stdio")
    elif args.transport == "sse":
        logger.info("🔌 Transport: sse at http://%s:%s/sse", args.host, args.port)
    else:
        logger.info("🔌 Transport: streamable-http at http://%s:%s/mcp", args.host, args.port)
    logger.info("✅  Server ready")

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="streamable-http", host=args.host, port=args.port, json_response=True)


if __name__ == "__main__":
    init()
