from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()

def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)

def verify_password(pw: str, hpw: str) -> bool:
    return pwd_context.verify(pw, hpw)

def create_access_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRES)
    return jwt.encode({"sub": sub, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")

def get_current_user_id(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        return int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
