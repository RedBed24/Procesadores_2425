package procesadores.partitune.partitune;

public enum Clave {
    SOL,
    FA,
    DO;
    
    public static Clave getClaveType(String word) {
        switch (word.toUpperCase()) {
            case "SOL":
                return Clave.SOL;
            case "FA":
                return Clave.FA;
            case "DO":
                return Clave.DO;
            default:
                throw new IllegalArgumentException("Clave no valida solo puede ser SOL, FA o DO: " + word);
        }
    }
}
