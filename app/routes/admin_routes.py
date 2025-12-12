from fastapi import APIRouter
from .admin.teams import router as teams_router
from .admin.players import router as players_router
from .admin.leagues import router as league_router
from .admin.seasons import router as season_router
from .admin.games import router as game_router
from .contracts import router as contract_router
from .admin.form import router as forms_router
# from .tournaments import router as tournaments_router
# from .matches import router as matches_router
# from .results import router as results_router

admin_router = APIRouter(tags=["admin"])

admin_router.include_router(teams_router)
admin_router.include_router(players_router)
admin_router.include_router(season_router)
admin_router.include_router(league_router)
admin_router.include_router(contract_router)
admin_router.include_router(game_router)
admin_router.include_router(forms_router)
# admin_router.include_router(tournaments_router)
# admin_router.include_router(matches_router)
# admin_router.include_router(results_router)
