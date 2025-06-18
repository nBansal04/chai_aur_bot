# utils/chat_memory.py
import streamlit as st

def init_chat(system_prompt, examples):
    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt] + examples

def append_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
