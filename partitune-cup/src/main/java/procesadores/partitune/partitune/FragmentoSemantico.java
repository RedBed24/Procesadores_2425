package procesadores.partitune.partitune;
import java.util.List;

import lombok.Getter;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Setter
@Getter
@RequiredArgsConstructor
public class FragmentoSemantico extends FragmentoSimple{
    
    @NonNull public List<Object> secuencias;
    public int linea;
    public int columna;
    
    public Clave clave;
    public Compas compas;
    public Armadura armadura;

    public FragmentoSemantico(String nombre, List<Object> secuencias, int linea, int columna, Clave clave, Compas compas, Armadura armadura) {
        super(nombre);
        this.secuencias = secuencias;
        this.linea = linea;
        this.columna = columna;
        this.clave = clave;
        this.compas = compas;
        this.armadura = armadura;
    }
}

