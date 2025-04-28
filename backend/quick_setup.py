import firebase_admin
from firebase_admin import credentials, firestore, auth
import pyrebase
import sys
import json
import uuid
import os

from backend.config import firebase_config

def quick_setup():
    """Quickly set up a test user and initialize Firestore with sample data."""
    try:
        # Initialize Firebase Admin SDK
        try:
            app = firebase_admin.get_app()
        except ValueError:
            # Check if the certificate file exists
            cert_path = "hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json"
            if not os.path.exists(cert_path):
                print(f"Error: Firebase Admin SDK certificate file not found at {cert_path}")
                print("Please make sure to place the Firebase Admin SDK certificate in the backend directory.")
                return False
                
            cred = credentials.Certificate(cert_path)
            app = firebase_admin.initialize_app(cred)
        
        # Initialize Firebase with Pyrebase (for auth)
        firebase = pyrebase.initialize_app(firebase_config)
        pyrebase_auth = firebase.auth()
        
        # Get Firestore client
        db = firestore.client()
        
        # Create test user
        test_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
        test_password = "Test123!"
        
        try:
            # Create user in Firebase Auth
            print(f"Creating test user with email: {test_email}")
            user = pyrebase_auth.create_user_with_email_and_password(test_email, test_password)
            user_id = user['localId']
            
            # Create welcome message
            welcome_message = [
                {
                    "role": "assistant",
                    "content": "Welcome to Huberman RAG! Ask me anything about Dr. Huberman's teachings."
                }
            ]
            
            # Set the welcome message in Firestore
            db.collection("chats").document(user_id).set({"messages": welcome_message})
            
            # Print credentials
            print("\n=== TEST USER CREATED SUCCESSFULLY ===")
            print(f"User ID: {user_id}")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print("=====================================")
            print("\nUse these credentials to log in to the application.")
            
            return True
            
        except Exception as e:
            print(f"Error creating test user: {e}")
            return False
    
    except Exception as e:
        print(f"Error in quick setup: {e}")
        return False

if __name__ == "__main__":
    success = quick_setup()
    sys.exit(0 if success else 1) 