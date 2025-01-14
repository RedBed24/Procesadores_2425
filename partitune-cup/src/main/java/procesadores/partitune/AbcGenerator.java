package procesadores.partitune;

import procesadores.partitune.partitune.*;
import java.util.*;
import java.util.stream.Collectors;

public class AbcGenerator {

    public static String generateAbc(Obra obra) {
        // Encabezado del archivo ABC
        StringBuilder abcBuilder = new StringBuilder();
        abcBuilder.append("X:1\n"); // Número de referencia
        abcBuilder.append("T:").append(obra.getNombre()).append("\n"); // Título
        abcBuilder.append("M:").append(parseCompas(obra.getCompas())).append("\n"); // Compás
        abcBuilder.append("K:").append(parseClave(obra.getClave(), obra.getArmadura())).append("\n"); // Clave y armadura
        abcBuilder.append("L:1/4\n"); // Valor de referencia de la nota (negra)

        // Procesar el cuerpo de la obra
        String cuerpo = procesarBloque(obra.getBloque_notas(), 
                                       obra.getClave(), 
                                       obra.getCompas(), 
                                       obra.getArmadura());

        cuerpo = cuerpo.trim(); // Quitar espacios innecesarios 
        cuerpo = generarLineasDivisorias(cuerpo, obra.getCompas());
        abcBuilder.append(cuerpo); 

        return abcBuilder.toString();
    }

    private static String parseCompas(Compas compas) {
        switch (compas) {
            case DOSPORCUATRO:
                return "2/4";
            case TRESPORCUATRO:
                return "3/4";
            case CUATROPORCUATRO:
                return "4/4";
            case SEISPOROCHO:
                return "6/8";
            default:
                throw new IllegalArgumentException("Compas no válido: " + compas);
        }
    }

    private static String parseClave(Clave clave, Armadura armadura) {
        StringBuilder claveStr = new StringBuilder();
        switch (clave) {
            case SOL -> claveStr.append("");
            case FA -> claveStr.append("clef=bass");
            case DO -> claveStr.append("clef=alto");
        }

        if (armadura != null) {
            String[] notas = armadura.getTipo_modificacion() == ModificadorArmadura.BEMOL
                    ? new String[]{"F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"}
                    : new String[]{"G", "D", "A", "E", "B", "F#", "C#"};
            claveStr.append(" ").append(String.join(" ", Arrays.copyOf(notas, armadura.getCantidadModificadores())));
        } else {
            claveStr.append(" C");
        }

        return claveStr.toString();
    }

    private static String procesarBloque(List<Object> bloqueNotas, Clave clave, Compas compas, Armadura armadura) {
        StringBuilder resultado = new StringBuilder();

        for (Object elemento : bloqueNotas) {
            if (elemento instanceof Secuencia) {
                resultado.append(procesarSecuencia((Secuencia) elemento)).append(" ");
            } else if (elemento instanceof Repeticion) {
                resultado.append(procesarRepeticion((Repeticion) elemento)).append(" ");
            } else if (elemento instanceof Ligadura) {
                resultado.append(procesarLigadura((Ligadura) elemento)).append(" ");
            } else if (elemento instanceof FragmentoSemantico fragmentoSemantico) {
                if (fragmentoSemantico.getClave() != null || fragmentoSemantico.getCompas() != null) {
                    if (fragmentoSemantico.getClave() != null) {
                        resultado.append("K:").append(parseClave(fragmentoSemantico.getClave(), fragmentoSemantico.getArmadura())).append("\n");
                    }
                    if (fragmentoSemantico.getCompas() != null) {
                        resultado.append("M:").append(parseCompas(fragmentoSemantico.getCompas())).append("\n");
                    }
                }

                resultado.append(procesarBloque(fragmentoSemantico.getSecuencias(), 
                                               fragmentoSemantico.getClave() != null ? fragmentoSemantico.getClave() : clave,
                                               fragmentoSemantico.getCompas() != null ? fragmentoSemantico.getCompas() : compas,
                                               fragmentoSemantico.getArmadura() != null ? fragmentoSemantico.getArmadura() : armadura)).append("\n");
            } else if (elemento instanceof Fragmento fragmento) {
                if (fragmento.getClave() != null || fragmento.getCompas() != null) {
                    if (fragmento.getClave() != null) {
                        resultado.append("K:").append(parseClave(fragmento.getClave(), fragmento.getArmadura())).append("\n");
                    }
                    if (fragmento.getCompas() != null) {
                        resultado.append("M:").append(parseCompas(fragmento.getCompas())).append("\n");
                    }
                }
            }
        }

        return resultado.toString();
    }

    private static String procesarSecuencia(Secuencia secuencia) {
        return secuencia.getNotas().stream()
                .map(nota -> {
                    if (nota == null) {
                        return "z" + duracionToAbc(null, secuencia.getDuracion());
                    } else {
                        return procesarNota(nota) + duracionToAbc(nota, secuencia.getDuracion());
                    }
                })
                .collect(Collectors.joining(" "));
    }

    private static String procesarRepeticion(Repeticion repeticion) {
        String cuerpo = repeticion.getSecuencias().stream()
                .map(AbcGenerator::procesarSecuencia)
                .collect(Collectors.joining(" "));

        if (repeticion.getTipo_repeticion() == TipoRepeticion.CON_INICIO) {
            return "|: " + cuerpo + " :|";
        } else {
            return cuerpo + " :|";
        }
    }

    private static String procesarLigadura(Ligadura ligadura) {
        return ligadura.getSecuencias().stream()
                .map(secuencia -> "(" + procesarSecuencia(secuencia) + ")")
                .collect(Collectors.joining(" "));
    }

    private static String procesarNota(Nota nota) {
        Map<NotaBase, String> notaBaseMap = Map.of(
                NotaBase.DO, "C",
                NotaBase.RE, "D",
                NotaBase.MI, "E",
                NotaBase.FA, "F",
                NotaBase.SOL, "G",
                NotaBase.LA, "A",
                NotaBase.SI, "B"
        );

        String base = notaBaseMap.getOrDefault(nota.getNota_base(), "C");
        if (nota.getOctava() == Octava.AGUDO) {
            base = base.toLowerCase();
        } else if (nota.getOctava() == Octava.GRAVE) {
            base += ",";
        }

        Map<Modificador, String> modMap = Map.of(
                Modificador.SOSTENIDO, "^",
                Modificador.BEMOL, "_",
                Modificador.BECUADRO, "="
        );
        String modificador = nota.getModificador() != null ? modMap.getOrDefault(nota.getModificador(), "") : "";
        return modificador + base;
    }

    private static String duracionToAbc(Nota nota, Duracion duracion) {
        Map<Duracion, String> duracionMap = nota != null && nota.isPuntillo()
                ? Map.of(
                Duracion.SEMIFUSA, "3/32",
                Duracion.FUSA, "3/16",
                Duracion.SEMICORCHEA, "3/8",
                Duracion.CORCHEA, "3/4",
                Duracion.NEGRA, "3/2",
                Duracion.BLANCA, "3",
                Duracion.REDONDA, "6"
        ) : Map.of(
                Duracion.SEMIFUSA, "1/16",
                Duracion.FUSA, "1/8",
                Duracion.SEMICORCHEA, "1/4",
                Duracion.CORCHEA, "1/2",
                Duracion.NEGRA, "1",
                Duracion.BLANCA, "2",
                Duracion.REDONDA, "4"
        );

        return duracionMap.getOrDefault(duracion, "");
    }

        private static String generarLineasDivisorias(String abcCuerpo, Compas compas) {
        float pulsosTotales = obtenerPulsosPorCompas(compas);
        float pulsosRestantes = pulsosTotales;
        StringBuilder resultado = new StringBuilder();

        for (String linea : abcCuerpo.split("\\n")) {
            if (linea.startsWith("M:") || linea.startsWith("K:")) {
                resultado.append(linea).append("\n");
                continue;
            }

            for (String elemento : linea.split(" ")) {
                if (elemento.isEmpty()) {
                    continue;
                }

                if (esNotaOUnSilencio(elemento)) {
                    double duracionElemento = obtenerDuracion(elemento);
                    
                    if (duracionElemento > pulsosTotales){
                        duracionElemento = pulsosTotales;
                    }
                    
                    if (duracionElemento > pulsosRestantes) {
                        if (pulsosRestantes > 0) {
                            resultado.append("z").append(valorSilencio(pulsosRestantes)).append(" | ");
                        }
                        resultado.append(dividirNota(elemento, duracionElemento)).append(" ");
                        pulsosRestantes = pulsosTotales - (float) duracionElemento;
                    } else {
                        resultado.append(dividirNota(elemento, duracionElemento)).append(" ");
                        pulsosRestantes -= duracionElemento;

                        if (pulsosRestantes == 0) {
                            resultado.append("| ");
                            pulsosRestantes = pulsosTotales;
                        }
                    }
                } else {
                    resultado.append(elemento).append(" ");
                }
            }

            resultado.append("\n");
        }

        return resultado.toString();
    }

    private static String dividirNota(String elemento, double duracion) {
        if (duracion % 1 == 0) {
            return elemento.replaceAll("[0-9]+(/[0-9]+)?", String.valueOf((int) duracion));
        } else {
            int numerador = (int) Math.round(duracion * 16);
            int denominador = 16;
            while (numerador % 2 == 0 && denominador > 1) {
                numerador /= 2;
                denominador /= 2;
            }
            return elemento.replaceAll("[0-9]+(/[0-9]+)?", numerador + "/" + denominador);
        }
    }

    private static String valorSilencio(double duracion) {
        if (duracion % 1 == 0) {
            return String.valueOf((int) duracion);
        } else {
            int numerador = (int) Math.round(duracion * 16);
            int denominador = 16;
            while (numerador % 2 == 0 && denominador > 1) {
                numerador /= 2;
                denominador /= 2;
            }
            return numerador + "/" + denominador;
        }
    }

    private static boolean esNotaOUnSilencio(String elemento) {
        return elemento.matches("[A-Ga-gz].*");
    }

    private static double obtenerDuracion(String elemento) {
        // Extraer números y fracciones del elemento
        List<Character> numeros = new ArrayList<>();
        for (char c : elemento.toCharArray()) {
            if (Character.isDigit(c)) {
            numeros.add(c);
            }
        }
        if (numeros.isEmpty()) {
            return 1.0; 
        }
        if (numeros.size() == 1) {
            return Double.parseDouble(numeros.get(0).toString());
        }
        try {
            double numerador = Double.parseDouble(numeros.get(0).toString());
            double denominador = Double.parseDouble(numeros.get(1).toString());
            return numerador / denominador;
        } catch (NumberFormatException e) {
            // Si el formato no es válido, devolver duración predeterminada
            return 1.0;
        }
    }


    private static int obtenerPulsosPorCompas(Compas compas) {
        switch (compas) {
            case DOSPORCUATRO: return 2;
            case TRESPORCUATRO: return 3;
            case CUATROPORCUATRO: return 4;
            case SEISPOROCHO: return 6; // Manejo como ternario compuesto
            default: throw new IllegalArgumentException("Compas no válido: " + compas);
        }
    }
}
