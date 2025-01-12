package procesadores.partitune.partitune;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Obra {
    public String nombre;
    public Clave clave = Clave.SOL;
    public Compas compas = Compas.DOSPORCUATRO;
    public Armadura armadura; //opcional
    public List<Object> bloque_notas;

    public Obra(String nombre, List<Object> bloque_notas) {
        this();
        this.nombre = nombre;
        this.bloque_notas = bloque_notas;
    }
}
