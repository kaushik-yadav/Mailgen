from langchain.memory import ConversationBufferWindowMemory

from agent.email_agent import get_email_response

# initialize LangChain memory (stores last 5 messages)
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

print("\n📧 Smart Email Assistant (CLI Mode)")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    session_id = "temp-cli-session"
    # add user message to memory
    memory.chat_memory.add_user_message(user_input)

    # get response from agent
    response = get_email_response(user_input, session_id)

    # add agent response to memory
    memory.chat_memory.add_ai_message(response.content)

    print(f"Assistant: {response.content}\n")
