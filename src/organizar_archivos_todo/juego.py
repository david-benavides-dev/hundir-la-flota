import time

from config import cargar_json, guardar_json
from main import pedir_coordenadas
from utils import *

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


def verificar_ganador(config_jugador: dict) -> bool:
    """
    Verifica si todos los barcos de un jugador están hundidos (estado 'H').

    Args:
        config_jugador (dict): Diccionario con la configuración del jugador, incluyendo los estados de sus barcos.

    Returns:
        bool: True si todos los barcos están hundidos, False en caso contrario.
    """
    # Recorre todos los barcos y verifica que el estado de cada parte sea 'H' (hundido).
    # Bucle que itera por el estado de todos los barcos del diccionario y verifica que todos tienen 'H'.

    for barcos in config_jugador["barcos"].values():
        for estado in barcos["estado"].values():
            if estado != "H":
                return False
    return True


def es_movimiento_valido(movimientos: set, coordenadas: tuple) -> bool:
    """
    Verifica si un movimiento ya ha sido realizado en las coordenadas dadas.
    
    Args:
        movimientos (set): Conjunto de movimientos del jugador.
        coordenadas (tuple): Coordenada a verificar (fila, columna).
    
    Returns:
        bool: True si el movimiento es válido, False si ya ha sido realizado.
    """
    for movimiento in movimientos:
        if list(movimiento["coordenada"]) == coordenadas:
            return False
    return True


def realizar_ataque(jugador_pasivo: dict, coordenadas: tuple) -> str:
    """
    Realiza un ataque al jugador pasivo, actualizando el estado del tablero y los barcos según el resultado.

    Esta función realiza un ataque en las coordenadas especificadas y determina si el ataque
    fue a un área vacía (agua), un área tocada o un barco hundido.

    Args:
        jugador_pasivo (dict): Diccionario con la configuración del jugador pasivo, incluyendo su
                               tablero y la información sobre sus barcos.
        coordenadas (tuple): Coordenada (fila, columna) en la que se realiza el ataque.

    Returns:
        str: El resultado del ataque:
             - "A" si el ataque fue agua (sin impacto en un barco).
             - "T" si el ataque tocó un barco.
             - "H" si el barco fue hundido (todos sus segmentos han sido tocados).
    """
    y, x = coordenadas
    celda = jugador_pasivo['tablero'][y][x]
    
    if celda == "~":
        resultado = "A"
        print("Resultado del ataque: Agua")
        time.sleep(3)
        return resultado

    resultado = "T"
    for _, detalles_barco in jugador_pasivo["barcos"].items():
        estado = detalles_barco["estado"]
        coord_str = str(list(coordenadas))

        if coord_str in estado:
            estado[coord_str] = "T"

            if all(valor == "T" for valor in estado.values()):
                for key in estado.keys():
                    estado[key] = "H"
                resultado = "H"

    if resultado == "A":
        resultado_format = "Agua"
    elif resultado == "T":
        resultado_format = "Tocado"
    else:
        resultado_format = "Hundido"

    print(f"Resultado del ataque: {resultado_format}")
    time.sleep(3)
    return resultado


def registrar_resultado_ataque(movimientos: list, coordenadas: tuple, resultado: str) -> None:
    """
    Registra un movimiento en la lista de movimientos de la configuración del jugador.
    
    Args:
        configuracion_jugador: (dict): Diccionario del jugador.
        coordenadas (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque ("A", "T", "H").
    
    Returns:
        None
    """
    movimiento = {"coordenada": list(coordenadas), "resultado": resultado}
    movimientos.append(movimiento)

    return None


def actualizar_tablero(configuracion_enemigo: dict, coordenadas: tuple, resultado: str) -> None:
    """
    Actualiza el tablero del jugador enemigo con el resultado de un ataque.

    Esta función actualiza el tablero del jugador enemigo marcando la celda correspondiente
    según el resultado del ataque. Si el ataque hunde un barco, todas sus coordenadas
    en el tablero se marcan como "H".

    Args:
        configuracion_enemigo (dict): Diccionario que contiene la configuración del jugador enemigo, incluyendo su tablero y los detalles de sus barcos.
        coordenadas (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque.
    """
    y, x = coordenadas

    if resultado == "H":

        for barco in configuracion_enemigo["barcos"].values():
            if coordenadas in barco["coordenadas"]:
                for coord in barco["coordenadas"]:
                    configuracion_enemigo['tablero'][coord[0]][coord[1]] = "H"
    else:
        configuracion_enemigo['tablero'][y][x] = resultado
    
    return None


def esperar_turno_jugador(jugador: str, configuracion_default: dict, carpeta_root: str, nombre_partida: str, configuracion_jugador: dict, numero_jugador: str, resultado_ataque: str) -> None:
    """
    Espera hasta que sea el turno del jugador.
    
    Args:
        jugador (str): El identificador del jugador que está esperando su turno.
        configuracion_default (dict): Configuración predeterminada.
        carpeta_root (str): Ruta de las carpetas de ficheros.
        nombre_partida (str): Nombre de la partida.
        configuracion_jugador (dict): Configuración del jugador.
        numero_jugador (str): Número del jugador.
        resultado_ataque (str): Resultado del último ataque.

    Returns:
        None
    """
    while True:
        limpiar_terminal()
        config_default = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json")
        configuracion_jugador = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
        print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
        mostrar_tablero(configuracion_jugador['tablero'], "estado")
        if resultado_ataque is None:
            print(f"Esperando ataque...")
        else:
            if resultado_ataque == "A":
                ataque_string = "Agua"
            elif resultado_ataque == "T":
                ataque_string = "Tocado"
            else:
                ataque_string = "Hundido"
            print(f"Resultado del ataque: {ataque_string}")
        turno_actual = config_default['turno_actual']

        if turno_actual == jugador:
            time.sleep(configuracion_default['tiempo_refresco'])
            return None
        time.sleep(configuracion_default['tiempo_refresco'])


def jugar(configuracion_j1: dict, configuracion_j2: dict, configuracion_default: dict, numero_jugador: str, carpeta_root: str, nombre_partida: str):
    """
    Controla el flujo principal del juego, gestionando los turnos de los jugadores y las interacciones entre ellos.

    El juego se desarrolla en turnos, donde cada jugador puede atacar al otro mediante la selección de coordenadas en el tablero. En cada turno, la función valida las coordenadas de ataque, registra el resultado (agua, tocado, hundido), y actualiza el estado del tablero y los movimientos realizados. Además, maneja el cambio de turno y guarda la configuración actual del juego después de cada acción. 

    La función también verifica si un jugador ha ganado (es decir, si ha hundido todos los barcos del adversario) y finaliza el juego al determinar al ganador.

    Args:
        configuracion_j1 (dict): Diccionario con la configuración y estado del Jugador 1, que incluye su tablero, barcos y movimientos.
        configuracion_j2 (dict): Diccionario con la configuración y estado del Jugador 2, similar a `configuracion_j1`.
        configuracion_default (dict): Configuración general del juego que contiene información como el turno actual, número de turnos jugados, y otras configuraciones predeterminadas del juego.
        numero_jugador (str): Identificador del jugador actual, puede ser "j1" o "j2". Determina cuál es el jugador que está tomando su turno.
        carpeta_root (str): Ruta a la carpeta donde se encuentran los archivos JSON con la configuración del juego y los tableros de los jugadores.
        nombre_partida (str): Nombre de la partida en curso, utilizado para acceder a los archivos correspondientes a la partida en la carpeta `carpeta_root`.

    Returns:
        None

    El flujo de la función es el siguiente:

    1. **Asignación de jugadores**: La función determina quién es el jugador actual (jugador 1 o jugador 2) y quién es el enemigo basándose en el valor de `numero_jugador`.

    2. **Ciclo de turnos**: Un ciclo infinito (`while not jugador_ganador`) controla la alternancia de turnos entre los jugadores. En cada iteración:
        - Se muestra el tablero del jugador enemigo para que el jugador actual vea las coordenadas disponibles para atacar.
        - El jugador actual ingresa las coordenadas de su ataque. Si las coordenadas ya fueron atacadas, se les pide que ingrese otras coordenadas.
        - Se realiza el ataque, se registra el resultado (agua, tocado, hundido), y se actualiza el tablero del jugador enemigo.
        - Si el ataque es "agua", el turno se pasa al jugador contrario.
        - Si el ataque es "hundido", el juego verifica si el jugador enemigo ha perdido todos sus barcos.

    3. **Actualización de archivos**: Después de cada acción, la función guarda los archivos de configuración, tableros y movimientos de ambos jugadores en la carpeta `carpeta_root` para asegurar que el progreso se conserve.

    4. **Determinación del ganador**: Si un jugador hunde todos los barcos del adversario, la función determina que el juego ha finalizado, actualizando el estado del juego y mostrando al ganador.
    """
    if numero_jugador == "j1":
        configuracion_jugador = configuracion_j1
        configuracion_enemigo = configuracion_j2
        jugador_enemigo = "j2"
    else:
        configuracion_jugador = configuracion_j2
        configuracion_enemigo = configuracion_j1
        jugador_enemigo = "j1"

    jugador_ganador = False

    resultado_ataque = None

    while not jugador_ganador:
        if configuracion_default['turno_actual'] == numero_jugador:
            print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
            mostrar_tablero(configuracion_enemigo['tablero'], "ataque")
            coordenadas = pedir_coordenadas((color("Introduce coordenadas para atacar (fila, columna) >> ")), configuracion_default['dimensiones_tablero'])

            while not es_movimiento_valido(configuracion_jugador['movimientos'], coordenadas):
                print("*ERROR* Ya has atacado esas coordenadas.")
                time.sleep(2)
                limpiar_terminal()
                print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
                mostrar_tablero(configuracion_enemigo['tablero'], "ataque")
                coordenadas = pedir_coordenadas((color("Introduce coordenadas para atacar (fila, columna) >> ")), configuracion_default['dimensiones_tablero'])

            resultado_ataque = realizar_ataque(configuracion_enemigo, coordenadas)
            registrar_resultado_ataque(configuracion_jugador['movimientos'], coordenadas, resultado_ataque)
            actualizar_tablero(configuracion_enemigo, coordenadas, resultado_ataque)

            # Pasamos turno modificando la variable de control del diccionario por defecto, sumandole un turno jugado
            # siempre que el resultado de ataque sea agua.
            if resultado_ataque == "A":
                configuracion_default['turnos_jugados'] += 1
                configuracion_default['turno_actual'] = jugador_enemigo

            guardar_json(carpeta_root, configuracion_default, nombre_partida)
            guardar_json(carpeta_root, configuracion_jugador, nombre_partida, numero_jugador)
            guardar_json(carpeta_root, configuracion_enemigo, nombre_partida, jugador_enemigo)
            configuracion_jugador = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json")

            # Verifica si hay un jugador ganador para cambiar la variable de control del bucle principal.
            if verificar_ganador(configuracion_enemigo) and resultado_ataque == "H":
                configuracion_default['turno_actual'] = jugador_enemigo
                guardar_json(carpeta_root, configuracion_default, nombre_partida)
                ganador = numero_jugador
            jugador_ganador = verificar_ganador(configuracion_enemigo)

            limpiar_terminal()

        else:
            limpiar_terminal()
            esperar_turno_jugador(numero_jugador, configuracion_default, carpeta_root, nombre_partida, configuracion_jugador, numero_jugador, resultado_ataque)
            configuracion_jugador = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json")

            # Verifica si hay un jugador ganador para cambiar la variable de control del bucle principal.
            if verificar_ganador(configuracion_jugador):
                ganador = jugador_enemigo
            jugador_ganador = verificar_ganador(configuracion_jugador)

            limpiar_terminal()

    mostrar_tablero(configuracion_jugador['tablero'], "finalizada")
    print(f"Turnos jugados: {configuracion_default['turnos_jugados']}")
    
    if ganador == "j1":
        ganador = "Jugador 1"
    else:
        ganador = "Jugador 2"

    print(f"Gana el {ganador} !")