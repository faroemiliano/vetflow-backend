from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# aqui cada request que se haga a la base de datos, se creara una nueva sesion de base de datos y se cerrara al finalizar la peticion. Esto es importante para evitar problemas de concurrencia y mantener la integridad de los datos.