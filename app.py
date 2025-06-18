import streamlit as st
from prompts.system_prompt import system_prompt, few_shot_examples
from services.openai_service import get_openai_response
from utils.chat_memory import init_chat, append_message
from PIL import Image
import base64
from io import BytesIO

# Function to convert image to base64
def hitesh_img_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode()

st.set_page_config(page_title="Chai aur Code Bot ☕️", page_icon="🤖")

# Load Hitesh Sir's image
hitesh_img = Image.open("assets/hitesh.jpg")

# CSS for styling chat layout
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        margin-bottom: 1rem;
    }
    .chat-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 10px;
        flex-shrink: 0;
    }
    .chat-bubble {
        background-color: #f0f2f6;
        padding: 12px;
        border-radius: 10px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .chat-user {
        justify-content: flex-end;
        text-align: right;
    }
    .chat-user .chat-bubble {
        background-color: #dcf8c6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize memory
init_chat(system_prompt, few_shot_examples)

# Page UI
st.title("🤖 Chai aur Code Bot")
st.caption("Powered by GPT · Inspired by Hitesh Choudhary")

# Input
user_input = st.chat_input("Btaiye kya puchna hai?")

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    role = msg["role"]
    with st.container():
        if role == "user":
            st.markdown(f"""
                <div class="chat-container chat-user">
                    <div class="chat-bubble">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-avatar">
                        <img src="data:image/jpeg;base64,{hitesh_img_to_base64(hitesh_img)}" width="48" height="48"/>
                    </div>
                    <div class="chat-bubble">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)

# Process new input
if user_input:
    append_message("user", user_input)
    with st.spinner("☕ Hitesh sir soch rahe hain..."):
        reply = get_openai_response(st.session_state.messages)
        append_message("assistant", reply)
        st.rerun()
