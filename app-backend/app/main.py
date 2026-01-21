from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from app.api import (
    auth,
    users,
    orders,
    payments,
    dashboard,
    search,
    bulk,
    health
)

app = FastAPI(
    title="Smart App Backend",
    description="Backend for small business app: users, orders, payments, dashboard",
    version="1.0.0"
)

# Allow CORS (frontend can run on localhost:3000)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(bulk.router, prefix="/bulk", tags=["bulk"])
app.include_router(health.router, prefix="/health", tags=["health"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Smart App Backend is running!"}
