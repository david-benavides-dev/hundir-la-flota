from juego import *
import os
import time
import json

# Constante con las opciones disponibles
opciones = "1","2","3"

# Directorio ROOT donde se guardarán las partídas.
DIRECTORIO_PARTIDAS = 'src/partidas_hundirflota'

config_default = {
    "nombre_partida": "",
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


def pausa() -> None:
    """
    Pausa el programa hasta que el usuario presione ENTER.
    """
    input("Presiona ENTER para continuar...")

    return None


def limpiar_terminal() -> None:
    """
    Limpia la terminal o consola independientemente del sistema operativo.
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


def mostrar_menu() -> None:
    """
    Genera y muestra el menú principal del juego con las opciones disponibles.

    Este menú se muestra con colores definidos en formateo de código ANSI.

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

    print(f"""
        {color("═════════════════════════════════════════")}
                    {titulo}             
        {color("═════════════════════════════════════════")}
           1. ⚓ Iniciar una nueva partida
           2. 🌊 Unirse a una partida
           3. 🚪 Salir
        {color("═════════════════════════════════════════")}
        """)
    
    return None


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


def crear_carpeta_partidas(carpeta_root: str) -> None:
    """
    Crea la carpeta raíz para guardar partidas si no existe.
    
    Args:
        carpeta_root (str): Ruta de la carpeta a crear.
    """
    if not os.path.exists(carpeta_root):
        os.mkdir(carpeta_root)
        print(f"Carpeta inicial creada con éxito.")

    return None


def colocar_barco(tablero: list, barco: dict, coordenadas: list[tuple], orientacion_direccion: tuple, nombre_barco: str) -> tuple[dict, list]:
    """
    Coloca un barco en el tablero en las coordenadas especificadas, verificando que las condiciones sean válidas.

    Args:
        tablero (list[list]): El tablero donde se colocarán los barcos.
        barco (dict): Un diccionario que contiene los datos del barco (como el tamaño).
        coordenadas (list[tuple]): Una lista de coordenadas iniciales donde se desea colocar el barco.
        orientacion_direccion (tuple): Una tupla que contiene la orientación ("H" para horizontal, "V" para vertical) y la dirección ("+" o "-").
        nombre_barco (str): El nombre del barco que se va a colocar.

    Returns:
        tuple[dict, list]: Un diccionario con las coordenadas ocupadas por el barco y un lista con las mismas coordenadas. Si ocurre un error, retorna False.
    
    Raises:
        Exception: Si las coordenadas proporcionadas no son válidas para colocar el barco (por ejemplo, si se sobreponen con otro barco o están fuera del rango).
        IndexError: Si las coordenadas están fuera del tamaño del tablero.
    
    Notes:
        El barco se representa en el tablero con la letra "B". Si el barco se coloca correctamente, el estado y las coordenadas se almacenan en un diccionario y una lista, respectivamente.
    """
    orientacion, direccion = orientacion_direccion
    y, x = coordenadas
    estado_barco = {}
    coordenadas_barco = []

    try:
        # Orientación horizontal hacia la derecha
        if orientacion == "H" and direccion == "+":
            for i in range(barco['tamano']):
                if tablero[y][x+i] != "~":
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y][x+i] = "B"
                estado_barco[f"[{y}, {x+i}]"] = "B"
                coordenadas_barco.append([y, x+i])
            print(f"Colocando {nombre_barco} ...")
        # Orientación Vertical hacia la abajo
        elif orientacion == "V" and direccion == "+":
            for i in range(barco['tamano']):
                if tablero[y+i][x] != "~" or (y+i) < 0:
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y+i][x] = "B"
                estado_barco[f"[{y+i}, {x}]"] = "B"
                coordenadas_barco.append([y+i, x])
            print(f"Colocando {nombre_barco} ...")
        # Orientación Horizontal hacia la izquierda
        elif orientacion == "H" and direccion == "-":
            for i in range(barco['tamano']):
                if tablero[y][x-i] != "~" or (x-i) < 0:
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y][x-i] = "B"
                estado_barco[f"[{y}, {x-i}]"] = "B"
                coordenadas_barco.append([y, x-i])
            print(f"Colocando {nombre_barco} ...")
        # Orientación Vertical hacia arriba
        else:
            for i in range(barco['tamano']):
                if tablero[y-i][x] != "~" or (y-i) < 0:
                    raise Exception("*ERROR* No puedes colocar un barco ahí.")
            for i in range(barco['tamano']):
                tablero[y-i][x] = "B"
                estado_barco[f"[{y-i}, {x}]"] = "B"
                coordenadas_barco.append([y-i, x])
            print(f"Colocando {nombre_barco} ...")
        return estado_barco, coordenadas_barco
    except IndexError:
        print("*ERROR* Barco fuera de rango.")
        time.sleep(2)
        limpiar_terminal()
        return False, False
    except Exception as e:
        print(e)
        time.sleep(2)
        limpiar_terminal()
        return False, False


def pedir_orientacion_direccion(msj: str) -> tuple:
    """
    Solicita al usuario la orientación y dirección para colocar un barco, asegurándose de que la entrada sea válida.

    Args:
        msj (str): El mensaje que se muestra al usuario solicitando la entrada (por ejemplo, "Introduce orientación y dirección").

    Returns:
        tuple: Una tupla con la orientación y la dirección introducidas por el usuario. La orientación puede ser "H" (horizontal) o "V" (vertical), y la dirección puede ser "+" o "-".
        
    Raises:
        ValueError: Si el usuario no introduce un valor válido para la orientación y dirección.
    
    Notes:
        El valor introducido debe seguir el formato "H,+", "V,-", etc. En caso de entrada inválida, el usuario será solicitado nuevamente hasta proporcionar una entrada correcta.
    """
    validar_orientacion_direccion = False

    while not validar_orientacion_direccion:
        try:
            orientacion, direccion = input(msj).strip().upper().split(",")

            if (orientacion == "H" or orientacion == "V") and (direccion == "+" or direccion == "-"):
                validar_orientacion_direccion = True
                return (orientacion, direccion)
            else:
                raise ValueError

        except ValueError:
            print(f"*ERROR* Debes introducir H o V seguido de + o - (separados por coma).")


def pedir_coordenadas(msj: str, dimensiones: int) -> list:
    """
    Solicita coordenadas válidas al usuario para colocar un barco en el tablero.

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
            if validar_num(y):
                y = int(y) - 1
                x = convertir_letra(x)
                x = int(x) - 1
                if not (0 <= y < dimensiones and 0 <= x < dimensiones):
                    raise Exception("*ERROR* Coordenadas fuera de rango.")
                # Limpia directamente los espacios en el caso de que un usuario los introduzca en el input al pasarlos a int.
                return [y, x]
        except ValueError:
            print("*ERROR* Coordenadas no válidas. El input debe ser 'Numero,Letra' (separado con coma).")
            validar_coordenadas = False
        except Exception as e:
            print(e)
            validar_coordenadas = False


def convertir_letra(letra: str) -> int:
    """
    Convierte una letra a número mediante su índice en el abecedario + 1.

    Args:
        letra (str): Letra a convertir, que debe estar entre 'A' y 'Z'.

    Returns:
        int: Número correspondiente al índice de la letra en el abecedario + 1.
    """
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letra = letra.upper()
    return alfabeto.index(letra) + 1


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


def crear_configuracion_jugador(barcos: dict, nombre_jugador: str) -> dict:
    """
    Crea la configuración inicial de un jugador, incluyendo su tablero y flota de barcos.

    Args:
        barcos (dict): Diccionario de barcos donde la clave es el nombre del barco y los valores incluyen el tamaño y número de barcos.
        nombre_jugador (str): Nombre del jugador.

    Returns:
        dict: Diccionario con la configuración del jugador, que incluye su nombre, el tablero y la flota de barcos con sus coordenadas y estado.
    """
    tablero = crear_tablero(config_default["dimensiones_tablero"])

    flota = {}

    limpiar_terminal()

    for nombre, datos in barcos.items():
        i = 0
        while i < datos["numero"]:
            mostrar_tablero(tablero)
            coordenadas = pedir_coordenadas(f"⚓ Introduce coordenadas para colocar '{nombre}' (T{datos['tamano']}) [{i+1}/{datos['numero']}] >> ", config_default['dimensiones_tablero'])
            orientacion_direccion = pedir_orientacion_direccion("⚓ Introduce orientación y direccion '[H o V],[+ o -]' >> ")
            estado_barco, coordenadas_barco = colocar_barco(tablero, datos, coordenadas, orientacion_direccion, f"{nombre} #{i+1}")
            if estado_barco and coordenadas_barco:
                flota[f"{nombre}{i+1}"] = {
                    "coordenadas": coordenadas_barco,
                    "estado": estado_barco
                }
                time.sleep(2)
                limpiar_terminal()
                i += 1

    config_jugador = {"nombre": nombre_jugador,
                          "tablero": tablero,
                          "barcos": flota,
                          "movimientos": [],
                          }

    mostrar_tablero(tablero)

    return config_jugador


def crear_configuracion_inicial(carpeta_root: str, datos_iniciales: dict, nombre_partida: str, nombre_jugador: str, numero_jugador: int) -> None:
    """
    Crea la configuración inicial de la partida y guarda los archivos correspondientes en formato JSON.

    Args:
        carpeta_root (str): Carpeta raíz donde se almacenarán las partidas.
        datos_iniciales (dict): Diccionario con la configuración predeterminada de la partida.
        nombre_partida (str): Nombre de la partida a crear.
        nombre_jugador (str): Nombre del jugador que participará en la partida.
        numero_jugador (int): Número del jugador (por ejemplo, 1 o 2).

    Returns:
        None
    """
    # Crea la carpeta con el nombre de la partida dentro del root partidas_hundirflota.
    if not os.path.exists(f"{carpeta_root}/{nombre_partida}"):
        os.mkdir(f"{carpeta_root}/{nombre_partida}")

    # Genera el archivo de configuracion inicial json con el nombre de la partida dentro de la carpeta con su mismo nombre en root.
    if os.path.exists(f"{carpeta_root}/{nombre_partida}"):
        with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json", "w") as archivo:
            json.dump(datos_iniciales, archivo, indent = 4)
            print("Archivo de configuración creado con éxito.")

    config_jugador = crear_configuracion_jugador(datos_iniciales['configuracion_barcos'], nombre_jugador)

    with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json", "w") as archivo:
        json.dump(config_jugador, archivo, indent = 4)
        print(f"Archivo de jugador {numero_jugador} - {nombre_jugador} creado con éxito.")
    
    return None


def crear_tablero(dimension: int) -> list[list]:
    """
    Crea un tablero vacío de tamaño dimension x dimension.

    Args:
        dimension (int): Tamaño del tablero (número de filas y columnas).

    Returns:
        list[list]: Una lista de listas que representa el tablero, con cada celda inicializada como "~" (olas).
    """
    tablero = []

    for i in range(dimension):
        tablero.append([])
        for _ in range(dimension):
            tablero[i].append("~")

    return tablero


def mostrar_tablero(tablero: list, modo: str = "mostrar") -> None:
    """
    Genera y muestra una representación visual del tablero en formato string por consola. Dependiendo del modo, puede ocultar los barcos intactos o mostrar el tablero en su totalidad.

    Args:
        tablero (list): Matriz que representa el tablero, donde cada celda contiene un valor como "~", "B", etc.
        modo (str): Modo de visualización del tablero. Puede ser uno de los siguientes:
            - "ataque": Muestra el tablero con los barcos ocultos (se reemplazan los barcos por "~").
            - "estado": Muestra el tablero con el estado actual.
            - "finalizada": Muestra el título "Partida finalizada".
            - "mostrar" (predeterminado): Muestra el tablero con todos los barcos y celdas intactas.
    """

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
    elif modo == "finalizada":
        titulo = f"{' ' * len(tablero[0])}Partida finalizada\n"
    else:
        titulo = f"{' ' * len(tablero[0])}Coloca tus barcos:\n"

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
            tablero_completo += f"\n {i} {color('║')} {'  '.join(map(str, fila))} {color('║')}" + f""
        else:
            tablero_completo += f"\n{i} {color('║')} {'  '.join(map(str, fila))} {color('║')}" + f""
        i += 1
    
    tablero_completo = titulo + color(marco_superior) + tablero_completo + "\n" + color(marco_inferior) + coordenadas_inferior

    print(tablero_completo)

    return None


def cargar_json(ruta_archivo: str, max_reintentos: int = 4, pausa_ms: int = 150) -> dict | None:
    """
    Carga un archivo JSON en un diccionario con reintentos en caso de error por bloqueo (OSError e IOError).

    Args:
        ruta_archivo (str): Ruta al archivo JSON.
        max_reintentos (int): Número máximo de intentos permitidos.
        pausa_ms (int): Tiempo de pausa entre intentos en milisegundos.

    Returns:
        dict | None: Diccionario con los datos del archivo JSON o None si no es posible cargarlo.
    """
    try:
        intentos = 0
        while intentos < max_reintentos:
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    return json.load(archivo)
            except (OSError, IOError):
                intentos += 1
                time.sleep(pausa_ms / 1000)
        return None
    except Exception:
        return None


def guardar_json(ruta_archivo: str, configuracion: dict, nombre_partida: str, numero_jugador = None) -> None:
    """
    Guarda la configuración de la partida o del jugador en un archivo JSON.

    Args:
        ruta_archivo (str): Ruta donde se almacenará el archivo JSON.
        configuracion (dict): Configuración a guardar en el archivo.
        nombre_partida (str): Nombre de la partida que será utilizado en el nombre del archivo.
        numero_jugador (int, opcional): Número del jugador. Si se proporciona, se guarda el archivo con el número de jugador; si no, se guarda el archivo con el nombre de la partida.

    Returns:
        None
    """
    if numero_jugador is None:

        with open(f"{ruta_archivo}/{nombre_partida}/{nombre_partida}.json", "w") as archivo:
            json.dump(configuracion, archivo, indent = 4)
    else:

        with open(f"{ruta_archivo}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json", "w") as archivo:
            json.dump(configuracion, archivo, indent = 4)


def main():
    """
    Función principal que controla el flujo del juego.

    Muestra el menú principal y ejecuta las acciones según la opción seleccionada por el jugador.
    Existen tres opciones:
        1. Iniciar una nueva partida: Solicita nombre de jugadores, crea los archivos necesarios y espera a que el segundo jugador se una.
        2. Unirse a una partida existente: Permite al segundo jugador unirse a una partida ya creada.
        3. Salir: Termina la ejecución del programa.

    En el caso de la opción 1, espera a que el segundo jugador se una antes de comenzar la partida.
    En la opción 2, se valida que la partida exista antes de permitir que el segundo jugador se una.
    """
    limpiar_terminal()

    mostrar_menu()

    opcion = pedir_opcion()

    match opcion:

        case 1:

            nombre_j1 = input(color("Nombre J1 >> ")).capitalize()
            numero_jugador = "j1"
            nombre_partida = input(color("Introduce el nombre de la partida >> ")).strip()
            crear_carpeta_partidas(DIRECTORIO_PARTIDAS)
            crear_configuracion_inicial(DIRECTORIO_PARTIDAS, config_default, nombre_partida, nombre_j1, numero_jugador)
            time.sleep(2)
            print("Esperando a J2...")
            config_j1 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_default = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.json")

            validar_partida = False

            while not validar_partida:
                # Meter cargar_json directamente en el if porque retorna None si hay excepcion.
                config_j2 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.j2.json")
                if config_j2 is None:
                    time.sleep(3)
                else:
                    config_j2 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.j2.json")
                    limpiar_terminal()

                    validar_partida = True

            jugar(config_j1, config_j2, configuracion_default, numero_jugador, DIRECTORIO_PARTIDAS, nombre_partida)

        case 2:

            validar_partida = False

            while not validar_partida:
                nombre_partida = input(color("Introduce el nombre de la partida >> ")).strip()
                config_j1 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.j1.json")
                if config_j1 is None:
                    print("*ERROR* La partida no existe.")
                else:
                    nombre_j2 = input((color("Nombre J2 >> "))).capitalize()
                    numero_jugador = "j2"
                    config_j1 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
                    crear_configuracion_inicial(DIRECTORIO_PARTIDAS, config_default, nombre_partida, nombre_j2, numero_jugador)
                    config_j2 = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
                    configuracion_default = cargar_json(f"{DIRECTORIO_PARTIDAS}/{nombre_partida}/{nombre_partida}.json")
                    
                    validar_partida = True
            
            jugar(config_j1, config_j2, configuracion_default, numero_jugador, DIRECTORIO_PARTIDAS, nombre_partida)

        case 3:

            exit()


if __name__ == "__main__":
    main()