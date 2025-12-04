from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.database.db import init_db,reset_db
from app.database.db import seed_data
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from sqlmodel import Session
# Importar routers
from app.routes.admin_routes import admin_router
# from app.routes.user import router as user_router
from app.routes.auth import router as auth_router



app = FastAPI(
    title="Sport League UH",
    description="Backend migrado desde Flask a FastAPI",
    version="1.0.0"
)

# CORS (importante porque tu frontend será separado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# # Registrar routers
# app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación"""
    reset_db()
    seed_data()

@app.get("/")
def root():
    return {"message": "Backend FastAPI funcionando correctamente"}
