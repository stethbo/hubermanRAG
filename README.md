# Huberman RAG

A chat application that allows users to ask questions about Dr. Andrew Huberman's teachings using a Retrieval-Augmented Generation (RAG) system for accurate and detailed responses.

## Features

- Next.js frontend with a clean, modern UI
- FastAPI backend with RAG capabilities
- Firebase authentication (email/password and Google login)
- Chat history stored in Firestore
- Toggle to enable/disable RAG functionality

## Project Structure

- `/frontend` - Next.js frontend application
- `/backend` - FastAPI backend application
- `/db` - ChromaDB vector database (not included in this repo)

## Quick Start

### Setting up the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have the Firebase service account file in the backend root directory:
```
hubermanrag-firebase-adminsdk-fbsvc-1fb326ddbd.json
```

4. Create a `.env` file with the following variables:
```
AZURE_API_KEY=your_azure_api_key
JWT_SECRET=your_jwt_secret
```

5. Start the backend server:
```bash
python run.py
```

The backend will be available at http://localhost:8000.

### Setting up the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

4. Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000.

## API Documentation

Backend API documentation is available at http://localhost:8000/docs when the backend is running.

## Technologies Used

- **Frontend**: Next.js, React, TailwindCSS, Firebase Auth
- **Backend**: FastAPI, Langchain, ChromaDB, OpenAI
- **Database**: Firebase Firestore, ChromaDB
- **Authentication**: Firebase Authentication, JWT
