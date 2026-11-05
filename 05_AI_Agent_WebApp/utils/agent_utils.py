from contextlib import contextmanager
from typing import Any, Generator

from langchain_core.runnables import Runnable
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from tools import tools_live



def invoke_agent(
    agent: Runnable[Any, Any],
    user_query: str,
    thread_id: str | None = None,
) -> Any:
    """
    Send a user prompt to a LangChain agent and optionally keep state
    per thread. It wraps the query in the expected message format and 
    invokes the runnable with or without a thread identifier.
    """
    input_data = {"messages": [{"role": "user", "content": user_query}]}
    if thread_id is None:
        return agent.invoke(input_data)

    return agent.invoke(
        input_data,
        {"configurable": {"thread_id": thread_id}},
    )


@contextmanager
def create_agent_instance(
    checkpoint_path: str = "sqlite/checkpoints.db",
) -> Generator[Runnable[Any, Any], None, None]:
    """Create an agent and keep its SQLite checkpointer open while it is in use."""
    with SqliteSaver.from_conn_string(checkpoint_path) as checkpointer:
        yield create_agent(
            model=create_llm(),
            tools=[tools_live.get_weather, tools_live.get_location],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=checkpointer,
        )


agent_context = create_agent_instance()
agent = agent_context.__enter__()
