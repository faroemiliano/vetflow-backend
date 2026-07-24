"""create vacunas and aplicaciones vacunas

Revision ID: 0f229937cbf6
Revises: 206edde8284d
Create Date: 2026-07-23 20:20:50.020876

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f229937cbf6"
down_revision: Union[str, Sequence[str], None] = "206edde8284d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    especieanimal = sa.Enum(
        "CANINO",
        "FELINO",
        "AVE",
        "EQUINO",
        "BOVINO",
        "CAPRINO",
        "OVINO",
        "PORCINO",
        "EXOTICO",
        "OTRO",
        name="especieanimal",
    )

    especieanimal.create(
        op.get_bind(),
        checkfirst=True,
    )


    op.create_table(
        "vacunas",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "nombre",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "descripcion",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "activo",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "veterinaria_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["veterinaria_id"],
            ["veterinarias.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
    )


    op.create_index(
        op.f("ix_vacunas_id"),
        "vacunas",
        ["id"],
        unique=False,
    )


    op.create_table(
        "aplicacion_vacunas",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "mascota_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "vacuna_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "fecha_aplicacion",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "fecha_proxima",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "observaciones",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "veterinaria_id",
            sa.Integer(),
            nullable=False,
        ),
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
        sa.ForeignKeyConstraint(
            ["mascota_id"],
            ["mascotas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacuna_id"],
            ["vacunas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["veterinaria_id"],
            ["veterinarias.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
    )


    op.create_index(
        op.f("ix_aplicacion_vacunas_id"),
        "aplicacion_vacunas",
        ["id"],
        unique=False,
    )


    op.execute(
        """
        UPDATE mascotas
        SET especie = 'CANINO'
        WHERE especie = 'Perrito'
        """
    )

    op.execute(
        """
        UPDATE mascotas
        SET especie = 'FELINO'
        WHERE especie = 'Gatito'
        """
    )

    op.execute(
        """
        ALTER TABLE mascotas
        ALTER COLUMN especie TYPE especieanimal
        USING especie::especieanimal
        """
    )


def downgrade() -> None:
    """Downgrade schema."""


    especieanimal = sa.Enum(
        "CANINO",
        "FELINO",
        "AVE",
        "EQUINO",
        "BOVINO",
        "CAPRINO",
        "OVINO",
        "PORCINO",
        "EXOTICO",
        "OTRO",
        name="especieanimal",
    )


    op.alter_column(
        "mascotas",
        "especie",
        existing_type=especieanimal,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
    )


    op.drop_index(
        op.f("ix_aplicacion_vacunas_id"),
        table_name="aplicacion_vacunas",
    )

    op.drop_table(
        "aplicacion_vacunas",
    )


    op.drop_index(
        op.f("ix_vacunas_id"),
        table_name="vacunas",
    )

    op.drop_table(
        "vacunas",
    )


    especieanimal.drop(
        op.get_bind(),
        checkfirst=True,
    )