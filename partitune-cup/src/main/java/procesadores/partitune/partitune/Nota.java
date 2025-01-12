package procesadores.partitune.partitune;
import lombok.Data;
import lombok.NonNull;

@Data
public class Nota {
    public @NonNull NotaBase nota_base;
    public Modificador modificador = Modificador.BECUADRO;
    public Octava octava = Octava.NORMAL;
    public boolean puntillo = false;
    
}