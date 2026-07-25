from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.historia_clinica import HistoriaClinica
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria
    from app.models.receta_medicamento import RecetaMedicamento


class Receta(Base):
    __tablename__ = "recetas"

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

    indicaciones_generales: Mapped[str | None] = mapped_column(
        String(1000),
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
        back_populates="recetas",
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="recetas",
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="recetas",
    )

    medicamentos: Mapped[list["RecetaMedicamento"]] = relationship(
        back_populates="receta",
        cascade="all, delete-orphan",
    )


