from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from config import API_SETTINGS
from app.services.firebase_service import FirebaseService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
firebase_service = FirebaseService()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=API_SETTINGS["ACCESS_TOKEN_EXPIRE_MINUTES"])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_SETTINGS["JWT_SECRET"], algorithm=API_SETTINGS["JWT_ALGORITHM"])
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, API_SETTINGS["JWT_SECRET"], algorithms=[API_SETTINGS["JWT_ALGORITHM"]])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id}
    except JWTError:
        raise credentials_exception 