from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum

from app.database.base import Base

from datetime import datetime
from sqlalchemy import DateTime, func

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.veterinaria import Veterinaria
    from app.models.turno import Turno

class RolUsuario(str, Enum):
    ADMIN = "admin"
    VETERINARIO = "veterinario"
    RECEPCIONISTA = "recepcionista"


class Usuario(Base):
    __tablename__ = "usuarios"

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

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
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
        default=RolUsuario.RECEPCIONISTA,
        nullable=False
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