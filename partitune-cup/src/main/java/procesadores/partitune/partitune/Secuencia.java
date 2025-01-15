package procesadores.partitune.partitune;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Secuencia {
    public Duracion duracion;
    public List<Nota> notas; //silencios?
}
