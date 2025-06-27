import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from agent2 import agent_graph

# Title of the app
st.title("🤖 Google Calendar Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history container with scrollable layout
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input box fixed at the bottom
if user_input := st.chat_input(placeholder="Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Display user message in real-time
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare a container for assistant's response
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())  # Streaming callback
        cfg = {"callbacks": [st_callback]}

        # Run the agent and get the response
        result = agent_graph.invoke({"messages": st.session_state.messages}, cfg)

        # Extract and append assistant's final message
        ai_msg = result["messages"][-1]
        st.session_state.messages.append(ai_msg)

        # Display the assistant's response
        st.markdown(ai_msg.content)
