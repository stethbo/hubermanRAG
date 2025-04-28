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
        firebase_service.save_message(user_id, user_message)
        
        # Generate response
        if request.use_rag:
            response_text = rag_service.query_with_rag(request.message)
        else:
            response_text = rag_service.query_without_rag(request.message)
        
        # Save assistant response
        assistant_message = {"role": "assistant", "content": response_text}
        chat_history = firebase_service.save_message(user_id, assistant_message)
        
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
        raise HTTPException(status_code=500, detail=str(e)) 