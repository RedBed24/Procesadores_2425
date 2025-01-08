import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from graphviz import Digraph

from .analysis.Parser import Parser  # Importa el Parser
from .analysis.Scanner import Scanner  # Importa el Scanner
from .antlr_to_abc import antlr_to_abc  # Importa la función de transcripción a ABC
from .listener import Listener  # Importa el Listener
from .generacion import generar_abc

from python.utils.logger import logger


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
    tokens = CommonTokenStream(lexer)
    parser = Parser(tokens)
    parse_tree = parser.partitura()
    logger.debug(parse_tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()
    listener = Listener()

    walker.walk(listener, parse_tree)

    abc_output = generar_abc(listener.obra)

    if not abc_output.strip():
        logger.warning(
            "Advertencia: No se generó contenido en el archivo ABC. Verifica el archivo de entrada o la gramática."
        )

    output_file = input_file.replace(".txt", ".abc")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(abc_output)

    logger.info(f"Archivo ABC generado: {output_file}")


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
        generate_abc(input_file)
    else:
        logger.error("Modo no reconocido. Usa --tree o --abc.")
        sys.exit(1)


if __name__ == "__main__":
    main()
