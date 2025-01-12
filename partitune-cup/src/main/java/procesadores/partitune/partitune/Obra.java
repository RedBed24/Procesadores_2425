package procesadores.partitune.partitune;
import java.util.List;

import lombok.Data;

@Data
public class Obra {
    public String nombre;
    public Clave clave = Clave.SOL;
    public Compas compas = Compas.DOSPORCUATRO;
    public Armadura armadura; //opcional
    public List<Object> bloque_notas;

    public Obra(String nombre, Clave clave, Compas compas, Armadura armadura, List<Object> bloque_notas) {
        this.nombre = nombre;
        this.clave = clave;
        this.compas = compas;
        this.armadura = armadura;
        this.bloque_notas = bloque_notas;
    }

    public Obra(String nombre, Clave clave, Compas compas) {
        this(nombre, clave, compas, null, null);
    }
    public Obra(String nombre, Clave clave, Compas compas, List<Object> bloque_notas) {
        this(nombre, clave, compas, null, bloque_notas);
    }
}
