from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.historia_clinica import HistoriaClinica
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria


class Estudio(Base):

    __tablename__ = "estudios"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    historia_clinica_id: Mapped[int] = mapped_column(
        ForeignKey("historias_clinicas.id"),
        nullable=False,
    )


    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )


    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )


    tipo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )


    resultado: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    fecha_realizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


    historia_clinica: Mapped["HistoriaClinica"] = relationship(
        back_populates="estudios",
    )


    usuario: Mapped["Usuario"] = relationship(
        back_populates="estudios",
    )


    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="estudios",
    )