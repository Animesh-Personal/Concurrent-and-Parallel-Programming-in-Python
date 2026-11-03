# AI Weather Agent with PostgreSQL

This project demonstrates a LangChain weather agent with mock weather tools and persistent conversation checkpoints stored in PostgreSQL.

## Project structure

- `interactive_postgres_checkpoint_chat.py` – starts the interactive agent and configures PostgreSQL-backed checkpoints.
- `config/model_config.py` – loads the model settings and creates the OpenAI-compatible chat model.
- `prompts/system_prompt.txt` – tells the agent when to use the weather and location tools.
- `tools/tools_mock.py` – provides mock weather and location tools.
- `utils/agent_utils.py` – invokes the agent, optionally with a conversation thread ID.
- `postgresDB/check_connection.py` – checks that the configured PostgreSQL database is reachable.
- `requirements.txt` – lists the project's Python dependencies.

## Configuration

Create a `.env` file in the project root and set the following values:

```env
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE_URL=https://your-openai-compatible-endpoint/v1
OPENAI_MODEL_NAME=your_model_name
SUPABASE_DB_URI=postgresql://user:password@host:5432/database
```

`OPENAI_API_BASE_URL` should point to an OpenAI-compatible API. `SUPABASE_DB_URI` should be a PostgreSQL connection URI; the example uses Supabase, but another PostgreSQL service can be used. Keep real credentials out of source control.

## Install dependencies

From the project root, run:

```powershell
python -m pip install -r requirements.txt
```

## Run

Optionally verify the database connection:

```powershell
python postgresDB/check_connection.py
```

Start the interactive weather agent:

```powershell
python interactive_postgres_checkpoint_chat.py
```

On startup, the application initializes the PostgreSQL checkpoint tables. The database user must have permission to create and use them. Enter `exit`, `quit`, or `bye` to end the chat.

## Behavior and persistence

- If a question names a city, the agent calls `get_weather(city)`.
- If no city is specified, the agent calls `get_location()` first and then `get_weather(location)`.
- Both tools return mock data; no live weather or location service is queried.
- The chat uses the thread ID `1`, so messages in that thread share checkpointed conversation state across runs.

## Dependencies

All packages listed in `requirements.txt` are used directly by the project: LangChain for agent creation, LangChain OpenAI for the chat model, LangGraph's PostgreSQL checkpointer for persistence, `psycopg` for PostgreSQL connectivity, and `python-dotenv` for loading configuration.
