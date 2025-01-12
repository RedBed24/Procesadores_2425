package procesadores.partitune.utils;

public class Errors {
    public static final String[] LEXER_ERROR_MESSAGES = {
        "Error: Comentario sin cerrar en línea %d columna %d\n",
        "Error: Caracter no reconocido en línea %d columna %d\n",
        "Error: Identificador no permitido en línea %d columna %d\n",
        "Error: Duracion de compas erronea en línea %d columna %d\n",
        "Error: Titulo incorrecto, faltan las comillas de cierre en línea %d columna %d\n",
        "Error: Error desconocido en línea %d columna %d\n",
    };

    public static final int LEXER_COMMENT_ERROR = 0;
    public static final int LEXER_UNRECOGNIZED_CHAR = 1;
    public static final int LEXER_UNRECOGNIZED_ID = 2;
    public static final int LEXER_COMPAS_DURATION_ERROR = 3;
    public static final int LEXER_UNFINISHED_TITLE = 4;
    public static final int LEXER_UNKNOWN_ERROR = 5;

}
