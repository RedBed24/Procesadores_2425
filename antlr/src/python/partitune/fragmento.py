from __future__ import annotations
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura


class Fragmento:
    def __init__(
        self,
        nombre: str,
        clave: Optional[Clave] = None,
        armadura: Optional[Armadura] = None,
        compas: Optional[Compas] = None,
    ):
        self.nombre = nombre
        self.clave = clave
        self.armadura = armadura
        self.compas = compas


class FragmentoSemantico(Fragmento):
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | str | Repeticion | Ligadura],
        clave: Optional[Clave] = None,
        armadura: Optional[Armadura] = None,
        compas: Optional[Compas] = None,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas


class FragmentoFinal(Fragmento):
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | Fragmento | Repeticion | Ligadura],
        clave: Optional[Clave] = None,
        armadura: Optional[Armadura] = None,
        compas: Optional[Compas] = None,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas
