from typing import List, Optional

from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Vacuna(Base):

    __tablename__ = "vacunas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )


    # Relaciones

    veterinaria: Mapped["Veterinaria"] = relationship(
        "Veterinaria",
        back_populates="vacunas",
    )

    aplicaciones: Mapped[List["AplicacionVacuna"]] = relationship(
        "AplicacionVacuna",
        back_populates="vacuna",
    )