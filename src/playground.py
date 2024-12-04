import os
import time
import json

opciones = {"1","2","3"}

# 1. Se crea una carpeta en x directorio llamada partidas_hundirflota. EJ:
#     C:\Usuarios\User\AppData\Local\partidas_hundirflota
#         - Dentro de la misma se crearán subcarpetas con los nombres de las partidas en cuestion y los archivos de configuración default. EJ:
#             C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\config.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\j1.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1.j2.json

# 2. Al inicializar el programa, se muestra un menu para seleccionar si quieres crear una partida o continuar una ya empezada (para el caso del 2º player por ej).
# 3. Si se selecciona cear partida, se pedira nombre de la partida y se verificará que la partida no existe, en el caso de ya existir, se pedirá si quiere empezar de 0 o continuarla.
#   - Caso de no existir, se creará una carpeta con el nombre de la partida mas toda la configuración inicial, tanto base como J1 y J2.


def pausa() -> None:
    """
    Pausa el programa hasta que el usuario presione una tecla.
    """
    input("Presiona ENTER para continuar...")

    return None


def limpiar_terminal() -> None:
    """
    Limpia la terminal.
    """
    comando = ""
    if os.name == 'nt':
        comando = 'cls'
    else:
        comando = 'posix'
    os.system(comando)

    return None


def azul(texto: str, intensidad: int):
    "Recibe un texto y un número y retorna el texto con un color ANSI apropiado dependiendo del parámetro dado."
    return f"\033[38;5;{intensidad}m{texto}\033[0m"


def mostrar_menu():
    """
    Muestra el menu inicial.
    """
    titulo = (
        azul("P", 27) +
        azul("I", 33) +
        azul("R", 39) +
        azul("A", 45) +
        azul("T", 51) +
        azul("A", 45) +
        azul("S", 39) +
        azul(" ", 33) +
        azul("C", 27) +
        azul("A", 33) +
        azul("L", 39) +
        azul("E", 45) +
        azul("T", 51) +
        azul("E", 45) +
        azul("R", 39) +
        azul("O", 33) +
        azul("S", 27)
    )

    # TODO Quizá opcion 4 para ver configuracion inicial, creditos u otros.
    return f"""
        {azul("=========================================", 39)}
                    {titulo}             
        {azul("=========================================", 39)}
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Continuar una partida guardada
           3. 🚪 Salir
        {azul("=========================================", 39)}
"""


def pedir_opcion() -> int:
    """
    Pedir opcion porrillero edition por ahora, just testing.
    """
    opcion = None
    while not opcion:
        opcion = input("Yaaarrr? >> ")
        if opcion not in opciones:
            print("Opción no válida")
            opcion = None
    return int(opcion)


def crear_carpeta_configuracion_inicial():
    """
    Crea la carpeta inicial donde se guardarán las partidas del juego.
    """

    # Carpeta root (#TODO cambiar para carpeta compartida)
    carpeta_root = 'src/partidas_hundirflota'


    if not os.path.exists(carpeta_root):
        os.mkdir(carpeta_root)
        print(f"Carpeta inicial creada con éxito.")


def main():
    crear_carpeta_configuracion_inicial()
    limpiar_terminal()
    print(mostrar_menu())
    pedir_opcion()


if __name__ == "__main__":
    main()