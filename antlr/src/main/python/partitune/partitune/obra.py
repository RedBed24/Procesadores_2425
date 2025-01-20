"""Módulo para la representación de las obras musicales."""
from __future__ import annotations
from typing import Optional

from .armadura import Armadura
from .compas import Compas
from .clave import Clave
from .secuencia import Secuencia
from .repeticion import Repeticion
from .ligadura import Ligadura
from .fragmento import FragmentoFinal, FragmentoLlamado

# Clase principal para las obras
class Obra:
    """Clase común para la obra."""
    def __init__(
        self,
        nombre: str,
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        self.nombre = nombre
        self.clave = clave if clave else Clave.SOL
        self.armadura = armadura
        self.compas = compas if compas else Compas.DOSPORCUATRO

# clases que extienden Obra con un bloque de notas
class ObraSemantica(Obra):
    """Clase para la representación de la obra semántica.
    Las llamadas son representadas por un FragmentoLlamado."""
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | FragmentoLlamado | Repeticion | Ligadura],
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas

# clase que extiende Obra con un bloque de notas final
class ObraFinal(Obra):
    """Clase para la representación de la obra final.
    Las llamadas son representadas por un FragmentoFinal, que tiene todos los atributos"""
    def __init__(
        self,
        nombre: str,
        bloque_notas: list[Secuencia | FragmentoFinal | Repeticion | Ligadura],
        clave: Clave = Clave.SOL,
        armadura: Optional[Armadura] = None,
        compas: Compas = Compas.DOSPORCUATRO,
    ):
        super().__init__(nombre, clave, armadura, compas)
        self.bloque_notas = bloque_notas
