from langchain.agents import create_agent
#--Provide In-Memory STORAGE and CHECKPOINT capabilities to the agent--#
from langgraph.checkpoint.memory import InMemorySaver
from tools import tools_mock
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from utils.agent_utils import invoke_agent

# Initialize the configured chat model
llm = create_llm()

agent = create_agent(
    model = llm,
    tools = [tools_mock.get_weather, tools_mock.get_location],
    system_prompt = SYSTEM_PROMPT,
    checkpointer = InMemorySaver()
    )

while True:
    #---Making using of thread for memory to act, but it's not going to be persistent---#
    user_query = input("Ask the agent a question: ")

    if user_query.lower() in ["exit", "quit","bye"]:
        break
    else:
        response = invoke_agent(agent, user_query, thread_id="1")
        print(response['messages'][-1].text)
