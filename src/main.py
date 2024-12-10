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


def color(texto: str, color: int = 39):
    """
    Aplica un color ANSI al texto proporcionado, basado en el número de color especificado por parámetro.

    Args:
        texto (str): El texto al que se le aplicará el color.
        color (int): Un número entero que representa el color ANSI. Por defecto es 39 (azul).

    Returns:
        str: El texto con el color aplicado en formato ANSI.
    """
    return f"\033[38;5;{color}m{texto}\033[0m"


def mostrar_menu() -> str:
    """
    Genera y devuelve el menú principal con colores y las opciones del juego.

    Returns:
        str: El menú principal como un string con formato ANSI.
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

    return f"""
        {color("=========================================")}
                    {titulo}             
        {color("=========================================")}
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Unirse a una partida
           3. 🚪 Salir
        {color("=========================================")}
        """


def pedir_opcion() -> int:
    """
    Solicita al usuario una opción válida entre las disponibles (1, 2, 3).

    Returns:
        int: La opción seleccionada.
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
    Crea la carpeta raíz para guardar partidas si no existe.
    
    Args:
        carpeta_root (str): Ruta de la carpeta a crear.
    """
    if not os.path.exists(carpeta_root):
        os.mkdir(carpeta_root)
        print(f"Carpeta inicial creada con éxito.")

    return None


# TODO Permitir barcos tanto en horizontal como vertical.
# BUG No debería dejar colocar un barco si es mas grande que coordenadas (EJ barco de 5 en 9,9)
def colocar_barco(tablero: list, barco: dict, coordenadas: list[tuple], nombre_barco: str) -> tuple[dict, list]:
    """
    Coloca un barco en el tablero si las coordenadas son válidas.
    
    Args:
        tablero (list[list]): Tablero del jugador.
        barco (dict): Diccionario que representa el barco.
        coordenadas (list[tuple]): Lista de coordenadas donde colocar el barco.
        nombre_barco (str): Nombre del barco que se está colocando.
    
    Returns:
        dict, list: Diccionario con las coordenadas y lista con el estado del barco, o un diccionario y lista vacías si hay algún un error.
    """
    y, x = coordenadas
    estado_barco = {}
    coordenadas_barco = []

    try:
        for i in range(barco['tamano']):
            if tablero[y][x+i] != "~":
                raise Exception("*ERROR* No puedes colocar un barco ahí.")
            tablero[y][x+i] = "B"
            estado_barco[f"[{y}, {x+i}]"] = "B"
            coordenadas_barco.append([y, x+i])

        return estado_barco, coordenadas_barco
    except IndexError:
        print("*ERROR* No puedes colocar el barco ahí")
        return {}, []
    except Exception as e:
        print(e)
        return {}, []


def pedir_coordenadas(msj: str, dimensiones: int) -> list:
    """
    Solicita coordenadas válidas para el tablero.

    Args:
        msj (str): Mensaje a mostrar al usuario.
        dimensiones (int): Tamaño máximo permitido para las coordenadas.

    Returns:
        list: Coordenadas [y, x] válidas para el tablero.
    """
    validar_coordenadas = False
    while not validar_coordenadas:
        try:
            y, x = input(msj).split(",")
            if validar_num(y) and validar_num(x):
                y = int(y) - 1
                x = int(x) - 1
                if not (0 <= y < dimensiones and 0 <= x < dimensiones):
                    raise Exception("*ERROR* Números no válidos.")
                # Limpia directamente los espacios en el caso de que un usuario los introduzca en el input al pasarlos a int.
                return [y, x]
        except ValueError:
            print("*ERROR* Coordenadas no válidas. El input debe ser 'N,N' (con comilla).")
            validar_coordenadas = False
        except Exception as e:
            print(e)
            validar_coordenadas = False


def validar_num(num:str) -> bool:
    """
    Valida si una cadena de texto puede ser convertida a un número entero.

    Args:
        num (str): El string que se quiere validar como número.

    Returns:
        bool: True si es válido, False si no lo es.
    """
    try:
        int(num)
        return True
    except ValueError:
        print("*ERROR* Debes introducir números")
        return False


def crear_configuracion_jugador(barcos: dict, nombre_jugador: str) -> dict:
    """
    Crea la configuración inicial de un jugador.

    Args:
        barcos (list): Lista de barcos para el jugador.
        nombre_jugador (str): Nombre del jugador.

    Returns:
        dict: Configuración del jugador con el tablero y la flota con el estado de cada uno de los barcos.
    """
    tablero = crear_tablero(config_default["dimensiones_tablero"])

    flota = {}

    limpiar_terminal()
    print(mostrar_tablero(tablero))

    for nombre, datos in barcos.items():
        i = 0
        while i < datos["numero"]:
            coordenadas = pedir_coordenadas(f"Introduce coordenadas para colocar '{nombre}' ({i+1}/{datos['numero']}) >> ", 10)
            estado_barco, coordenadas_barco = colocar_barco(tablero, datos, coordenadas, f"{nombre}{i+1}")
            if estado_barco:
                flota[f"{nombre}{i+1}"] = {
                    "coordenadas": coordenadas_barco,
                    "estado": estado_barco
                }
                limpiar_terminal()
                print(mostrar_tablero(tablero))
                i += 1

    config_jugador = {"nombre": nombre_jugador,
                          "tablero": tablero,
                          "barcos": flota,
                          "movimientos": [{}],
                          }

    return config_jugador


def crear_configuracion_inicial(carpeta_root: str, datos_iniciales: dict, nombre_partida: str, config_barcos: dict, nombre_jugador:str) -> None:
    """
    Crea la configuración inicial de la partida y guarda los archivos correspondientes en un JSON.

    Args:
        carpeta_root (str): Carpeta raíz donde se almacenarán las partidas.
        datos_iniciales (dict): Configuración default.
        nombre_partida (str): Nombre de la partida.
        config_barcos (dict): Configuración de los barcos.
        nombre_jugador (str): Nombre del jugador.
    """
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

    config_jugador = crear_configuracion_jugador(config_barcos, nombre_jugador)

    with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{nombre_jugador}.j{1}.json", "w") as archivo:
        json.dump(config_jugador, archivo, indent = 4)
        print(f"Archivo de jugador {1} creado con éxito.")
    
    return None
    

def mostrar_tablero(tablero: list) -> str:
    """
    Genera y devuelve una representación visual del tablero en formato string.

    Args:
        tablero (list): Matriz que representa el tablero.

    Returns:
        str: Tablero formateado como una cadena de texto.
    """
    # indice_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = 1

    parte_arriba = "\n "
    for fila in tablero:
        parte_arriba += f" {i} "
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


def crear_tablero(dimension: int) -> list[list]:
    """
    Crea un tablero vacío de tamaño dimension x dimension.

    Args:
        dimension (int): Tamaño que tendrá el tablero.

    Returns:
        list[list]: Matriz con celdas inicializadas como "~" (olas).
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
    match opcion:
        case 1:
            nombre_j1 = input(color("Nombre J1 >> "))
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
            crear_configuracion_inicial(carpetas_ficheros, config_default, nombre_partida, config_barcos, nombre_j1)
            print("Comenzando partida")
            time.sleep(2)
        case 2:
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
        case 3:
            exit()


if __name__ == "__main__":
    main()