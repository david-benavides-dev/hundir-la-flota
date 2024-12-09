"""
Posible flujo:

CREAR PARTIDA
    Pide nombre de la partida
    Pide nombre del jugador
        Genera carpeta inicial
        Genera subcarpeta con el nombre de la partida
            Pide a J1 que ponga los barcos en su tablero
        Genera el archivo de J1
    Queda esperando a que exista el archivo J2

UNIRSE A PARTIDA
    Pide nombre de la partida
        Valida hasta que la carpeta exista
        Valida que exista archivo J1
    Pide nombre del jugador
        Pide al J2 que ponga los barcos en su tablero
        Genera el archivo de J2
    Valida que exista J1 y J2

JUEGO
    Carga json
    Lee dict
    jugador1 hace x
    jugador2 espera
    Guarda el dict
    Guarda dict en json

    Carga json
    Lee dict
    jugador2 hace x
    jugador 1 espera
    Guarda el dict
    Guarda dict en json
"""

# 1. Se crea una carpeta en x directorio llamada partidas_hundirflota. EJ:
#     C:\Usuarios\User\AppData\Local\partidas_hundirflota
#         - Dentro de la misma se crearán subcarpetas con los nombres de las partidas en cuestion y los archivos de configuración default. EJ:
#             C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\config.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\j1.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\j2.json
# 2. Al inicializar el programa, se muestra un menu para seleccionar si quieres crear una partida o continuar una ya empezada (para el caso del 2º player por ej).
# TODO 3. Si se selecciona Iniciar nueva partida, se pedira nombre de la partida y se verificará que la partida no existe, en el caso de ya existir, se pedirá si quiere empezar de 0 o continuarla.
#   - Caso de no existir, se creará una carpeta con el nombre de la partida mas toda la configuración inicial, tanto base como J1 y J2.