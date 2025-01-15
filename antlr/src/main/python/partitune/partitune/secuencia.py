from dataclasses import dataclass
from enum import Enum

from .duracion import Duracion
from .nota import Nota


@dataclass
class Secuencia:
    duracion: Duracion
    lista_notas: list[Nota | None]  # None es para silencios

    def __iter__(self):
        return iter(self.lista_notas)

    def __len__(self):
        return len(self.lista_notas)
