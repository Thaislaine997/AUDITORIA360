from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use uma variável de ambiente para a URL do banco de dados, com um fallback para SQLite em memória.
# Para produção, você configuraria DATABASE_URL para apontar para seu banco de dados real (PostgreSQL, MySQL, etc.)
# Exemplo para PostgreSQL: "postgresql://user:password@host:port/database"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") # Usando um arquivo SQLite para persistência local simples

engine = create_engine(
    DATABASE_URL,
    # connect_args são necessários apenas para SQLite para permitir o uso em múltiplos threads (como no FastAPI)
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db_session_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Você pode adicionar funções aqui para criar todas as tabelas no banco de dados
# Exemplo:
# def create_db_and_tables():
#     Base.metadata.create_all(bind=engine)
