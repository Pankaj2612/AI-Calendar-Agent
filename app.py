import logging
from urllib.request import Request
import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain_core.messages import HumanMessage, AIMessage
from agent2 import agent_graph


st.title("🤖 Google Calendar Assistant")

CLIENT_SECRET_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.owned",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.freebusy",
]
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
REDIRECT_URI = st.secrets["REDIRECT_URI"]  # Ensure this is set in your Streamlit secrets
TOKEN_DIR = "token_files"
TOKEN_FILE = os.path.join(TOKEN_DIR, "token_google_calendar.json")

if "authorized" not in st.session_state:
    st.session_state["authorized"] = False

# Ensure token directory exists
if not os.path.exists(TOKEN_DIR):
    os.mkdir(TOKEN_DIR)

# Check if user is authenticated
creds = None

# Authorization step
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not st.session_state["authorized"]:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
            )
           
            auth_url, _ = flow.authorization_url(
                access_type="offline", prompt="consent"
            )
            st.write("### Authorization Required")
            st.write("Please click the link below to authorize:")
            st.markdown(f"[Authorize Here]({auth_url})")

            query_params = st.query_params
            logging.info(f"Query parameters: {query_params}")
            if "code" in query_params:
                code = query_params["code"]  # Extract the authorization code
                logging.info(code)
                try:
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    # Save the credentials for future use
                    with open(TOKEN_FILE, "w") as token_file:
                        token_file.write(creds.to_json())
                    st.success(
                        "Authorization successful! You can now use the assistant."
                    )
                    st.session_state["authorized"] = True
                except Exception as e:
                    st.error(f"Error during authorization: {e}")


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
