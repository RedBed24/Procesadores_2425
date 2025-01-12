package procesadores.partitune.partitune;

import java.util.List;

public class ObraSemantica extends Obra{
    public List<Object> bloque_notas;

    public ObraSemantica(String nombre, Clave clave, Compas compas, Armadura armadura, List<Object> bloque_notas) {
        super(nombre, clave, compas, armadura);
        this.bloque_notas = bloque_notas;
    }
}
