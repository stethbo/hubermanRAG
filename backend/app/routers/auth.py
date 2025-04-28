from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.models import UserCredentials, TokenResponse
from app.services.firebase_service import FirebaseService
from app.utils.auth import create_access_token
from typing import Dict

router = APIRouter()
firebase_service = FirebaseService()

@router.post("/signup", response_model=TokenResponse)
async def signup(user_credentials: UserCredentials):
    try:
        user = firebase_service.create_user(user_credentials.email, user_credentials.password)
        token = create_access_token(data={"user_id": user["localId"]})
        return {
            "token": token,
            "user_id": user["localId"],
            "email": user_credentials.email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserCredentials):
    try:
        user = firebase_service.login_user(user_credentials.email, user_credentials.password)
        token = create_access_token(data={"user_id": user["localId"]})
        return {
            "token": token,
            "user_id": user["localId"],
            "email": user_credentials.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/google-login", response_model=TokenResponse)
async def google_login(data: Dict[str, str] = Body(...)):
    try:
        # Extract the ID token from the request body
        id_token = data.get("id_token")
        if not id_token:
            raise HTTPException(status_code=400, detail="ID token is required")
            
        # Verify the Google ID token
        decoded_token = firebase_service.verify_token(id_token)
        user_id = decoded_token["uid"]
        email = decoded_token.get("email", "")
        
        # Create our own JWT token
        token = create_access_token(data={"user_id": user_id})
        
        return {
            "token": token,
            "user_id": user_id,
            "email": email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) 