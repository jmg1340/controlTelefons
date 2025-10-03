# Importa la librería nmap para realizar escaneos de red.
import nmap
# Importa la librería requests para hacer peticiones HTTP a las páginas web de los teléfonos.
import requests
# Importa BeautifulSoup de bs4 para parsear el HTML de las páginas web.
from bs4 import BeautifulSoup

def scrape_device_info(ip):
    """
    Se conecta a la página web de un dispositivo (teléfono IP) en la IP especificada,
    extrae (hace scraping) de información relevante como el número de serie, la MAC, etc.,
    y la devuelve en un diccionario.
    Está diseñado para manejar redirecciones 'meta refresh' que algunas páginas de 
    dispositivos utilizan.

    Args:
        ip (str): La dirección IP del dispositivo del que se extraerá la información.

    Returns:
        dict: Un diccionario con la información extraída. Si ocurre un error o no se 
              encuentra algún dato, los valores correspondientes serán 'N/A'.
    """
    # Inicializa un diccionario con valores por defecto.
    scraped_data = {
        'serial_number': 'N/A',
        'web_mac': 'N/A',
        'host_name': 'N/A',
        'phone_directory': 'N/A',
        'model': 'N/A'
    }
    base_url = f"http://{ip}"
    try:
        # Realiza una petición GET a la URL base del dispositivo con un timeout de 5 segundos.
        response = requests.get(base_url, timeout=5)
        # Lanza una excepción si la respuesta HTTP no fue exitosa (ej. error 404 o 500).
        response.raise_for_status()
        # Parsea el contenido HTML de la respuesta.
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Busca una etiqueta <meta http-equiv="REFRESH"> para manejar redirecciones.
        meta_refresh = soup.find('meta', attrs={'http-equiv': 'REFRESH'})
        if meta_refresh:
            # Si encuentra una redirección, construye la URL final y realiza una nueva petición.
            content = meta_refresh.get('content')
            redirect_url_part = content.split('URL=')[1]
            final_url = f"{base_url}/{redirect_url_part}"
            response = requests.get(final_url, timeout=5)
            response.raise_for_status()
            response.encoding = 'utf-8' # Asegura la codificación correcta.
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # Diccionario que mapea los nombres internos de los campos con los posibles textos
        # que pueden tener en la página web (en varios idiomas).
        fields_map = {
            "serial_number": ("Número de serie", "N.º de serie", "Número de sèrie"),
            "web_mac": ("Dirección MAC", "Adreça MAC"),
            "host_name": ("Nombre de host", "Nom de host"),
            "phone_directory": ("N.º directorio telefónico", "N.º de directorio telefónico", "Número de directori telefònic"),
            "model": ("N.º de modelo", "Número de model")
        }
        # Busca todas las filas <tr> en la tabla del HTML.
        rows = soup.find_all('tr')
        for row in rows:
            # Obtiene todas las celdas <td> de la fila.
            cells = row.find_all('td')
            if len(cells) > 1:
                # El texto de la primera celda es la clave (ej: "Número de serie").
                key_text = cells[0].get_text(strip=True)
                # Comprueba si el texto de la clave coincide con alguno de los nombres buscados.
                for internal_key, possible_names in fields_map.items():
                    if key_text in possible_names:
                        # Si coincide, el texto de la última celda es el valor.
                        value_text = cells[-1].get_text(strip=True)
                        scraped_data[internal_key] = value_text
                        break # Pasa a la siguiente fila.
    except Exception as e:
        # Captura cualquier excepción durante la petición o el parseo.
        print(f"  [!] Ocurrió un error al procesar {ip}: {e}")
    return scraped_data




def escanear_redes( array ):
    onlineHostsRedes = []
    for red in array:
        print( f"\tEscaneando red: {red}...")
        onlineHostsRedes.extend( escanear_red( red ) )

    return onlineHostsRedes





def escanear_red(network_ip_with_mask):
    """
    Utiliza Nmap para escanear la red especificada en busca de dispositivos que tengan 
    el puerto 80 (HTTP) abierto. Para cada dispositivo encontrado, intenta extraer 
    su información utilizando la función `scrape_device_info`.

    Args:
        network_ip_with_mask (str): La red a escanear en formato CIDR (ej: "192.168.1.0/24").

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un teléfono 
              activo encontrado y contiene su IP y la información extraída.
    """
    nm = nmap.PortScanner()
    try:
        # Ejecuta el escaneo de nmap en la red especificada, buscando solo el puerto 80.
        nm.scan(hosts=network_ip_with_mask, arguments='-p 80')
    except nmap.PortScannerError:
        # Captura el error si nmap no está instalado o no se puede ejecutar.
        print("Error: Nmap no está instalado o no se puede ejecutar. Asegúrate de que tienes permisos (ejecuta con sudo).")
        return []
        
    online_hosts = []
    # Itera sobre todos los hosts encontrados por nmap.
    for host in nm.all_hosts():
        # Comprueba si el host está 'up' (encendido) y si tiene el puerto 80 TCP abierto.
        if nm[host].state() == 'up' and 'tcp' in nm[host] and 80 in nm[host]['tcp'] and nm[host]['tcp'][80]['state'] == 'open':
            # Si cumple las condiciones, es probablemente un teléfono IP.
            host_info = {'ip': host}
            # Llama a la función de scraping para obtener más detalles del dispositivo.
            scraped_info = scrape_device_info(host)
            # Combina la IP con la información extraída.
            host_info.update(scraped_info)
            # Añade el dispositivo a la lista de hosts activos.
            online_hosts.append(host_info)
    return online_hosts
