# API

Documentación de la API de la aplicación.

## Endpoints

### GET /iamalive

Devuelve un mensaje de confirmación de que el servidor está activo.

### POST /generateABC

El endpoint /generateABC recibe un archivo en formato partitune, llama al procesador de partitune y devuelve el archivo en formato abc o un mensajde de error si no se pudo generar el archivo.

Input:
- file: archivo en formato partitune

Ejemplo:
```bash
curl -X POST "http://localhost:8000/generateABC" -F "file=@path/to/your/file.partitune"
```

Output, respuesta exitosa:
- status: 200
- content: JSON   
```json
{
  "filename": "generated_file.abc",
  "content": "contenido del archivo abc"
}
```

Output, respuesta fallida:
- status: 500
- content: JSON  
```json
{
  "detail": "Error generating abc file."
}
```

## Ejectuar la aplicación

Instalar las dependencias necesarias:

1. Instalar el paquete de `Partitune`:  
En la carpeta de `antlr` ejecutar el siguiente comando:
```bash
pip install .
```

2. Instalar las dependencias de la API:
```bash
pip install fastapi[standard]
```

3. Ejecutar el servidor:

Desde la carpeta `api` ejecutar el siguiente comando para iniciar el servidor:

En desarrollo:
```bash
uvicorn src.main:app --reload
```

En producción:
```bash
uvicorn src.main:app
```