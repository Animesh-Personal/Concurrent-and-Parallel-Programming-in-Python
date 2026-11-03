# AI Agent Weather Assistant

This project is a Python web app that wraps a LangChain/LangGraph weather agent in a Flask interface. It uses OpenAI models for conversational reasoning and OpenWeatherMap for live weather data. The app also captures browser geolocation, resolves city context when needed, and maintains conversation state across requests using a SQLite-backed checkpoint store.

## Features

- Conversational weather assistant powered by LangChain agents
- OpenAI model integration using `ChatOpenAI`
- Tool-calling workflow for:
  - resolving user location
  - fetching weather for a city
- Browser geolocation support with a fallback location lookup flow
- Session-aware chat using `LangGraph` SQLite checkpoints
- Lightweight Flask UI for interacting with the agent

## Project structure

- `web_app.py` – Flask application entry point
- `weather_agent.py` – LangGraph agent setup and tool wiring
- `config/model_config.py` – LLM configuration and environment validation
- `tools/tools_live.py` – weather and location tool implementations
- `prompts/system_prompt.txt` – agent behavior rules
- `templates/chat.html` – chat UI
- `sqlite/checkpoints.db` – LangGraph checkpoint database
- `.env` – runtime environment variables

## Prerequisites

- Python 3.11
- Access to an OpenAI-compatible API endpoint
- OpenWeatherMap API key

## Setup

1. Create and activate a virtual environment in PowerShell:

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the required values:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE_URL=https://your-openai-endpoint/v1
OPENAI_MODEL_NAME=gpt-4o-mini
OPENWEATHER_API_KEY=your_openweather_api_key
```

4. Update the Flask secret key in `web_app.py` before running in a non-local environment:

```python
app.secret_key = 'replace_with_a_secure_secret_key'
```

## Run the app

From the project root:

```powershell
python web_app.py
```

Then open the app in a browser at:

```text
http://127.0.0.1:5000/
```

## Example prompts

- `What's the weather in London?`
- `Will it rain today?`
- `How hot is it where I am right now?`

The agent is designed to automatically fetch the user's location when a weather request does not include a city name.

## Notes

- The default app runs in debug mode for local development.
- Checkpoint history is persisted in the SQLite database under `sqlite/checkpoints.db`.
- The agent is configured to use the OpenAI `gpt-4o-mini` model by default, but this can be changed via `OPENAI_MODEL_NAME` in `.env`.

