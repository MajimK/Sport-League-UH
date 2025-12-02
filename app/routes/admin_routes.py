from fastapi import APIRouter
from .admin.teams import router as teams_router
from .admin.players import router as players_router
# from .tournaments import router as tournaments_router
# from .matches import router as matches_router
# from .results import router as results_router

admin_router = APIRouter(tags=["admin"])

admin_router.include_router(teams_router)
admin_router.include_router(players_router)
# admin_router.include_router(tournaments_router)
# admin_router.include_router(matches_router)
# admin_router.include_router(results_router)
