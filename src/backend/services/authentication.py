""" JWT Authentication """
import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.backend.config import get_settings

security = HTTPBearer()


def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """User Authentication by JWT token for cancel button"""
    settings = get_settings()
    admin_user = settings.ADMIN_USER
    secret_key = settings.JWT_SECRET
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username = payload.get("name")

        if not username or username != admin_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        ) from None
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from None
