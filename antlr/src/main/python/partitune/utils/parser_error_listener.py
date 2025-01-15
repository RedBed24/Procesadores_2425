from antlr4.error.ErrorListener import ErrorListener

from .errors import GenericParserError

class ParserErrorListener(ErrorListener):
    def __init__(self):
        self.errors: list[GenericParserError] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(GenericParserError(line, column, recognizer._ctx.getRuleIndex(), offendingSymbol.type, offendingSymbol.text, list(recognizer.getExpectedTokens()), recognizer._ctx))
