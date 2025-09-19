import requests
from bs4 import BeautifulSoup

# Usaremos el HTML que proporcionaste directamente para este ejemplo
# En un caso real, la llamada a requests.get() lo obtendría de la red.
html_content = """
<html><head><meta http-equiv=Content-Type content="text/html; charset=utf-8"><title>Cisco Systems, Inc.</title></head><body bgcolor=white lang=ZH-TW link=white vlink=white style='tab-interval:36.0pt'alink="#ffffff"><div><table border=1 cellspacing=0 cellpadding=0 width="100%" style='width:100.0%;mso-cellspacing:0cm;border:outset #003031 1.0pt; mso-border-alt:outset #003031 .75pt;mso-padding-alt:0cm 0cm 0cm 0cm'> <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;height:37.5pt'>  <td WIDTH="200" HEIGHT="100" ALIGN=center><A HREF="http://www.cisco.com"><IMG SRC="cisco_Logo.gif"></A></TD>  <td style='border:inset #003031 1.0pt;mso-border-alt:inset #003031 .75pt;  background:#003031;padding:0cm 0cm 0cm 0cm;height:37.5pt'>  <p align=center style='text-align:center'><b><span  style='font-size:24.0pt;color:white'>Info. dispositivo</span></b></p>  <p align=center style='text-align:center'><b><span   style='font-size:13.5pt;color:white'>Teléfono IP de Cisco <span class=SpellE>CP-6901</span> (SEP247E12BF54B5)</span></b></p></td></tr> <tr style='mso-yfti-irow:1;mso-yfti-lastrow:yes'>  <td width=200 valign=top style='width:150.0pt;border:inset #003031 1.0pt;  mso-border-alt:inset #003031 .75pt;background:#003031;padding:0cm 0cm 0cm 0cm'>  <div align=center>  <table border=0 cellspacing=10 cellpadding=0 style='mso-cellspacing:   7.5pt;mso-padding-alt:0cm 0cm 0cm 0cm'>   <tr><td><p><b><a href="Device_Information.html">Info. dispositivo</a></b></p></td></tr>   <tr><td><p><b><a href="Network_Setup.html">Configuración de red</a></b></p></td></tr>   <tr><td><p><b><span style='color:white'>Estadísticas de red</span></b></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Ethernet_Information.html">Información Ethernet</a></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Network.html">Red</a></p></td></tr>   <tr><td><p><b><span style='color:white'>Reg. dispositivos</span></b></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Console_Logs.html">Registros de consola</a></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Core_Dumps.html">Volcados de memoria</a></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Status_Messages.html">Mensajes de estado</a></p></td></tr>   <tr><td><p><b><span style='color:white'>Estadísticas de flujo</span></b></p></td></tr>   <tr><td><p>&nbsp;&nbsp;&nbsp;<a href="Stream1.html">Flujo 1</a></p></td></tr>  </table></div>  <p align=center style='text-align:center'></p></td>  <td valign=top style='border:inset #003031 1.0pt;mso-border-alt:inset #003031 .75pt;  padding:0cm 0cm 0cm 0cm'>  <div align=center>  <table border=0 cellspacing=10 cellpadding=0 style='mso-cellspacing:   7.5pt;mso-padding-alt:0cm 0cm 0cm 0cm'>   <tr>    <td><p><b>Dirección MAC</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>24:7E:12:BF:54:B5</b></p></td></tr>   <tr>    <td><p><b>Nombre de host</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>SEP247E12BF54B5</b></p></td></tr>   <tr>    <td><p><b>N.º de directorio telefónico</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>10885129</b></p></td></tr>      <tr>    <td><p><b>ID de carga de la aplicación</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>SIP6901.9-3-1-SR2-3</b></p></td></tr>   <tr>    <td><p><b>ID de carga de inicio</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>6901.0-0-0-01-05</b></p></td></tr>   <tr>    <td><p><b>Revisión de Hardware</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>1.0</span></strong></p></td></tr>   <tr>    <td><p><b>N.º de serie</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>FCH2201DJ99</b></p></td></tr>   <tr>    <td><p><b>N.º de modelo</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>CP-6901</b></p></td></tr>   <tr>    <td><p><b>Mensaje en espera</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>No</b></p></td></tr>   <tr>    <td><p><b>UDI</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>Phone</b></p></td></tr>   <tr>    <td><p>&nbsp;</p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>Cisco IP Phone 6901</b></p></td></tr>   <tr>    <td><p>&nbsp;</p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>CP-6901</b></p></td></tr>   <tr>    <td><p>&nbsp;</p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>V01</b></p></td></tr>   <tr>    <td><p>&nbsp;</p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>FCH2201DJ99</b></p></td></tr>   <tr>    <td><p><b>Hora</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>10:55:16</b></p></td></tr>   <tr>    <td><p><b>Zona horaria</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>Europe/Madrid</b></td></tr>   <tr>    <td><p><b>Fecha</b></p></td>    <td width=20 style='width:15.0pt;padding:0cm 0cm 0cm 0cm'></td>    <td><p><b>09/19/2025</b></p></td></tr>  </table></div>  <p align=center style='text-align:center'></p></td></tr></table><p><span style='color:windowtext'><o:p>&nbsp;</o:p></span></p></div></body></html>
"""

def scrape_device_info(html_doc):
    """
    Extrae información específica de la página web de un dispositivo.
    Versión corregida y más robusta.
    """
    scraped_data = {
        'serial_number': 'N/A',
        'web_mac': 'N/A',
        'phone_directory': 'N/A',
        'model': 'N/A'
    }
    
    try:
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Mapeo del texto en la web a nuestras claves internas
        fields_map = {
            "N.º de serie": "serial_number",
            "Dirección MAC": "web_mac",
            "N.º de directorio telefónico": "phone_directory",
            "N.º de modelo": "model"
        }

        # Busca todas las filas de la tabla
        rows = soup.find_all('tr')
        
        for row in rows:
            # Obtiene todas las celdas de la fila
            cells = row.find_all('td')
            # Aseguramos que la fila tenga celdas para procesar
            if len(cells) > 1:
                # La clave está en la primera celda
                key_text = cells[0].get_text(strip=True)
                
                # Si la clave es una de las que buscamos...
                if key_text in fields_map:
                    # El valor está en la última celda
                    value_text = cells[-1].get_text(strip=True)
                    
                    # Guardamos el dato en nuestro diccionario
                    internal_key = fields_map[key_text]
                    scraped_data[internal_key] = value_text

    except Exception as e:
        print(f"  [!] Ocurrió un error al procesar el HTML: {e}")

    return scraped_data

if __name__ == "__main__":
    # Para probar, pasamos el contenido HTML directamente a la función
    # En tu caso real, llamarías a la función con la IP: scrape_device_info(requests.get(url).text)
    device_data = scrape_device_info(html_content)
    print(device_data)
