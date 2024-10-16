# Proyecto de IPD 440

Se busca construir un simulador de estacionamiento en el que se pueda mejorar un algoritmo de enrutamiento basado en Dijkstra para optimizar consumo de combustible, tiempo, etc.

## Instalación

- Clonar este repositorio.
- En la carpeta raíz ejecutar python -m venv venv
- Activar el entorno venv/Scripts/activate (en Windows) o source venv/bin/activate (en Linux).
- pip install -r requirements.txt


## Cómo usar el editor de mapas

Al ejecutar el script map_editor.py se abrirá una ventana que mostrará una grilla con todas las celdas de la pantalla.

### Brocha

La brocha permite pintar casillas que van en cualquiera de las cuatro direcciones disponibles. También es posible pintar interesecciones y eliminar errores. Para pintar usando la brocha, se debe pulsar el botón correspondiente al tipo de celda que se quiera pintar (descripción más abajo) y hacer click izquierdo en la celda.

#### Pinceles

- Direcciones: Permiten el flujo vehicular solamente en una dirección. Seleccionar utilizando las flechas del teclado.
- Intersecciones: Conectan la celda pintada con todas las casillas adyacentes y no diagonales a su alrededor. Esto permite el acceso desde cualquiera que vaya en su dirección y salida hacia cualquier otra, lo que permite redirigir el tráfico proveniente de más de una rama. Seleccionar con la tecla Enter.
- Eliminaciones: Vuelven a pintar la celda blanca, haciendo que la casilla quede sin uso. Seleccionar con la tecla Suprimir (Del).
- Parkings: Habilitan la celda para estacionamiento. Conectan la casilla con todas a su alrededor para permitir entrar o salir del estacionamiento.

### Cómo guardar

Para guardar simplemente pulsar la tecla E. En la consola se verá el mensaje "Map exported".

## Cómo correr el simulador

- Ejecutar el script simulator.py. Para esto es necesario haber creado previamente un mapa.
