# Web para interactuar con la API

La web permite generar partituras en el lenguaje 'Partitune' y convertirlas a 'ABC'. La web se conecta a la API del backend para realizar la conversión. Además, permite visualizar las partituras y reproducirlas.

## Apartados

### Editor

Esta página se abre por defecto. Tiene un cuadro de texto para que el usuario pueda escribir. Debajo hay un botón para subir un archivo. Los otros botones permiten borrar el contenido del cuadro de texto y enviar el contenido al backend.

Debajo del editor, se muestra a la izquierda la partitura en formato 'ABC' y a la derecha el reproductor de audio y la partitura. Todo esto se puede descargar.

### Ejemplos

TODO: Añadir ejemplos ya generados

### Ayuda

Muestra los autores.
TODO: Añadir ayuda



## Ejectuar la aplicación

Instalar dependencias:
```bash
npm install
```

En desarrollo:
```bash
npm run dev
```

En producción:
```bash
npm run build
npm run start
```
