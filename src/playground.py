import os
import time
import json


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


if __name__ == "__main__":
    main()