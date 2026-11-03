import argparse
import json
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver

DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "checkpoints.db"


def get_conversation(
    thread_id: str,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[BaseMessage]:
    """Return the messages for a thread in chronological order."""
    if not thread_id.strip():
        raise ValueError("thread_id must not be empty.")

    database_path = Path(db_path)
    if not database_path.is_file():
        raise FileNotFoundError(f"Checkpoint database not found: {database_path}")

    config = {"configurable": {"thread_id": thread_id}}
    with SqliteSaver.from_conn_string(str(database_path)) as checkpointer:
        checkpoint = next(checkpointer.list(config), None)

    if checkpoint is None:
        raise ValueError(f"No checkpoints found for thread_id {thread_id!r}.")

    messages = checkpoint.checkpoint.get("channel_values", {}).get("messages", [])
    if not messages:
        raise ValueError(f"No conversation messages found for thread_id {thread_id!r}.")

    return messages


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and isinstance(block.get("text"), str)
        )
    return str(content)


def print_conversation(
    thread_id: str,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> None:
    """Print a thread's human, assistant, and tool messages in order."""
    for message in get_conversation(thread_id, db_path):
        if isinstance(message, HumanMessage):
            print(f"[Human] {_content_text(message.content)}")
        elif isinstance(message, AIMessage):
            for tool_call in message.tool_calls:
                arguments = json.dumps(tool_call["args"], ensure_ascii=False)
                print(f"[AI -> {tool_call['name']}] {arguments}")

            text = _content_text(message.content)
            if text:
                print(f"[AI] {text}")
        elif isinstance(message, ToolMessage):
            print(f"[Tool: {message.name}] {_content_text(message.content)}")
        else:
            print(f"[{message.type}] {_content_text(message.content)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display the conversation stored for a SQLite checkpoint thread."
    )
    parser.add_argument("thread_id", help="The conversation's LangGraph thread ID.")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Checkpoint database path (default: {DEFAULT_DB_PATH})",
    )
    args = parser.parse_args()

    try:
        print_conversation(args.thread_id, args.db)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    #python .\sqlite\show_sqlite_conversation.py 3ca62880-7cf4-4bf8-a1f1-4a49c24691de
    main()
