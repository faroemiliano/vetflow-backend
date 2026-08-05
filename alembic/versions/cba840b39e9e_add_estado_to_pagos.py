"""add estado to pagos

Revision ID: cba840b39e9e
Revises: 830244f89ba8
Create Date: 2026-07-31 18:41:29.045733
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'cba840b39e9e'
down_revision: Union[str, Sequence[str], None] = '830244f89ba8'
branch_labels = None
depends_on = None


def upgrade() -> None:

    estado_pago = postgresql.ENUM(
        "ACTIVO",
        "ANULADO",
        name="estadopago",
    )

    estado_pago.create(
        op.get_bind(),
        checkfirst=True,
    )


    op.add_column(
        "pagos",
        sa.Column(
            "estado",
            estado_pago,
            nullable=False,
            server_default="ACTIVO",
        ),
    )


    op.alter_column(
        "pagos",
        "estado",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column(
        "pagos",
        "estado",
    )

    estado_pago = postgresql.ENUM(
        "ACTIVO",
        "ANULADO",
        name="estadopago",
    )

    estado_pago.drop(
        op.get_bind(),
        checkfirst=True,
    )