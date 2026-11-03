# AI Agent Memory

This project demonstrates a LangChain/LangGraph agent that uses tool calling and thread-based conversation memory. It is built around a weather assistant that can answer location-aware questions while keeping separate conversation state for different `thread_id` values.

## What this project includes

- OpenAI-backed LLM configuration using `langchain-openai`
- A simple tool-calling weather agent with mock tools
- In-memory conversation memory with `InMemorySaver`
- A reusable helper for invoking the agent with a `thread_id`

## Project structure

- `agent_memory_thread_demo.py` – demonstrates how the same agent can handle multiple conversations using different thread IDs
- `interactive_agent_memory_chat.py` – interactive terminal chat with in-memory conversation tracking
- `config/model_config.py` – loads the OpenAI environment variables
- `prompts/system_prompt.txt` – system instructions for the weather assistant
- `tools/tools_mock.py` – mock tools used by the agent
- `utils/agent_utils.py` – helper for invoking the agent with a thread ID
- `requirements.txt` – project dependencies

## Environment setup

This project expects the following environment variables to be defined in a `.env` file:

```env
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE_URL=https://your-openai-endpoint/v1
OPENAI_MODEL_NAME=gpt-4o-mini
```

## Running the examples

Run the thread-memory demo:

```powershell
python agent_memory_thread_demo.py
```

Run the interactive chat demo:

```powershell
python interactive_agent_memory_chat.py
```

## Example interactions

The agent is configured to behave as a weather assistant:

- If the user asks for weather in a city, it calls `get_weather(city)` directly.
- If the user asks for weather without naming a city, it first calls `get_location()` and then `get_weather(location)`.

Example prompts:

- `What is the weather in Paris?`
- `What is the weather like today?`

## Notes

- The project uses a mock weather tool and mock location lookup rather than a real weather API.
- The memory is in-memory only, so the conversation state is not persisted across program restarts.
- The agent uses `thread_id` to keep conversations separated while still preserving context within the same thread.
