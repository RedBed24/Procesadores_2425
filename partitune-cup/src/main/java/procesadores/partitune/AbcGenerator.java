package procesadores.partitune;
import java.util.*;
import java.util.regex.*;
import java.math.BigInteger;


public class AbcGenerator {

    private static String duracionToAbc(Nota nota, Duracion duracion) {
       
        // Sin puntillo
        switch (duracion) {
            case SEMIFUSA:      return "1/16";
            case FUSA:          return "1/8";
            case SEMICORCHEA:   return "1/4";
            case CORCHEA:       return "1/2";
            case NEGRA:         return "1";
            case BLANCA:        return "2";
            case REDONDA:       return "4";
            default:            return "";
        }
        
    }

    private static String procesarNota(Nota nota) {
        // Mapeo de notas base
        Map<String, String> notaBaseMap = new HashMap<>();
        notaBaseMap.put("DO",  "C");
        notaBaseMap.put("RE",  "D");
        notaBaseMap.put("MI",  "E");
        notaBaseMap.put("FA",  "F");
        notaBaseMap.put("SOL", "G");
        notaBaseMap.put("LA",  "A");
        notaBaseMap.put("SI",  "B");

        String base = notaBaseMap.getOrDefault(nota.getNotaBase().name(), "C");

        // Mapeo de modificadores
        String mod = "";
        if (nota.getModificador() != null) {
            switch (nota.getModificador()) {
                case SOSTENIDO: mod = "^"; break;
                case BEMOL:     mod = "_"; break;
                case BECUADRO:  mod = "="; break;
                default:        mod = "";
            }
        }

        // Ajuste de octava (ejemplo: 'AGUDO' => minúscula, 'GRAVE' => añadir coma)
        switch (nota.getOctava()) {
            case AGUDO:
                // minúscula
                base = base.toLowerCase();
                break;
            case GRAVE:
                // añade coma
                base = base + ",";
                break;
            default:
                // Sin modificación
                break;
        }

        return mod + base;
    }


    private static String procesarSecuencia(Secuencia secuencia) {
        List<String> notasAbc = new ArrayList<>();
        for (Nota nota : secuencia.getListaNotas()) {
            if (nota == null) {
                // Silencio
                notasAbc.add("z" + duracionToAbc(nota, secuencia.getDuracion()));
            } else {
                // Nota normal
                String n = procesarNota(nota) + duracionToAbc(nota, secuencia.getDuracion());
                notasAbc.add(n);
            }
        }
        // Unimos con espacio
        return String.join(" ", notasAbc);
    }


    private static String parseCompas(Compas compas) {
        // Asume compas.value como "4/4", "3/4", etc.
        return compas.getValue();
    }

    private static String procesarBloque(List<Object> bloqueNotas, Clave claveActual, Compas compasActual, Armadura armaduraActual) {
        StringBuilder sb = new StringBuilder();

        for (Object elemento : bloqueNotas) {
            if (elemento instanceof Secuencia) {
                sb.append(procesarSecuencia((Secuencia) elemento)).append(" ");
            }
            // else if (elemento instanceof Repeticion) {
            //     sb.append(procesarRepeticion((Repeticion) elemento)).append(" ");
            // }
            // else if (elemento instanceof Ligadura) {
            //     sb.append(procesarLigadura((Ligadura) elemento)).append(" ");
            // }
            else if (elemento instanceof Fragmento) {
                Fragmento fragmento = (Fragmento) elemento;
                List<String> cambios = new ArrayList<>();

                // Claves y armaduras
                Clave nuevaClave = claveActual;
                Armadura nuevaArmadura = armaduraActual;
                if (fragmento.getClave() != null) {
                    nuevaClave = fragmento.getClave();
                    nuevaArmadura = fragmento.getArmadura();
                    cambios.add("K:" + parseClave(nuevaClave, nuevaArmadura));
                }

                // Compás
                Compas nuevoCompas = compasActual;
                if (fragmento.getCompas() != null) {
                    nuevoCompas = fragmento.getCompas();
                    cambios.add("M:" + parseCompas(nuevoCompas));
                }

                if (!cambios.isEmpty()) {
                    sb.append(String.join("", cambios)).append("\n");
                }

                // Procesar recursivamente
                String contenidoFrag = procesarBloque(fragmento.getBloqueNotas(), nuevaClave, nuevoCompas, nuevaArmadura);
                sb.append(contenidoFrag).append("\n");

                List<String> reversiones = new ArrayList<>();
                if (fragmento.getClave() != null) {
                    reversiones.add("K:" + parseClave(claveActual, armaduraActual));
                }
                if (fragmento.getCompas() != null) {
                    reversiones.add("M:" + parseCompas(compasActual));
                }
                if (!reversiones.isEmpty()) {
                    sb.append(String.join("", reversiones)).append("\n");
                }
            }
        }

        return sb.toString();
    }


    private static boolean elementoEsNota(String elemento) {
        String upper = elemento.toUpperCase();
        return (upper.contains("C") 
             || upper.contains("D")
             || upper.contains("E")
             || upper.contains("F")
             || upper.contains("G")
             || upper.contains("A")
             || upper.contains("B")
             || upper.contains("Z"));
    }


    private static float valorDuracion(String elemento) {
        Pattern pattern = Pattern.compile("\\d+");
        Matcher matcher = pattern.matcher(elemento);
        
        List<Integer> nums = new ArrayList<>();
        while (matcher.find()) {
            nums.add(Integer.parseInt(matcher.group()));
        }

        if (nums.isEmpty()) {
            return 1.0f;
        }
        int numerador = nums.get(0);
        int denominador = (nums.size() > 1) ? nums.get(1) : 1;
        return (float) numerador / (float) denominador;
    }

    public static String generarAbc(Obra obra) {
        List<String> abcLines = new ArrayList<>();
        // Encabezado
        abcLines.add("X:1");                       // referencia
        abcLines.add("T:" + obra.getNombre());     // título
        abcLines.add("M:" + parseCompas(obra.getCompas()));
        abcLines.add("K:" + parseClave(obra.getClave(), obra.getArmadura()));

        // Procesamos el bloque de notas
        String cuerpo = procesarBloque(
                obra.getBloqueNotas(),
                obra.getClave(),
                obra.getCompas(),
                obra.getArmadura()
        );

        // Insertamos las líneas divisorias
        cuerpo = generarLineasDivisorias(cuerpo, obra.getCompas());
        abcLines.add(cuerpo);

        // Unir todo
        return String.join("\n", abcLines);
    }

    
    public static void generateAbc(String inputFile) throws Exception {
        
        // Obtener la obra
        Obra obra = listener.getObra();

        // Generar la notación ABC
        String abc = generarAbc(obra);

        // Imprimir o guardar
        System.out.println(abc);
    }

}
