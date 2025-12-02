from sqlmodel import SQLModel, create_engine, Session
from config import Config
from sqlalchemy import text

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
    drop_db()
    init_db()


def get_session():
    with Session(engine) as session:
        yield session
