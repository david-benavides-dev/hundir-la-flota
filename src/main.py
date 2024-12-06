import os
import time
import json

opciones = "1","2","3"
# TODO cambiar a carpeta para MP maybe permitir al usuario selccionar carpeta (doubt)
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

config_barcos = {
        "Portafritura": {
            "tamano": 5, "numero": 1},
        "Gamba de Oro": {
            "tamano": 2, "numero": 2},
        "Barquita de la Caseria": {
            "tamano": 1, "numero": 3}
    }


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


# Funcion para colores
def color(texto: str, intensidad: int = 39):
    "Recibe un texto y un número y retorna el texto con un color ANSI apropiado dependiendo del parámetro dado."
    return f"\033[38;5;{intensidad}m{texto}\033[0m"


def mostrar_menu() -> str:
    """
    Muestra el menu inicial.
    """
    titulo = (
        color("P", 27) +
        color("I", 33) +
        color("R", 39) +
        color("A", 45) +
        color("T", 51) +
        color("A", 45) +
        color("S", 39) +
        color(" ", 33) +
        color("C", 27) +
        color("A", 33) +
        color("L", 39) +
        color("E", 45) +
        color("T", 51) +
        color("E", 45) +
        color("R", 39) +
        color("O", 33) +
        color("S", 27)
    )

    # TODO Quizá opcion 4 para ver configuracion inicial, creditos u otros.
    return f"""
        {color("=========================================")}
                    {titulo}             
        {color("=========================================")}
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Continuar una partida guardada
           3. 🚪 Salir
        {color("=========================================")}
        """


def pedir_opcion() -> int:
    """
    Pedir opcion porrillero edition por ahora, just testing.
    """
    opcion = None
    while not opcion:
        opcion = input(color("Yaaarrr? >> "))
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


# Genera la flota de barcos.
def generar_flota(config_barcos: dict) -> dict:
    """
    
    """
    barcos = {}

    for nombre, datos in config_barcos.items():
        for i in range(1, datos["numero"] + 1):
            barco_nombre = f"{nombre}{i}"

            estado = {}
            for j in range(datos["tamano"]):
                estado[f"[{j+1}]"] = " "

            coordenadas = []
            for _ in range(datos["tamano"]):
                coordenadas.append([])

            barcos[barco_nombre] = {
                "coordenadas": coordenadas,
                "estado": estado
            }

    return barcos


def crear_configuracion_inicial(carpeta_root: str, datos_iniciales: dict, nombre_partida: str, nombrej1: str, nombrej2: str) -> None:
    """
    
    """
    if nombrej1 and nombrej2 != "":
        nombres = nombrej1, nombrej2
    else:
        nombres = "Jugador1", "Jugador2"

    # Modifica la configuración por defecto con el nombre que queramos darle a la partida
    if nombre_partida != "":
        config_default['nombre_partida'] = nombre_partida
    else:
        nombre_partida = config_default['nombre_partida']

    # Crea la carpeta con el nombre de la partida dentro del root partidas_hundirflota.
    if not os.path.exists(f"{carpeta_root}/{nombre_partida}"):
        os.mkdir(f"{carpeta_root}/{nombre_partida}")

    # Genera el archivo de configuracion inicial json con el nombre de la partida dentro de la carpeta con su mismo nombre en root.
    with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json", "w") as archivo:
        json.dump(datos_iniciales, archivo, indent = 4)
        print("Archivo de configuración creado con éxito")

    tablero = crear_tablero(config_default['dimensiones_tablero'])
    flota = generar_flota(config_barcos)

    # Genera el archivo de configuracion de cada jugador
    for i in range(1, 2+1):
        config_jugador = {"nombre": nombres[i-1],
                          "tablero": tablero,
                          "movimientos": [{}],
                          "barcos": flota
                          }

        with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{nombres[i-1]}.j{i}.json", "w") as archivo:
            json.dump(config_jugador, archivo, indent = 2)
            print(f"Archivo de jugador{i} creado con éxito.")
    

def mostrar_tablero(tablero):
    """
    
    """
    indice_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = 0

    parte_arriba = "\n "
    for fila in tablero:
        parte_arriba += f" {indice_letras[i]} "
        i += 1

    parte_arriba += "\n"

    separador_top = "╔" + ("═" * (len(tablero[0]) * 3)) + "╗"
    separador_bot = "╚" + ("═" * (len(tablero[0]) * 3)) + "╝"

    i = 1

    tablero_completo = ""

    for fila in tablero:
        tablero_completo += f"\n{color('║')} {'  '.join(map(str, fila))} {color('║')} {i}" + f""
        i += 1
    
    tablero_completo = parte_arriba + color(separador_top) + tablero_completo + "\n" + color(separador_bot)
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


def colocar_barco(tablero: list, barco: dict, coordenadas: list[tuple]) -> bool:
    """
    Coloca un barco en el tablero si las coordenadas son válidas.
    
    Args:
        tablero (list): Tablero del jugador.
        barco (dict): Diccionario que representa el barco.
        coordenadas (list[tuple]): Lista de coordenadas donde colocar el barco.
    
    Returns:
        bool: True si el barco se colocó correctamente, False si hubo un error.
    """


def leer_archivo_jugador(carpeta: str, nombre_partida: str, jugador: str) -> dict:
    """
    Lee el archivo JSON de un jugador específico.
    
    Args:
        carpeta (str): Ruta a la carpeta donde se encuentra el archivo de la partida.
        nombre_partida (str): Nombre de la partida.
        jugador (str): Identificador del jugador ("j1" o "j2").
    
    Returns:
        dict: Contenido del archivo del jugador en forma de diccionario.
    """


def guardar_archivo_global(carpeta: str, nombre_partida: str, datos: dict) -> None:
    """
    Guarda los cambios en el archivo global de configuración de la partida.
    
    Args:
        carpeta (str): Ruta a la carpeta donde se encuentra el archivo de la partida.
        nombre_partida (str): Nombre de la partida.
        datos (dict): Contenido actualizado del archivo global.
    
    Returns:
        None
    """


def guardar_archivo_jugador(carpeta: str, nombre_partida: str, jugador: str, datos: dict) -> None:
    """
    Guarda los cambios en el archivo JSON de un jugador.
    
    Args:
        carpeta (str): Ruta a la carpeta donde se encuentra el archivo de la partida.
        nombre_partida (str): Nombre de la partida.
        jugador (str): Identificador del jugador ("j1" o "j2").
        datos (dict): Contenido actualizado del archivo del jugador.
    
    Returns:
        None
    """


def leer_archivo_global(carpeta: str, nombre_partida: str) -> dict:
    """
    Lee el archivo global de configuración de la partida.
    
    Args:
        carpeta (str): Ruta a la carpeta donde se encuentra el archivo de la partida.
        nombre_partida (str): Nombre de la partida.
    
    Returns:
        dict: Contenido del archivo global en forma de diccionario.
    """


def pedir_numero(msj):
    """
    
    """
    num = False
    while not num:
        num = input(msj)
        if validar_numero(num):
            return int(num)
        else:
            num = False


def validar_numero(num: str) -> bool:
    """
    
    """
    try:
        int(num)
        return True
    except ValueError:
        print("*ERROR* El número no es válido.")
        return False


def pedir_nombres():
    """
    
    """
    pass


def comenzar_partida():
    """
    
    """
    pass


def jugar():
    """
    
    """
    pass


def main():
    crear_carpeta_inicial(carpetas_ficheros)

    limpiar_terminal()

    print(mostrar_menu())

    opcion = pedir_opcion()
    match opcion:
        case 1:
            nombre_j1 = input(color("Nombre J1 >> "))
            nombre_j2 = input(color("Nombre J2 >> "))
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
            crear_configuracion_inicial(carpetas_ficheros, config_default, nombre_partida, nombre_j1, nombre_j2)
            print("Comenzando partida")
            time.sleep(2)
            limpiar_terminal()
            print("Limpiando los barquitos")
            time.sleep(2)
            print("Preparando las gambitas...")
            time.sleep(1)
            print("Echándole pienso a la criatura...")
            time.sleep(2)
            limpiar_terminal()
            tablero1 = crear_tablero(10)
            print(mostrar_tablero(tablero1))
            input(f"\nJUGADOR: {nombre_j1}\nColoca tu Barquita de la Caseria >> ")
        case 2:
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
        case 3:
            exit


if __name__ == "__main__":
    main()