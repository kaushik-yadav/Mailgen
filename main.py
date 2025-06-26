import os

from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# setting up credentials and configs
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
TOGETHER_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.together.xyz/v1")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise ValueError("Please set the TOGETHER_API_KEY environment variable.")

# main llm initiation with credentials
llm = ChatOpenAI(
    openai_api_key=TOGETHER_API_KEY,
    openai_api_base=TOGETHER_API_BASE,
    model_name=MODEL,
    temperature=0.4
)

# prompt template
email_prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a smart, reactive email assistant for non-native English speakers.
        - **STRICTLY** : Never generate an email unless you have: recipient name, reason, and timeframe (days or dates).
        - Ask one short follow-up question at a time with no extra text.
        - Remember user responses across turns; don’t repeat questions.
        - Only write the email when all info is available or the user explicitly asks.
        - Adjust tone based on input: polite (requests), apologetic (apologies), follow-up (reminders), or neutral (unclear).
        - Match formal/informal style to user language.
        - Include Subject, Greeting, Body, and Closing while generating the mail.
    """),
    
    MessagesPlaceholder(variable_name="history"),
    ("user", "{user_input}")
])

# using buffer Window memory to store last 4 chats
memory_store = {}

def get_session_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferWindowMemory(
            memory_key="history",
            return_messages=True,
            k=4
        )
    return memory_store[session_id].chat_memory

# creating a reactive agent to ask questions when needed
agent = RunnableWithMessageHistory(
    runnable=email_prompt | llm,
    get_session_history=get_session_memory,
    input_messages_key="user_input",
    history_messages_key="history"
)

# cli code block
if __name__ == "__main__":
    print("\nEmail Assistant Ready.\n")
    # using a specific session id
    session_id = "email-session"

    while True:
        user_input = input("You: ").strip()
        # exits the convo if typed either "exit" or "quit"
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = agent.invoke(
            {"user_input": user_input},
            config=RunnableConfig(configurable={"session_id": session_id})
        )

        print(f"\nAI : {response.content}\n")
