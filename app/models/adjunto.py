from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.historia_clinica import HistoriaClinica
    from app.models.estudio_medico import Estudio
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria


class Adjunto(Base):

    __tablename__ = "adjuntos"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    historia_clinica_id: Mapped[int] = mapped_column(
        ForeignKey("historias_clinicas.id"),
        nullable=False,
    )


    estudio_id: Mapped[int | None] = mapped_column(
        ForeignKey("estudios.id"),
        nullable=True,
    )


    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )


    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )


    nombre_archivo: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    ruta_archivo: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )


    tipo_archivo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    tamano: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )


    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
        back_populates="adjuntos",
    )


    estudio: Mapped["Estudio | None"] = relationship(
        back_populates="adjuntos",
    )


    usuario: Mapped["Usuario"] = relationship(
        back_populates="adjuntos",
    )


    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="adjuntos",
    )