from __future__ import annotations
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura


class FragmentoSimple:
    def __init__(
        self,
        nombre: str,
    ):
        self.nombre = nombre

    def __eq__(self, value):
        if not isinstance(value, Fragmento):
            return False
        return self.nombre.upper() == value.nombre.upper()


class Fragmento(FragmentoSimple):
    def __init__(
        self,
        nombre: str,
        clave: Optional[Clave] = None,
        armadura: Optional[Armadura] = None,
        compas: Optional[Compas] = None,
    ):
        super().__init__(nombre)
        self.clave = clave
        self.armadura = armadura
        self.compas = compas


class FragmentoLlamado(FragmentoSimple):
    def __init__(self, nombre: str, linea: int, columna: int):
        super().__init__(nombre)
        self.linea = linea
        self.columna = columna


class FragmentoSemantico(Fragmento):
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | FragmentoLlamado | Repeticion | Ligadura],
        linea: int,
        columna: int,
        clave: Optional[Clave] = None,
        armadura: Optional[Armadura] = None,
        compas: Optional[Compas] = None,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas
        self.linea = linea
        self.columna = columna


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
