from juego import *
from utils import *
from config import *


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