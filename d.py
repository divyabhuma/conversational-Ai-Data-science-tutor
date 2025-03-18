import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.memory import ChatMessageHistory

# Set Google API Key
GOOGLE_API_KEY = "AIzaSyDX-UyxgsUZZiVBjfe4GFPxXOXEVjx_igQ"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Google Gemini AI
llm = GoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=GOOGLE_API_KEY)

# Memory for conversation history
memory = ChatMessageHistory()

# Function to check if the query is related to Data Science using LLM
def is_data_science_related(query):
    check_prompt = f"Is the following question related to Data Science? Answer only with 'yes' or 'no': {query}"
    try:
        response = llm.invoke(check_prompt).strip().lower()
        return response == "yes"
    except Exception:
        return False  # Default to False in case of API failure

# Streamlit UI
st.set_page_config(page_title="Conversational AI Data Science Tutor", layout="wide")
st.title("🤖 Conversational AI Data Science Tutor")

# Initialize session state for memory
if "memory" not in st.session_state:
    st.session_state.memory = memory

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask your Data Science doubt...")

if user_input:
    if is_data_science_related(user_input):
        try:
            response = llm.invoke(user_input)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        # Store conversation in memory
        st.session_state.memory.add_user_message(user_input)
        st.session_state.memory.add_ai_message(response)

        # Store messages in session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display user query
        with st.chat_message("user"):
            st.markdown(user_input)

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            st.markdown("❌ I can only assist with Data Science-related questions.")

