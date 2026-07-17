from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Turno(Base):
    __tablename__ = "turnos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    motivo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        default="pendiente",
        nullable=False
    )

    mascota_id: Mapped[int] = mapped_column(
        ForeignKey("mascotas.id"),
        nullable=False
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )

    mascota: Mapped["Mascota"] = relationship(
        back_populates="turnos"
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="turnos"
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="turnos"
    )
    