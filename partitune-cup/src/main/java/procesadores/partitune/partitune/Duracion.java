package procesadores.partitune.partitune;

public enum Duracion {
    SEMIFUSA,
    FUSA,
    SEMICORCHEA,
    CORCHEA,
    NEGRA,
    BLANCA,
    REDONDA;

    public static Duracion getDurationType(String word) {
        switch (word.toUpperCase()) {
            case "SF":
                return Duracion.SEMIFUSA;
            case "F":
                return Duracion.FUSA;
            case "SC":
                return Duracion.SEMICORCHEA;
            case "C":
                return Duracion.CORCHEA;
            case "N":
                return Duracion.NEGRA;
            case "BL":
                return Duracion.BLANCA;
            case "R":
                return Duracion.REDONDA;
            default:
                throw new IllegalArgumentException("Duracion no valida: " + word);
        }
    }
}
