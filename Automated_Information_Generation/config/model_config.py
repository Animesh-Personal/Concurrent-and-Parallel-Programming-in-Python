import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# 1. Read environment variables
openai_model = os.getenv("OPENAI_MODEL")
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