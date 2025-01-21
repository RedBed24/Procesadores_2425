import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from graphviz import Digraph

from .analysis.Parser import Parser  # Importa el Parser
from .analysis.Scanner import Scanner  # Importa el Scanner
from .visitor import Visitor
from .generacion import generar_abc


from .utils.logger import logger
from partitune.utils.parser_error_listener import ParserErrorListener
from .utils.errors import PartituneError, TituloError, DuracionCompasError, ComentarioError, CaracterNoReconocidoError
from .utils.error_messages import get_str_from_warning, get_str_from_error


# Para visualización gráfica
def build_tree(parser, node, graph, parent=None):
    """Función recursiva para construir un árbol en Graphviz."""

    label = Trees.getNodeText(node, parser.ruleNames)  # Obtener etiqueta del nodo
    node_id = str(id(node))  # Identificador único para el nodo

    # Agregar el nodo al grafo
    graph.node(node_id, label)

    # Conectar con el nodo padre, si existe
    if parent:
        graph.edge(parent, node_id)

    # Recorrer los hijos y construir el grafo
    if node.getChildCount() > 0:
        for child in node.getChildren():
            build_tree(parser, child, graph, node_id)


def generate_tree(input_file):
    """Genera un árbol de sintaxis y lo guarda como PNG."""
    # Utiliza input_file en lugar de sys.argv[1]
    input_stream = FileStream(input_file, encoding="utf-8")
    lexer = Scanner(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = Parser(tokens)

    parse_tree = parser.partitura()

    # Crear representación en Graphviz
    graph = Digraph(format="png")
    graph.attr(rankdir="TB")  # Dirección del árbol
    build_tree(parser, parse_tree, graph)

    # Renderizar el grafo
    output_file = "parse_tree"
    graph.render(output_file, view=True)
    logger.info(f"Árbol guardado como {output_file}.png")


def generate_abc(input_file):
    """Genera el archivo ABC a partir de un archivo de entrada."""
    input_stream = FileStream(input_file, encoding="utf-8")
    lexer = Scanner(input_stream)
    # Hace que los errores se muestren por el logger
    lexer.removeErrorListeners()
    scanner_error_listener = ParserErrorListener()
    lexer.addErrorListener(scanner_error_listener)
    tokens = CommonTokenStream(lexer)
    parser = Parser(tokens)
    parser.removeErrorListeners()
    parser_error_listener = ParserErrorListener()
    parser.addErrorListener(parser_error_listener)

    # lee todos los tokens
    tokens.fill()
    errores_lexicos = scanner_error_listener.errors
    # para todo token del canal de error
    for token in filter(lambda token: token.channel == Scanner.ERROR_CHANNEL, tokens.tokens):
        match token.type:
            case Scanner.TITULO_ERROR:
                errores_lexicos.append(TituloError(token.line, token.column))
            case Scanner.COMPAS_DURATION_ERROR:
                errores_lexicos.append(DuracionCompasError(token.line, token.column, token.text))
            case Scanner.BAD_COMMENT:
                errores_lexicos.append(ComentarioError(token.line, token.column))
            case Scanner.UNKNOWN:
                errores_lexicos.append(CaracterNoReconocidoError(token.line, token.column, token.text))

    try: 
        # creamos el arbol de parseo
        parse_tree = parser.partitura()
        logger.debug(parse_tree.toStringTree(recog=parser))

        # visitamos el arbol de parseo, con una lista de posibles errores para asegurar que no hay generación
        visitor = Visitor(errores_lexicos + parser_error_listener.errors)
        # excepción PartituneError si algún error es detectado
        obra = visitor.visit(parse_tree)

        if visitor.warnings:
            for warning in visitor.warnings:
                logger.warning(get_str_from_warning(warning))

        abc_output = generar_abc(obra)

        output_file = input_file.replace(".txt", ".abc")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(abc_output)

        logger.info(f"Archivo ABC generado: {output_file}")

    except PartituneError as e:
        for error in e.lista_errores:
            logger.error(get_str_from_error(error))
        for warning in e.lista_warnings:
            logger.warning(get_str_from_warning(warning))
    except Exception as e:
        logger.error("Error en el archivo de entrada:")
        logger.error(e)


def main():
    """Punto de entrada para los comandos partitune."""
    if len(sys.argv) != 3:
        logger.error("Uso: partitune <modo> <archivo>")
        logger.info(
            "Modos disponibles:\n  --tree : Generar el árbol de sintaxis como PNG\n  --abc  : Generar el archivo en formato ABC"
        )
        sys.exit(1)

    mode, input_file = sys.argv[1], sys.argv[2]

    if mode == "--tree":
        generate_tree(input_file)
    elif mode == "--abc":
        # Llama directamente a la función que genera el ABC en generacion.py
        generate_abc(input_file)
    else:
        logger.error("Modo no reconocido. Usa --tree o --abc.")
        sys.exit(1)


if __name__ == "__main__":
    main()
