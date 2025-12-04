from sqlmodel import SQLModel, create_engine, Session
from config import Config
from sqlalchemy import text
from sqlmodel import Session, select
from app.database.models.games import Games, League_games
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
        games_list = [
            Games(name="Fútbol"),
            Games(name="Baloncesto"),
            Games(name="Voleibol")
        ]

        for game in games_list:
            if not session.exec(select(Games).where(Games.name == game.name)).first():
                session.add(game)

        session.commit()

        futbol = session.exec(select(Games).where(Games.name == "Fútbol")).first()
        basket = session.exec(select(Games).where(Games.name == "Baloncesto")).first()
        voley  = session.exec(select(Games).where(Games.name == "Voleibol")).first()

        # -------------------------
        # 2) Crear Ligas
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
            Season(curso="2024-2025")
        ]

        for season in seasons_list:
            if not session.exec(select(Season).where(Season.curso == season.curso)).first():
                session.add(season)

        session.commit()

        # -------------------------
        # 5) Teams
        # -------------------------
        teams_list = [
            Team(name="Tigres FC", description="Equipo de fútbol", game_id=futbol.game_id),
            Team(name="Leones BC", description="Equipo de baloncesto", game_id=basket.game_id),
            Team(name="Panteras VB", description="Equipo de voleibol", game_id=voley.game_id),
        ]

        for team in teams_list:
            if not session.exec(select(Team).where(Team.name == team.name)).first():
                session.add(team)

        session.commit()

        tigres = session.exec(select(Team).where(Team.name == "Tigres FC")).first()
        leones = session.exec(select(Team).where(Team.name == "Leones BC")).first()
        panteras = session.exec(select(Team).where(Team.name == "Panteras VB")).first()

        # -------------------------
        # 6) Players
        # -------------------------
        players_list = [
            Players(CI="111111", name="Carlos Torres", faculty="Informatica"),
            Players(CI="222222", name="Luis Perez", faculty="Matematica"),

            Players(CI="333333", name="Jose Diaz", faculty="Fisica"),
            Players(CI="444444", name="Pedro Lopez", faculty="Historia"),

            Players(CI="555555", name="Miguel Ruiz", faculty="Biologia"),
            Players(CI="666666", name="Juan Gomez", faculty="Quimica"),
        ]

        for p in players_list:
            if not session.exec(select(Players).where(Players.CI == p.CI)).first():
                session.add(p)

        session.commit()

        # -------------------------
        # 7) Assign players to teams
        # -------------------------
        Carlos, Luis, Jose, Pedro, Miguel, Juan = session.exec(select(Players)).all()

        tp_list = [
            Teams_Player(player_id=Carlos.player_id, team_id=tigres.team_id),
            Teams_Player(player_id=Luis.player_id, team_id=tigres.team_id),

            Teams_Player(player_id=Jose.player_id, team_id=leones.team_id),
            Teams_Player(player_id=Pedro.player_id, team_id=leones.team_id),

            Teams_Player(player_id=Miguel.player_id, team_id=panteras.team_id),
            Teams_Player(player_id=Juan.player_id, team_id=panteras.team_id),
        ]

        for tp in tp_list:
            exists = session.exec(
                select(Teams_Player).where(
                    (Teams_Player.player_id == tp.player_id) &
                    (Teams_Player.team_id == tp.team_id)
                )
            ).first()

            if not exists:
                session.add(tp)

        session.commit()

        print("🌱 Base de datos sembrada con éxito!")
