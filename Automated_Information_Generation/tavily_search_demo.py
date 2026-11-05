from langchain_tavily import TavilySearch
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

query = "coffee health benefits"

tavily_search = TavilySearch(
    max_results=5,
    topic="news",
    search_depth="basic", #User 'advanced' for more in depth search results
    time_range="week",
    include_raw_content=False,
    include_answer=True #AI Generated answers will be included in the results
)

results = tavily_search.invoke(query)
pprint(results)