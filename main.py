
"""
Executar el script de la següent manera:
    sudo /home/jordi/projectes/python/descobrimentIPsPort80/.entvirt/bin/python main.py
"""



import nmap
import requests
from bs4 import BeautifulSoup

def scrape_device_info(ip):
    """
    Extrae información específica de la página web de un dispositivo.
    Maneja redirecciones 'meta refresh'.
    """
    scraped_data = {
        'serial_number': 'N/A',
        'web_mac': 'N/A',
        'host_name': 'N/A',
        'phone_directory': 'N/A',
        'model': 'N/A'
    }

    # La URL inicial
    base_url = f"http://{ip}"

    try:
        # Petición inicial
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- INICIO DE LA MODIFICACIÓN: DETECCIÓN DE REDIRECCIÓN ---

        # Buscamos una etiqueta <meta> de tipo refresh
        meta_refresh = soup.find('meta', attrs={'http-equiv': 'REFRESH'})

        if meta_refresh:
            #print(f"  [i] Detectada redirección en {ip}. Siguiendo enlace...")
            # Extraemos el contenido del atributo 'content'
            content = meta_refresh.get('content')
            # La URL está después de 'URL='
            redirect_url_part = content.split('URL=')[1]

            # Construimos la URL completa para la segunda petición
            final_url = f"{base_url}/{redirect_url_part}"

            # Hacemos una segunda petición a la URL final
            response = requests.get(final_url, timeout=5)
            response.raise_for_status()


            # Forzamos la codificación también en la segunda respuesta
            response.encoding = 'utf-8'


            # Actualizamos el objeto soup con el contenido de la página real
            soup = BeautifulSoup(response.text, 'html.parser')

        # --- FIN DE LA MODIFICACIÓN ---

        # El resto del código de scraping funciona sobre el 'soup' correcto
        # Ahora cada clave apunta a una tupla de posibles nombres
        fields_map = {
            "serial_number": ("Número de serie", "N.º de serie", "Número de sèrie"),
            "web_mac": ("Dirección MAC", "Adreça MAC"), # Usamos una tupla con un solo elemento
            "host_name": ("Nombre de host", "Nom de host"),
            "phone_directory": ("N.º directorio telefónico", "N.º de directorio telefónico", "Número de directori telefònic"),
            "model": ("N.º de modelo", "Número de model")
        }

        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                key_text = cells[0].get_text(strip=True)

                # Iteramos sobre nuestro mapa para encontrar una coincidencia
                for internal_key, possible_names in fields_map.items():
                    if key_text in possible_names:
                        value_text = cells[-1].get_text(strip=True)
                        scraped_data[internal_key] = value_text
                        # Rompemos el bucle interior una vez que encontramos una coincidencia para esta fila
                        break


    except Exception as e:
        print(f"  [!] Ocurrió un error al procesar {ip}: {e}")

    return scraped_data


def scan_network(network_ip_with_mask):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_ip_with_mask, arguments='-O -p 80')

    online_hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            host_info = {'ip': host}

            # ... (código para MAC y OS que ya tenías)
            if 'mac' in nm[host]['addresses']:
                host_info['mac'] = nm[host]['addresses']['mac']
                if 'vendor' in nm[host] and nm[host]['vendor'].get(host_info['mac']):
                     host_info['mac_vendor'] = nm[host]['vendor'][host_info['mac']]
                else:
                     host_info['mac_vendor'] = 'N/A'
            else:
                host_info['mac'] = 'N/A'
                host_info['mac_vendor'] = 'N/A'

            if 'tcp' in nm[host] and 80 in nm[host]['tcp'] and nm[host]['tcp'][80]['state'] == 'open':
                host_info['port_80_open'] = True

                # --- INICIO DE LA MODIFICACIÓN ---
                # Si el puerto 80 está abierto, intentamos hacer scraping
                #print(f"[*] Puerto 80 abierto en {host}. Intentando scraping...")
                scraped_info = scrape_device_info(host)
                host_info.update(scraped_info) # Unimos la info del scraping a la del host
                # --- FIN DE LA MODIFICACIÓN ---

            else:
                host_info['port_80_open'] = False

            if 'osclass' in nm[host] and nm[host]['osclass']:
                os_class = nm[host]['osclass'][0]
                host_info['os_name'] = os_class['osfamily']
            elif 'osmatch' in nm[host] and nm[host]['osmatch']:
                os_match = nm[host]['osmatch'][0]
                host_info['os_name'] = os_match['name']
            else:
                host_info['os_name'] = 'N/A (Detection failed)'

            online_hosts.append(host_info)
    return online_hosts


if __name__ == "__main__":
    network = "192.168.80.0/24"
    responsive_ips = scan_network(network)

    print(f"\n--- ✅ Escaneo de Red ({network}) finalizado ---")

    print( f"{'IP'.ljust(15)} | {'N/S'.ljust(11)} | {'HostName'.ljust(15)} | {'Ext'.ljust(8)} | {'Model'.ljust(6)}"  )
    for host in responsive_ips:
        if host['port_80_open']:
            #print(
            #    f"\nIP: {host['ip']} | MAC (Nmap): {host.get('mac', 'N/A')}\n"
            #    f"  -> Puerto 80: Abierto\n"
            #    f"  -> OS (Nmap): {host.get('os_name', 'N/A')}\n"
            #    f"  -> WEB | N/S: {host.get('serial_number', 'N/A')} | MAC: {host.get('web_mac', 'N/A')} | Teléfono: {host.get('phone_directory', 'N/A')}"
            #)

            print( f"{host['ip'].ljust(15)} | {host.get('serial_number', 'N/A').ljust(11)} | {host.get('host_name', 'N/A').ljust(15)} | {host.get('phone_directory', 'N/A').ljust(8)} | {host.get('model', 'N/A').ljust(6)}" )
