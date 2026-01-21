#dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User

router = APIRouter()

# Dashboard summary
@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_orders = db.query(Order).filter(Order.user_id==current_user.id).count()
    total_payments = db.query(Payment).join(Order).filter(Order.user_id==current_user.id).count()
    return {
        "total_orders": total_orders,
        "total_payments": total_payments,
    }

# Recent orders (last 5)
@router.get("/recent_orders")
def recent_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id==current_user.id).order_by(Order.id.desc()).limit(5).all()
    return orders

# Recent payments (last 5)
@router.get("/recent_payments")
def recent_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Payment).join(Order).filter(Order.user_id==current_user.id).order_by(Payment.id.desc()).limit(5).all()
    return payments
