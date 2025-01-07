from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura
from .fragmento import Fragmento


@dataclass
class Obra:
    nombre: str
    bloque_notas: list[Secuencia | Fragmento | Repeticion | Ligadura]
    clave: Clave = Clave.SOL
    armadura: Optional[Armadura] = None
    compas: Compas = Compas.DOSPORCUATRO
    
