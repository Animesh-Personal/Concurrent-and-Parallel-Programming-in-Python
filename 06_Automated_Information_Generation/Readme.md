# Coffee Newsletter Generator

This application searches for recent coffee news with Tavily and uses a
configured chat model to generate a Markdown newsletter saved as `Article.md`.

## Project structure

- `generate_coffee_newsletter.py` runs the search and newsletter-generation workflow.
- `config/model_config.py` configures the shared chat model from environment variables.
- `tavilysearch/` contains the Tavily search configuration, default queries, and search function.
- `prompt/prompt.txt` contains the newsletter prompt. The `{{SEARCH_RESULTS}}` placeholder is replaced with search results.
- `requirements.txt` lists the Python dependencies.

## Setup

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Copy `.env_example` to `.env` and set your API credentials and model settings:

```powershell
Copy-Item .env_example .env
```

Set these values in `.env`:

- `OPENAI_API_KEY` — API key used by the chat model.
- `OPENAI_API_BASE_URL` — API base URL for the chat model provider.
- `OPENAI_MODEL` — model name.
- `TAVILY_API_KEY` — Tavily API key.

## Run

```powershell
python generate_coffee_newsletter.py
```

The generated newsletter is written to `Article.md` in the current working
directory.
