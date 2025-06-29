
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
import streamlit as st
def createService(client_secret_file,api_name,api_version,*scopes,prefix=''):

  CLIENT_SECRET_FILE = client_secret_file
  API_SERVICE_NAME = api_name
  API_VERSION = api_version
  SCOPES = [scope for scope in scopes[0]]
  creds = None
  working_dir = os.getcwd()
  token_dir = 'token_files'
  token_file = f'token_google_calendar.json'
  
  ### Check if token dir exists first , if not , create folder
  if not os.path.exists(os.path.join(working_dir,token_dir)):
    os.mkdir(os.path.join(working_dir,token_dir))
    
  if os.path.exists(os.path.join(working_dir,token_dir,token_file)):
    creds = Credentials.from_authorized_user_file(os.path.join(working_dir,token_dir,token_file), SCOPES)

  try:
    service = build(API_SERVICE_NAME, API_VERSION, credentials=creds,static_discovery=False)
    print(API_SERVICE_NAME,API_VERSION, 'SERVICE CREATED SUCCESSFULLY')
    return service
  except Exception as error:
    print(f"An error occurred creating service for {API_SERVICE_NAME}: {error}")
    os.remove(os.path.join(working_dir,token_dir,token_file))
    return None
