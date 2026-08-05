"""add estado to facturas

Revision ID: 929691a7b6fd
Revises: 69a5a986d66e
Create Date: 2026-07-31 16:53:21.490611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '929691a7b6fd'
down_revision: Union[str, Sequence[str], None] = '69a5a986d66e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    estado_factura = postgresql.ENUM(
        "PENDIENTE",
        "PARCIAL",
        "PAGADA",
        "ANULADA",
        name="estadofactura",
    )

    estado_factura.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "facturas",
        sa.Column(
            "estado",
            estado_factura,
            nullable=False,
            server_default="PENDIENTE",
        ),
    )

    op.alter_column(
        "facturas",
        "estado",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column(
        "facturas",
        "estado",
    )

    estado_factura = postgresql.ENUM(
        "PENDIENTE",
        "PARCIAL",
        "PAGADA",
        "ANULADA",
        name="estadofactura",
    )

    estado_factura.drop(op.get_bind(), checkfirst=True)

