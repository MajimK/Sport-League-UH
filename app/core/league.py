from sqlmodel import Session, select
from app.database.models.leagues import Leagues
from app.database.models.seasons import Season
from app.database.models.history import Season_league_team_player
from app.database.models.players import Players, Teams_Player
from app.database.models.teams import Team

from app.schemas.leagues import LeagueCreate
from app.schemas.utils import AddPlayersRequest


def get_league_by_id(league_id: int, session: Session):
    query = select(Leagues).where(Leagues.league_id == league_id)
    league = session.exec(query).first()
    return league

def get_league_by_name(league_name: str, session: Session):
    query = select(Leagues).where(Leagues.name == league_name)
    league = session.exec(query).first()
    return league

def get_all_leagues(session: Session):
    query = select(Leagues).limit(100)
    league = session.exec(query).all()
    return league

def save_league(league: LeagueCreate, session: Session):
    existing_league = get_league_by_name(league.name, session)

    if existing_league:
        raise ValueError("El equipo ya esta creado")
    
    db_league = Leagues.from_orm(league)
    session.add(db_league)
    session.commit()
    session.refresh(db_league)
    return db_league


def get_players_by_league(league_id: int, session: Session):
    league = session.get(Leagues, league_id)
    if not league:
        return None
    
    query = ( select(Players)
            .join(Season_league_team_player)
            .where(Season_league_team_player.league_id == league_id)
            .distinct()
            )
    players_league = session.exec(query).all()
    return players_league


def get_teams_by_league(league_id: int, session: Session):
    league = session.get(Leagues, league_id)
    if not league:
        return None
    
    query = ( select(Team)
            .join(Season_league_team_player)
            .where(Season_league_team_player.league_id == league_id)
            .distinct()
            )
    teams_league = session.exec(query).all()
    return teams_league

def get_seasons_by_league(league_id: int, session: Session):
    league = session.get(Leagues, league_id)
    if not league:
        return None
    
    query = ( select(Season)
            .join(Season_league_team_player)
            .where(Season_league_team_player.league_id == league_id)
            .distinct()
            )
    seasons_league = session.exec(query).all()
    return seasons_league
