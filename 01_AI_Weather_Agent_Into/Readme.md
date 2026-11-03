# AI Weather Agent

This project demonstrates a LangChain-based AI agent that can answer weather and location questions using either mock data or live services.

It includes:
- `weather_agent_mock.py` for offline testing with sample responses
- `weather_agent_live.py` for real weather and location lookups
- `tools/tools_mock.py` for mock tool functions
- `tools/tools_live.py` for live API-backed tools

## Features

The agent can handle:
- Weather lookups for a specified city
- Weather queries without a city by detecting the user's current location first
- Location lookup via IP-based geolocation
- Weather responses with useful details such as temperature, humidity, condition, and wind

## Project structure

- `weather_agent_mock.py` — uses mocked weather and location tools
- `weather_agent_live.py` — uses real APIs for weather and location data
- `tools/tools_mock.py` — static demo tools for testing the agent logic
- `tools/tools_live.py` — live OpenWeatherMap and IP geolocation integration
- `.env` — environment variables for API keys and model configuration

## Setup

### 1. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root with the following values:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

`OPENAI_API_KEY`, `OPENAI_MODEL_NAME`, and `OPENAI_API_BASE_URL` must all be set
to non-empty values.

## Run the mock agent

The mock version returns sample data and is useful for testing the agent workflow without external API calls:

```powershell
python weather_agent_mock.py
```

## Run the live agent

The live version calls OpenWeatherMap and IP-based geolocation services:

```powershell
python weather_agent_live.py
```

## Test or debug a tool from the Python console

Start Python from the project root:

```powershell
python
```

To test the mock tools without making external requests:

```pycon
>>> from tools import tools_mock
>>> tools_mock.get_location()
'Rome, Italy'
>>> tools_mock.get_weather("Prayagraj")
'The weather in Prayagraj is sunny with a high of 25°C.'
>>> exit()
```

To test the live tools, make sure `OPENWEATHER_API_KEY` is set in `.env` first.
`get_location()` uses IP-based geolocation, and `get_weather()` makes a request
to OpenWeatherMap:

```pycon
>>> from tools import tools_live
>>> tools_live.get_location()
'Hyderabad, India'
>>> tools_live.get_weather("Prayagraj")
...
>>> exit()
```

The live location output depends on your network. `get_weather()` returns the
weather API response data together with the temperature converted to Fahrenheit.

## Sample inputs for terminal testing

When the script is running, try these prompts:

```text
How is the weather?
Where am I?
How is the weather in Prayagraj?
```

Example interaction:

```powershell
Ask the agent a question: How is the weather?
AI Message: The weather in Hyderabad, India is ...
```

```powershell
Ask the agent a question: Where am I?
AI Message: You are in Hyderabad, India.
```

```powershell
Ask the agent a question: How is the weather in Prayagraj?
AI Message: The weather in Prayagraj is ...
```

## Notes

- If the user asks for the weather without naming a city, the agent first calls `get_location()` and then `get_weather(city)`.
- If a city is explicitly provided, it calls `get_weather(city)` directly.
- `get_location()` depends on your current public IP address, so the returned city may differ between environments.

