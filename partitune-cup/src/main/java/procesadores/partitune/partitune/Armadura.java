package procesadores.partitune.partitune;
import java.util.List;
import java.util.Arrays;

import lombok.Getter;
import lombok.ToString;

@Getter
@ToString
public class Armadura {
    public int cantidadModificadores;
    public ModificadorArmadura tipo_modificacion;

    public Armadura(ModificadorArmadura tipo_modificacion, List<NotaArmadura> notas) {
        this.tipo_modificacion = tipo_modificacion;
        this.cantidadModificadores = validate_armadura(tipo_modificacion, notas);
    }

    public int validate_armadura(ModificadorArmadura tipo_modificacion, List<NotaArmadura> notas) {
        List<NotaBase> notas_posibles;
        int i = 0;

        switch (tipo_modificacion) {
            case BEMOL:
                notas_posibles = Arrays.asList(
                NotaBase.SI,
                NotaBase.MI,
                NotaBase.LA,
                NotaBase.RE,
                NotaBase.SOL,
                NotaBase.DO,
                NotaBase.FA
            );
                break;
            case SOSTENIDO:
                notas_posibles = Arrays.asList(
                    NotaBase.FA,
                    NotaBase.DO,
                    NotaBase.SOL,
                    NotaBase.RE,
                    NotaBase.LA,
                    NotaBase.MI,
                    NotaBase.SI
                );
                break;
            default:
                throw new IllegalArgumentException("Tipo de modificación no válido.");
        }

        int[] cuenta = new int[notas_posibles.size()];


        for (NotaArmadura nota : notas) {
            cuenta[notas_posibles.indexOf(nota.getNota())]++;
        }

        for (i = 0; i < cuenta.length; i++) {
            if (cuenta[i] == 0) {
                break;
            }
        }
        // caso: [1, 1, 0, 1, 1, 1, 1] falta una nota pero despues hay
        for (int j = i + 1; j < cuenta.length; j++) {
            if (cuenta[j] != 0) {
                throw new IllegalArgumentException("Las notas de la armadura no son válidas.");
            }
        }

        return i;
    }
}
