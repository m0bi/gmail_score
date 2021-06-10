from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
   
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. It must be refreshed daily.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_643245849556-3bc5kon1dtv3md1h41eos6j01sgb2t4a.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results_inbox = service.users().messages().list(userId='me', q="newer_than:1d in:inbox").execute()
    results_sent = service.users().messages().list(userId='me', q="newer_than:1d in:sent").execute()
    print("Recieved", results_inbox["resultSizeEstimate"])
    print("Sent", results_sent["resultSizeEstimate"])


if __name__ == '__main__':
    main()