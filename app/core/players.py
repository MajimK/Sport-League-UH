from sqlmodel import Session, select
from app.database.models.players import Players
from app.schemas.players import PlayerCreate

def get_player_by_id(player_id: int, session: Session):
    query = select(Players).where(Players.player_id == player_id)
    team = session.exec(query).first()
    return team

def get_player_by_CI(player_ci: str, session: Session):
    query = select(Players).where(Players.CI == player_ci)
    player = session.exec(query).first()
    return player

def get_all_players(session: Session):
    query = select(Players).limit(100)
    players = session.exec(query).all()
    return players

def save_player(player: PlayerCreate, session: Session):
    existing_player = get_player_by_CI(player.name, session)
    if existing_player:
        raise ValueError("El deportista ya existe")

    db_player = Players.from_orm(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

def get_teams_by_player(player_id: int, session: Session):
    player = session.get(Players, player_id)
    if not player:
        return None
    return player.team


