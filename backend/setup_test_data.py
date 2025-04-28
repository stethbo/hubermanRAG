import firebase_admin
from firebase_admin import credentials, firestore, auth
import pyrebase
import sys
import json
import uuid
import os

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import firebase_config
from backend.config import firebase_config

# Test data for chat history
SAMPLE_CHATS = [
    [
        {
            "role": "assistant",
            "content": "Welcome to Huberman RAG! Ask me anything about Dr. Huberman's teachings."
        },
        {
            "role": "user",
            "content": "What does Andrew recommend for better sleep?"
        },
        {
            "role": "assistant",
            "content": "Dr. Huberman recommends several evidence-based strategies for better sleep:\n\n1. Get morning sunlight exposure (within 30-60 minutes of waking)\n2. Avoid bright light exposure in the evening, especially blue light\n3. Keep a consistent sleep-wake schedule\n4. Exercise regularly, but not too close to bedtime\n5. Avoid caffeine 8-10 hours before sleep\n6. Consider supplements like magnesium threonate, apigenin, and theanine\n7. Keep your sleeping environment cool (around 65°F/18°C)\n8. Use the non-sleep deep rest (NSDR) protocol if you have trouble falling asleep\n\nHe emphasizes that the timing of behaviors is critical for optimizing sleep quality."
        }
    ],
    [
        {
            "role": "assistant",
            "content": "Welcome to Huberman RAG! Ask me anything about Dr. Huberman's teachings."
        },
        {
            "role": "user",
            "content": "What does Andrew say about dopamine?"
        },
        {
            "role": "assistant",
            "content": "Dr. Huberman discusses dopamine extensively as a key neurotransmitter that influences motivation, focus, and reward. Here are some key points he makes about dopamine:\n\n1. Dopamine is about motivation and drive, not just pleasure\n2. The dopamine 'pursuit-reward' circuit drives us to take action\n3. When dopamine is released in anticipation of a reward, we feel heightened focus and motivation\n4. Modern technology and social media exploit dopamine pathways, leading to potential addiction\n5. Boosting baseline dopamine in healthy ways includes: morning sunlight, exercise, completing challenging tasks, cold exposure, and proper sleep\n6. Limiting dopamine spikes from unhealthy sources (like excessive social media, gambling, drugs) helps maintain a healthy dopamine system\n7. 'Dopamine fasting' or 'dopamine scheduling' can help reset sensitivity\n\nHe emphasizes that understanding and managing your dopamine system is crucial for motivation, focus, and achieving goals."
        }
    ]
]

def setup_test_data():
    """Set up test users and sample chat histories in Firestore."""
    try:
        # Initialize Firebase Admin SDK
        try:
            app = firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate("hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json")
            app = firebase_admin.initialize_app(cred)
        
        # Initialize Firebase with Pyrebase (for auth)
        firebase = pyrebase.initialize_app(firebase_config)
        pyrebase_auth = firebase.auth()
        
        # Get Firestore client
        db = firestore.client()
        
        # Create test user
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "TestPassword123!"
        
        try:
            # Create user in Firebase Auth
            print(f"Creating test user: {test_email}")
            user = pyrebase_auth.create_user_with_email_and_password(test_email, test_password)
            user_id = user['localId']
            
            print(f"User created successfully!")
            print(f"User ID: {user_id}")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            
            # Create sample chat histories
            for i, chat in enumerate(SAMPLE_CHATS):
                db.collection("chats").document(user_id).set({"messages": chat})
                print(f"Chat sample {i+1} created in Firestore")
            
            # Print credentials for easy copy-paste
            print("\n=== TEST CREDENTIALS ===")
            print(f"User ID: {user_id}")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print("========================")
            
            # Save credentials to a local file for reference
            with open('test_credentials.txt', 'w') as f:
                f.write("=== TEST CREDENTIALS ===\n")
                f.write(f"User ID: {user_id}\n")
                f.write(f"Email: {test_email}\n")
                f.write(f"Password: {test_password}\n")
                f.write("========================\n")
            
            print("Credentials saved to test_credentials.txt")
            
            return True
            
        except Exception as e:
            if "EMAIL_EXISTS" in str(e):
                print("Email already exists. Trying to sign in instead...")
                try:
                    user = pyrebase_auth.sign_in_with_email_and_password(test_email, test_password)
                    user_id = user['localId']
                    print(f"Successfully signed in existing user: {user_id}")
                    return True
                except Exception as signin_error:
                    print(f"Error signing in: {signin_error}")
                    return False
            else:
                print(f"Error creating user: {e}")
                return False
    
    except Exception as e:
        print(f"Error setting up test data: {e}")
        return False

if __name__ == "__main__":
    success = setup_test_data()
    sys.exit(0 if success else 1) 