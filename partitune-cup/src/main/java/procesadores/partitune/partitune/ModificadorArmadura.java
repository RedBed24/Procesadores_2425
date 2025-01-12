package procesadores.partitune.partitune;

public enum ModificadorArmadura {
    SOSTENIDO,
    BEMOL;

    public static ModificadorArmadura getModificadorType(String modificador) {
        switch (modificador) {
            case "#":
                return ModificadorArmadura.SOSTENIDO;
            case "b":
                return ModificadorArmadura.BEMOL;
            default:
                throw new IllegalArgumentException("Modificador de armadura no valido: " + modificador);
        }
    }
}
