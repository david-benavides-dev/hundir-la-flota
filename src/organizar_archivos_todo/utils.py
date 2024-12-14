import time
import os


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