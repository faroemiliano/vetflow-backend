from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories.cliente_repository import (
    create_cliente,
    delete_cliente,
    get_cliente,
    get_cliente_by_email,
    get_clientes,
    update_cliente,
)
from app.schemas.cliente_schemas import ClienteCreate, ClienteUpdate


def create_cliente_service(
    db: Session,
    cliente_data: ClienteCreate,
    veterinaria_id: int,
) -> Cliente:
    """
    Crea un cliente validando que el email no exista
    dentro de la misma veterinaria.
    """

    if cliente_data.email:
        cliente_existente = get_cliente_by_email(
            db,
            cliente_data.email,
            veterinaria_id,
        )

        if cliente_existente:
            raise ValueError("Ya existe un cliente con ese email.")

    return create_cliente(db, cliente_data, veterinaria_id)


def get_cliente_service(
    db: Session,
    cliente_id: int,
    veterinaria_id: int,
) -> Cliente:
    """
    Obtiene un cliente por ID.
    """

    cliente = get_cliente(db, cliente_id, veterinaria_id)

    if cliente is None:
        raise ValueError("Cliente no encontrado.")

    return cliente


def get_clientes_service(
    db: Session,
    veterinaria_id: int,
) -> list[Cliente]:
    """
    Obtiene todos los clientes de una veterinaria.
    """

    return get_clientes(db, veterinaria_id)


def update_cliente_service(
    db: Session,
    cliente_id: int,
    cliente_data: ClienteUpdate,
    veterinaria_id: int,
) -> Cliente:
    """
    Actualiza un cliente.
    """

    cliente = get_cliente(db, cliente_id, veterinaria_id)

    if cliente is None:
        raise ValueError("Cliente no encontrado.")

    # Validar email duplicado solo si se intenta modificar
    if (
        cliente_data.email
        and cliente_data.email != cliente.email
    ):
        cliente_existente = get_cliente_by_email(
            db,
            cliente_data.email,
            veterinaria_id,
        )

        if cliente_existente:
            raise ValueError("Ya existe un cliente con ese email.")

    return update_cliente(
        db,
        cliente_id,
        cliente_data,
        veterinaria_id,
    )


def delete_cliente_service(
    db: Session,
    cliente_id: int,
    veterinaria_id: int,
) -> bool:
    """
    Elimina un cliente.
    """

    cliente = get_cliente(db, cliente_id, veterinaria_id)

    if cliente is None:
        raise ValueError("Cliente no encontrado.")

    return delete_cliente(
        db,
        cliente_id,
        veterinaria_id,
    )