from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.mascota import Mascota
    from app.models.veterinaria import Veterinaria
    from app.models.factura import Factura


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False
    )


    mascotas: Mapped[list["Mascota"]] = relationship(
        back_populates="cliente"
    )


    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="clientes"
    )


    facturas: Mapped[list["Factura"]] = relationship(
        back_populates="cliente"
    )