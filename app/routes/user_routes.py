from fastapi import APIRouter
from .users.matches import router as matches_routes
from .users.players import router as players_routes

users_router = APIRouter(tags=["admin"])

users_router.include_router(matches_routes)
users_router.include_router(players_routes)
