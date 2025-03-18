import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.memory import ChatMessageHistory
GOOGLE_API_KEY = "API_KEY"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
llm = GoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=GOOGLE_API_KEY)
memory = ChatMessageHistory()
def is_data_science_related(query):
    check_prompt = f"Is the following question related to Data Science? Answer only with 'yes' or 'no': {query}"
    try:
        response = llm.invoke(check_prompt).strip().lower()
        return response == "yes"
    except Exception:
        return False 
st.set_page_config(page_title="Conversational AI Data Science Tutor", layout="wide")
st.title("🤖 Conversational AI Data Science Tutor")
if "memory" not in st.session_state:
    st.session_state.memory = memory

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
user_input = st.chat_input("Ask your Data Science doubt...")

if user_input:
    if is_data_science_related(user_input):
        try:
            response = llm.invoke(user_input)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        st.session_state.memory.add_user_message(user_input)
        st.session_state.memory.add_ai_message(response)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            st.markdown("❌ I can only assist with Data Science-related questions.")

