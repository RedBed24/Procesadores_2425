package procesadores.partitune.partitune;
import procesadores.partitune.sym;

public enum Modificador {
    SOSTENIDO,
    BEMOL,
    BECUADRO;

    public static Modificador getModificadorType(int modificador) {
        switch (modificador) {
            case sym.SOSTENIDO:
                return Modificador.SOSTENIDO;
            case sym.BEMOL:
                return Modificador.BEMOL;
            case sym.BECUADRO:
                return Modificador.BECUADRO;
            default:
                throw new IllegalArgumentException("Modificador no valido: " + modificador);
        }
    }
}
