from datetime import datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AplicacionVacuna(Base):

    __tablename__ = "aplicacion_vacunas"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    mascota_id: Mapped[int] = mapped_column(
        ForeignKey("mascotas.id"),
        nullable=False,
    )


    vacuna_id: Mapped[int] = mapped_column(
        ForeignKey("vacunas.id"),
        nullable=False,
    )


    fecha_aplicacion: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
    )


    fecha_proxima: Mapped[Optional[datetime]] = mapped_column(
        Date,
        nullable=True,
    )


    observaciones: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )


    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
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
        nullable=False,
    )


    # Relaciones

    mascota: Mapped["Mascota"] = relationship(
        "Mascota",
        back_populates="aplicaciones_vacunas",
    )


    vacuna: Mapped["Vacuna"] = relationship(
        "Vacuna",
        back_populates="aplicaciones",
    )


    veterinaria: Mapped["Veterinaria"] = relationship(
        "Veterinaria",
        back_populates="aplicaciones_vacunas",
    )