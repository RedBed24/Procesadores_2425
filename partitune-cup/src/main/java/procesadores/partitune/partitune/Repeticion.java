package procesadores.partitune.partitune;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Repeticion {
    public TipoRepeticion tipo_repeticion;    
    public List<Secuencia> secuencias;
}
