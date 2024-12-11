import time
from main import limpiar_terminal, mostrar_tablero, pedir_coordenadas, color, cargar_json

"""
JUEGO
    Carga json
    Lee dict
    jugador1 hace x mientras jugador2 espera
    Guarda el dict
    Guarda dict en json

    Carga json
    Lee dict
    jugador2 hace x
    jugador 1 espera
    Guarda el dict
    Guarda dict en json
"""


def esperar_turno(jugador: str, configuracion_default: dict, carpetas_ficheros: str, nombre_partida: str):
    """Espera hasta que sea el turno del jugador."""
    print(f"Esperando ataque...")
    while True:
        config_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
        turno_actual = config_default['turno_actual']
        if turno_actual == jugador:
            return None
            time.sleep(2)
            break
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
            print(color("--- Tiempo de espera máximo: 30 segundos ---"))
            y, x = pedir_coordenadas((color("Introduce coordenadas para atacar >> ")), configuracion_default['dimensiones_tablero'])
            configuracion_default['turno_actual'] = jugador_enemigo
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
            limpiar_terminal()

        else:
            print(f"Turno de Jugador {configuracion_default['turno_actual'][1]}\n")
            print(mostrar_tablero(configuracion_jugador['tablero'], "estado"))
            esperar_turno(numero_jugador, configuracion_default, carpetas_ficheros, nombre_partida)
            configuracion_jugador = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{numero_jugador}.json")
            configuracion_enemigo = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.{jugador_enemigo}.json")
            configuracion_default = cargar_json(f"{carpetas_ficheros}/{nombre_partida}/{nombre_partida}.json")
            limpiar_terminal()

    print("Partida finalizada")