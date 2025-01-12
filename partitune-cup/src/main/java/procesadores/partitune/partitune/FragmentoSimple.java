package procesadores.partitune.partitune;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
public class FragmentoSimple {
    public String nombre;

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Fragmento)){
            return false;
        }
        return ((Fragmento)obj).nombre.equals(this.nombre);
    }
}
