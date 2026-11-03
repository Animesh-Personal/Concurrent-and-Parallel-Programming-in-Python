# AI Weather Agent with SQLite Memory

This project demonstrates a LangChain/LangGraph-based weather assistant that uses an OpenAI chat model and SQLite-backed checkpoint memory to persist conversation state across turns.

## What this project includes

- OpenAI-backed LLM configuration using `langchain-openai`
- A tool-calling weather agent built with LangChain/LangGraph
- SQLite checkpoint persistence using `SqliteSaver`
- Mock weather and location tools for local development
- A reusable helper for invoking the agent with a thread ID

## Project structure

- `interactive_sqlite_checkpoint_chat.py` – interactive chat with SQLite-backed conversation memory
- `sqlite/show_sqlite_conversation.py` – displays a saved conversation by thread ID and exposes reusable retrieval/printing functions
- `config/model_config.py` – loads environment variables and creates the chat model
- `prompts/__init__.py` – prompt configuration for the weather assistant
- `tools/tools_mock.py` – mock tools used by the agent
- `utils/agent_utils.py` – helper used to invoke the agent with a `thread_id`
- `checkpoints.db` – SQLite database storing agent checkpoint history
- `checkpoints.db-x-checkpoints-*.bin` – companion binary files containing serialized checkpoint data
- `checkpoints.db-x-writes-*.bin` – companion binary files containing serialized checkpoint writes, such as messages and tool results
- `requirements.txt` – project dependencies

## Environment setup

Create a `.env` file in the project root with the following values:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE_URL=https://your-openai-endpoint/v1
OPENAI_MODEL_NAME=gpt-4o-mini
```

Notes:
- The project currently uses the SQLite checkpoint pattern only.
- No PostgreSQL or Supabase configuration is required for the default workflow.

## Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app

Start the interactive SQLite-backed weather agent:

```powershell
python interactive_sqlite_checkpoint_chat.py
```

The app generates and prints a UUID thread ID at startup. It uses that same ID for the entire chat and displays the saved conversation when you exit.

Display a saved conversation by passing its thread ID:

```powershell
python .\sqlite\show_sqlite_conversation.py 3ca62880-7cf4-4bf8-a1f1-4a49c24691de
```

The conversation functions can also be imported from other Python code:

```python
from sqlite import get_conversation, print_conversation

messages = get_conversation("3ca62880-7cf4-4bf8-a1f1-4a49c24691de")
print_conversation("3ca62880-7cf4-4bf8-a1f1-4a49c24691de")
```

## Example interactions

The agent behaves like a weather assistant:

- If the user asks for weather in a city, it calls `get_weather(city)` directly.
- If the user asks for weather without specifying a location, it first calls `get_location()` and then `get_weather(location)`.

Example prompts:

- `What is the weather in Paris?`
- `What is the weather like today?`
- `Tell me the weather in Tokyo and compare it to London.`

## Notes

- The project uses mock tools instead of a real weather API.
- Conversation state is persisted in the local SQLite database `checkpoints.db`.
- The database may have companion `checkpoints.db-x-*.bin` files. They hold serialized checkpoint and write data; keep them alongside `checkpoints.db`, and include them together in backups. Do not delete them manually while using or preserving the database.
- Each app run gets a new `thread_id`, separating it from conversations saved by earlier runs.
- This project is intentionally focused on the SQLite checkpoint-based memory pattern and does not include separate PostgreSQL examples.
