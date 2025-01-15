# Partitune

Partitune makes music composition easy.
Describe your song in a simple text format and translate it into an ABC notation file.

## Usage

bash
mvn clean compile

mvn clean package

java -jar target/partitune-cup-0.0.0.jar input.txt

## Tests

TEST-1: generacion es correcta
TEST-2: Semantic error: En la ligadura no puede haber silencios 
TEST-3: manejo de fragmentos con cambios de compas
TEST-4: armadura incorrecta y ligadura con menos de 2 notas
TEST-5: generacion es correcta con fragmentos
