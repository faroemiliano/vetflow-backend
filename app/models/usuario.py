from sqlalchemy import String, Boolean, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum as PyEnum

from app.database.base import Base

from datetime import datetime
from sqlalchemy import DateTime, func

from typing import TYPE_CHECKING

from app.models.enums import RolUsuario

if TYPE_CHECKING:
    from app.models.veterinaria import Veterinaria
    from app.models.turno import Turno
    from app.models.historia_clinica import HistoriaClinica
    from app.models.recetas import Receta



class Usuario(Base):
    __tablename__ = "usuarios"

    __table_args__ = (
        UniqueConstraint(
            "email",
            "veterinaria_id",
            name="uq_usuario_email_veterinaria",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apellido: Mapped[str] = mapped_column(
    String(100),
    nullable=False
)

    telefono: Mapped[str | None] = mapped_column(
    String(30),
    nullable=True
)

    email: Mapped[str] = mapped_column(
        String(150),
        
        nullable=False
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )   

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    rol: Mapped[RolUsuario] = mapped_column(
        Enum(RolUsuario),
        default=RolUsuario.RECEPCIONISTA,
        nullable=False,
    )

    foto_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    google_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
    back_populates="usuarios"
    )
    
    turnos: Mapped[list["Turno"]] = relationship(
    back_populates="usuario"
    )

    historias_clinicas: Mapped[list["HistoriaClinica"]] = relationship(
        back_populates="usuario"
    )

    recetas: Mapped[list["Receta"]] = relationship(
        back_populates="usuario"
    )

    estudios: Mapped[list["Estudio"]] = relationship(
        back_populates="usuario",
    )