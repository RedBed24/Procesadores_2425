package procesadores.partitune.partitune;
import java.util.List;
import lombok.Data;

@Data
public class Secuencia {
    public Duracion duracion;
    public List<Nota> notas; //silencios?
}
