import re
from antlr4 import *

def antlr_to_abc(parse_tree):
    """
    Transforma un árbol de sintaxis generado por ANTLR en una representación ABC.
    
    :param parse_tree: Árbol de sintaxis parseado por ANTLR.
    :return: String en formato ABC.
    """
    abc_output = []
    current_index = 1  # Identificador incremental para obras
    current_compas = None
    current_clave = None

    # Traducciones de notas y duraciones
    note_map = {
        "DO": "C", "RE": "D", "MI": "E", "FA": "F", "SOL": "G", "LA": "A", "SI": "B"
    }
    duration_map = {
        "sf": "/8", "f": "1/8", "sc": "1/16", "c": "1/4",
        "n": "", "bl": "2", "r": "4"
    }
    clave_map = {
        "SOL": "G", "FA": "F", "DO": "C"
    }

    def clean_label(label):
        """Limpia y estructura correctamente los nodos complejos."""
        match = re.match(r"(\w+)=?(.*)", label)
        if match:
            return match.groups()[0], match.groups()[1].strip()
        return label, ""

    def translate_note(note, duration):
        """Traduce una nota al formato ABC, incluyendo la duración y octava."""
        note_base = note_map.get(note.upper().strip("'"), note.upper())
        octava = "'" if "'" in note else "," if "_" in note else ""
        return f"{note_base}{octava}{duration}"

    def process_secuencia(node):
        """Procesa una secuencia, incluyendo duraciones y notas dentro de paréntesis."""
        print("Procesando secuencia...")  # Depuración
        elementos = []

        for child in node.getChildren():
            label, content = clean_label(child.getText())
            print(f"  Nodo de secuencia: {label}, contenido: {content}")  # Depuración

            if label in duration_map:
                duration = duration_map.get(label, "")
                notas = []
                for nota in child.getChildren():
                    nota_label, _ = clean_label(nota.getText())
                    notas.append(translate_note(nota_label, ""))
                if notas:
                    elementos.append(f"{' '.join(notas)}{duration}")

        return " ".join(elementos)

    def process_notas_y_estructuras(node):
        """Procesa notas, repeticiones, ligaduras y otras estructuras generales."""
        elementos = []
        if not hasattr(node, 'getChildren') or node.getChildCount() == 0:
            return ""  # Devolver una cadena vacía si es un nodo terminal

        for child in node.getChildren():
            label, content = clean_label(child.getText())
            print(f"Procesando nodo: {label}, contenido: {content}")  # Depuración

            if label.upper == "SECUENCIA":
                # Procesar secuencia
                secuencia = process_secuencia(child)
                if secuencia:
                    elementos.append(secuencia)

            elif label.upper == "REPETICION":
                # Manejo de repeticiones
                inner_bloque = process_notas_y_estructuras(child.getChild(1))  # Nodo dentro de |: y :|
                if inner_bloque:
                    elementos.append(f"|: {inner_bloque} :|")

            elif label.upper == "LIGADURA":
                # Manejo de ligaduras
                ligadura = process_notas_y_estructuras(child.getChild(1))  # Contenido dentro de ligadura
                if ligadura:
                    elementos.append(f"({ligadura})")

        return " ".join(elementos)

    def process_bloque_notas(node):
        """Procesa el bloque de notas que contiene múltiples elementos."""
        print("Procesando bloque de notas...")  # Depuración
        elementos = []
        for child in node.getChildren():
            label, content = clean_label(child.getText())
            print(f"  Nodo de bloque_notas: {label}, contenido: {content}")  # Depuración
            if label.upper == "ELEMENTO":
                for sub_elemento in child.getChildren():
                    sub_elemento_content = process_notas_y_estructuras(sub_elemento)
                    if sub_elemento_content:
                        elementos.append(sub_elemento_content)
        return " ".join(elementos)

    def process_obra(node):
        """Procesa una obra musical."""
        nonlocal current_index, current_compas, current_clave
        abc_output.append(f"X: {current_index}")  # Incrementar identificador
        current_index += 1

        for child in node.getChildren():
            label, content = clean_label(child.getText())
            print(f"Procesando nodo de obra: {label}, contenido: {content}")  # Depuración

            if label.startswith("\"") and label.endswith("\""):
                titulo = label.strip('"')
                abc_output.append(f"T: {titulo}")
            elif label.upper() == "COMPAS":
                abc_output.append(f"M: {content}")
                current_compas = content
            elif label.upper() == "CLAVE":
                clave = clave_map.get(content.upper(), "G")
                abc_output.append(f"K: {clave}")
                current_clave = clave
                abc_output.append("")  # Salto de línea después de la clave
            elif label.upper == "BLOQUE_NOTAS":
                # Procesar bloque de notas
                bloque_notas_content = process_bloque_notas(child)
                if bloque_notas_content:
                    abc_output.append(bloque_notas_content)

    print("Estructura del árbol:")
    print(parse_tree.toStringTree())  # Depuración

    for child in parse_tree.getChildren():
        label, _ = clean_label(child.getText())
        if label.lower() == "obra":
            process_obra(child)

    return "\n".join(filter(None, abc_output))
