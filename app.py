import streamlit as st

from agent.email_agent import get_email_response

# Set Streamlit app configuration
st.set_page_config(page_title="Smart Email Assistant", page_icon="📧")

st.title("Smart Email Assistant")
st.markdown("Type your email request in any form :  broken, short, or unclear. The assistant will interact with you and generate a complete professional email.")

# session ID for memory
SESSION_ID = "streamlit-session"

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# user input
user_input = st.chat_input("Type your email request here...")

if user_input:
    # append user's input to chat history
    st.session_state.chat_history.append(("user", user_input))

    # call your reactive agent
    response = get_email_response(user_input, SESSION_ID)

    # append AI response
    st.session_state.chat_history.append(("ai", response.content))

# display conversation
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
