# api/__init__.py
"""
This file imports all API routers so that they can be included easily in main.py
"""

from .auth import router as auth_router
from .users import router as users_router
from .orders import router as orders_router
from .payments import router as payments_router
from .dashboard import router as dashboard_router
from .search import router as search_router
from .bulk import router as bulk_router
from .health import router as health_router
