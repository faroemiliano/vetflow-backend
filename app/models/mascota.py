from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.turno import Turno
    from app.models.veterinaria import Veterinaria

class Mascota(Base):
    __tablename__ = "mascotas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    especie: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    raza: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    edad: Mapped[int | None] = mapped_column(
        nullable=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=False
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )

    cliente: Mapped["Cliente"] = relationship(
        back_populates="mascotas"
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="mascotas"
    )

    turnos: Mapped[list["Turno"]] = relationship(
        back_populates="mascota"
    )

    