from sqlmodel import Session, select, and_
from app.database.models.leagues import Leagues
from app.database.models.seasons import Season
from app.database.models.history import Season_league_team_player
from app.database.models.players import Players, Teams_Player
from app.database.models.teams import Team

from app.schemas.contracts import ContractCreate
from app.schemas.utils import AddPlayersRequest


def get_contract(contract: ContractCreate, session:Session):
    query = (select(Season_league_team_player)
             .where(
                 and_(
                    Season_league_team_player.season_id == contract.season_id,
                    Season_league_team_player.league_id == contract.league_id,
                    Season_league_team_player.team_id == contract.team_id,  
                    Season_league_team_player.player_id == contract.player_id
                    )))
    
    existing_contract = session.exec(query).first()
    return existing_contract

def get_all_teams_season_league(season_id: int, league_id: int, session: Session):
    query = (select(Team)
             .join(Season_league_team_player)
             .where(
                 and_(Season_league_team_player.season_id == season_id,
                      Season_league_team_player.league_id == league_id)
             )).distinct()
    teams = session.exec(query).all()
    return teams

def save_contract(contract: ContractCreate, session: Session):
    existing_contract = get_contract(contract, session)

    if existing_contract:
        raise ValueError("El equipo ya esta creado")
    
    db_contract = Season_league_team_player.from_orm(contract)
    session.add(db_contract)
    session.commit()
    session.refresh(db_contract)
    return db_contract


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
