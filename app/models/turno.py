from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Index, String, ForeignKey, DateTime, func,Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import EstadoTurno



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
        DateTime(timezone=True),
        nullable=False
    )

    motivo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    estado: Mapped[EstadoTurno] = mapped_column(
        SQLEnum(EstadoTurno),
        default=EstadoTurno.PENDIENTE,
        nullable=False,
    )

    mascota_id: Mapped[int] = mapped_column(
        ForeignKey("mascotas.id"),
        nullable=False
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )

    

    observaciones: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
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



    mascota: Mapped["Mascota"] = relationship(
        back_populates="turnos"
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="turnos"
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="turnos"
    )
    
    __table_args__ = (
        Index(
            "ix_turnos_veterinaria_fecha",
            "veterinaria_id",
            "fecha_hora",
        ),
    )