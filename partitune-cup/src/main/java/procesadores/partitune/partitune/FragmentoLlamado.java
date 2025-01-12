package procesadores.partitune.partitune;

public class FragmentoLlamado extends FragmentoSimple {
    public int linea;
    public int columna;


    public FragmentoLlamado(String nombre, int linea, int columna) {
        super(nombre);
        this.linea = linea;
        this.columna = columna;
    }
}
