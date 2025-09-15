# main.py
import streamlit as st
from query_generation import build_agent
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
os.environ["PYTORCH_NO_LAZY_INIT"] = "1"


st.set_page_config(page_title="SkyHR Chatbot", layout="wide")
st.title("🤖 SkyHR Chatbot")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

st.sidebar.subheader("🧠 Conversation History")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm SkyHR Chatbot. Ask me anything about your employee data!"}
    ]

# Limit session messages to last 10
MAX_HISTORY = 10
if len(st.session_state["messages"]) > MAX_HISTORY:
    st.session_state["messages"] = st.session_state["messages"][-MAX_HISTORY:]

for msg in st.session_state["messages"]:
    prefix = "🧑" if msg["role"] == "user" else "🤖"
    st.sidebar.markdown(f"**{prefix} {msg['role'].capitalize()}:** {msg['content'][:40]}{'...' if len(msg['content']) > 40 else ''}")

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
import time
from groq import RateLimitError

def safe_agent_invoke(agent, prompt, retries=3, delay=60):
    for attempt in range(retries):
        try:
            return agent.invoke({"input": prompt})
        except RateLimitError as e:
            st.warning(f"Rate limit reached. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return {"output": "Sorry, something went wrong while processing your request."}
    return {"output": "Rate limit exceeded. Please try again later."}

if prompt := st.chat_input("Ask about employee data..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        st.chat_message("assistant").write("Please enter your Groq API Key in the sidebar.")
    else:
        agent = build_agent(api_key)
        # recent_context = st.session_state["messages"][-5:]
        # prompt_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_context])
        # full_input = f"{prompt_context}\nuser: {prompt}"

        with st.chat_message("assistant"):
            response = agent.invoke({"input": prompt})
            # response = safe_agent_invoke(agent, prompt)
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            st.write(response["output"])


# Use "zero-shot-react-description" when:

# You want the agent to reason and decide which tool to use