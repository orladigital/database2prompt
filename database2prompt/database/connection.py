from sqlalchemy import create_engine,inspect,text
from sqlalchemy.orm import sessionmaker


## criar variaveis de ambiente
## essa classe no futuro deve ser uma Strategy para adicionar outros bancos de forma mais fácil
DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/database_agent"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def list_tables():
    """Return all table names of database"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

