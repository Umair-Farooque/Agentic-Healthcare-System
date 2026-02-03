import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Initialize the Chat Model
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    temperature=0
)
