from antlr4.error.ErrorListener import ErrorListener

from .errors import GenericParserError

class ParserErrorListener(ErrorListener):
    """Clase para manejar errores de análisis."""
    def __init__(self):
        self.errors: list[GenericParserError] = []

    def syntaxError(self, recognizer, offendingSymbol: int, line: int, column: int, msg, e):
        """Método que se llama cuando se detecta un error de sintaxis.
        
        :param recognizer: Parser o Lexer que detectó el error.
        :param offendingSymbol: Símbolo que causó el error. recognizer.symbolicNames
        :param line: Línea en la que se encuentra el error.
        :param column: Columna en la que se encuentra el error.
        :param msg: Mensaje de error.
        """
        self.errors.append(GenericParserError(line, column, recognizer._ctx.getRuleIndex(), offendingSymbol.type, offendingSymbol.text, list(recognizer.getExpectedTokens()), recognizer._ctx))
