import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

def createService(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    creds = None

    # Use session_state to store credentials per user
    if 'google_creds' in st.session_state:
        creds = st.session_state['google_creds']
    
    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            st.session_state['google_creds'] = creds
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            flow.redirect_uri = st.secrets["google_oauth"]["redirect_uri"]
            auth_url, _ = flow.authorization_url(prompt="consent")
            st.write(f"[Authorize Google API]({auth_url})")
            code = st.text_input("Paste the authorization code here:")
            if code:
                try:
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    st.session_state['google_creds'] = creds
                    st.success("Google authentication successful!")
                except Exception as e:
                    st.error(f"Failed to fetch token: {e}")
            return None  # Wait for user to complete auth

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'SERVICE CREATED SUCCESSFULLY')
        return service
    except Exception as error:
        print(f"An error occurred creating service for {API_SERVICE_NAME}: {error}")
        if 'google_creds' in st.session_state:
            del st.session_state['google_creds']
        return None

