# API

Documentacuón de la API de la aplicación.

## Endpoints

### GET /iamalive

Devuelve un mensaje de confirmación de que el servidor está activo.

### POST /generate_abc

El endpoint /generate_abc recibe un archivo en formato partitune, llama al compilador de partitune y devuelve el archivo en formato abc o un mensajde de error si no se pudo generar el archivo.


Input:
- file: archivo en formato partitune

Ejemplo:
```bash
curl -X POST "http://localhost:8000/generate_abc" -F "file=@path/to/your/file.partitune"
```

Output, respuesta exitosa:
- status: 200
- content: JSON
´´´json
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

En desarrollo:
```bash
uvicorn main:app --reload
```

En producción:
```bash
uvicorn main:app
```