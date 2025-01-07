from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura


@dataclass
class Fragmento:
    nombre: str
    clave: Optional[Clave] = None
    armadura: Optional[Armadura] = None
    compas: Optional[Compas] = None


class FragmentoSemantico(Fragmento):
    bloque_notas: list[Secuencia | str | Repeticion | Ligadura]


class FragmentoFinal(Fragmento):
    bloque_notas: list[Secuencia | Fragmento | Repeticion | Ligadura]

    def __str__(self) -> str:
        return ""
