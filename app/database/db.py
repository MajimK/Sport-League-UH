from sqlmodel import SQLModel, create_engine, Session
from config import Config

DATABASE_URL = Config.DATABASE_URL

if not DATABASE_URL:
    DATABASE_URL =""

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session
