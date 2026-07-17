from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Veterinaria(Base):
    __tablename__ = "veterinarias"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    usuarios: Mapped[list["Usuario"]] = relationship(
    back_populates="veterinaria"
)
    
    clientes: Mapped[list["Cliente"]] = relationship(
    back_populates="veterinaria"
)
    
    mascotas: Mapped[list["Mascota"]] = relationship(
    back_populates="veterinaria"
)
    
    turnos: Mapped[list["Turno"]] = relationship(
    back_populates="veterinaria"
)