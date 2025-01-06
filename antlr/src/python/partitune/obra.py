from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia, Repeticion, Ligadura
from .fragmento import Fragmento


@dataclass
class Obra:
    nombre: str
    clave: Clave = Clave.SOL
    armadura: Optional[Armadura] = None
    compas: Compas = Compas.DOSPORCUATRO
    bloque_notas: list[Secuencia | Fragmento | Repeticion | Ligadura]
