package procesadores.partitune.partitune;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class FragmentoSemantico extends FragmentoSimple{
    
    public List<Object> secuencias;
    public int linea;
    public int columna;
    
    public Clave clave;
    public Compas compas;
    public Armadura armadura;

    public FragmentoSemantico(List<Object> secuencias, int linea, int columna) {
        this();
        this.secuencias = secuencias;
        this.linea = linea;
        this.columna = columna;
    }
}

