package procesadores.partitune.partitune;

public enum TipoRepeticion {
    CON_INICIO(0),
    CON_FINAL(1);

    private final int value;

    TipoRepeticion(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}
