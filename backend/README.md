# Huberman RAG Backend

This is the FastAPI backend for the Huberman RAG application. It provides endpoints for authentication and chat with RAG functionality.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have the Firebase service account file:
```
hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json
```

3. Create a `.env` file with the following variables:
```
AZURE_API_KEY=your_azure_api_key
JWT_SECRET=your_jwt_secret
```

4. Run the server:
```bash
python run.py
```

The server will be available at http://localhost:8000.

## API Endpoints

- **Authentication**:
  - POST `/api/auth/signup`: Register a new user
  - POST `/api/auth/login`: Log in a user
  - POST `/api/auth/google-login`: Log in with Google

- **Chat**:
  - GET `/api/chat/history`: Get chat history
  - POST `/api/chat/message`: Send a message and get a response 