import os

from langchain_community.chat_message_histories import SQLChatMessageHistory

# Build safe absolute DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "chat_history.db"))

def get_session_memory(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=f"sqlite:///{DB_PATH}"  # ✅ use `connection`, not deprecated `connection_string`
    )
