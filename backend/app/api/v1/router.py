from fastapi import APIRouter
from app.tables.router import router as tables_router
from app.users.router import router as users_router
from app.products.router import router as products_router
from app.orders.router import router as orders_router
from app.tenants.router import router as tenants_router
from app.auth.router import router as auth_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)

api_router.include_router(tables_router)
api_router.include_router(tenants_router)
api_router.include_router(auth_router)