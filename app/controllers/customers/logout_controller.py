from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.logout_service import logout_user

security = HTTPBearer()

def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    return logout_user(db, token, user_id)
