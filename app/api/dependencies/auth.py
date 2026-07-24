from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import get_usuario_id_from_token
from app.database.session import get_db
from app.models.usuario import RolUsuario, Usuario


bearer_scheme = HTTPBearer()



def get_current_user(
    credenciales: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        usuario_id = get_usuario_id_from_token(
            credenciales.credentials
        )
    except ValueError as error:
        raise credenciales_invalidas from error

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == usuario_id,
            Usuario.activo.is_(True),
        )
        .first()
    )

    if usuario is None:
        raise credenciales_invalidas

    return usuario

def require_roles(*roles_permitidos: RolUsuario):
    def verificar_rol(
        current_user: Usuario = Depends(get_current_user),
    ) -> Usuario:
        if current_user.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para realizar esta acción.",
            )

        return current_user

    return verificar_rol

admin_or_recepcionista = Depends(
    require_roles(
        RolUsuario.ADMIN,
        RolUsuario.RECEPCIONISTA,
    )
)