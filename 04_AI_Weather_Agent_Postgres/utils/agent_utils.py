from typing import Any

from langchain_core.runnables import Runnable


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
