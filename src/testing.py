import time


valor = 0

def espera():
    while valor is 0:
        print("Esperando...")
        if valor == 1:
            print("Terminado")
            return None
        time.sleep(2)


espera()