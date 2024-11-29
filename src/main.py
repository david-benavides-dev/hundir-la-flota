# WORK WORK


def mostrar_menu():
    return"""
    TEST TEST
    """

def crear_tablero(dimension: int) -> list:
    """
    
    """
    tablero = []

    for i in range(dimension):
        tablero.append([])
        for _ in range(dimension):
            tablero[i].append("~")

    return tablero


def mostrar_tablero(tablero: list) -> str:
    """
    
    """
    indice_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = 0

    parte_arriba = ""
    for fila in tablero:
        parte_arriba += f"  {indice_letras[i]} "
        i += 1

    parte_arriba += "\n"

    separador_lineas = "-" * (len(tablero[0]) * 4) + "-"

    i = 1

    tablero_completo = ""

    for fila in tablero:
        tablero_completo += f"\n| {' | '.join(map(str, fila))} | {i}" + f"\n{separador_lineas}"
        i += 1
    
    tablero_completo = parte_arriba + separador_lineas + tablero_completo
    return tablero_completo


def main():
    tablero = crear_tablero(10)
    salir = False
    while not salir:
        print(mostrar_tablero(tablero))
        input("Presiona ENTER")


if __name__ == "__main__":
    main()