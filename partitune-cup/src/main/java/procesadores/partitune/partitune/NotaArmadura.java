package procesadores.partitune.partitune;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class NotaArmadura {
    public ModificadorArmadura modificador = ModificadorArmadura.BEMOL;
    public NotaBase nota;
}
