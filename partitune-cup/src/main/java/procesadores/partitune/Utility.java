package procesadores.partitune;

import procesadores.partitune.sym;

class Utility {
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

    /**
     * Palabras/identificadores reservados
     */
    public static final String[] KEY_WORDS = {
        "fragmento",
        "obra",
        "clave",
        "compas",
        "armadura",
        "lig",
        "DO","RE","MI","FA", "SOL", "LA", "SI",
        "sf","f","sc","c","n","bl","r",
        "b",
    };

    public enum Note {
        DO,
        RE,
        MI,
        FA,
        SOL,
        LA,
        SI;
    }

    public enum Duration {
        SEMIFUSA,
        FUSA,
        SEMICORCHEA,
        CORCHEA,
        NEGRA,
        BLANCA,
        REDONDA;
    }

    public static boolean isKeyWord(String word) {
        for (String keyWord : KEY_WORDS) {
            if (keyWord.equalsIgnoreCase(word)) {
                return true;
            }
        }
        return false;
    }

    public static int getTokenType(String word) {
        switch (word.toLowerCase()) {
            case "fragmento":
                return sym.FRAGMENTO;
            case "obra":
                return sym.OBRA;
            case "clave":
                return sym.CLAVE;
            case "compas":
                return sym.COMPAS;
            case "armadura":
                return sym.ARMADURA;
            case "lig":
                return sym.LIGADURA;
            case "do":
            case "re":
            case "mi":
            case "fa":
            case "sol":
            case "la":
            case "si":
                return sym.NOTA_BASE;
            case "sf":
            case "f":
            case "sc":
            case "c":
            case "n":
            case "bl":
            case "r":
                return sym.DURACION;
            case "b":
                return sym.BEMOL;
            default:
                throw new IllegalArgumentException(word);
        }
    }

    public static Note getNoteType(String word) {
        switch (word.toLowerCase()) {
            case "do":
                return Note.DO;
            case "re":
                return Note.RE;
            case "mi":
                return Note.MI;
            case "fa":
                return Note.FA;
            case "sol":
                return Note.SOL;
            case "la":
                return Note.LA;
            case "si":
                return Note.SI;
            default:
                throw new IllegalArgumentException(word);
        }
    }

    public static Duration getDurationType(String word) {
        switch (word.toLowerCase()) {
            case "sf":
                return Duration.SEMIFUSA;
            case "f":
                return Duration.FUSA;
            case "sc":
                return Duration.SEMICORCHEA;
            case "c":
                return Duration.CORCHEA;
            case "n":
                return Duration.NEGRA;
            case "bl":
                return Duration.BLANCA;
            case "r":
                return Duration.REDONDA;
            default:
                throw new IllegalArgumentException(word);
        }
    }

    public enum Compas {
        DOSPORCUATRO,
        TRESPORCUATRO,
        CUATROPORCUATRO,
        SEISPOROCHO;
    }

    public static Compas getCompasType(String word) {
        switch (word.toLowerCase()) {
            case "2/4":
                return Compas.DOSPORCUATRO;
            case "3/4":
                return Compas.TRESPORCUATRO;
            case "4/4":
                return Compas.CUATROPORCUATRO;
            case "6/8":
                return Compas.SEISPOROCHO;
            default:
                throw new IllegalArgumentException(word);
        }
    }
}
