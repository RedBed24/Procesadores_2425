package procesadores.partitune.partitune;

public enum Compas {
    DOSPORCUATRO,
    TRESPORCUATRO,
    CUATROPORCUATRO,
    SEISPOROCHO;

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
                throw new IllegalArgumentException("Compas no valido: " + word);
        }
    }
}
