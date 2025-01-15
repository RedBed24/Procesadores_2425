package procesadores.partitune.utils;

public class Errors {
    private static final String[] LEXER_ERROR_MESSAGES = {
        "Lexer error: El archivo termina con un comentario abierto",
        "Lexer error: Caracter no reconocido",
        "Lexer error: Identificador no permitido",
        "Lexer error: Duracion de compas incorrecta",
        "Lexer error: Titulo incorrecto, faltan las comillas de cierre",
        "Lexer error: Error desconocido",
    };

    public static final int LEXER_COMMENT_ERROR = 0;
    public static final int LEXER_UNRECOGNIZED_CHAR = 1;
    public static final int LEXER_UNRECOGNIZED_ID = 2;
    public static final int LEXER_COMPAS_DURATION_ERROR = 3;
    public static final int LEXER_UNFINISHED_TITLE = 4;
    public static final int LEXER_UNKNOWN_ERROR = 5;


    private static final String[] PARSER_ERROR_MESSAGES = {
        "Parser error: Bloque de elementos contiene elementos inesperados",
        "Parser error: Bloque de notas vacio",
    };

    public static final int PARSER_BLOCK = 0;
    public static final int PARSER_EMPTY_BLOCK = 1;

    private static final String[] SEMANTIC_ERROR_MESSAGES = {
        "Semantic error: Armadura con mezcla de modificadores",
        "Semantic error: Notas de armadura incorrectas",
        "Semantic error: Nota de clave incorrecta solo se permiten [SOL, FA, DO]",
        "Semantic error: Llamada a fragmento no definido",
        "Semantic error: Fragmento duplicado",
        "Semantic error: Al menos dos elementos en una ligadura",
        "Semantic error: En la ligadura no puede haber silencios",
    };

    private static final String[] WARNIGS = {
        "Warning: Compas duplicado",
        "Warning: Clave duplicada",
        "Warning: Armadura duplicada",
    };

    public static final int SEMANTIC_MIXED_MODIFIERS = 0;
    public static final int SEMANTIC_WRONG_KEY_NOTES = 1;
    public static final int SEMANTIC_WRONG_KEY = 2;
    public static final int SEMANTIC_UNDEFINED_FRAGMENT = 3;
    public static final int SEMANTIC_DUPLICATE_FRAGMENT = 4;
    public static final int SEMANTIC_TWO_ELEMENTS_IN_LIGATURE = 5;
    public static final int SEMANTIC_SILENCE_IN_LIGATURE = 6;

    public static final int WARNING_DUPLICATE_COMPAS = 0;
    public static final int WARNING_DUPLICATE_KEY = 1;
    public static final int WARNING_DUPLICATE_ARMOR = 2;

    private static String checkError(String[] messages, int codigo, int linea, int columna) {
        if (codigo >= 0 && codigo < messages.length) {
            return messages[codigo] + " en la línea " + (linea+1) + ", columna " + (columna+1);
        }
        return "Código de error desconocido";
    }

    public static String lexerGetError(int codigo, int linea, int columna) {
        return checkError(LEXER_ERROR_MESSAGES, codigo, linea, columna);
    }

    public static String parserGetError(int codigo, int linea, int columna) {
        return checkError(PARSER_ERROR_MESSAGES, codigo, linea, columna);
    }
    public static String semanticGetError(int codigo, int linea, int columna) {
        return checkError(SEMANTIC_ERROR_MESSAGES, codigo, linea, columna);
    }
    public static String semanticGetError(int codigo) {
        return SEMANTIC_ERROR_MESSAGES[codigo];
    }

    public static String warningGetError(int codigo, int linea, int columna) {
        return checkError(WARNIGS, codigo, linea, columna);
    }

}
