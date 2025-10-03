

Popuesta detallada por fases para desarrollar el sistema de monitorización de conectividad.

### **Propuesta del Proyecto: Monitor de Conectividad de Teléfonos IP**

El objetivo es crear un script que, basándose en el `main.py` existente, gestione un registro histórico del estado de conexión de una lista de teléfonos IP definida en un fichero CSV.

---

#### **Fase 1: Carga de Datos y Definición de Estructuras**

En esta fase inicial, nos centraremos en preparar los datos y las estructuras que usará la aplicación.

1.  **Leer el listado de teléfonos:** Crear una función que lea el fichero `TelefonsPacientsStCugat.csv` y cargue los datos de los teléfonos (Extensión, Hostname, etc.) en una estructura de datos fácil de consultar, como un diccionario donde la clave sea la extensión del teléfono.
2.  **Cargar el estado histórico:** Crear una función para leer un fichero `estado_telefonos.json` (si existe). Este fichero contendrá el estado y el historial de cada teléfono de ejecuciones anteriores. Si no existe, se inicializará una estructura de datos vacía en memoria con el formato especificado en el README.
3.  **Definir la estructura de datos principal:** Se trabajará con un diccionario principal en memoria que almacenará la información de cada teléfono, siguiendo la estructura solicitada.

#### **Fase 2: Integración del Escaneo de Red**

Esta fase consiste en reutilizar la lógica existente en `main.py`.

1.  **Analizar `main.py`:** Revisar el código de `main.py` para entender cómo realiza el escaneo de la red y la extracción de datos de los teléfonos.
2.  **Modularizar el escaneo:** Refactorizar la lógica de `main.py` para encapsularla en una única función, por ejemplo `escanear_red()`. Esta función se encargará de realizar el escaneo y devolver una lista de los teléfonos activos encontrados, junto con sus datos (IP, HostName, Extensión, etc.).

#### **Fase 3: Lógica de Comparación y Actualización de Estado**

El núcleo del proyecto. Aquí se compararán los datos para detectar cambios.

1.  **Comparar resultados:** Implementar una función que reciba la lista de teléfonos de referencia (del CSV) y la lista de teléfonos activos (del escaneo).
2.  **Detectar cambios de estado:** Para cada teléfono del listado de referencia, se comprobará si ha sido encontrado en el escaneo actual.
    *   Se comparará su estado de conexión actual (`True` si está en la lista de activos, `False` si no) con el último estado registrado en el historial.
    *   Si es la primera vez que se procesa el teléfono o si su estado ha cambiado (de `True` a `False` o viceversa), se añadirá una nueva entrada al `historial` de ese teléfono con la fecha y hora del cambio, el nuevo estado y el hostname detectado.
3.  **Actualizar estado actual:** Se actualizará el campo `estadoActual` para cada teléfono.

#### **Fase 4: Persistencia de Datos**

Para que el historial no se pierda, lo guardaremos en disco.

1.  **Guardar estado:** Crear una función que escriba la estructura de datos completa (el diccionario con el estado y el historial de todos los teléfonos) en el fichero `estado_telefonos.json`.
2.  **Integrar el guardado:** Esta función se llamará cada vez que se detecte y registre un cambio de estado en la Fase 3, asegurando que el fichero esté siempre actualizado.

#### **Fase 5: Bucle Principal y Orquestación**

Finalmente, se unirá todo en un proceso continuo.

1.  **Crear el bucle principal:** Implementar un bucle infinito (`while True`) que orqueste la ejecución de todas las fases en orden:
    *   Llamar a `escanear_red()` para obtener los teléfonos activos (Fase 2).
    *   Llamar a la lógica de comparación para detectar y registrar cambios (Fase 3).
    *   (La Fase 4 se ejecuta automáticamente desde la 3).
2.  **Añadir temporizador:** Al final de cada iteración del bucle, se introducirá una pausa de 60 segundos (`time.sleep(60)`) para cumplir con el requisito de ejecutar el escaneo cada minuto.
3.  **Logging:** Se añadirá un sistema de logs simple para mostrar en consola los eventos importantes, como los cambios de estado detectados y posibles errores.

---

Si estás de acuerdo con esta propuesta, puedo empezar a desarrollar la **Fase 1**.
