package procesadores.partitune;

import procesadores.partitune.parser;
import procesadores.partitune.partitune.Obra;
import java_cup.runtime.*;
import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Uso: java -jar partitune.jar <archivo_entrada>");
            System.exit(1);
        }

        String inputFile = args[0];

        try (FileInputStream stream = new FileInputStream(inputFile);
             Reader reader = new InputStreamReader(stream)) {

            // Crear el parser
            parser parser = new parser(new Scanner(reader));

            // Parsear el archivo
            Symbol result = parser.parse();
            Obra obra = (Obra) result.value;

            // Generar el archivo ABC
            String abcContent = AbcGenerator.generateAbc(obra);
            String outputFileName = inputFile.replace(".txt", ".abc");
            Files.writeString(Paths.get(outputFileName), abcContent);

            System.out.println("Archivo ABC generado: " + outputFileName);

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Error durante el análisis");
            System.exit(1);
        }
    }
}