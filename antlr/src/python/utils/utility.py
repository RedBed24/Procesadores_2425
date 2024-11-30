class Utility:
    LEXER_ERROR_MESSAGES = [
        "Error: Comentario sin cerrar",
        "Error: Caracter no reconocido",
        "Error: Identificador no permitido",
        "Error: Duración de compás errónea",
        "Error: Título incorrecto, faltan las comillas de cierre",
        "Error: Error desconocido",
    ]

    LEXER_COMMENT_ERROR = 0
    LEXER_UNRECOGNIZED_CHAR = 1
    LEXER_UNRECOGNIZED_ID = 2
    LEXER_COMPAS_DURATION_ERROR = 3
    LEXER_UNFINISHED_TITLE = 4
    LEXER_UNKNOWN_ERROR = 5

    KEY_WORDS = [
        "fragmento",
        "obra",
        "clave",
        "compas",
        "armadura",
        "lig",
        "DO", "RE", "MI", "FA", "SOL", "LA", "SI",
        "sf", "f", "sc", "c", "n", "bl", "r",
        "b",
    ]

    class TokenType:
        FRAGMENTO = "FRAGMENTO"
        OBRA = "OBRA"
        CLAVE = "CLAVE"
        COMPAS = "COMPAS"
        ARMADURA = "ARMADURA"
        LIG = "LIG"
        NOTA = "NOTA"
        DURACION = "DURACION"
        BEMOL = "BEMOL"

    class Note:
        DO = "DO"
        RE = "RE"
        MI = "MI"
        FA = "FA"
        SOL = "SOL"
        LA = "LA"
        SI = "SI"

    class Duration:
        SEMIFUSA = "SEMIFUSA"
        FUSA = "FUSA"
        SEMICORCHEA = "SEMICORCHEA"
        CORCHEA = "CORCHEA"
        NEGRA = "NEGRA"
        BLANCA = "BLANCA"
        REDONDA = "REDONDA"

    @staticmethod
    def is_key_word(word):
        return word.lower() in (key_word.lower() for key_word in Utility.KEY_WORDS)

    @staticmethod
    def get_token_type(word):
        word_lower = word.lower()
        if word_lower == "fragmento":
            return Utility.TokenType.FRAGMENTO
        elif word_lower == "obra":
            return Utility.TokenType.OBRA
        elif word_lower == "clave":
            return Utility.TokenType.CLAVE
        elif word_lower == "compas":
            return Utility.TokenType.COMPAS
        elif word_lower == "armadura":
            return Utility.TokenType.ARMADURA
        elif word_lower == "lig":
            return Utility.TokenType.LIG
        elif word_lower in ["do", "re", "mi", "fa", "sol", "la", "si"]:
            return Utility.TokenType.NOTA
        elif word_lower in ["sf", "f", "sc", "c", "n", "bl", "r"]:
            return Utility.TokenType.DURACION
        elif word_lower == "b":
            return Utility.TokenType.BEMOL
        else:
            raise ValueError(f"Invalid token: {word}")

    @staticmethod
    def get_note_type(word):
        word_lower = word.lower()
        if word_lower == "do":
            return Utility.Note.DO
        elif word_lower == "re":
            return Utility.Note.RE
        elif word_lower == "mi":
            return Utility.Note.MI
        elif word_lower == "fa":
            return Utility.Note.FA
        elif word_lower == "sol":
            return Utility.Note.SOL
        elif word_lower == "la":
            return Utility.Note.LA
        elif word_lower == "si":
            return Utility.Note.SI
        else:
            raise ValueError(f"Invalid note: {word}")

    @staticmethod
    def get_duration_type(word):
        word_lower = word.lower()
        if word_lower == "sf":
            return Utility.Duration.SEMIFUSA
        elif word_lower == "f":
            return Utility.Duration.FUSA
        elif word_lower == "sc":
            return Utility.Duration.SEMICORCHEA
        elif word_lower == "c":
            return Utility.Duration.CORCHEA
        elif word_lower == "n":
            return Utility.Duration.NEGRA
        elif word_lower == "bl":
            return Utility.Duration.BLANCA
        elif word_lower == "r":
            return Utility.Duration.REDONDA
        else:
            raise ValueError(f"Invalid duration: {word}")

    class Compas:
        DOSPORCUATRO = "2/4"
        TRESPORCUATRO = "3/4"
        CUATROPORCUATRO = "4/4"
        SEISPOROCHO = "6/8"

    @staticmethod
    def get_compas_type(word):
        word_lower = word.lower()
        if word_lower == "2/4":
            return Utility.Compas.DOSPORCUATRO
        elif word_lower == "3/4":
            return Utility.Compas.TRESPORCUATRO
        elif word_lower == "4/4":
            return Utility.Compas.CUATROPORCUATRO
        elif word_lower == "6/8":
            return Utility.Compas.SEISPOROCHO
        else:
            raise ValueError(f"Invalid compas: {word}")
