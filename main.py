from agent.email_agent import get_email_response

if __name__ == "__main__":
    # creating a default session id
    session_id = "email-session"
    print("\nEmail Assistant Ready. Type your request or 'exit'.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = get_email_response(user_input, session_id)
        print(f"\nAI: {response.content}\n")