import time
from main import limpiar_terminal, mostrar_tablero, pedir_coordenadas, color, cargar_json, guardar_json


def registrar_movimiento(movimientos: set, coordenada: tuple, resultado: str) -> None:
    """
    Registra un movimiento en el conjunto de movimientos del jugador.
    
    Args:
        movimientos (set): Conjunto de movimientos del jugador.
        coordenada (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque ("A", "T", "H").
    
    Returns:
        None
    """


# DONE
def verificar_movimiento(movimientos: set, coordenadas: tuple) -> bool:
    """
    Verifica si un movimiento ya ha sido realizado en las coordenadas dadas.
    
    Args:
        movimientos (set): Conjunto de movimientos del jugador.
        coordenadas (tuple): Coordenada a verificar (fila, columna).
    
    Returns:
        bool: True si el movimiento es válido, False si ya ha sido realizado.
    """
    return coordenadas not in movimientos


def actualizar_tablero(tablero: list, coordenada: tuple, resultado: str) -> None:
    """
    Actualiza el tablero con el resultado de un ataque.
    
    Args:
        tablero (list): Tablero del jugador.
        coordenada (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque ("A", "T", "H").
    
    Returns:
        None
    """


def condicion_ganador(config_jugador: dict) -> bool:
    """
    Verifica si todos los barcos de un jugador han sido hundidos.
    
    Args:
        jugador (dict): Diccionario con la información del jugador.
    
    Returns:
        bool: True si todos los barcos han sido hundidos, False en caso contrario.
    """


def realizar_ataque(jugador_activo: dict, jugador_pasivo: dict, coordenada: tuple) -> str:
    """
    Realiza un ataque del jugador activo al jugador pasivo, registrando el resultado.
    
    Args:
        jugador_activo (dict): Diccionario con la información del jugador activo.
        jugador_pasivo (dict): Diccionario con la información del jugador pasivo.
        coordenada (tuple): Coordenada del ataque (fila, columna).
    
    Returns:
        str: Resultado del ataque ("A", "T", "H").
    """


def actualizar_tablero(tablero: list, coordenada: tuple, resultado: str) -> None:
    """
    Actualiza el tablero con el resultado de un ataque.
    
    Args:
        tablero (list): Tablero del jugador.
        coordenada (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque ("A", "T", "H").
    
    Returns:
        None
    """


def esperar_turno_ataque(jugador: str, configuracion_default: dict, carpetas_ficheros: str, nombre_partida: str, configuracion_jugador: dict, numero_jugador: str):
    """
    Espera hasta que sea el turno del jugador.
    """
    print(f"Esperando ataque...")
    while True:
        limpiar_terminal()
        config_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
        configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
        print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
        print(mostrar_tablero(configuracion_jugador['tablero'], "estado"))
        turno_actual = config_default['turno_actual']

        # Debe actualizar el tablero en esperar_turno_ataque para ir mostrandolo con los ataques realizados.
        # Cargar y mostrar tablero en cada iteracion con sleep de 2.

        if turno_actual == jugador:
            time.sleep(configuracion_default['tiempo_refresco'])
            return None
        time.sleep(configuracion_default['tiempo_refresco'])


def jugar(configuracion_j1: dict, configuracion_j2: dict, configuracion_default: dict, numero_jugador: str, carpetas_ficheros: str, nombre_partida: str):
    """

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

    while not jugador_ganador:
        if configuracion_default['turno_actual'] == numero_jugador:
            print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
            print(mostrar_tablero(configuracion_enemigo['tablero'], "ataque"))
            y, x = pedir_coordenadas((color("Introduce coordenadas para atacar (fila, columna) >> ")), configuracion_default['dimensiones_tablero'])
            configuracion_default['turno_actual'] = jugador_enemigo
            guardar_json(carpetas_ficheros, configuracion_default, nombre_partida)
            guardar_json(carpetas_ficheros, configuracion_jugador, nombre_partida, numero_jugador)
            guardar_json(carpetas_ficheros, configuracion_enemigo, nombre_partida, jugador_enemigo)
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
            limpiar_terminal()

        else:
            limpiar_terminal()
            esperar_turno_ataque(numero_jugador, configuracion_default, carpetas_ficheros, nombre_partida, configuracion_jugador, numero_jugador)
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
            limpiar_terminal()

# Debe actualizar el tablero en esperar_turno_ataque para ir mostrandolo con los ataques realizados.