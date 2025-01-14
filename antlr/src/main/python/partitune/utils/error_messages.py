from .errors import *


def get_str_from_warnings(warnings: list[Warning]) -> str:
    mensaje = "Advertencias:"
    for warning in warnings:
        match warning:
            case CompasDuplicationWarning():
                mensaje += f"\n   Compás duplicado en línea {warning.line}, columna {warning.column}: {warning.compas}"
            case ClaveDuplicationWarning():
                mensaje += f"\n   Clave duplicada en línea {warning.line}, columna {warning.column}: {warning.clave}"
            case ArmaduraDuplicationWarning():
                mensaje += f"\n   Armadura duplicada en línea {warning.line}, columna {warning.column}: {warning.armadura}"
            case FragmentoNoUsadoWarning():
                mensaje += f"\n   Fragmento no usado en línea {warning.line}, columna {warning.column}: {warning.fragmento}"
    return mensaje


def get_str_from_errors(errors: list[LexerError | ParserError | SemanticError]) -> str:
    mensaje = ""
    for error in filter(lambda error: isinstance(error, LexerError), errors):
        mensaje += get_str_from_lexic_errors(errors)
    for error in filter(lambda error: isinstance(error, ParserError), errors):
        mensaje += get_str_from_parser_errors(errors)
    for error in filter(lambda error: isinstance(error, SemanticError), errors):
        mensaje += get_str_from_semantic_errors(errors)


def get_str_from_lexic_errors(errors: list[LexerError]) -> str:
    mensaje = "Errores Léxicos:"
    for error in errors:
        match error:
            case DuracionCompasError():
                mensaje += f'\n   Duración de compás incorrecta en línea {error.line}, columna {error.column}: {error.compas_erroneo}, se esperaba una de ["2/4", "3/4", "4/4", "6/8"]'
            case TituloError():
                mensaje += f"\n   El archivo termina con un título abierto en línea {error.line}, columna {error.column}"
            case ComentarioError():
                mensaje += f"\n   El archivo termina con un comentario abierto en línea {error.line}, columna {error.column}"
            case CaracterNoReconocidoError():
                mensaje += f"\n   Caracter no reconocido en línea {error.line}, columna {error.column}: {error.caracter}"
    return mensaje


def get_str_from_parser_errors(errors: list[ParserError]) -> str:
    mensaje = "Errores Sintácticos:"
    for error in errors:
        # TODO: añadir casos
        mensaje += f"\n   Error en línea {error.line}, columna {error.column}"
    return mensaje


def get_str_from_semantic_errors(errors: list[SemanticError]) -> str:
    mensaje = "Errores Semánticos:"
    for error in errors:
        match error:
            case ModificadorArmaduraError():
                mensaje += f"\n   Armadura con mezcla de modificadores en línea {error.line}, columna {error.column}"
            case NotasArmaduraError():
                mensaje += f"\n   Notas de armadura incorrectas en línea {error.line}, columna {error.column}: {error.notas}"
            case NotaClaveError():
                mensaje += f'\n   Nota de clave incorrecta en línea {error.line}, columna {error.column}: {error.nota}, se esperaba una de ["SOL", "FA", "DO"]'
            case LlamadaCircularError():
                mensaje += f"\n   Llamada circular entre los siguientes fragmentos: {', '.join(error.ciclo)}"
            case LlamadaNoDefinidaError():
                mensaje += f"\n   Llamada a fragmento no definido en línea {error.line}, columna {error.column}: {error.llamada}"
            case FragmentoDuplicationError():
                mensaje += f"\n   Fragmento duplicado en línea {error.line}, columna {error.column}: {error.fragmento}"
    return mensaje
