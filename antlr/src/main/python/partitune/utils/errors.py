"""Módulo que contiene las clases de errores y warnings que se pueden generar en el proceso de análisis de una partitura."""

from antlr4 import ParserRuleContext
from ..partitune.nota_base import NotaBase


class Warning:
    """Clase base para los warnings."""
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class CompasDuplicationWarning(Warning):
    """Warning que se genera cuando un compás se define más de una vez dentro de un fragmento."""
    def __init__(self, line: int, column: int, compas: str):
        super().__init__(line, column)
        self.compas = compas

class ClaveDuplicationWarning(Warning):
    """Warning que se genera cuando una clave se define más de una vez dentro de un fragmento."""
    def __init__(self, line: int, column: int, clave: str):
        super().__init__(line, column)
        self.clave = clave

class ArmaduraDuplicationWarning(Warning):
    """Warning que se genera cuando una armadura se define más de una vez dentro de un fragmento."""
    def __init__(self, line: int, column: int, armadura: str):
        super().__init__(line, column)
        self.armadura = armadura

class FragmentoNoUsadoWarning(Warning):
    """Warning que se genera cuando un fragmento no es usado en la partitura."""
    def __init__(self, line: int, column: int, fragmento: str):
        super().__init__(line, column)
        self.fragmento = fragmento

class LexerError(Exception):
    """Clase base para los errores léxicos."""
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class DuracionCompasError(LexerError):
    """Error que se genera cuando la duración de un compás no es válida."""
    def __init__(self, line: int, column: int, compas_erroneo: str):
        super().__init__(line, column)
        self.compas_erroneo = compas_erroneo

class TituloError(LexerError):
    """Error que se genera cuando hay un título sin cerrar."""
    pass

class ComentarioError(LexerError):
    """Error que se genera cuando hay un comentario sin cerrar."""
    pass

class CaracterNoReconocidoError(LexerError):
    """Error que se genera cuando se encuentra un caracter no reconocido."""
    def __init__(self, line: int, column: int, caracter: str):
        super().__init__(line, column)
        self.caracter = caracter

class ParserError(Exception):
    """Clase base para los errores de análisis sintáctico"""
    def __init__(self, line: int, column: int, context: ParserRuleContext):
        self.line = line
        self.column = column
        self.context = context

class GenericParserError(ParserError):
    """Error genérico que se genera cuando se ha encontrado un token donde no debería estar."""
    def __init__(self, line: int, column: int, rule_idx: int, offending_symbol_type: int, offending_text: str, expected_tokens: list[int], context: ParserRuleContext):
        """Constructor de la clase:
        
        :param line: Línea en la que se ha encontrado el error.
        :param column: Columna en la que se ha encontrado el error.
        :param rule_idx: Índice de la regla en la que se ha encontrado el error. Parser.ruleNames
        :param offending_symbol_type: Tipo del símbolo ofensivo. Parser.symbolicNames
        :param offending_text: Texto del símbolo ofensivo.
        :param expected_tokens: Tokens esperados. Parser.symbolicNames
        """
        super().__init__(line, column, context)
        self.offending_text = offending_text
        self.expected_tokens = expected_tokens
        self.rule_idx = rule_idx
        self.offending_symbol_type = offending_symbol_type

class ElementoDentroElementoError(ParserError):
    """Error que se genera cuando un elemento (como una ligadura, repetición o llamada) está dentro de otro elemento."""
    def __init__(self, line: int, column: int, end_line: int, end_column: int, context: ParserRuleContext):
        super().__init__(line, column, context)
        self.end_line = end_line
        self.end_column = end_column

class RepeticionError(ElementoDentroElementoError):
    """Error que se genera cuando una repetición tiene elementos (como una ligadura, repetición o llamada) dentro de ella."""
    pass

class LigaduraError(ElementoDentroElementoError):
    """Error que se genera cuando una ligadura tiene elementos (como una ligadura, repetición o llamada) dentro de ella."""
    pass

class SemanticError(Exception):
    """Clase base para los errores semánticos."""
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class PartituneError(Exception):
    """Clase que contiene una lista de errores y warnings. Se lanzará cuando se detecten errores en la partitura."""
    def __init__(self, lista_errores: list[SemanticError], lista_warnings: list[Warning]):
        self.lista_errores = lista_errores
        self.lista_warnings = lista_warnings

class ArmaduraError(SemanticError):
    """Clase base para los errores relacionados con la armadura."""
    pass

class ModificadorArmaduraError(ArmaduraError):
    """Error que se genera cuando una armadura mezcla sostenidos y bemoles."""
    pass

class NotasArmaduraError(ArmaduraError):
    """Error que se genera cuando una armadura no tiene las notas correctas."""
    def __init__(self, line: int, column: int, lista_notas: list[NotaBase]):
        super().__init__(line, column)
        self.lista_notas = lista_notas

class NotaClaveError(SemanticError):
    """Error que se genera cuando se ha especificado una clave que no es válida."""
    def __init__(self, line: int, column: int, nota_clave: str):
        super().__init__(line, column)
        self.nota_clave = nota_clave

class LlamadaCircularError(SemanticError):
    """Error que se genera cuando se ha detectado una llamada circular entre fragmentos."""
    def __init__(self, ciclo: list[str]):
        self.ciclo = ciclo

class LlamadaNoDefinidaError(SemanticError):
    """Error que se genera cuando se ha detectado una llamada a un fragmento que no ha sido definido."""
    def __init__(self, line, column, llamada: str):
        super().__init__(line, column)
        self.llamada = llamada

class FragmentoDuplicationError(SemanticError):
    """Error que se genera cuando un fragmento se define más de una vez."""
    def __init__(self, line, column, fragmento: str):
        super().__init__(line, column)
        self.fragmento = fragmento

class LigaduraError(SemanticError):
    """Clase base para los errores relacionados con las ligaduras."""
    pass

class LigaduraSilencioError(LigaduraError):
    """Error que se genera cuando una ligadura contiene un silencio."""
    pass

class LigaduraNotasError(LigaduraError):
    """Error que se genera cuando una ligadura no contiene las notas suficientes."""
    pass
