import firebase_admin
from firebase_admin import credentials, firestore
import sys
import uuid
import os
import importlib.util

from backend.config import firebase_config

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def initialize_firestore():
    """Initialize Firestore with sample data for testing."""
    try:
        # Initialize Firebase Admin
        try:
            app = firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate("hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json")
            app = firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        db = firestore.client()
        
        # Create a test user ID if one isn't provided
        test_user_id = str(uuid.uuid4())
        print(f"Using test user ID: {test_user_id}")
        
        # Create welcome message
        welcome_messages = [
            {
                "role": "assistant",
                "content": "Welcome to Huberman RAG! Ask me anything about Dr. Huberman's teachings."
            }
        ]
        
        # Set the welcome message in Firestore
        db.collection("chats").document(test_user_id).set({"messages": welcome_messages})
        
        print(f"Successfully initialized Firestore with test data.")
        print(f"Test User ID: {test_user_id}")
        print("Add this user ID to your frontend localStorage or use it for testing.")
        
        return True
    
    except Exception as e:
        print(f"Error initializing Firestore: {e}")
        return False

if __name__ == "__main__":
    success = initialize_firestore()
    sys.exit(0 if success else 1) 