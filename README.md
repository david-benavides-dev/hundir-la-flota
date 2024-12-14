[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2hBlx73D)
# Práctica Primer Trimestre (U1, U2 y U3)

# Hundir la flota Multijugador



### Objetivo del juego:
Hundir todos los barcos del rival antes de que el hunda los tuyos.


### Funcionamiento:
- Al iniciar el programa, se mostrará un menu al usuario con tres posibles opciones:
```
        ═════════════════════════════════════════
                    PIRATAS CALETEROS
        ═════════════════════════════════════════
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Unirse a una partida
           3. 🚪 Salir
        ═════════════════════════════════════════

Yaaarrr? >>
```        

1. Iniciar una nueva partida

    - Crea una partida nueva, solicitando al usuario su nombre y el nombre para la partida a crear. Además, se asignará como Jugador 1 de esa partida.
      ```
        Nombre J1 >> David
        Introduce el nombre de la partida >> prueba
        ```
    - Creará la carpeta 'src/partidas_hundirflota' en el caso de que no exista, junto con el archivo de configuración inicial con el mismo nombre que la partida.
        ```
        /src
        └── /partidas_hundirflota
            └── /prueba
                └── prueba.json
        ```
    - A continuación pedirá al usuario colocar sus barcos en el tablero. En este juego existen los siguientes barcos:

        - Portafritura: Una unidad, de tamaño 5.
        - Gamba de Oro: Dos unidades, de tamaño 2
        - Barquita de la Casería: Tres unidades, de tamaño 1.
    
        ```
                     Coloca tus barcos:
              ╔══════════════════════════════╗
            1 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            4 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            5 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            6 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            8 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            9 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
           10 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
              ╚══════════════════════════════╝
                A  B  C  D  E  F  G  H  I  J

        ⚓ Introduce coordenadas para colocar 'Portafritura' (T5) [1/1] >>
        ```
    - El programa seguirá preguntando al usuario por sus barcos hasta colocar todos correctamente.
    - El juego también permite declarar la orientación y dirección del barco a la hora de colocarlo, además de mostrar el barco a colocar, los barcos que quedan de ese tipo y el tamaño del mismo.
        ```
                    Coloca tus barcos:
            ╔══════════════════════════════╗
          1 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          4 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          5 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          6 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          8 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          9 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
         10 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            ╚══════════════════════════════╝
              A  B  C  D  E  F  G  H  I  J

        ⚓ Introduce coordenadas para colocar 'Portafritura' (T5) [1/1] >> 1,a
        ⚓ Introduce orientación y direccion '[H o V],[+ o -]' >> h,+
            Colocando Portafritura #1 ...
        ```

        ```
                   Coloca tus barcos:
            ╔══════════════════════════════╗
          1 ║ B  B  B  B  B  ~  ~  ~  ~  ~ ║
          2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          4 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          5 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          6 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          8 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          9 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
         10 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
            ╚══════════════════════════════╝
              A  B  C  D  E  F  G  H  I  J

        ⚓ Introduce coordenadas para colocar 'Gamba de Oro' (T2) [1/2] >>
        ```
    - Una vez el usuario termine de colocar sus barcos, se crea un archivo JSON de configuración en la carpeta con el mismo nombre de la partida, con el nombre "nombreDeLaPartida.j1.json"
    - Queda esperando a que exista el archivo "nombreDeLaPartida.j2.json" en bucle.
        ```
                    Coloca tus barcos:
            ╔══════════════════════════════╗
          1 ║ B  B  B  B  B  ~  ~  ~  ~  ~ ║
          2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          4 ║ ~  ~  ~  B  B  ~  ~  ~  ~  ~ ║
          5 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          6 ║ ~  ~  ~  B  B  ~  ~  ~  ~  ~ ║
          7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          8 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
          9 ║ ~  ~  ~  ~  ~  ~  ~  B  ~  ~ ║
         10 ║ B  ~  ~  ~  ~  ~  ~  ~  ~  B ║
            ╚══════════════════════════════╝
              A  B  C  D  E  F  G  H  I  J

        Archivo de jugador j1 - David creado con éxito.
        Esperando a J2...
        ```

2. Unirse a una partida
    - Intenta unirse a una partida ya creada mediante el nombre de la misma. En este caso, el jugador siempre será el Jugador 2.
    - El programa solicitará al usuario el nombre de la partida y verificará si los archivos de dicha partida existen. En el caso de que no existan, mostrará un mensaje de error al usuario.
    - Si la partida existe, pedirá un nombre al usuario y le dejará colocar sus barcos en su tablero, exactamente como cuando creas una partida.
    - Si todas las validaciones son correctas, existen los tres ficheros en la carpeta correspondiente y el J1 está esperando al J2, comienza el juego.
3. Salir
    - Salir del programa.

# Flujo del juego

El juego se desarrolla en una función llamada **jugar** con un **bucle principal** que organiza la lógica de turnos y permite que los jugadores alternen para atacar el tablero del oponente. 

Descripción del flujo del programa:

1. Un jugador comienza el juego identificado su **nombre** y el **nombre de la partida**. 
2. Se genera un archivo configuración general mediante un diccionario. Este archivo se usará para obtener las dimensiones del tablero, la configuración de los barcos y el jugador que comienza.
3. El programa intentará crear el archivo del j1.
3. Cada jugador dispone de su propio archivo JSON con su tablero, barcos, y registro de movimientos. Al iniciar, se generará el tablero en base a la configuración de los barcos, preguntando por la posición de cada uno. Esta posición tiene que ser correcta y no puede superponerse con otro barco, ni estar fuera del tablero. 
4. El jugador que crea la partida siempre será el jugador activo. Siendo el otro, el jugador pasivo.
5. Se muestra los tableros actualizados: jugador activo "tablero de ataque", y jugador pasivo "tablero de estado". 
```
Turno de Jugador 1

          Tablero de estado:
   ╔══════════════════════════════╗
 1 ║ B  B  B  B  B  ~  ~  ~  ~  ~ ║
 2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 4 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 5 ║ B  ~  ~  ~  B  B  ~  ~  ~  ~ ║
 6 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 8 ║ ~  ~  ~  ~  ~  ~  B  B  ~  ~ ║
 9 ║ B  ~  ~  ~  ~  ~  ~  B  ~  ~ ║
10 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
   ╚══════════════════════════════╝
     A  B  C  D  E  F  G  H  I  J

Esperando ataque...
```
6. Se solicita al jugador activo que introduzca una coordenada para atacar.
```
Turno de Jugador 1

          Tablero de ataque:
   ╔══════════════════════════════╗
 1 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 2 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 3 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 4 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 5 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 6 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 7 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 8 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
 9 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
10 ║ ~  ~  ~  ~  ~  ~  ~  ~  ~  ~ ║
   ╚══════════════════════════════╝
     A  B  C  D  E  F  G  H  I  J

Introduce coordenadas para atacar (fila, columna) >>
```
7. En el JSON del jugador pasivo: Se comprueba el ataque realizado y se registra el movimiento en el estado de los barcos y el tablero. 
8. En el JSON del jugador activo: Se registra el movimiento y su resultado. 
9. En consola, el "tablero de estado" del jugador pasivo se actualiza con el resultado del ataque. 
10. En consola, el "tablero de ataque" del jugador activo se muestra actualizado. 
11. Se actualiza el archivo global con el nuevo turno: Si es exitoso, se cambia el turno al siguiente jugador.
12. Volvemos al paso 4. 
13. Se declara al ganador y se finaliza el juego, mostrando su tablero, el jugador que ha ganado y los turnos que ha tenido la partida.