# Importa las funciones necesarias de los otros módulos del proyecto.
from gestion_datos import cargar_telefonos_csv, cargar_estado_json, guardar_estado_json, registrar_log_conexion, sincronizar_eliminacion_estado
from escaner_red import escanear_redes
# Importa datetime para obtener la fecha y hora actual para los registros de historial.
from datetime import datetime
# Importa time para poder pausar la ejecución del script.
import time

def inicializar_estado(telefonos_referencia, estado_actual):
    """
    Inicializa el estado para los teléfonos que están en el CSV de referencia 
    pero que aún no existen en el fichero de estado (estado_telefonos.json).
    Esto es útil cuando se añaden nuevos teléfonos al CSV.

    Args:
        telefonos_referencia (dict): Diccionario con los teléfonos cargados del CSV.
        estado_actual (dict): Diccionario con el estado actual cargado del JSON.

    Returns:
        tuple: Una tupla conteniendo el diccionario de estado actualizado y un booleano 
               que indica si se realizó algún cambio.
    """
    changed = False
    # Itera sobre cada teléfono del fichero CSV de referencia.
    for ext, datos in telefonos_referencia.items():
        # Comprueba si la extensión del teléfono no existe en la estructura de estado actual.
        if ext not in estado_actual:
            # Si no existe, crea una entrada por defecto para ese teléfono.
            estado_actual[ext] = {
                'hostname': datos.get('device_name'),
                'model': datos.get('model'),
                'description': datos.get('description'),
                'estadoActual': {
                    'conectado': False,
                    'ip': None,
                    'timestamp': None
                },
                'historial': []
            }
            # Marca que se ha realizado un cambio.
            changed = True
    return estado_actual, changed

def actualizar_estado_telefonos(estado_telefonos, telefonos_activos):
    """
    Compara la lista de teléfonos activos escaneados en la red con el último estado 
    conocido de los teléfonos y registra cualquier cambio de estado (conexión, 
    desconexión o cambio de IP).

    Args:
        estado_telefonos (dict): El diccionario principal con el estado de todos los teléfonos.
        telefonos_activos (list): Una lista de diccionarios, donde cada uno representa 
                                  un teléfono encontrado activo en la red.

    Returns:
        tuple: Una tupla con el diccionario de estado actualizado y un booleano 
               que indica si se detectaron cambios.
    """
    # Convierte la lista de teléfonos activos en un diccionario (mapa) usando la extensión 
    # como clave para una búsqueda más eficiente.
    telefonos_activos_map = {tel.get('phone_directory'): tel for tel in telefonos_activos if tel.get('phone_directory')}
    # Obtiene la fecha y hora actual en formato ISO para registrar el momento del cambio.
    timestamp = datetime.now().isoformat()
    cambios_detectados = False

    print("\n--- Comparando resultados y actualizando estados (Fase 3) ---")

    # Itera sobre cada teléfono registrado en la estructura de estado.
    for ext, datos_telefono in estado_telefonos.items():
        # Guarda el estado de conexión anterior para poder compararlo.
        estado_previo = datos_telefono['estadoActual']['conectado']
        # Busca si el teléfono actual fue encontrado en el último escaneo de red.
        telefono_encontrado = telefonos_activos_map.get(ext)

        if telefono_encontrado:
            # --- CASO 1: El teléfono está CONECTADO ---
            if not estado_previo:
                # CAMBIO: El teléfono estaba DESCONECTADO y ahora está CONECTADO.
                print(f"  [+] Cambio de estado: Teléfono {ext} ahora está CONECTADO en la IP {telefono_encontrado['ip']}.")
                # Registra el evento en el log.
                registrar_log_conexion(timestamp, "conectado", ext, datos_telefono['description'], telefono_encontrado['ip'])
                # Actualiza el estado actual.
                datos_telefono['estadoActual']['conectado'] = True
                datos_telefono['estadoActual']['ip'] = telefono_encontrado['ip']
                datos_telefono['estadoActual']['timestamp'] = timestamp
                # Añade un nuevo registro al historial del teléfono.
                datos_telefono['historial'].append({
                    'timestamp': timestamp,
                    'conectado': True,
                    'ip': telefono_encontrado['ip']
                })
                cambios_detectados = True
            elif datos_telefono['estadoActual']['ip'] != telefono_encontrado['ip']:
                # CAMBIO: El teléfono ya estaba conectado, pero su dirección IP ha cambiado.
                print(f"  [i] Cambio de IP: Teléfono {ext} ahora tiene la IP {telefono_encontrado['ip']} (antes {datos_telefono['estadoActual']['ip']}).")
                # Actualiza solo la IP y el timestamp en el estado actual.
                datos_telefono['estadoActual']['ip'] = telefono_encontrado['ip']
                datos_telefono['estadoActual']['timestamp'] = timestamp
                # Opcional: Se podría añadir también un registro al historial para cambios de IP.
                cambios_detectados = True
        else:
            # --- CASO 2: El teléfono está DESCONECTADO ---
            if estado_previo:
                # CAMBIO: El teléfono estaba CONECTADO y ahora está DESCONECTADO.
                print(f"  [-] Cambio de estado: Teléfono {ext} ahora está DESCONECTADO.")
                # Registra el evento en el log.
                registrar_log_conexion(timestamp, "desconectado", ext, datos_telefono['description'], None)
                # Actualiza el estado actual.
                datos_telefono['estadoActual']['conectado'] = False
                datos_telefono['estadoActual']['ip'] = None
                datos_telefono['estadoActual']['timestamp'] = timestamp
                # Añade un nuevo registro al historial.
                ##datos_telefono['historial'].append({
                ##    'timestamp': timestamp,
                ##    'conectado': False,
                ##    'ip': None
                ##})
                cambios_detectados = True

    if not cambios_detectados:
        print("  No se han detectado cambios de estado en esta ejecución.")
        
    return estado_telefonos, cambios_detectados


def main():
    """
    Función principal que orquesta la ejecución completa del monitor de conectividad.
    Carga los datos, y luego entra en un bucle infinito para escanear la red y 
    actualizar el estado de los teléfonos periódicamente.
    """
    # --- FASE 1: Carga de datos inicial y definición de estructuras ---
    print("--- Iniciando monitor de conectividad (Fase 1) ---")
    # Carga la lista de teléfonos de referencia desde el fichero CSV.
    telefonos_referencia = cargar_telefonos_csv()
    if telefonos_referencia is None:
        print("Error crítico: No se pudo cargar el fichero de teléfonos de referencia. Saliendo.")
        return

    print(f"Se han cargado {len(telefonos_referencia)} teléfonos desde el CSV.")

    # Carga el estado histórico de los teléfonos desde el fichero JSON.
    estado_telefonos = cargar_estado_json()
    if estado_telefonos:
        print(f"Se ha cargado el estado de {len(estado_telefonos)} teléfonos desde el JSON.")

    # Sincroniza el estado con el fichero CSV para eliminar teléfonos que ya no existen.
    sincronizar_eliminacion_estado()
    
    # Comprueba si hay teléfonos nuevos en el CSV que no estén en el estado y los inicializa.
    estado_telefonos, anadido_nuevo = inicializar_estado(telefonos_referencia, estado_telefonos)
    if not estado_telefonos and anadido_nuevo:
         print("No se ha encontrado un fichero de estado existente. Se creará una nueva estructura.")

    # Si se añadieron teléfonos nuevos, se informa y se guarda el estado inicial.
    if anadido_nuevo:
        print("Se han añadido nuevos teléfonos a la estructura de estado.")
        guardar_estado_json(estado_telefonos)
    
    print("\n" + "="*50)
    print("      Monitor de Conectividad Iniciado")
    print("      El sistema escaneará la red cada 60 segundos.")
    print("="*50 + "\n")

    # --- FASE 5: Bucle principal de monitorización ---
    while True:
        # --- FASE 2: Escaneo de la red ---
        print("\n--- Iniciando escaneo de red (Fase 2) ---")
        networkTelefonsPacients = "192.168.81.0/24"  # Define la red a escanear.
	
        redes_a_escanear = [ "192.168.81.0/24", "192.168.12.0/24", "192.168.13.0/24" ]
	
        telefonos_activos = escanear_redes(redes_a_escanear)

        if telefonos_activos:
            print(f"Se han encontrado {len(telefonos_activos)} teléfonos activos en la red.")
        else:
            print("No se encontraron teléfonos activos en la red o ocurrió un error durante el escaneo.")

        # --- FASE 3: Comparación y actualización de estado ---
        estado_telefonos, hubo_cambios = actualizar_estado_telefonos(estado_telefonos, telefonos_activos)

        # --- FASE 4: Persistencia de datos ---
        # Si se detectó algún cambio, se guarda el estado completo en el fichero JSON.
        if hubo_cambios:
            print("\n--- Guardando estado actualizado (Fase 4) ---")
            guardar_estado_json(estado_telefonos)
            print("El fichero 'estado_telefonos.json' ha sido actualizado.")

        # --- FASE 5: Pausa antes del siguiente ciclo ---
        print("\n--- Esperando 60 segundos para el próximo escaneo (Fase 5) ---")
        # El script se detiene durante 60 segundos antes de volver a empezar el bucle.
        time.sleep(60)



# Punto de entrada del script: si se ejecuta este fichero directamente, se llama a la función main().
if __name__ == '__main__':
    main()
