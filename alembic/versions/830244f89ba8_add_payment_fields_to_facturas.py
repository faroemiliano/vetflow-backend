"""add payment fields to facturas

Revision ID: 830244f89ba8
Revises: 929691a7b6fd
Create Date: 2026-07-31 17:20:51.130472

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "830244f89ba8"
down_revision: Union[str, Sequence[str], None] = "929691a7b6fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pagos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("factura_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("veterinaria_id", sa.Integer(), nullable=False),
        sa.Column("monto", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "metodo_pago",
            sa.Enum(
                "EFECTIVO",
                "TARJETA",
                "TRANSFERENCIA",
                "MERCADO_PAGO",
                "OTRO",
                name="metodopago",
            ),
            nullable=False,
        ),
        sa.Column("observaciones", sa.String(1000), nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["factura_id"], ["facturas.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["veterinaria_id"], ["veterinarias.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_pagos_id"),
        "pagos",
        ["id"],
        unique=False,
    )

    op.add_column(
        "facturas",
        sa.Column(
            "total_pagado",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "facturas",
        sa.Column(
            "saldo_pendiente",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0",
        ),
    )

    op.execute(
        """
        UPDATE facturas
        SET
            total_pagado = 0,
            saldo_pendiente = total
        """
    )

    op.alter_column(
        "facturas",
        "total_pagado",
        server_default=None,
    )

    op.alter_column(
        "facturas",
        "saldo_pendiente",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "facturas",
        "saldo_pendiente",
    )

    op.drop_column(
        "facturas",
        "total_pagado",
    )

    op.drop_index(
        op.f("ix_pagos_id"),
        table_name="pagos",
    )

    op.drop_table("pagos")