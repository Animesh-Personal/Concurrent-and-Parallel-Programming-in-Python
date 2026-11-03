from uuid import uuid4

from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from tools import tools_mock
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from utils.agent_utils import invoke_agent
from sqlite.show_sqlite_conversation import print_conversation

# Initialize the configured chat model
llm = create_llm()
thread_id = str(uuid4())

print(f"Thread ID: {thread_id}")

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    agent = create_agent(
        model = llm,
        tools = [tools_mock.get_weather, tools_mock.get_location],
        system_prompt = SYSTEM_PROMPT,
        checkpointer = checkpointer
        )

    while True:
        user_query = input("Ask the agent a question: ")

        if user_query.lower() in ["exit", "quit","bye"]:
            break
        else:
            response = invoke_agent(agent, user_query, thread_id=thread_id)

            #--NOTE: To get access to conversation history, pulled out of database--#
            #(Format might change depending on the model used, so check the response object for the correct format)
            # for i in response['messages']:
            #     print(i.content)

            #--NOTE: To retrieve the last n message from the agent's response--#
            # n = 5
            # messages = response['messages'][-n:]
            # for message in messages:
            #     print(f"{message.content}")

            print(response['messages'][-1].text)
print("\n******************Conversation history for the thread********************\n")
print_conversation(thread_id, db_path="checkpoints.db")