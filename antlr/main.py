from antlr4 import *
from Scanner import Scanner
from Parser import Parser
from antlr4.tree.Trees import Trees
import os
import sys

from graphviz import Digraph

# Para visualización gráfica
def build_tree(parser, node, graph, parent=None):
    """
    Función recursiva para construir un árbol en Graphviz.
    """
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

def main():
    # Input arithmetic expression

    # Create input stream
    input_stream = FileStream(sys.argv[1])

    # Create the lexer
    lexer = Scanner(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = Parser(tokens)

    tree = parser.partitura()

    # Crear representación en Graphviz
    graph = Digraph(format='png')
    graph.attr(rankdir='TB')  # Dirección de top-bottom
    
    # Construir el árbol
    build_tree(parser, tree, graph)
    
    # Renderizar el grafo
    output_file = "parse_tree"
    graph.render(output_file, view=True)
    print(f"Árbol guardado como {output_file}.png")


# Itera sobre los tokens uno a uno
#    print("Procesando tokens:")
#    while True:
#        token = lexer.nextToken()
#        if token.type == Token.EOF:
#            break
#        print(f"Token: {token.text}, Tipo: {token.type}, Nombre {lexer.symbolicNames[token.type]}")


if __name__ == "__main__":
    main()
