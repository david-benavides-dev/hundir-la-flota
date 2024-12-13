import time
from main import limpiar_terminal, mostrar_tablero, pedir_coordenadas, color, cargar_json, guardar_json


def condicion_ganador(config_jugador: dict) -> bool:
    """
    Verifica si todos los barcos de un jugador estan hundidos.
    
    Args:
        jugador (dict): Diccionario con la información del jugador.
    
    Returns:
        bool: True si todos los barcos estan hundidos, False en caso contrario.
    """
    # Bucle que itera por el estado de todos los barcos del diccionario y verifica que todos tienen 'H'.

    for barcos in config_jugador["barcos"].values():
        for estado in barcos["estado"].values():
            if estado != "H":
                return False
    return True


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


def realizar_ataque(jugador_pasivo: dict, coordenada: tuple) -> str:
    # TODO si todas las posiciones del barco en cuestion estan en T, retornar H y actualizar barco con H
    """
    Realiza un ataque al jugador pasivo, registrando el resultado.
    
    Args:
        jugador_pasivo (dict): Diccionario con la información del jugador pasivo.
        coordenada (tuple): Coordenada del ataque (fila, columna).
    
    Returns:
        str: Resultado del ataque ("A", "T").
    """
    y, x = coordenada
    celda = jugador_pasivo['tablero'][y][x]
    
    if celda == "~":
        resultado = "A"
    else:
        resultado = "T"
        jugador_pasivo['tablero'][y][x] = "T" 

    return resultado


def registrar_movimiento(movimientos: list, coordenadas: tuple, resultado: str) -> None:
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


def actualizar_tablero(tablero: list, coordenadas: tuple, resultado: str) -> None:
    """
    Actualiza un tablero con el resultado de un ataque.
    
    Args:
        tablero (list): Tablero del jugador.
        coordenada (tuple): Coordenada del ataque (fila, columna).
        resultado (str): Resultado del ataque ("A", "T", "H").
    
    Returns:
        None
    """
    # TODO Si el resultado fue H, actualizar toda la fila del barco a H en el tablero.
    y, x = coordenadas
    tablero[y][x] = resultado


def esperar_turno_ataque(jugador: str, configuracion_default: dict, carpetas_ficheros: str, nombre_partida: str, configuracion_jugador: dict, numero_jugador: str) -> None:
    """
    Espera hasta que sea el turno del jugador.
    """
    while True:
        limpiar_terminal()
        config_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
        configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
        print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
        print(mostrar_tablero(configuracion_jugador['tablero'], "estado"))
        print(f"Esperando ataque...")
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
            coordenadas = pedir_coordenadas((color("Introduce coordenadas para atacar (fila, columna) >> ")), configuracion_default['dimensiones_tablero'])

            while not verificar_movimiento(configuracion_jugador['movimientos'], coordenadas):
                print("*ERROR* Ya has atacado esas coordenadas.")
                time.sleep(2)
                limpiar_terminal()
                print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
                print(mostrar_tablero(configuracion_enemigo['tablero'], "ataque"))
                coordenadas = pedir_coordenadas((color("Introduce coordenadas para atacar (fila, columna) >> ")), configuracion_default['dimensiones_tablero'])

            # TODO Si el resultado de ataque es igual a T o H, juega de nuevo.
            resultado_ataque = realizar_ataque(configuracion_enemigo, coordenadas)
            registrar_movimiento(configuracion_jugador['movimientos'], coordenadas, resultado_ataque)
            actualizar_tablero(configuracion_enemigo['tablero'], coordenadas, resultado_ataque)

            # Pasamos turno modificando la variable de control del diccionario por defecto, sumandole un turno jugado.
            configuracion_default['turnos_jugados'] =+ 1
            configuracion_default['turno_actual'] = jugador_enemigo
            guardar_json(carpetas_ficheros, configuracion_default, nombre_partida)
            guardar_json(carpetas_ficheros, configuracion_jugador, nombre_partida, numero_jugador)
            guardar_json(carpetas_ficheros, configuracion_enemigo, nombre_partida, jugador_enemigo)
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")

            # Verifica si hay un jugador ganador para cambiar la variable de control del bucle principal.
            jugador_ganador = condicion_ganador(configuracion_enemigo)

            limpiar_terminal()

        else:
            limpiar_terminal()
            esperar_turno_ataque(numero_jugador, configuracion_default, carpetas_ficheros, nombre_partida, configuracion_jugador, numero_jugador)
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")

            # Verifica si hay un jugador ganador para cambiar la variable de control del bucle principal.
            jugador_ganador = condicion_ganador(configuracion_enemigo)

            limpiar_terminal()