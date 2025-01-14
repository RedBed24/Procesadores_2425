package procesadores.partitune.utils;

public class Errors {
    public static final String[] LEXER_ERROR_MESSAGES = {
        "Lexer error: Comentario sin cerrar en linea %d columna %d\n",
        "Lexer error: Caracter no reconocido en linea %d columna %d\n",
        "Lexer error: Identificador no permitido en linea %d columna %d\n",
        "Lexer error: Duracion de compas erronea en linea %d columna %d\n",
        "Lexer error: Titulo incorrecto, faltan las comillas de cierre en linea %d columna %d\n",
        "Lexer error: Error desconocido en linea %d columna %d\n",
    };

    public static final int LEXER_COMMENT_ERROR = 0;
    public static final int LEXER_UNRECOGNIZED_CHAR = 1;
    public static final int LEXER_UNRECOGNIZED_ID = 2;
    public static final int LEXER_COMPAS_DURATION_ERROR = 3;
    public static final int LEXER_UNFINISHED_TITLE = 4;
    public static final int LEXER_UNKNOWN_ERROR = 5;
}
