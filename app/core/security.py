from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

def create_access_token(data: dict) ->str:
    datos_token = data.copy()

    fecha_expiracion= datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos_token.update({"exp": fecha_expiracion})

    return jwt.encode(
        datos_token,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def get_usuario_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as error:
        raise ValueError("Token inválido o vencido.") from error

    usuario_id = payload.get("sub")

    if usuario_id is None:
        raise ValueError("El token no contiene un usuario.")

    try:
        return int(usuario_id)
    except ValueError as error:
        raise ValueError("El ID de usuario en el token no es válido.") from error