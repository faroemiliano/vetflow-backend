from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class HistoriaClinica(Base):

    __tablename__ = "historias_clinicas"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    mascota_id: Mapped[int] = mapped_column(
        ForeignKey("mascotas.id"),
        nullable=False
    )


    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )


    diagnostico: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    tratamiento: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )


    mascota: Mapped["Mascota"] = relationship(
        back_populates="historias_clinicas"
    )


    usuario: Mapped["Usuario"] = relationship(
        back_populates="historias_clinicas"
    )