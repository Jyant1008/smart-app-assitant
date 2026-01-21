#users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

# Get current logged in user
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

# Update user profile
@router.put("/update")
def update_user(email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.email = email
    db.commit()
    db.refresh(current_user)
    return {"id": current_user.id, "email": current_user.email}

# User preferences
USER_PREFS = {}  # in-memory storage
@router.get("/preferences")
def get_preferences(current_user: User = Depends(get_current_user)):
    return USER_PREFS.get(current_user.id, {"notifications": True})

@router.put("/preferences")
def update_preferences(preferences: dict, current_user: User = Depends(get_current_user)):
    USER_PREFS[current_user.id] = preferences
    return preferences

# Enable/disable notifications (shortcut)
@router.put("/notifications")
def update_notifications(enabled: bool, current_user: User = Depends(get_current_user)):
    prefs = USER_PREFS.get(current_user.id, {"notifications": True})
    prefs["notifications"] = enabled
    USER_PREFS[current_user.id] = prefs
    return prefs

# Delete account
@router.delete("/delete")
def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    USER_PREFS.pop(current_user.id, None)
    return {"message": "User deleted"}
