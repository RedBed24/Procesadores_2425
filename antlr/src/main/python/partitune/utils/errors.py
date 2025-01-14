from ..partitune.nota_base import NotaBase


class Warning:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class CompasDuplicationWarning(Warning):
    def __init__(self, line: int, column: int, compas: str):
        super().__init__(line, column)
        self.compas = compas

class ClaveDuplicationWarning(Warning):
    def __init__(self, line: int, column: int, clave: str):
        super().__init__(line, column)
        self.clave = clave

class ArmaduraDuplicationWarning(Warning):
    def __init__(self, line: int, column: int, armadura: str):
        super().__init__(line, column)
        self.armadura = armadura

class FragmentoNoUsadoWarning(Warning):
    def __init__(self, line: int, column: int, fragmento: str):
        super().__init__(line, column)
        self.fragmento = fragmento

class LexerError(Exception):
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class DuracionCompasError(LexerError):
    def __init__(self, line: int, column: int, compas_erroneo: str):
        super().__init__(line, column)
        self.compas_erroneo = compas_erroneo

class TituloError(LexerError):
    pass

class ComentarioError(LexerError):
    pass

class CaracterNoReconocidoError(LexerError):
    def __init__(self, line: int, column: int, caracter: str):
        super().__init__(line, column)
        self.caracter = caracter

class ParserError(Exception):
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class SemanticError(Exception):
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class PartituneError(SemanticError):
    def __init__(self, lista_errores: list[SemanticError], lista_warnings: list[Warning]):
        self.lista_errores = lista_errores
        self.lista_warnings = lista_warnings

class ArmaduraError(SemanticError):
    pass

class ModificadorArmaduraError(ArmaduraError):
    pass

class NotasArmaduraError(ArmaduraError):
    def __init__(self, line: int, column: int, lista_notas: list[NotaBase]):
        super().__init__(line, column)
        self.lista_notas = lista_notas

class NotaClaveError(SemanticError):
    def __init__(self, line: int, column: int, nota_clave: str):
        super().__init__(line, column)
        self.nota_clave = nota_clave

class LlamadaCircularError(SemanticError):
    def __init__(self, ciclo: list[str]):
        self.ciclo = ciclo

class LlamadaNoDefinidaError(SemanticError):
    def __init__(self, line, column, llamada: str):
        super().__init__(line, column)
        self.llamada = llamada

class FragmentoDuplicationError(SemanticError):
    def __init__(self, line, column, fragmento: str):
        super().__init__(line, column)
        self.fragmento = fragmento
