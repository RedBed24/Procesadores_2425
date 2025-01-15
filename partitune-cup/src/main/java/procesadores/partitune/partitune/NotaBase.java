package procesadores.partitune.partitune;

public enum NotaBase {
    DO,
    RE,
    MI,
    FA,
    SOL,
    LA,
    SI;
    
    public static NotaBase getNoteType(String word) {
        switch (word.toUpperCase()) {
            case "DO":
                return NotaBase.DO;
            case "RE":
                return NotaBase.RE;
            case "MI":
                return NotaBase.MI;
            case "FA":
                return NotaBase.FA;
            case "SOL":
                return NotaBase.SOL;
            case "LA":
                return NotaBase.LA;
            case "SI":
                return NotaBase.SI;
            default:
                throw new IllegalArgumentException("Nota Base no valida: " + word);
        }
    }
}
