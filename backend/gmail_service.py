import os
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailService:
    def __init__(self):
        # Path to credentials file
        self.credentials_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'gmail_credentials.json'
        )
        
        # OAuth scopes
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        
        # Redirect URI (must match what's in Google Cloud Console)
        self.REDIRECT_URI = 'http://localhost:8000/api/gmail-callback'
        
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Gmail credentials not found at {self.credentials_path}")
    
    def get_authorization_url(self):
        """Generate OAuth authorization URL"""
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.SCOPES,
            redirect_uri=self.REDIRECT_URI
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return auth_url
    
    def handle_callback(self, authorization_code):
        """Exchange authorization code for credentials"""
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.SCOPES,
            redirect_uri=self.REDIRECT_URI
        )
        
        flow.fetch_token(code=authorization_code)
        credentials = flow.credentials
        
        return credentials
    
    def send_email(self, to_email, subject, body, access_token):
        """Send email using Gmail API"""
        try:
            # Create credentials from access token
            credentials = Credentials(token=access_token)
            
            # Build Gmail service
            service = build('gmail', 'v1', credentials=credentials)
            
            # Create message
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = subject
            message['from'] = 'me'  # Gmail API automatically uses authenticated user
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            send_message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return send_message['id']
            
        except HttpError as error:
            raise Exception(f"Gmail API error: {error}")
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")
    
    def refresh_access_token(self, refresh_token):
        """Refresh access token using refresh token"""
        with open(self.credentials_path, 'r') as f:
            client_config = json.load(f)
        
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri=client_config['web']['token_uri'],
            client_id=client_config['web']['client_id'],
            client_secret=client_config['web']['client_secret']
        )
        
        # Refresh the token
        from google.auth.transport.requests import Request
        credentials.refresh(Request())
        
        return credentials.token
