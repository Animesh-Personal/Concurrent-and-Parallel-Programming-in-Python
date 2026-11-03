import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def create_llm() -> ChatOpenAI:
    model_name = os.getenv("OPENAI_MODEL_NAME")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE_URL")
    missing_variables = [
        name
        for name, value in (
            ("OPENAI_MODEL_NAME", model_name),
            ("OPENAI_API_KEY", api_key),
            ("OPENAI_API_BASE_URL", base_url),
        )
        if value is None or not value.strip()
    ]
    if missing_variables:
        variables = ", ".join(missing_variables)
        raise ValueError(
            f"Required environment variable(s) are missing or empty: {variables}"
        )

    return ChatOpenAI(
        model=model_name.strip(),
        temperature=0.7,
        base_url=base_url.strip(),
        api_key=api_key.strip(),
    )
