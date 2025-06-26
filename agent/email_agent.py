from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.llm import llm
from src.memory import get_session_memory
from src.prompt import email_prompt

# creating a reactive agent to ask questions when needed
agent = RunnableWithMessageHistory(
    runnable = email_prompt | llm,
    get_session_history = get_session_memory,
    input_messages_key = "user_input",
    history_messages_key = "history"
)

# fetch response from llm by invoking it
def get_email_response(user_input, session_id):
    return agent.invoke(
        {"user_input": user_input},
        config=RunnableConfig(configurable = {"session_id": session_id})
    )