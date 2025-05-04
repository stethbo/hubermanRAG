import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pyrebase
from config import firebase_config
from typing import List, Dict, Any

load_dotenv()

# Initialize Firebase with Pyrebase (for auth)
firebase = pyrebase.initialize_app(firebase_config)
pyrebase_auth = firebase.auth()

# Initialize Firebase Admin SDK (for Firestore)
try:
    app = firebase_admin.get_app()
except ValueError:
    # Path to your service account key JSON file
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    app = firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

class FirebaseService:
    def __init__(self):
        self.db = db
        self.auth = pyrebase_auth
        self.admin_auth = auth

    def create_user(self, email, password):
        return self.auth.create_user_with_email_and_password(email, password)
    
    def login_user(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)
    
    def verify_token(self, id_token):
        """Verify Firebase ID token"""
        try:
            decoded_token = self.admin_auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            raise e
    
    def get_chat_history(self, user_id) -> List[Dict[str, str]]:
        """Get chat history for a user with validated message format"""
        chat_history = self.db.collection("history").document(user_id).get()
        if chat_history.exists:
            messages = chat_history.to_dict().get("messages", [])
            # Validate each message has the required fields
            return self._validate_messages(messages)
        return []
    
    def save_message(self, user_id, message) -> List[Dict[str, str]]:
        """Save a message to chat history"""
        # Validate message format
        if not self._is_valid_message(message):
            raise ValueError("Invalid message format. Must have 'role' and 'content' fields")
            
        chat_ref = self.db.collection("history").document(user_id)
        chat_history = self.get_chat_history(user_id)
        chat_history.append(message)
        chat_ref.set({"messages": chat_history})
        return chat_history
    
    def _is_valid_message(self, message) -> bool:
        """Check if a message has valid format"""
        if not isinstance(message, dict):
            return False
        if "role" not in message or "content" not in message:
            return False
        if message["role"] not in ["user", "assistant"]:
            return False
        if not isinstance(message["content"], str):
            return False
        return True
    
    def _validate_messages(self, messages) -> List[Dict[str, str]]:
        """Filter out invalid messages"""
        valid_messages = []
        for msg in messages:
            if self._is_valid_message(msg):
                valid_messages.append(msg)
        return valid_messages 