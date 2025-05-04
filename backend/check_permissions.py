import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import sys
import json

load_dotenv()

def check_firebase_permissions():
    """Check Firebase service account details and verify permissions."""
    try:
        # Print the path being used for credentials
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        print(f"Using Firebase credentials from: {cred_path}")
        
        # Verify the file exists
        if not os.path.exists(cred_path):
            print(f"❌ Credentials file not found at: {cred_path}")
            print(f"Current working directory: {os.getcwd()}")
            return False
        
        # Load and analyze the service account file
        with open(cred_path, 'r') as f:
            service_account = json.load(f)
            
        # Extract key information from the service account
        project_id = service_account.get('project_id', 'Not found')
        client_email = service_account.get('client_email', 'Not found')
        private_key_id = service_account.get('private_key_id', 'Not found')
        
        print("\nService Account Details:")
        print(f"Project ID: {project_id}")
        print(f"Service Account Email: {client_email}")
        print(f"Private Key ID: {private_key_id[:6]}... (partial)")
        
        # Check if this is a Firebase Admin SDK service account
        if 'firebase-adminsdk' not in client_email:
            print("⚠️ Warning: This does not appear to be a Firebase Admin SDK service account")
            print("Service accounts should contain 'firebase-adminsdk' in the email")
        
        # Try to initialize Firebase
        try:
            cred = credentials.Certificate(cred_path)
            try:
                app = firebase_admin.initialize_app(cred)
                print("\n✅ Successfully initialized Firebase app")
            except ValueError:
                # App already initialized
                app = firebase_admin.get_app()
                print("\n✅ Firebase app already initialized")
                
            # Print app details
            print(f"App name: {app.name}")
            print(f"App options: {app.options}")
            
            # Try basic Firestore operations
            print("\nTesting Firestore operations:")
            
            try:
                db = firestore.client()
                print("✅ Successfully got Firestore client")
                
                # Test listing collections
                try:
                    collections = list(db.collections())
                    print(f"✅ Successfully listed {len(collections)} collections")
                    if collections:
                        print(f"   Collection IDs: {[collection.id for collection in collections]}")
                except Exception as e:
                    print(f"❌ Failed to list collections: {e}")
                
                # Try to read a document (test collection)
                try:
                    doc_ref = db.collection('test_collection').document('test_doc')
                    doc = doc_ref.get()
                    print(f"✅ Successfully tested document read operation")
                except Exception as e:
                    print(f"❌ Failed to read document: {e}")
                
            except Exception as e:
                print(f"❌ Failed to get Firestore client: {e}")
                
            # Common troubleshooting steps
            print("\nTroubleshooting recommendations:")
            print("1. Verify you've created a Firestore database in your Firebase project")
            print("2. Check your Firebase Security Rules - they may be too restrictive")
            print("3. Make sure the service account has proper IAM roles (at least 'Firebase Admin' role)")
            print("4. Verify the project ID in your credentials matches your actual Firebase project")
            print("5. Check if you need to enable the Firestore API in Google Cloud Console")
            
        except Exception as e:
            print(f"\n❌ Error initializing Firebase: {e}")
        
        return True
    except Exception as e:
        print(f"\n❌ Error checking permissions: {e}")
        return False

if __name__ == "__main__":
    success = check_firebase_permissions()
    sys.exit(0 if success else 1)
