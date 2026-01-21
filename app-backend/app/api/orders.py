#orders.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate

router = APIRouter()

# Create order
@router.post("/")
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_order = Order(item_name=order.item_name, user_id=current_user.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# List orders with optional filters
@router.get("/")
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None)
):
    query = db.query(Order).filter(Order.user_id == current_user.id)
    if status:
        query = query.filter(Order.item_name.ilike(f"%{status}%"))  # example
    return query.all()

# Order details
@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Update order
@router.put("/{order_id}")
def update_order(order_id: int, item_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.item_name = item_name
    db.commit()
    db.refresh(order)
    return order

# Cancel order
@router.delete("/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order cancelled"}

# Cancel all pending orders
@router.post("/cancel_all_pending")
def cancel_all_pending(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    count = len(orders)
    for order in orders:
        db.delete(order)
    db.commit()
    return {"message": f"Cancelled {count} orders"}

# Mark order shipped
@router.post("/{order_id}/mark_shipped")
def mark_shipped(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.item_name += " [Shipped]"  # simple flag
    db.commit()
    db.refresh(order)
    return order

# Mark order delivered
@router.post("/{order_id}/mark_delivered")
def mark_delivered(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.item_name += " [Delivered]"  # simple flag
    db.commit()
    db.refresh(order)
    return order

# Orders stats
@router.get("/stats")
def orders_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total = db.query(Order).filter(Order.user_id == current_user.id).count()
    return {"total_orders": total}
