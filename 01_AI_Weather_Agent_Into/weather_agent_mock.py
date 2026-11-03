from langchain.agents import create_agent
from tools import tools_mock
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from utils.agent_utils import invoke_agent

# Initialize the configured chat model
llm = create_llm()

agent = create_agent(
    model=llm, 
    tools=[tools_mock.get_weather, tools_mock.get_location], 
    system_prompt=SYSTEM_PROMPT
    )

#response1 = llm.invoke("How is the weather in Rome?")
#----Below will give an error as agent.invoke doesn't expect string input----#
#response1 = agent.invoke("How is the weather in Rome?")
#print(response1.content)

user_query = input("Ask the agent a question: ")
response1 = invoke_agent(agent, user_query)
print(f"AI Message: {response1['messages'][-1].content}")