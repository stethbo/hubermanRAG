from fastapi import APIRouter, Depends, HTTPException
from app.models.models import ChatRequest, ChatResponse, ChatHistory, Message
from app.services.rag_service import RAGService
from app.services.firebase_service import FirebaseService
from app.utils.auth import get_current_user
from typing import Dict, Any, List

router = APIRouter()
rag_service = RAGService()
firebase_service = FirebaseService()

@router.get("/history", response_model=ChatHistory)
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["user_id"]
        chat_history = firebase_service.get_chat_history(user_id)
        
        # Ensure each message has role and content fields
        validated_history = []
        for msg in chat_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                validated_history.append(msg)
        
        return {"messages": validated_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["user_id"]
        
        # Save user message
        user_message = {"role": "user", "content": request.message}
        
        try:
            # Try to save the user message, which might fail due to permissions
            firebase_service.save_message(user_id, user_message)
        except Exception as firebase_error:
            # Check if it's a permissions error
            if "403" in str(firebase_error) or "permission" in str(firebase_error).lower():
                raise HTTPException(
                    status_code=403, 
                    detail="Firebase permission error. Possible causes: 1) Firestore security rules are too restrictive, "
                           "2) The service account lacks proper permissions, or "
                           "3) The 'chats' collection doesn't exist yet."
                )
            else:
                # Re-raise if it's not a permissions error
                raise firebase_error
        
        # Generate response
        if request.use_rag:
            response_text = rag_service.query_with_rag(request.message)
        else:
            response_text = rag_service.query_without_rag(request.message)
        
        # Save assistant response
        assistant_message = {"role": "assistant", "content": response_text}
        
        try:
            chat_history = firebase_service.save_message(user_id, assistant_message)
        except Exception as firebase_error:
            # If we can't save the assistant message, still return the response
            # but with a warning and without updated chat history
            print(f"Warning: Could not save assistant message: {str(firebase_error)}")
            return {
                "response": response_text + "\n\nNote: Your message history could not be saved due to a database permission issue.",
                "chat_history": [user_message, assistant_message]  # Return just the current conversation
            }
        
        # Ensure each message in chat_history has role and content fields
        validated_history = []
        for msg in chat_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                if msg["role"] in ["user", "assistant"] and isinstance(msg["content"], str):
                    validated_history.append(msg)
        
        return {
            "response": response_text,
            "chat_history": validated_history
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) 