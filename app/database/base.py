from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# aqui creamos la clase base para todos los modelos de la base de datos, 
# que hereda de DeclarativeBase
#  de SQLAlchemy. Esto nos permite definir nuestras tablas y relaciones en la 
# base de datos utilizando clases de Python.

# Importar todos los modelos para que SQLAlchemy registre las tablas
from app.models import *  # noqa: F401,F403