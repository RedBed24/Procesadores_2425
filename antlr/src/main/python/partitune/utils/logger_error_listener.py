from antlr4.error.ErrorListener import ErrorListener

from .logger import logger

class LoggerErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        logger.error(f"Error at line {line}, column {column}: {msg}")
