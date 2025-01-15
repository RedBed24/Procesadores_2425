# Partitune Yacc

## Requirements

- Java 21
- Maven 3.8.1

## Usage

Aunque ya se incluye un ejecutable, también se puede compilar el proyecto con Maven.

Usando el jar que se proporciona:
```bash
java -jar partitune-cup.jar input.txt
```

Con MAVEN, para compilar el proyecto:
```bash
mvn clean compile
mvn clean package
```
Para ejecutar el proyecto compilado:
```bash
java -jar target/partitune-cup-0.0.0.jar input.txt
```

## Examples

TEST-1: generacion es correcta
TEST-2: Semantic error: En la ligadura no puede haber silencios 
TEST-3: manejo de fragmentos con cambios de compas
TEST-4: armadura incorrecta y ligadura con menos de 2 notas
TEST-5: generacion es correcta con fragmentos
