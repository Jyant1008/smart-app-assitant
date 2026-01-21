#payments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.payment import Payment
from app.models.order import Order
from app.models.user import User

router = APIRouter()

# List payments
@router.get("/")
def list_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Payment).join(Order).filter(Order.user_id == current_user.id).all()
    return payments

# Payment details
@router.get("/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Create payment
@router.post("/create")
def create_payment(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    new_payment = Payment(status="pending", order_id=order.id)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# Update payment status
@router.put("/{payment_id}/status")
def update_payment_status(payment_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = status
    db.commit()
    db.refresh(payment)
    return payment

# Refund payment
@router.post("/refund/{payment_id}")
def refund_payment(payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = "refunded"
    db.commit()
    db.refresh(payment)
    return payment

# Payments stats
@router.get("/stats")
def payments_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total = db.query(Payment).join(Order).filter(Order.user_id == current_user.id).count()
    success = db.query(Payment).join(Order).filter(Order.user_id == current_user.id, Payment.status=="completed").count()
    failed = db.query(Payment).join(Order).filter(Order.user_id == current_user.id, Payment.status=="failed").count()
    return {"total": total, "success": success, "failed": failed}
