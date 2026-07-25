from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import ViaAdministracion

if TYPE_CHECKING:
    from app.models.recetas import Receta


class RecetaMedicamento(Base):
    __tablename__ = "receta_medicamentos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    receta_id: Mapped[int] = mapped_column(
        ForeignKey("recetas.id"),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    presentacion: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    dosis: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    frecuencia: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    duracion: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    via_administracion: Mapped[ViaAdministracion] = mapped_column(
        Enum(ViaAdministracion),
        nullable=False,
    )

    observaciones: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    receta: Mapped["Receta"] = relationship(
        back_populates="medicamentos",
    )