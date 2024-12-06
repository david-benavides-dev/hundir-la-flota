# TODO
# Logica del juego sin usar json para luego aplicarlo al mismo.



"""


"""
# Funcion para colores
def color(texto: str, intensidad: int = 39):
    "Recibe un texto y un número y retorna el texto con un color ANSI apropiado dependiendo del parámetro dado."
    return f"\033[38;5;{intensidad}m{texto}\033[0m"

def crear_tablero(dimension = 10):
    tablero = []
    for i in range(dimension):
        tablero.append([])
        for _ in range(dimension):
            tablero[i].append("~")
    return tablero

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

config_barcos = {
        "Portafritura": {
            "tamano": 5, "numero": 1},
        "Gamba de Oro": {
            "tamano": 2, "numero": 2},
        "Barquita de la Caseria": {
            "tamano": 1, "numero": 3}
    }
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


def pedir_coordenadas(barco: dict, msj: str) -> tuple:
    """
    """
    validar_coordenadas = False
    while not validar_coordenadas:
        try:
            x, y = input(msj).split(",")
            if validar_num(x) and validar_num(y):
                # Limpia directamente los espacios en el caso de que un usuario los introduzca en el input al pasarlos a int.
                coordenadas = (int(x), int(y))
                validar_coordenadas = True
                return coordenadas
        except ValueError:
            print("*ERROR*")
            validar_coordenadas = False


def validar_num(num:str) -> bool:
    try:
        int(num)
        return True
    except ValueError:
        print("*ERROR* Debes introducir números")
        False


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
    y,x = coordenadas

    try:
        for i in range(barco['tamano']):
            tablero[y-1][x+i-1] = "A"
        return True
    except IndexError:
        print("*ERROR* No puedes colocar el barco ahí")
        return False


Barquita_de_la_Caseria = {
            "tamano": 1, "numero": 3}

tablero = crear_tablero()
coordenadas = pedir_coordenadas(Barquita_de_la_Caseria, "Introduce las coordenadas: ")
colocar_barco(tablero, Barquita_de_la_Caseria, coordenadas)
print(mostrar_tablero(tablero))


"""
Posible flujo:

CREAR PARTIDA
    Pide nombre de la partida
    Pide nombre del jugador
        Genera carpeta inicial
        Genera subcarpeta con el nombre de la partida
            Pide a J1 que ponga los barcos en su tablero
    Queda esperando a que exista el archivo J2

UNIRSE A PARTIDA
    Pide nombre de la partida
        Valida hasta que la carpeta exista
        Valida que exista archivo J1
    Pide nombre del jugador
        Pide al J2 que ponga los barcos en su tablero
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