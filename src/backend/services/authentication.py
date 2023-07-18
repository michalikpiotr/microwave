import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.backend.config import get_settings

security = HTTPBearer()

admin_users = ["Piotr Michalik"]


def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """User Authentication by JWT token for cancel button"""
    settings = get_settings()
    SECRET_KEY = settings.JWT_SECRET
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("name")

        if not username or username not in admin_users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
