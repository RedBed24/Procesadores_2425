from .errors import *
from ..analysis.Parser import Parser


def get_str_from_warning(warning: Warning) -> str:
    match warning:
        case CompasDuplicationWarning():
            return f"Compás duplicado en línea {warning.line}, columna {warning.column}: {warning.compas}"
        case ClaveDuplicationWarning():
            return f"Clave duplicada en línea {warning.line}, columna {warning.column}: {warning.clave}"
        case ArmaduraDuplicationWarning():
            return f"Armadura duplicada en línea {warning.line}, columna {warning.column}: {warning.armadura}"
        case FragmentoNoUsadoWarning():
            return f"Fragmento no usado en línea {warning.line}, columna {warning.column}: {warning.fragmento}"


def get_str_from_error(error: LexerError | ParserError | SemanticError) -> str:
    match error:
        # Lexer errors
        case DuracionCompasError():
            return f"Duración de compás incorrecta en línea {error.line}, columna {error.column}: {error.compas_erroneo}, se esperaba una de ['2/4', '3/4', '4/4', '6/8']"
        case TituloError():
            return f"El archivo termina con un título abierto en línea {error.line}, columna {error.column}"
        case ComentarioError():
            return f"El archivo termina con un comentario abierto en línea {error.line}, columna {error.column}"
        case CaracterNoReconocidoError():
            return f"Caracter no reconocido en línea {error.line}, columna {error.column}: {error.caracter}"
        # Parser errors
        case GenericParserError():
            return f"En línea {error.line}, columna {error.column}: se encontró '{error.offending_text}', es un {Parser.symbolicNames[error.offending_symbol_type]}, mientras se reconocía {Parser.ruleNames[error.rule_idx]}, se esperaba uno de estos: {list(map(lambda i: Parser.symbolicNames[i], error.expected_tokens))}"
        case RepeticionError():
            return f"La repetición de la línea {error.line}, columna {error.column} no puede tener Llamadas, Repeticiones ni Ligaduras en su interior"
        case LigaduraError():
            return f"La ligadura de la línea {error.line}, columna {error.column} no puede tener Llamadas, Repeticiones ni Ligaduras en su interior"

        # Semantic errors
        case ModificadorArmaduraError():
            return f"Armadura con mezcla de modificadores en línea {error.line}, columna {error.column}"
        case NotasArmaduraError():
            return f"Notas de armadura incorrectas en línea {error.line}, columna {error.column}: {list(map(lambda nota: nota.value, error.lista_notas))}"
        case NotaClaveError():
            return f"Nota de clave incorrecta en línea {error.line}, columna {error.column}: {error.nota_clave}, se esperaba una de ['SOL', 'FA', 'DO']"
        case LlamadaCircularError():
            return f"Llamada circular entre los siguientes fragmentos: {' -> '.join(error.ciclo)}"
        case LlamadaNoDefinidaError():
            return f"Llamada a fragmento no definido en línea {error.line}, columna {error.column}: {error.llamada}"
        case FragmentoDuplicationError():
            return f"Fragmento duplicado en línea {error.line}, columna {error.column}: {error.fragmento}"
        case LigaduraNotasError():
            return f"Ligadura con menos de 2 notas en línea {error.line}, columna {error.column}"
        case LigaduraSilencioError():
            return f"Ligadura con silencio en línea {error.line}, columna {error.column}"
