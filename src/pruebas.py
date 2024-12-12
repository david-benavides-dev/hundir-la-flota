
def pedir_orientacion_direccion() -> tuple:
    """
    
    """
    validar_orientacion_direccion = False

    while not validar_orientacion_direccion:
        try:
            orientacion, direccion = input("Introduce orientación y direccion (H y V),(+ o -) >> ").upper().split(",")

            if orientacion == "H" or orientacion == "V" and direccion == "+" or direccion == "-":
                validar_orientacion_direccion = True
                return (orientacion, direccion)
            else:
                raise ValueError

        except ValueError:
            print(f"ERROR")


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
        for i in range(barco['tamano']):
            if tablero[y][x+i] != "~":
                raise Exception("*ERROR* No puedes colocar un barco ahí.")
        for i in range(barco['tamano']):
            tablero[y][x+i] = "B"
            estado_barco[f"[{y}, {x+i}]"] = "B"
            coordenadas_barco.append([y, x+i])
        print(f"Barco {nombre_barco} colocado con éxito.")

        return estado_barco, coordenadas_barco
    except IndexError:
        print("*ERROR* No puedes colocar el barco ahí")


        return False, False
    except Exception as e:
        print(e)

        return False, False
    
a, b = pedir_orientacion_direccion()
print(a)
print(b)