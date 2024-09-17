# Tubitos y bolitas

## Estructura

* Server: Backend utilizado para el modo multijugador.

* App: Interfaz del cliente

## Librerías principales utilizadas

**App**

* Pygame
* SocketIO

**Server**

* Flask
* flask-socketio

## Estructura del cliente

* app.py: Script con el bucle principal de pygame. Llama a determinada pantalla (screen) dependiendo del contexto.

* screens/: Contiene las pantallas del juego. Todas las pantallas asumen ya estar dentro de un bucle de pygame, y requieren de tres argumentos: *screen*, *switch_screen*, y *font*.

* components/: Contiene los componentes que se pueden reutilizar a lo largo del proyecto, e.g. *button.py*, e *input_field.py*; y los componentes complejos que se benefician de un código modular, e.g. *room_input_field.py*.

* utilities/: Contiene funciones que se pueden reutilizar a lo largo del proyecto, e.g. *generar_tubitos.py*, y *mover_bolita.py*

## Estructura del servidor

* server.py

### flask-socketio backend

El servidor se utiliza únicamente para la sincronización de datos de diferentes clientes en modo multijugador. El cliente se actualiza por medio de websockets distribuidos en cuartos (rooms).

> ### Advertencia! 
> Para que el modo multijugador funcione, se tiene que inicializar el servidor
> ```$ python server.py```
> En caso de querer conectar distintos dispositivos, se tiene que ajustar respectivamente la ip del servidor en screens/room_selection.py > connect_socket()