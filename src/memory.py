from langchain.memory import ConversationBufferWindowMemory

memory_store = {}

# creating a per session memory with last 4 chat storage
def get_session_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferWindowMemory(
            memory_key = "history",
            return_messages = True,
            k = 6
        )
    return memory_store[session_id].chat_memory