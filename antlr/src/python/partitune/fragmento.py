from dataclasses import dataclass

from .armadura import Armadura
from .compas import Compas
from .clave import Clave


@dataclass
class Fragmento:
    nombre: str
    clave: Clave = Clave.SOL
    armadura: Armadura
    compas: Compas = Compas.CUATROPORCUATRO
    # TODO: bloque notas: list[Secuencia | str | Repeticion | Ligadura]
