from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User

router = APIRouter()

# Bulk cancel orders by ids
@router.post("/orders/cancel")
def bulk_cancel_orders(order_ids: list[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id==current_user.id, Order.id.in_(order_ids)).all()
    for o in orders:
        db.delete(o)
    db.commit()
    return {"message": f"Cancelled {len(orders)} orders"}

# Bulk update payments status
@router.put("/payments/status")
def bulk_update_payments(payment_ids: list[int], status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Payment).join(Order).filter(Order.user_id==current_user.id, Payment.id.in_(payment_ids)).all()
    for p in payments:
        p.status = status
    db.commit()
    return {"message": f"Updated {len(payments)} payments"}
