import json

def actualizar_logs():
    try:
        with open('estado_telefonos.json', 'r') as f:
            estado_telefonos = json.load(f)
    except FileNotFoundError:
        print("El archivo estado_telefonos.json no se encontró.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar estado_telefonos.json.")
        return

    try:
        with open('logs.json', 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        print("El archivo logs.json no se encontró.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar logs.json.")
        return

    for log in logs:
        extension = log.get("extension")
        if extension in estado_telefonos:
            log["descripcion"] = estado_telefonos[extension].get("description")

    try:
        with open('logs.json', 'w') as f:
            json.dump(logs, f, indent=4)
        print("El archivo logs.json se ha actualizado correctamente.")
    except IOError:
        print("No se pudo escribir en el archivo logs.json.")

if __name__ == "__main__":
    actualizar_logs()
