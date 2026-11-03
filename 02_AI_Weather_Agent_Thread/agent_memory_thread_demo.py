from langchain.agents import create_agent
#--Enable Memory--#
from langgraph.checkpoint.memory import InMemorySaver
from tools import tools_mock
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from utils.agent_utils import invoke_agent

# Initialize the configured chat model
llm = create_llm()

#---Here agent is just one object, but it can handle multiple conversations with different thread_id---#
agent = create_agent(
    model = llm,
    tools = [tools_mock.get_weather, tools_mock.get_location],
    system_prompt = SYSTEM_PROMPT,
    checkpointer = InMemorySaver()
    )

#---Here we are making using of thread for memory to act---#
print("First Conversation")
user_query1 = input("Ask the agent a question: ")
response1 = invoke_agent(agent, user_query1, thread_id="1")
print(response1['messages'][-1].text)

#---Response connected via same thread_id, so the agent can remember the previous conversation---#
print("Second Conversation")
user_query2 = input("Ask the agent a question: ")
response2 = invoke_agent(agent, user_query2, thread_id="1")
print(response2['messages'][-1].text)

print("Third Conversation")
user_query3 = input("Ask the agent a question: ")
response3 = invoke_agent(agent, user_query3, thread_id="2")
print(response3['messages'][-1].text)

'''
NOTE:
1. Examining variables like response1 and response2 is useful when understanding agent memory as 
it reveals how conversation history and context are persisted across turns.
'''