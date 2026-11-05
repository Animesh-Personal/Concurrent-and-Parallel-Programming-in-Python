from langchain_tavily import TavilySearch

QUERIES = [
    "coffee health benefits",
    "organic coffee benefits studies",
    "coffee antioxidants wellness",
]


def search_for_articles(queries):
    tavily_search = TavilySearch(
        max_results=5,
        topic="news",
        search_depth="basic",
        time_range="week",
        include_raw_content=False,
        include_answer=False,
    )
    return [tavily_search.invoke(query) for query in queries]
