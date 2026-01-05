from sqlalchemy.orm import Session
from app.models.jwt_blacklist import JWTBlacklist
from app.models.user import User

def logout_user(db: Session, token: str, user_id: int):
    # blacklist token
    blacklist = JWTBlacklist(token=token, user_id=user_id)
    db.add(blacklist)

    # update logged_in flag
    db.query(User).filter(User.id == user_id).update({"logged_in": None})

    db.commit()

    return {
        "status": True,
        "message": "Successfully logged out!"
    }
