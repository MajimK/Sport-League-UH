from sqlmodel import SQLModel, create_engine, Session
from config import Config
from sqlalchemy import text
from sqlmodel import Session, select
from app.database.models.games import Games, League_games
from app.database.models.users import Users
from app.database.models.leagues import Leagues
from app.database.models.seasons import Season
from app.database.models.teams import Team
from app.database.models.players import Players, Teams_Player
from app.database.models.history import Season_league_team_player

DATABASE_URL = Config.DATABASE_URL

if not DATABASE_URL:
    DATABASE_URL =""

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Crea todas las tablas en la base de datos"""
    SQLModel.metadata.create_all(engine)

def drop_db():
    """Elimina todas las tablas con CASCADE"""
    
    with engine.connect() as conn:
        conn.execute(text("SET session_replication_role = 'replica';"))
        
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
        ))
        tables = [row[0] for row in result]
        
        print(f"📋 Tablas encontradas: {tables}")
        
        for table in tables:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE;'))
            print(f"  ✅ Eliminada: {table}")
        
        conn.execute(text("SET session_replication_role = 'origin';"))
        conn.commit()
    
    print("✅ Todas las tablas eliminadas con CASCADE")

def reset_db():
    """Resetea completamente la base de datos"""
    # SQLModel.metadata.clear()
    drop_db()
    init_db()


def get_session():
    with Session(engine) as session:
        yield session

def seed_data():
    with Session(engine) as session:
        # -------------------------
        # 1) Crear Deportes (Games)
        # -------------------------
        user = Users(username= "root", password="$pbkdf2-sha256$29000$AUCodU4pZcyZMwZAyJnzPg$4FHcWRF6Mmyf6tFLTeL7nOsxLOMG7WXCCwpYh8XoHw8",
                     email= "root@rect.uh.cu", is_admin=True)
        session.add(user)

        # Lista existente más la nueva lista de juegos solicitada
        juegos_nuevos = [
            "Kickingball femenino",
            "Handball masculino",
            "Tracción de la soga",
            "Tragabolas",
            "Lanzamiento de dardos",
            "Dominó",
            "Carrera de sacos",
            "Anillas",
            "Juegos mixtos"
        ]

        # Juegos originales de la semilla
        juegos_originales = [
            Games(name="Fútbol"),
            Games(name="Baloncesto"),
            Games(name="Voleibol")
        ]

        # Combinar ambas listas
        juegos_originales.extend([Games(name=juego) for juego in juegos_nuevos])
        games_list = juegos_originales

        for game in games_list:
            if not session.exec(select(Games).where(Games.name == game.name)).first():
                session.add(game)

        session.commit()

        # Obtener los deportes para usar luego (solo necesitamos los originales aquí)
        futbol = session.exec(select(Games).where(Games.name == "Fútbol")).first()
        basket = session.exec(select(Games).where(Games.name == "Baloncesto")).first()
        voley = session.exec(select(Games).where(Games.name == "Voleibol")).first()

        # -------------------------
        # 2) Crear Ligas (el resto del código original se mantiene igual)
        # -------------------------
        leagues_list = [
            Leagues(
                name="Liga de Invierno",
                description="Competencia oficial del invierno",
                initial_date=1,
                final_date=3,
            ),
            Leagues(
                name="Liga de Verano",
                description="Competencia oficial del verano",
                initial_date=6,
                final_date=8,
            )
        ]

        for league in leagues_list:
            if not session.exec(select(Leagues).where(Leagues.name == league.name)).first():
                session.add(league)

        session.commit()

        invierno = session.exec(select(Leagues).where(Leagues.name == "Liga de Invierno")).first()
        verano = session.exec(select(Leagues).where(Leagues.name == "Liga de Verano")).first()

        # -------------------------
        # 3) League-Games
        # -------------------------
        league_games = [
            League_games(league_id=invierno.league_id, game_id=futbol.game_id),
            League_games(league_id=invierno.league_id, game_id=basket.game_id),
            League_games(league_id=verano.league_id, game_id=voley.game_id),
        ]

        for lg in league_games:
            exists = session.exec(
                select(League_games).where(
                    (League_games.league_id == lg.league_id) &
                    (League_games.game_id == lg.game_id)
                )
            ).first()
            if not exists:
                session.add(lg)

        session.commit()

        # -------------------------
        # 4) Seasons
        # -------------------------
        seasons_list = [
            Season(curso="2023-2024"),
            Season(curso="2025-2026")
        ]

        for season in seasons_list:
            if not session.exec(select(Season).where(Season.curso == season.curso)).first():
                session.add(season)

        session.commit()

        print("🌱 Base de datos sembrada con éxito! (incluye nuevos juegos)")
