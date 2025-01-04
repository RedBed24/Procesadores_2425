from dataclasses import dataclass

from .duracion import Duracion

@dataclass
class Secuencia:
    duracion: Duracion
    lista_notas: list[str]