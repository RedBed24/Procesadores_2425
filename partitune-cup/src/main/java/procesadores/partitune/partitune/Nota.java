package procesadores.partitune.partitune;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NonNull;

@Data
@AllArgsConstructor
public class Nota {
    public @NonNull NotaBase nota_base;
    public Modificador modificador = null;
    public Octava octava = Octava.NORMAL;
    public boolean puntillo = false;
    
}