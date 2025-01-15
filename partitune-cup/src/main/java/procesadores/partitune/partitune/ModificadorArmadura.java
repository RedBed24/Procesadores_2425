package procesadores.partitune.partitune;

public enum ModificadorArmadura {
    SOSTENIDO,
    BEMOL;

    public static ModificadorArmadura getModificadorType(Modificador mod) {
        switch (mod) {
            case Modificador.SOSTENIDO:
                return ModificadorArmadura.SOSTENIDO;
            case Modificador.BEMOL:
                return ModificadorArmadura.BEMOL;
            default:
                throw new IllegalArgumentException("Modificador de armadura no valido: " + mod);
        }
    }
}
