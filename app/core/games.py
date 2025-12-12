from sqlmodel import Session, select
from app.database.models.games import Games

def get_all_sports(session: Session):
    query = select(Games).limit(100)
    sports = session.exec(query).all()
    return sports

def get_sport_by_name(name: str, session:Session):
    query = select(Games).where(Games.name == name)
    sport = session.exec(query).first()
    return sport