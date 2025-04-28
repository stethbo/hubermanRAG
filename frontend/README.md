# Huberman RAG Frontend

This is the Next.js frontend for the Huberman RAG application. It provides a modern, responsive UI for chatting with the RAG-powered assistant about Dr. Andrew Huberman's teachings.

## Features

- Firebase authentication (email/password and Google)
- Pop-up login modal
- Chat history sidebar
- RAG toggle for enabling/disabling retrieval-augmented generation
- Responsive design for mobile and desktop

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file with the following variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000.

## Building for Production

```bash
npm run build
npm start
```

## Connecting to Backend

Make sure the backend is running at http://localhost:8000 (or update the NEXT_PUBLIC_API_URL in your .env.local file to point to the correct backend URL).
