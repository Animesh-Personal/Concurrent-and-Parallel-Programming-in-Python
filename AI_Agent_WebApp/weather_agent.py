from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from prompts import SYSTEM_PROMPT
from config.model_config import create_llm
from tools import tools_live

# Initialize OpenAI GPT-4o-mini, LLM Object
llm = create_llm()

connection = SqliteSaver.from_conn_string("sqlite/checkpoints.db")
checkpointer = connection.__enter__()

agent = create_agent(
        model=llm,
        tools=[tools_live.get_weather, tools_live.get_location],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )
