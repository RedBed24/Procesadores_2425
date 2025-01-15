package procesadores.partitune.partitune;
import lombok.Setter;
import lombok.Getter;

@Setter
@Getter
public class Fragmento extends FragmentoSimple {
    //opcionales
    public Clave clave; 
    public Compas compas; 
    public Armadura armadura;

    public Fragmento(String nombre, Clave clave, Compas compas, Armadura armadura) {
        super(nombre);
        this.clave = clave;
        this.compas = compas;
        this.armadura = armadura;
    }
    public Fragmento(String nombre) {
        this(nombre, null, null, null);
    }
}
