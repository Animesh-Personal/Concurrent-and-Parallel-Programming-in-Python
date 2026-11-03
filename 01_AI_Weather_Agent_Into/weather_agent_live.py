from langchain.agents import create_agent
from tools import tools_live
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from utils.agent_utils import invoke_agent

# Initialize the configured chat model
llm = create_llm()

agent = create_agent(
    model=llm, 
    tools=[tools_live.get_weather, tools_live.get_location], 
    system_prompt=SYSTEM_PROMPT
    )

user_query = input("Ask the agent a question: ")
response1 = invoke_agent(agent, user_query)
print(response1['messages'][-1].content)