from enum import Enum

from ..analysis.Parser import Parser

# Modificadores posibles en partituras
class Modificador(Enum):
    SOSTENIDO = Parser.SOSTENIDO
    BEMOL = Parser.BEMOL
    BECUADRO = Parser.BECUADRO
