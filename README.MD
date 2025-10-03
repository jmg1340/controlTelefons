En una red de datos con mascara /24 tengo conenctados solo telefonos IP. 
Hay un servidor DHCP que asigna las IPs a los telefonos. 
Los telefonos no estan registrados en ningun servidor DNS
Los telefonos tienen activo el puerto 80.


PROBLEMA
De vez en cuando los telefonos pierden la conexion.


OBJETIVO.
Llevar un registro de conectividad por cada telefono

DATOS QUE SE TIENEN:
Fichero "TelefonsPacientsStCugat.csv" con listado de telefonos con:
- Extension (Ext)
- Hostname (Device_name)
- Numero Serie (SN)
- Descripcion (Description)


METODOLOGIA
A cada minuto, hacer un escaneo de puertos de la red 192.168.81.0/24 y a partir de la pagina web correspondiente a la IP,  obtener los datos:
- IP
- NS
- HostName
- Ext
- Model

Todo esto ya lo hace actualmente el fichero "main.py"


A partir de estos datos obtenidos, ver cuales coinicien con los del listado de "TelefonsPacientsStCugat.csv" y cuales no.

De los que coincidan, hacer un seguimiento para cada telefono con la siguiente información:
{
   extension: {
      estadoActual: True/False
      historial:[
         { fecha: xx/xx/xx, estado: True/False, hostname: "xxxxx" },
         { fecha: xx/xx/xx, estado: True/False, hostname: "xxxxx" },
         { fecha: xx/xx/xx, estado: True/False, hostname: "xxxxx" },
         ...
      ]
   }
}

Esta información se debe capturar si no hay ningun registro en el historial y cada vez que cambie el estado de la conexion.





PROYECTO PYTHON

Haz primero una propuesta de los pasos a hacer por fases para despues ir completando cada fase.
