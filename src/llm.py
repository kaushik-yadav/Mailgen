from langchain_openai import ChatOpenAI

from config import MODEL, TOGETHER_API_BASE, TOGETHER_API_KEY

if not TOGETHER_API_KEY:
    raise ValueError("Please set the TOGETHER_API_KEY environment variable.")

# main llm initiation with credentials
llm = ChatOpenAI(
    openai_api_key = TOGETHER_API_KEY,
    openai_api_base = TOGETHER_API_BASE,
    model_name = MODEL,
    temperature = 0.4
)