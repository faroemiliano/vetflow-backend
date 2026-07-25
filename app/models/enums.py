from enum import Enum


class RolUsuario(str, Enum):
    ADMIN = "ADMIN"
    VETERINARIO = "VETERINARIO"
    RECEPCIONISTA = "RECEPCIONISTA"


class EstadoTurno(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    ATENDIDO = "ATENDIDO"
    CANCELADO = "CANCELADO"


class EspecieAnimal(str, Enum):
    CANINO = "CANINO"
    FELINO = "FELINO"
    AVE = "AVE"
    EQUINO = "EQUINO"
    BOVINO = "BOVINO"
    CAPRINO = "CAPRINO"
    OVINO = "OVINO"
    PORCINO = "PORCINO"
    EXOTICO = "EXOTICO"
    OTRO = "OTRO"


class ViaAdministracion(str, Enum):
    ORAL = "ORAL"
    INYECTABLE = "INYECTABLE"
    TOPICA = "TOPICA"
    OFTALMICA = "OFTALMICA"
    OTICA = "OTICA"
    NASAL = "NASAL"
    RECTAL = "RECTAL"
    OTRA = "OTRA"