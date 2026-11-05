# AI Agent Weather Assistant

A Flask chat application backed by a LangChain/LangGraph weather agent. The
agent uses an OpenAI-compatible chat model and OpenWeatherMap to answer weather
questions. It can use browser-provided coordinates to identify the user's city
for location-based requests, and LangGraph persists conversation state in
SQLite.

## Features

- Chat interface rendered with Flask and Jinja2.
- Weather and location tools wired into a LangChain agent.
- Browser geolocation submitted with chat messages and reverse-geocoded with
  OpenStreetMap Nominatim.
- Separate agent conversation state per Flask session, identified by a
  `thread_id` and saved in a SQLite checkpoint database.
- Configurable model, API key, and API endpoint through environment variables.

## Project structure

- `weather_app.py` – main Flask application entry point.
- `flask_demo.py` – minimal Flask demo; it does not run the weather agent.
- `utils/agent_utils.py` – agent creation and the `invoke_agent` helper.
- `config/model_config.py` – validates model settings and creates the chat model.
- `tools/tools_live.py` – OpenWeatherMap weather lookup and location
  reverse-geocoding tools.
- `prompts/system_prompt.txt` – agent instructions; `prompts/__init__.py`
  loads them as `SYSTEM_PROMPT`.
- `templates/chat.html` – chat interface and browser geolocation code.
- `.env_example` – template for required environment variables.
- `sqlite/checkpoints.db` – default SQLite checkpoint database, created or used
  by the agent.

## Prerequisites

- Python 3.11 or newer.
- An OpenAI-compatible chat model endpoint and API key.
- An OpenWeatherMap API key.

## Setup

1. From the project directory, create and activate a virtual environment in
   PowerShell:

   ```powershell
   py -m venv .venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Create a local `.env` file from the example:

   ```powershell
   Copy-Item .env_example .env
   ```

   Set all four values in `.env`:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_API_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL_NAME=your-model-name
   OPENWEATHER_API_KEY=your-openweather-api-key
   ```

   `OPENAI_API_BASE_URL` and `OPENAI_MODEL_NAME` are required; the model name
   does not have a code-defined default. Use the base URL and model name
   appropriate for your OpenAI-compatible provider.

4. Before exposing the app beyond local development, replace the placeholder
   Flask session secret in `weather_app.py` with a secure secret key.

## Run

Start the application from the project directory:

```powershell
python weather_app.py
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a browser. The app
runs with Flask debug mode enabled, so use a production WSGI server and disable
debug mode when deploying.

## Using the assistant

Try prompts such as:

- `What's the weather in London?`
- `Will it rain today?`
- `How hot is it where I am right now?`

When a weather question has no city, the system prompt directs the agent to call
the location tool first and then look up that city's weather. The browser asks
for geolocation permission and submits coordinates with the chat form; location
requests require permission and a supported browser.

## Creating another agent

`create_agent_instance` is a context manager. It keeps the SQLite checkpointer
open while the agent is in use, and lets you select a different checkpoint path:

```python
from utils.agent_utils import create_agent_instance, invoke_agent

with create_agent_instance("sqlite/another-checkpoint.db") as agent:
    response = invoke_agent(agent, "What's the weather in Paris?", "thread-123")
```

The Flask application uses a module-level agent from `utils/agent_utils.py` and
passes the Flask session's `thread_id` to `invoke_agent` for each message.
Checkpoint state is persisted in `sqlite/checkpoints.db` by default.
