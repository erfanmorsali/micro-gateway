from fastapi import APIRouter

from apis.endpoints import users, addresses

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(addresses.router)
