package procesadores.partitune.partitune;
import java.util.List;
import lombok.Data;

@Data
public class Repeticion {
    public TipoRepeticion tipo_repeticion;    
    public List<Secuencia> secuencias;
}
