import os
from dotenv import load_dotenv
from langchain_openai import OpenAI

load_dotenv()  # This loads variables from .env

llm = OpenAI(
    model_name=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    temperature=0
)
