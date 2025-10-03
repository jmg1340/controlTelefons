import json

def eliminar_historial():
    try:
        with open('estado_telefonos.json', 'r') as f:
            estado_telefonos = json.load(f)
    except FileNotFoundError:
        print("El archivo estado_telefonos.json no se encontró.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar estado_telefonos.json.")
        return

    for extension in estado_telefonos:
        if "historial" in estado_telefonos[extension]:
            del estado_telefonos[extension]["historial"]

    try:
        with open('estado_telefonos.json', 'w') as f:
            json.dump(estado_telefonos, f, indent=4)
        print("El archivo estado_telefonos.json se ha actualizado correctamente.")
    except IOError:
        print("No se pudo escribir en el archivo estado_telefonos.json.")

if __name__ == "__main__":
    eliminar_historial()
