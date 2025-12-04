from sqlmodel import Session, select
from app.database.models.seasons import Season
from app.database.models.leagues import Leagues
from app.database.models.history import Season_league_team_player
from app.database.models.players import Players
from app.database.models.teams import Team
from app.schemas.season import SeasonCreate


def get_season_by_id(season_id: int, session: Session):
    query = select(Season).where(Season.season_id == season_id)
    season = session.exec(query).first()
    return season

def get_season_by_year(season_year: str, session: Session):
    query = select(Season).where(Season.curso == season_year)
    season = session.exec(query).first()
    return season

def get_all_seasons(session: Session):
    query = select(Season).limit(100)
    season = session.exec(query).all()
    return season

def save_season(season: SeasonCreate, session: Session):
    existing_season = get_season_by_year(season.curso, session)

    if existing_season:
        raise ValueError("El equipo ya esta creado")
    
    db_season = Season.from_orm(season)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season


def get_players_by_season(season_id: int, session: Session):
    season = session.get(Season, season_id)
    if not season:
        return None
    
    query = ( select(Players)
            .join(Season_league_team_player)
            .where(Season_league_team_player.season_id == season_id)
            .distinct()
            )
    players_season = session.exec(query).all()
    return players_season


def get_teams_by_season(season_id: int, session: Session):
    season = session.get(Season, season_id)
    if not season:
        return None
    
    query = ( select(Team)
            .join(Season_league_team_player)
            .where(Season_league_team_player.season_id == season_id)
            .distinct()
            )
    teams_season = session.exec(query).all()
    return teams_season

def get_leagues_by_season(season_id: int, session: Session):
    season = session.get(Season, season_id)
    if not season:
        return None
    
    query = ( select(Leagues)
            .join(Season_league_team_player)
            .where(Season_league_team_player.season_id == season_id)
            .distinct()
            )
    seasons_league = session.exec(query).all()
    return seasons_league
