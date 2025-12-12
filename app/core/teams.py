from sqlmodel import Session, select
from app.database.models.teams import Team
from app.database.models.players import Players, Teams_Player
from app.schemas.teams import TeamCreate, TempTeam
from app.schemas.utils import AddPlayersRequest
from app.core.games import get_sport_by_name


def get_teams_by_id(team_id: int, session: Session):
    query = select(Team).where(Team.team_id == team_id)
    team = session.exec(query).first()
    return team

def get_teams_by_name(team_name: str, session: Session):
    query = select(Team).where(Team.name == team_name)
    team = session.exec(query).first()
    return team

def get_all_teams(session: Session):
    query = select(Team).limit(100)
    teams = session.exec(query).all()
    return teams

def save_team(team: TeamCreate, session: Session):
    existing_team = get_teams_by_name(team.name, session)

    if existing_team:
        raise ValueError("El equipo ya esta creado")
    
    existing_sport = get_sport_by_name(team.game_name, session)
    if not existing_sport:
        raise ValueError("Ese deporte no existe")
    
    team_with_game_id = {
        "name": team.name,
        "description": team.description,
        "game_id": existing_sport.game_id
    }
    
    temp_team = TempTeam(**team_with_game_id)
    
    db_team = Team.from_orm(temp_team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

def get_players_by_team(team_id: int, session: Session):
    team = session.get(Team, team_id)
    if not team:
        return None
    return team.players

def add_players_to_team(team_id: int, body: AddPlayersRequest, session: Session):
    response = {"added": [], "skipped": [{}]}

    for player_id in body.players:
        player = session.get(Players, player_id)
        if not player:
            response["skipped"].append({"player_id": player_id, "reason": "El jugador no existe en la base de datos"})
            continue

        exist_query = select(Teams_Player).where(Teams_Player.team_id == team_id,
                                                 Teams_Player.player_id == player_id)
        
        exist_player = session.exec(exist_query).first()
        if exist_player:
            response["skipped"].append({"player_id": player_id, "reason": "El jugador ya existe en el equipo"})
            continue

        link = Teams_Player(team_id=team_id, player_id=player_id)
        response["added"].append(player_id)
        session.add(link)
        session.commit()
        session.refresh(link)
    
    return response
