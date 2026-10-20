
from pathlib import Path

from sqlmodel import Session, create_engine


# Caminho absoluto para o banco SQLite
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'database.db'}"

# Conexão com o banco
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Disponibiliza uma sessão para as rotas da API
def get_session():
    with Session(engine) as session:
        yield session
