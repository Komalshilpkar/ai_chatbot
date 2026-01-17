import streamlit as st
import os
from groq import Groq

# ===============================
# CONFIG
# ===============================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"

 # free & fast

# ===============================
# PAGE SETUP
# ===============================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Built with Streamlit + Groq Free API (Open-Source LLM)")

# ===============================
# SIDEBAR (UI + HISTORY)
# ===============================
st.sidebar.title("⚙️ Controls")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("### 📜 Recent Messages")
for msg in st.session_state.messages[-8:]:
    st.sidebar.write(f"**{msg['role'].capitalize()}**: {msg['content'][:40]}...")



st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["Chat", "Coding", "Interview"]
)

SYSTEM_PROMPTS = {
    "Chat": "You are a friendly and helpful AI assistant.",
    
    "Coding": (
        "You are an expert software developer. "
        "Give clean, correct, and optimized code with explanations."
    ),
    
    "Interview": (
        "You are an interview coach. "
        "Answer concisely, professionally, and with real-world examples."
    )
}


# ===============================
# DISPLAY CHAT
# ===============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# USER INPUT
# ===============================
prompt = st.chat_input("Type your message...")

if prompt:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = [
               {"role": "system", "content": SYSTEM_PROMPTS[mode]},
               *st.session_state.messages
           ]

            response = client.chat.completions.create(
               model=MODEL,
               messages=messages,
               temperature=0.7,
               max_tokens=300
   )

            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )





# import streamlit as st
# import os
# from dotenv import load_dotenv
# from utils.llm import get_client
# from utils.pdf_loader import load_pdf
# from utils.rag import split_text, create_faiss_index
# # import os


# load_dotenv()

# st.write("API KEY FOUND:", os.getenv("DEEPSEEK_API_KEY"))

# client = get_client()

# st.set_page_config("DeepSeek LLM App", "🤖")
# st.title("🤖 DeepSeek AI Assistant")

# mode = st.sidebar.selectbox(
#     "Select Mode",
#     ["Chatbot", "Coding Bot", "PDF Chat (RAG)"]
# )

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if st.sidebar.button("🗑 Clear Chat"):
#     st.session_state.messages = []

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# system_prompts = {
#     "Chatbot": "You are a helpful assistant.",
#     "Coding Bot": "You are an expert software developer.",
#     "PDF Chat (RAG)": "Answer only from the document."
# }

# if mode == "PDF Chat (RAG)":
#     pdf = st.file_uploader("Upload PDF", type="pdf")
#     if pdf:
#         text = load_pdf(pdf)
#         chunks = split_text(text)

#         embeddings = []
#         for chunk in chunks:
#             emb = client.embeddings.create(
#                 model="text-embedding-3-small",
#                 input=chunk
#             )
#             embeddings.append(emb.data[0].embedding)

#         index = create_faiss_index(embeddings)
#         st.success("PDF indexed successfully")

# prompt = st.chat_input("Type your message...")

# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = client.chat.completions.create(
#                 model="deepseek-coder" if mode == "Coding Bot" else "deepseek-chat",
#                 messages=[
#                     {"role": "system", "content": system_prompts[mode]},
#                     *st.session_state.messages
#                 ]
#             )
#             reply = response.choices[0].message.content
#             st.markdown(reply)

#     st.session_state.messages.append({"role": "assistant", "content": reply})
