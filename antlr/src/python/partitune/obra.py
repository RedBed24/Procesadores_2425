from __future__ import annotations
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura
from .fragmento import Fragmento


class Obra:
    def __init__(
        self,
        nombre: str,
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        self.nombre = nombre
        self.clave = clave
        self.armadura = armadura
        self.compas = compas


class ObraSemantica(Obra):
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | str | Repeticion | Ligadura],
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas


class ObraFinal(Obra):
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | Fragmento | Repeticion | Ligadura],
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas
