from dataclasses import dataclass
from enum import Enum

from .duracion import Duracion
from .nota import Nota

# Secuencia de notas
@dataclass
class Secuencia:
    duracion: Duracion
    lista_notas: list[Nota | None]  # None es para silencios
