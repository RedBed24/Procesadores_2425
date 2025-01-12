package procesadores.partitune.partitune;

public enum Clave {
    SOL,
    FA,
    DO;
    
    public static Clave getClaveType(NotaBase notaBase) {
        switch (notaBase) {
            case NotaBase.SOL:
                return Clave.SOL;
            case NotaBase.FA:
                return Clave.FA;
            case NotaBase.DO:
                return Clave.DO;
            default:
                throw new IllegalArgumentException("Clave no valida solo puede ser SOL, FA o DO: " + notaBase);
        }
    }
}
