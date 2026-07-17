# encargado de hablar con la base de datos, y realizar las operaciones CRUD (crear, leer, actualizar y eliminar) sobre los modelos de la base de datos. En este caso, el repositorio de cliente se encarga de manejar las operaciones relacionadas con el modelo Cliente.

from sqlalchemy.orm import Session
# coneccion actual con el modelo cliente (postgreSQL)
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

def create_cliente(
        db: Session,
        cliente_data: ClienteCreate,
        veterinaria_id: int
) -> Cliente:
    """
    Crea un nuevo cliente en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        cliente_data (ClienteCreate): Los datos del cliente a crear.
        veterinaria_id (int): El ID de la veterinaria asociada al cliente.

    Returns:
        Cliente: El cliente creado.
    """
    nuevoCliente = Cliente(
        nombre=cliente_data.nombre,
        telefono=cliente_data.telefono,
        email=cliente_data.email,
        veterinaria_id=veterinaria_id
    )
    db.add(nuevoCliente)
    db.commit()
    db.refresh(nuevoCliente)
    return nuevoCliente

def get_cliente(
        db: Session,
        cliente_id: int,
        veterinaria_id: int
) -> Cliente | None:
    """
    Obtiene un cliente específico de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        cliente_id (int): El ID del cliente a obtener.
        veterinaria_id (int): El ID de la veterinaria asociada al cliente.

    Returns:
        Cliente | None: El cliente encontrado o None si no se encuentra.
    """
    return db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.veterinaria_id == veterinaria_id
    ).first()

def get_clientes(
    db: Session,
    veterinaria_id: int
):
    return db.query(Cliente).filter(Cliente.veterinaria_id == veterinaria_id).all()

def update_cliente(
        db: Session,
        cliente_id: int,
        cliente_data: ClienteUpdate,
        veterinaria_id: int
) -> Cliente | None:
    """
    Actualiza un cliente existente en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        cliente_id (int): El ID del cliente a actualizar.
        cliente_data (ClienteUpdate): Los datos del cliente a actualizar.
        veterinaria_id (int): El ID de la veterinaria asociada al cliente.

    Returns:
        Cliente | None: El cliente actualizado o None si no se encuentra.
    """
    cliente = get_cliente(db, cliente_id, veterinaria_id)
    if not cliente:
        return None

    for key, value in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente  

def delete_cliente(
        db: Session,
        cliente_id: int,
        veterinaria_id: int
) -> bool:
    """
    Elimina un cliente de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        cliente_id (int): El ID del cliente a eliminar.
        veterinaria_id (int): El ID de la veterinaria asociada al cliente.

    Returns:
        bool: True si el cliente fue eliminado, False si no se encuentra.
    """
    cliente = get_cliente(db, cliente_id, veterinaria_id)
    if not cliente:
        return False

    db.delete(cliente)
    db.commit()
    return True 

def get_cliente_by_email(
    db: Session,
    email: str,
    veterinaria_id: int,
) -> Cliente | None:

    return (
        db.query(Cliente)
        .filter(
            Cliente.email == email,
            Cliente.veterinaria_id == veterinaria_id,
        )
        .first()
    )

"""la funcion de arriba es para futuramente buscar un cliente por su email, para evitar duplicados en la base de datos, y para poder enviarle notificaciones o recordatorios a los clientes por correo electrónico."""