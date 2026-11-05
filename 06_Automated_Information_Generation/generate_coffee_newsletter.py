from pathlib import Path
from pprint import pprint

from config.model_config import chat_model
from tavilysearch import QUERIES, search_for_articles

def generate_newsletter(search_results):
    prompt_path = Path(__file__).resolve().parent / "prompt" / "prompt.txt"
    prompt_template = prompt_path.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{SEARCH_RESULTS}}", str(search_results))
    
    response = chat_model.invoke(prompt)

    #NOTE: Sometimes the response content might be a list. It may also vary based on the model used. Adjust the code accordingly if needed.
    pprint(response.content)
    
    return response.content

if __name__ == "__main__":
    search_results = search_for_articles(QUERIES)
    article = generate_newsletter(search_results)

    with open("Article.md", "w", encoding="utf-8") as file:
        file.write(article)
    
    print("Article saved to Article.md")