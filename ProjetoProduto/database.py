from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

# conexão com o banco de dados sqlite: 
DATABASE_URL =  "sqlite:///./produtos.db"

# criar engine:
engine = create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False
})

# ssessão:
SessionLocal = sessionmaker(bind=engine)

# base para models:
Base = declarative_base()

# função para injetor sessão fastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db # coletar o database
    finally:
        db.close()