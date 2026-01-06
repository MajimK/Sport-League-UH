from fastapi import APIRouter
from .users.matches import router as matches_routes

users_router = APIRouter(tags=["admin"])

users_router.include_router(matches_routes)
