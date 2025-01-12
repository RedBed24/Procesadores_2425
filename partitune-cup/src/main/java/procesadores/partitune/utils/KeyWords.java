package procesadores.partitune.utils;
import procesadores.partitune.sym;
import procesadores.partitune.partitune.*;

import java.util.Arrays;
import java.util.List;


public class KeyWords {
    private static final List<String> KEY_WORDS = Arrays.asList(
        "fragmento",
        "obra",
        "clave",
        "compas",
        "armadura",
        "lig",
        "DO", "RE", "MI", "FA", "SOL", "LA", "SI",
        "sf", "f", "sc", "c", "n", "bl", "r",
        "b"
    );

    public static boolean isKeyWord(String word) {
        for (String keyWord : KEY_WORDS) {
            if (keyWord.equalsIgnoreCase(word)) {
                return true;
            }
        }
        return false;
    }

    public static int getTokenType(String word) {
        switch (word.toLowerCase()) {
            case "fragmento":
                return sym.FRAGMENTO;
            case "obra":
                return sym.OBRA;
            case "clave":
                return sym.CLAVE;
            case "compas":
                return sym.COMPAS;
            case "armadura":
                return sym.ARMADURA;
            case "lig":
                return sym.LIGADURA;
            case "do":
            case "re":
            case "mi":
            case "fa":
            case "sol":
            case "la":
            case "si":
                return sym.NOTA_BASE;
            case "sf":
            case "f":
            case "sc":
            case "c":
            case "n":
            case "bl":
            case "r":
                return sym.DURACION;
            case "b":
                return sym.BEMOL;
            default:
                throw new IllegalArgumentException(word);
        }
    }
    public static Object returnPartituneObject(int tokenType, String word) {
        switch (tokenType) {
            case sym.NOTA_BASE:
                return NotaBase.getNoteType(word);
            case sym.DURACION:
                return Duracion.getDurationType(word);
            case sym.BEMOL:
                return Modificador.getModificadorType(sym.BEMOL);
            default:
            return new String(word);
        }
}
