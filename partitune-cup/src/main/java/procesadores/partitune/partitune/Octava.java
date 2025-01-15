package procesadores.partitune.partitune;

public enum Octava {
    GRAVE,
    NORMAL,
    AGUDO;
    
    public static Octava getOctaveType(String octava) {
        switch (octava) {
            case "'":
                return Octava.AGUDO;
            case "":
                return Octava.NORMAL;
            case "_":
                return Octava.GRAVE;
            default:
                throw new IllegalArgumentException("Octava no valida: " + octava);
        }
    }
}
