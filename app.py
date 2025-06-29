import json
import os

import streamlit as st
from langchain_community.chat_message_histories import SQLChatMessageHistory

from agent.email_agent import get_email_response

USERS_FILE = "users.json"
DB_PATH = "chat_history.db"

# Load and Save users

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"usernames": {}}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, name, password):
    users = load_users()
    if username in users["usernames"]:
        return False, "Username already exists!"
    users["usernames"][username] = {"name": name, "password": password}
    save_users(users)
    return True, "Registered successfully—please log in."

def authenticate(username, password):
    users = load_users().get("usernames", {})
    if username in users and users[username]["password"] == password:
        return True, users[username]["name"]
    return False, None

# UI Setup
st.set_page_config(page_title="Smart Email Assistant", page_icon="📧")
st.title("📧 Smart Email Assistant")

# Login/Register
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Choose action", ["Login", "Register"])
    if choice == "Register":
        st.subheader("Create a new account")
        new_name = st.text_input("Full name")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Register"):
            ok, msg = register_user(new_user, new_name, new_pass)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    else:
        st.subheader("Login to your account")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, name = authenticate(user, pwd)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.name = name
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

# Logged in state
st.sidebar.success(f"Hello, {st.session_state.name}")
if st.sidebar.button("Logout"):
    for key in ["logged_in", "username", "name", "chat_history"]:
        st.session_state.pop(key, None)
    st.rerun()

# Session ID
SESSION_ID = f"user-session-{st.session_state.username}"

# Show past conversations
st.sidebar.markdown("---")
st.sidebar.markdown("### Your Chat History")

chat_db = SQLChatMessageHistory(session_id=SESSION_ID, connection_string=f"sqlite:///{DB_PATH}")
past_messages = chat_db.messages
if past_messages:
    for m in reversed(past_messages[-10:]):  # last 10 messages only
        role = "You" if m.type == "human" else "Assistant"
        st.sidebar.markdown(f"**{role}:** {m.content}")
else:
    st.sidebar.info("No history yet.")

# Main chat window
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your email request here…")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    resp = get_email_response(user_input, SESSION_ID)
    st.session_state.chat_history.append(("ai", resp.content))

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
