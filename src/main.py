import os
import time
import json

opciones = "1","2","3"
carpetas_ficheros = 'src/partidas_hundirflota'

config_default = {
    "nombre_partida": "MiPartida",
    "dimensiones_tablero": 10,
    "tiempo_refresco": 2,
    "tiempo_ataque": 30,
    "configuracion_barcos": {
        "Portafritura": {"tamano": 5, "numero": 1},
        "Gamba de Oro": {"tamano": 2, "numero": 2},
        "Barquita de la Caseria": {"tamano": 1, "numero": 3}
    },
    "turnos_jugados": 0,
    "turno_actual": "j1"
}


# 1. Se crea una carpeta en x directorio llamada partidas_hundirflota. EJ:
#     C:\Usuarios\User\AppData\Local\partidas_hundirflota
#         - Dentro de la misma se crearán subcarpetas con los nombres de las partidas en cuestion y los archivos de configuración default. EJ:
#             C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\config.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\j1.json
#                 C:\Usuarios\User\AppData\Local\partidas_hundirflota\partida1\j2.json
# 2. Al inicializar el programa, se muestra un menu para seleccionar si quieres crear una partida o continuar una ya empezada (para el caso del 2º player por ej).
# 3. Si se selecciona Iniciar nueva partida, se pedira nombre de la partida y se verificará que la partida no existe, en el caso de ya existir, se pedirá si quiere empezar de 0 o continuarla.
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


# Funciones para colores
def azul(texto: str, intensidad: int = 39):
    "Recibe un texto y un número y retorna el texto con un color ANSI apropiado dependiendo del parámetro dado en rango de azules."
    return f"\033[38;5;{intensidad}m{texto}\033[0m"


def mostrar_menu() -> str:
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
        {azul("=========================================")}
                    {titulo}             
        {azul("=========================================")}
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Continuar una partida guardada
           3. 🚪 Salir
        {azul("=========================================")}
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


def crear_carpeta_inicial(carpeta_root: str) -> None:
    """
    Crea la carpeta inicial donde se guardarán las partidas del juego.
    """
    if not os.path.exists(carpeta_root):
        os.mkdir(carpeta_root)
        print(f"Carpeta inicial creada con éxito.")

    return None


def crear_configuracion_inicial(carpeta_root: str, datos_iniciales: dict, nombre_partida: str, nombrej1: str, nombrej2: str) -> None:
    """
    
    """
    nombres = nombrej1, nombrej2
    # Modifica la configuración por defecto con el nombre que queramos darle a la partida
    config_default['nombre_partida'] = nombre_partida

    # Crea la carpeta con el nombre de la partida dentro del root partidas_hundirflota.
    if not os.path.exists(f"{carpeta_root}/{nombre_partida}"):
        os.mkdir(f"{carpeta_root}/{nombre_partida}")

    # Genera el archivo de configuracion inicial json con el nombre de la partida dentro de la carpeta con su mismo nombre en root.
    with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json", "w") as archivo:
        json.dump(datos_iniciales, archivo, indent = 4)
        print("Archivo de configuración creado con éxito")

    tablero = crear_tablero(5)
    # Genera el archivo de configuracion de cada jugador
    for i in range(1, 2+1):
        with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{nombres[i-1]}.j{i}.json", "w") as archivo:
            json.dump(datos_iniciales, archivo, indent = 4)
            print(f"Archivo de jugador{i} creado con éxito.")
    

def mostrar_tablero(tablero):
    """
    
    """
    indice_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = 0

    parte_arriba = "\n"
    for fila in tablero:
        parte_arriba += f"  {indice_letras[i]} "
        i += 1

    parte_arriba += "\n"

    separador_lineas = "-" * (len(tablero[0]) * 4) + "-"

    i = 1

    tablero_completo = ""

    for fila in tablero:
        tablero_completo += f"\n| {' | '.join(map(str, fila))} | {i}" + f"\n{separador_lineas}"
        i += 1
    
    tablero_completo = parte_arriba + separador_lineas + tablero_completo
    return tablero_completo


def crear_tablero(dimension: int) -> list:
    """
    
    """
    tablero = []

    for i in range(dimension):
        tablero.append([])
        for _ in range(dimension):
            tablero[i].append("~")

    return tablero


def main():
    crear_carpeta_inicial(carpetas_ficheros)

    limpiar_terminal()

    print(mostrar_menu())

    opcion = pedir_opcion()

    if opcion == 1:
        limpiar_terminal()
        nombre_j1 = input("Nombre J1 >> ")
        nombre_j2 = input("Nombre J2 >> ")
        nombre_partida = input("Introduce el nombre de la partida >> ")
        crear_configuracion_inicial(carpetas_ficheros, config_default, nombre_partida, nombre_j1, nombre_j2)
        time.sleep(2)
        limpiar_terminal()
        tablero1 = crear_tablero(10)
        print(mostrar_tablero(tablero1, nombre_j1))
        input(f"\nJUGADOR: {nombre_j1}\nColoca tu Barquita de la Caseria >> ")
        


if __name__ == "__main__":
    main()