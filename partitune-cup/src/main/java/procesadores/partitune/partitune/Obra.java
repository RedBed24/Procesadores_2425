package procesadores.partitune.partitune;
import lombok.Data;

@Data
public class Obra {
    public String nombre;
    public Clave clave = Clave.SOL;
    public Compas compas = Compas.DOSPORCUATRO;
    public Armadura armadura; //opcional

    public Obra(String nombre, Clave clave, Compas compas, Armadura armadura) {
        this.nombre = nombre;
        this.clave = clave;
        this.compas = compas;
        this.armadura = armadura;
    }

    public Obra(String nombre, Clave clave, Compas compas) {
        this(nombre, clave, compas, null);
    }

}
