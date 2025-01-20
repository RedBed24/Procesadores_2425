from dataclasses import dataclass
from .nota_base import NotaBase
from .octava import Octava
from .modificador import Modificador
from typing import Optional

# Nota en partituras
@dataclass
class Nota:
    nota_base: NotaBase
    modificador: Optional[Modificador] = None
    octava: Octava = Octava.NORMAL
    puntillo: bool = False
