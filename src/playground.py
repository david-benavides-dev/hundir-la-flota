# def crear_configuracion_inicial(carpeta_root: str, datos_iniciales: dict, nombre_partida: str, nombrej1: str, nombrej2: str) -> None:
#     """
    
#     """
#     # Modifica la configuración por defecto con el nombre que queramos darle a la partida
#     config_default['nombre_partida'] = nombre_partida

#     # Crea la carpeta con el nombre de la partida dentro del root partidas_hundirflota.
#     if not os.path.exists(f"{carpeta_root}/{nombre_partida}"):
#         os.mkdir(f"{carpeta_root}/{nombre_partida}")

#     # Genera el archivo de configuracion inicial json con el nombre de la partida dentro de la carpeta con su mismo nombre en root.
#     with open(f"{carpeta_root}/{nombre_partida}/{nombre_partida}.json", "w") as archivo:
#         json.dump(datos_iniciales, archivo, indent = 4)
#         print("Archivo de configuración creado con éxito")