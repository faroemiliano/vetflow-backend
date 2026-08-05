from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.cliente import Cliente
    from app.models.mascota import Mascota
    from app.models.turno import Turno
    from app.models.vacuna import Vacuna
    from app.models.aplicacion_vacuna import AplicacionVacuna
    from app.models.receta_medicamento import Receta
    from app.models.estudio_medico import Estudio
    from app.models.adjunto import Adjunto
    from app.models.factura import Factura
    from app.models.pago import Pago
    from app.models.caja import Caja
    from app.models.movimiento_caja import MovimientoCaja

class Veterinaria(Base):
    __tablename__ = "veterinarias"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    usuarios: Mapped[list["Usuario"]] = relationship(
    back_populates="veterinaria"
)
    
    clientes: Mapped[list["Cliente"]] = relationship(
    back_populates="veterinaria"
)
    
    mascotas: Mapped[list["Mascota"]] = relationship(
    back_populates="veterinaria"
)
    
    turnos: Mapped[list["Turno"]] = relationship(
    back_populates="veterinaria"
)
    
    vacunas: Mapped[list["Vacuna"]] = relationship(
    back_populates="veterinaria"
)

    aplicaciones_vacunas: Mapped[list["AplicacionVacuna"]] = relationship(
    back_populates="veterinaria"
)
    
    recetas: Mapped[list["Receta"]] = relationship(
        back_populates="veterinaria"
    )

    estudios: Mapped[list["Estudio"]] = relationship(
        back_populates="veterinaria",
    )

    adjuntos: Mapped[list["Adjunto"]] = relationship(
        back_populates="veterinaria",
    )

    facturas: Mapped[list["Factura"]] = relationship(
        back_populates="veterinaria",
    )

    pagos: Mapped[list["Pago"]] = relationship(
        back_populates="veterinaria",
    )

    cajas: Mapped[list["Caja"]] = relationship(
        back_populates="veterinaria",
    )

    movimientos_caja: Mapped[list["MovimientoCaja"]] = relationship(
        back_populates="veterinaria",
    )

    gastos: Mapped[list["Gasto"]] = relationship(
        back_populates="veterinaria",
    )