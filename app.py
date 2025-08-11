import streamlit as st
from agent.agent import agent
from agent.prompts import WELCOME_MESSAGE

st.set_page_config(page_title="Financial Research Assistant", layout="centered")
st.title("📊 Financial Research Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]

# Display previous messages in chat format
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for new message
user_prompt = st.chat_input("Ask a research question or ticker-based query…")

if user_prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Call agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                response = agent(user_prompt)
                result = response.message['content'][0]['text']
            except Exception as e:
                result = f"❌ Error: {e}"
            st.markdown(result)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": result})
