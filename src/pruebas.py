Gamba_de_Oro = {"tamano": 2, "numero": 2}



def pedir_orientacion_direccion() -> tuple:
    """
    
    """
    validar_orientacion_direccion = False

    while not validar_orientacion_direccion:
        try:
            orientacion, direccion = input("Introduce orientación y direccion con formato 'H' o 'V,'+' o '-' >> ").upper().split(",")

            if orientacion == "H" or orientacion == "V" and direccion == "+" or direccion == "-":
                validar_orientacion_direccion = True
                return (orientacion, direccion)
            else:
                raise ValueError

        except ValueError:
            print(f"*ERROR* Debes introducir H o V seguido de + o - (separados por coma).")


def colocar_barco(tablero: list, barco: dict, coordenadas: list[tuple], orientacion_direccion: tuple, nombre_barco: str) -> tuple[dict, list]:
    """
    Coloca un barco en el tablero si las coordenadas son válidas.
    
    Args:
        tablero (list[list]): Tablero del jugador.
        barco (dict): Diccionario que representa el barco.
        coordenadas (list[tuple]): Lista de coordenadas donde colocar el barco.
        nombre_barco (str): Nombre del barco que se está colocando.
    
    Returns:
        dict, list | False: Diccionario con las coordenadas y una lista con el estado del barco, o False si hay algún un error.
    """
    orientacion, direccion = orientacion_direccion
    y, x = coordenadas
    estado_barco = {}
    coordenadas_barco = []

    try:
        # Orientación horizontal hacia la derecha <- DONE
        if orientacion == "H" and direccion == "+":
            for i in range(barco['tamano']):
                if tablero[y][x+i] != "~":
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y][x+i] = "B"
                estado_barco[f"[{y}, {x+i}]"] = "B"
                coordenadas_barco.append([y, x+i])
            print(f"Barco {nombre_barco} colocado con éxito.")
        # TODO Orientación Vertical hacia la abajo <- DONE
        elif orientacion == "V" and direccion == "-":
            for i in range(barco['tamano']):
                if tablero[y+1][x] != "~":
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y+1][x] = "B"
                estado_barco[f"[{y+1}, {x}]"] = "B"
                coordenadas_barco.append([y+1, x])
            print(f"Barco {nombre_barco} colocado con éxito.")
        # TODO Orientación Horizontal hacia la izquierda <- DONE
        elif orientacion == "H" and direccion == "-":
            for i in range(barco['tamano']):
                if tablero[y][x-i] != "~":
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y][x-i] = "B"
                estado_barco[f"[{y}, {x-i}]"] = "B"
                coordenadas_barco.append([y, x-i])
            print(f"Barco {nombre_barco} colocado con éxito.")
        # TODO Orientación Vertical hacia arriba
        else:
            for i in range(barco['tamano']):
                if tablero[y-i][x] != "~":
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y-1][x] = "B"
                estado_barco[f"[{y-1}, {x}]"] = "B"
                coordenadas_barco.append([y-1, x])
            print(f"Barco {nombre_barco} colocado con éxito.")
        return estado_barco, coordenadas_barco
    except IndexError:
        print("*ERROR* No puedes colocar el barco ahí")


        return False, False
    except Exception as e:
        print(e)

        return False, False
    
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
            print("*ERROR* Coordenadas no válidas. El input debe ser 'N,N' (separado con coma).")
            validar_coordenadas = False
        except Exception as e:
            print(e)
            validar_coordenadas = False


def validar_num(num: str) -> bool:
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
    

def crear_tablero(dimension) -> list[list]:
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

def mostrar_tablero(tablero: list, modo: str = "mostrar") -> str:
    """
    Genera y devuelve una representación visual del tablero en formato string por consola. Si el modo es "ataque", oculta los barcos intactos. Por defecto ("mostrar") muestra todo el tablero.

    Args:
        tablero (list): Matriz que representa el tablero.
        modo (str): Modo de visualización ("ataque", "estado" o "mostrar").

    Returns:
        str: Tablero formateado como una cadena de texto.
    """
    # TODO cambiar coordenadas a letras + números maybe.
    indice_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


    # Condición para ocultar la posición de los barcos a la hora de mostrar el tablero en estado "ataque".
    # Itera sobre el tablero original, haciendo una réplica del mismo a otro tablero vacío y ocultando las 'B' por '~'.
    if modo == "ataque":
        tablero_ataque = []
        for fila in tablero:
            fila_ataque = []
            for celda in fila:
                if celda == "B":
                    fila_ataque.append("~")
                else:
                    fila_ataque.append(celda)
            tablero_ataque.append(fila_ataque)
        titulo = f"{' ' * len(tablero[0])}Tablero de ataque:\n"
    elif modo == "estado":
        titulo = f"{' ' * len(tablero[0])}Tablero de estado:\n"
    else:
        titulo = ""

    i = 0
    coordenadas_inferior = "\n    "
    for fila in tablero:
        coordenadas_inferior += f" {indice_letras[i]} "
        i += 1

    coordenadas_inferior += " " + "\n"

    marco_superior = "   ╔" + ("═" * (len(tablero[0]) * 3)) + "╗"
    marco_inferior = "   ╚" + ("═" * (len(tablero[0]) * 3)) + "╝"

    i = 1

    tablero_completo = ""

    for fila in tablero_ataque if modo == "ataque" else tablero:
        if i < 10:
            tablero_completo += f"\n {i} ║ {'  '.join(map(str, fila))} ║" + f""
        else:
            tablero_completo += f"\n{i} ║ {'  '.join(map(str, fila))} ║" + f""
        i += 1
    
    tablero_completo = titulo + marco_superior + tablero_completo + "\n" + marco_inferior + coordenadas_inferior

    return tablero_completo

    
# a, b = pedir_orientacion_direccion()
tablero = crear_tablero(10)
while True:
    coordenadas = pedir_coordenadas("Introduce coordenadas: ", 10)
    orientacion = pedir_orientacion_direccion("introduce orientacion: ")
    print(mostrar_tablero(tablero))
    input()
    colocar_barco(tablero, Gamba_de_Oro, coordenadas, "Gamba de Oro")
    print(tablero)
    input()