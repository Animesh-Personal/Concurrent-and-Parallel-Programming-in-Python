from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

queries = ["coffee health benefits", 
        "organic coffee benefits studies",
        "coffee antioxidants wellness",
        ]

def search_for_articles(queries):
    tavily_search = TavilySearch(
        max_results=5,
        topic="news",
        search_depth="basic",  #User 'advanced' for more in depth search results
        time_range="week",
        include_raw_content=False, #False to manage context window efficiently
        include_answer=False  # False to manage context window efficiently
    )
    all_results = []
    for query in queries:
        results = tavily_search.invoke(query)
        all_results.append(results)

    return all_results

def generate_newsletter(search_results):

    # 1. Read environment variables
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_base_url = os.getenv("OPENAI_API_BASE_URL")

    # 2. Build model kwargs
    model_kwargs = {
        "model": openai_model,
        "model_provider": "openai",
        "temperature": 0.7,
        "base_url":openai_base_url
    }

    # 3. Initialize chat model
    chat_model = init_chat_model(**model_kwargs)

    prompt = f"""
    You are a professional newsletter writer for an organic coffee business.
    Below are the search results for this week's coffee news. Each result includes the content and the source url.

    SEARCH RESULTS:
    {search_results}

    Write the article in a markdown format.

    RULES:
    - Focus on the positive news about the coffee.
    - Provide references using the URLs of the SEARCH RESULTS.
    """
    
    response = chat_model.invoke(prompt)

    #NOTE: Sometimes the response content might be a list.
    pprint(response.content)
    
    return response.content

if __name__ == "__main__":
    search_results = search_for_articles(queries)
    article = generate_newsletter(search_results)

    with open("Article.md", "w", encoding="utf-8") as file:
        file.write(article)
    
    print("Article saved to Article.md")