from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from tools import tools_mock
from prompts import SYSTEM_PROMPT
import os
from config.model_config import create_llm
from utils.agent_utils import invoke_agent

DB_URI = os.getenv("SUPABASE_DB_URI")

# Initialize the configured chat model
llm = create_llm()

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent(
        model = llm,
        tools = [tools_mock.get_weather, tools_mock.get_location],
        system_prompt = SYSTEM_PROMPT,
        checkpointer = checkpointer
        )

    while True:
        #---Making using of thread for memory to act, this time it's going to be persistent---#
        user_query = input("Ask the agent a question: ")

        if user_query.lower() in ["exit", "quit","bye"]:
            break
        else:
            response = invoke_agent(agent, user_query, thread_id="1")
            print(response['messages'][-1].content)
