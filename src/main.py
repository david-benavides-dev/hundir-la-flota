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


# TODO Permitir barcos tanto en horizontal como vertical.
# BUG No debería dejar colocar un barco si es mas grande que coordenadas (EJ barco de 5 en 9,9)
def colocar_barco(tablero: list, barco: dict, coordenadas: list[tuple], nombre_barco: str) -> tuple[dict, list]:
    """
    Coloca un barco en el tablero si las coordenadas son válidas.
    
    Args:
        tablero (list): Tablero del jugador.
        barco (dict): Diccionario que representa el barco.
        coordenadas (list[tuple]): Lista de coordenadas donde colocar el barco.
    
    Returns:
        dict, list: Diccionario con las coordenadas y lista con el estado del barco, o un diccionario y lista vacías si algún un error.
    """
    y, x = coordenadas
    estado_barco = {}
    coordenadas_barco = []

    try:
        for i in range(barco['tamano']):
            if tablero[y-1][x+i-1] != "~":
                raise Exception("*ERROR* No puedes colocar un barco ahí.")
            tablero[y-1][x+i-1] = "B"
            estado_barco[f"[{y-1}, {x+i-1}]"] = "B"
            coordenadas_barco.append([y-1, x+i-1])

        return estado_barco, coordenadas_barco
    except IndexError:
        print("*ERROR* No puedes colocar el barco ahí")
        return {}, []
    except Exception as e:
        print(e)
        return {}, []


def pedir_coordenadas(msj: str, dimensiones: int) -> tuple:
    """

    """
    validar_coordenadas = False
    while not validar_coordenadas:
        try:
            y, x = input(msj).split(",")
            if validar_num(y) and validar_num(x):
                # Limpia directamente los espacios en el caso de que un usuario los introduzca en el input al pasarlos a int.
                return [int(y), int(x)]
        except ValueError:
            print("*ERROR* Coordenadas no válidas. El input debe ser 'N,N' (con comilla).")
            validar_coordenadas = False


def validar_num(num:str) -> bool:
    try:
        int(num)
        return True
    except ValueError:
        print("*ERROR* Debes introducir números")
        return False


def crear_configuracion_jugador(barcos: dict, nombre_jugador: str):
    """
    
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
    

def mostrar_tablero(tablero):
    """
    
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
    match opcion:
        case 1:
            nombre_j1 = input(color("Nombre J1 >> "))
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
            crear_configuracion_inicial(carpetas_ficheros, config_default, nombre_partida, config_barcos, nombre_j1)
            print("Comenzando partida")
            # time.sleep(2)
            # limpiar_terminal()
            # print("Limpiando los barquitos")
            # time.sleep(2)
            # print("Preparando las gambitas...")
            # time.sleep(1)
            # print("Echándole pienso a la criatura...")
            # time.sleep(2)
            limpiar_terminal()
        case 2:
            nombre_partida = input(color("Introduce el nombre de la partida >> "))
        case 3:
            exit


if __name__ == "__main__":
    main()