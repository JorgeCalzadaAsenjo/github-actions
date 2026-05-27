from routes.auth import router as auth_router
from routes.items import router as item_router
from routes.users import router as user_router

__all__ = ["auth_router", "item_router", "user_router"]
