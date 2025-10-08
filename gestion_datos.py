# Importa el módulo csv para trabajar con ficheros CSV.
import csv
# Importa el módulo json para trabajar con ficheros JSON.
import json
# Importa el módulo os para interactuar con el sistema operativo, como comprobar si un fichero existe.
import os

def cargar_telefonos_csv(filename='TelefonsStCugat.csv'):
    """
    Lee un fichero CSV que contiene la lista de teléfonos de referencia y los carga 
    en un diccionario. La extensión del teléfono se utiliza como clave principal para 
    un acceso rápido.

    Args:
        filename (str): El nombre del fichero CSV a leer. Por defecto es 
                        'TelefonsStCugat.csv'.

    Returns:
        dict: Un diccionario donde cada clave es una extensión de teléfono y el valor 
              es otro diccionario con los datos de ese teléfono.
              Devuelve None si el fichero no se encuentra o si ocurre un error.
    """
    telefonos = {}
    try:
        # Abre el fichero CSV en modo lectura ('r') con codificación UTF-8.
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            # Utiliza DictReader para leer el CSV como una lista de diccionarios,
            # donde las claves son los nombres de las columnas.
            csv_reader = csv.DictReader(csv_file)
            # Itera sobre cada fila del fichero CSV.
            for row in csv_reader:
                # Obtiene la extensión ('EXT') de la fila actual.
                extension = row.get('EXT')
                # Si la extensión existe, la usa como clave en el diccionario de teléfonos.
                if extension:
                    telefonos[extension] = {
                        'model': row.get('model'),
                        'description': row.get('DESCRIPTION'),
                        'device_name': row.get('DEVICE_NAME'),
                        'sn': row.get('SN'),
                        'sw': row.get('SW'),
                        'pto': row.get('PTO')
                    }
    except FileNotFoundError:
        # Captura el error si el fichero CSV no existe.
        print(f"Error: El fichero {filename} no se ha encontrado.")
        return None
    except Exception as e:
        # Captura cualquier otro error que pueda ocurrir durante la lectura del fichero.
        print(f"Ha ocurrido un error al leer el fichero CSV: {e}")
        return None
    # Devuelve el diccionario con todos los teléfonos cargados.
    return telefonos

def cargar_estado_json(filename='estado_telefonos.json'):
    """
    Carga el estado y el historial de los teléfonos desde un fichero JSON.
    Este fichero actúa como una pequeña "base de datos" para mantener la persistencia 
    del estado entre ejecuciones del script.

    Args:
        filename (str): El nombre del fichero JSON del que se cargarán los datos.
                        Por defecto es 'estado_telefonos.json'.

    Returns:
        dict: Un diccionario con el estado de los teléfonos. Si el fichero no existe 
              o está mal formado, devuelve un diccionario vacío.
    """
    # Comprueba si el fichero JSON existe en la ruta especificada.
    if not os.path.exists(filename):
        # Si no existe, no hay estado previo que cargar, por lo que devuelve un diccionario vacío.
        return {}
        
    try:
        # Abre el fichero JSON en modo lectura ('r') con codificación UTF-8.
        with open(filename, 'r', encoding='utf-8') as json_file:
            # Carga el contenido del fichero JSON y lo convierte en un diccionario de Python.
            return json.load(json_file)
    except json.JSONDecodeError:
        # Captura el error si el fichero JSON tiene un formato incorrecto.
        print(f"Error: El fichero {filename} está mal formado y no se puede decodificar.")
        return {}
    except Exception as e:
        # Captura cualquier otro error durante la lectura del fichero.
        print(f"Ha ocurrido un error al leer el fichero JSON: {e}")
        return {}

import shutil

def guardar_estado_json(datos, filename='estado_telefonos.json'):
    """
    Guarda la estructura de datos del estado de los teléfonos en un fichero JSON.
    Después de guardar, copia el fichero a un directorio de destino especificado.

    Args:
        datos (dict): El diccionario con el estado de los teléfonos que se va a guardar.
        filename (str): El nombre del fichero JSON donde se guardarán los datos.
                        Por defecto es 'estado_telefonos.json'.
    """
    try:
        # Abre el fichero en modo escritura ('w') con codificación UTF-8.
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(datos, json_file, indent=4)
        
        # --- Replicar el fichero a otro directorio ---
        destination_dir = '/home/jordi/projectes/python/flask/bluePrints_utilitats/app/bp_estatTelefons/static/'
        destination_path = os.path.join(destination_dir, filename)
        
        try:
            shutil.copy2(filename, destination_path)
            print(f"  Fichero de estado replicado exitosamente en: {destination_path}")
        except FileNotFoundError:
            print(f"  [!] Error al replicar: El directorio de destino no existe: {destination_dir}")
        except Exception as e:
            print(f"  [!] Ocurrió un error inesperado al replicar el fichero: {e}")

    except Exception as e:
        print(f"Ha ocurrido un error al guardar el estado en {filename}: {e}")

def registrar_log_conexion(timestamp, estado, extension, descripcion, ip, filename='logs.json'):
    """
    Registra un evento de conexión o desconexión en el fichero logs.json y lo replica.

    Args:
        timestamp (str): La fecha y hora del evento.
        estado (str): El estado del teléfono ('conectado' or 'desconectado').
        extension (str): La extensión del teléfono.
        ip (str): La dirección IP actual del teléfono.
        filename (str): El nombre del fichero de log. Por defecto es 'logs.json'.
    """
    log_entry = {
        "timeStamp": timestamp,
        "estado": estado,
        "extension": extension,
        "descripcion": descripcion,
        "ip actual": ip
    }
    
    logs = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            print(f"Aviso: El fichero {filename} está mal formado. Se creará uno nuevo.")
            logs = []

    logs.append(log_entry)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=4)

        # --- Replicar el fichero a otro directorio ---
        destination_dir = '/home/jordi/projectes/python/flask/bluePrints_utilitats/app/bp_estatTelefons/static/'
        destination_path = os.path.join(destination_dir, filename)
        
        try:
            shutil.copy2(filename, destination_path)
            print(f"  Fichero de logs replicado exitosamente en: {destination_path}")
        except FileNotFoundError:
            print(f"  [!] Error al replicar: El directorio de destino no existe: {destination_dir}")
        except Exception as e:
            print(f"  [!] Ocurrió un error inesperado al replicar el fichero de logs: {e}")

    except Exception as e:
        print(f"Ha ocurrido un error al guardar el log en {filename}: {e}")

def sincronizar_estado(csv_filename='TelefonsStCugat.csv', json_filename='estado_telefonos.json'):
    """
    Sincroniza el fichero de estado JSON con el fichero CSV, añadiendo nuevas entradas
    y eliminando las que ya no existen en el CSV.
    """
    telefonos_csv = cargar_telefonos_csv(csv_filename)
    if telefonos_csv is None:
        return

    estado_telefonos = cargar_estado_json(json_filename)
    
    extensiones_csv = set(telefonos_csv.keys())
    extensiones_json = set(estado_telefonos.keys())

    extensiones_a_anadir = extensiones_csv - extensiones_json
    extensiones_a_eliminar = extensiones_json - extensiones_csv

    cambios = False

    if not extensiones_a_anadir and not extensiones_a_eliminar:
        print("No hay extensiones para añadir o eliminar. El fichero de estado está sincronizado.")
        return

    # Añadir nuevas extensiones
    for extension in extensiones_a_anadir:
        datos_csv = telefonos_csv[extension]
        estado_telefonos[extension] = {
            'hostname': datos_csv.get('device_name'),
            'model': datos_csv.get('model'),
            'description': datos_csv.get('description'),
            'estadoActual': {
                'conectado': False,
                'ip': None,
                'timestamp': None
            },
            'historial': []
        }
        print(f"Extensión {extension} añadida al fichero de estado.")
        cambios = True

    # Eliminar extensiones antiguas
    for extension in extensiones_a_eliminar:
        del estado_telefonos[extension]
        print(f"Extensión {extension} eliminada del fichero de estado.")
        cambios = True

    if cambios:
        guardar_estado_json(estado_telefonos, json_filename)
        print("El fichero de estado ha sido actualizado.")
