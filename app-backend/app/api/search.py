from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User

router = APIRouter()

# Search orders
@router.get("/orders")
def search_orders(q: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id==current_user.id, Order.item_name.ilike(f"%{q}%")).all()
    return orders

# Search payments
@router.get("/payments")
def search_payments(q: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Payment).join(Order).filter(Order.user_id==current_user.id).all()
    # filtering by order name
    filtered = [p for p in payments if q.lower() in p.order.item_name.lower()]
    return filtered
