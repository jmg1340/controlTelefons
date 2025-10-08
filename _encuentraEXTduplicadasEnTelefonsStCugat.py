import csv
from collections import defaultdict

def encontrar_duplicados_csv(filename='TelefonsStCugat.csv'):
    """
    Encuentra y muestra las extensiones duplicadas en un fichero CSV,
    indicando en qué líneas aparecen.

    Args:
        filename (str): El nombre del fichero CSV a analizar.
    """
    lineas_por_extension = defaultdict(list)
    try:
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for i, row in enumerate(csv_reader, 2): # Empezar en 2 para contar la cabecera
                extension = row.get('EXT')
                if extension:
                    lineas_por_extension[extension].append(i)
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero {filename}")
        return

    print(f"--- Buscando extensiones duplicadas en '{filename}' ---")
    duplicados_encontrados = False
    for extension, lineas in lineas_por_extension.items():
        if len(lineas) > 1:
            duplicados_encontrados = True
            print(f"  - Extensión duplicada: '{extension}' encontrada en las líneas: {lineas}")

    if not duplicados_encontrados:
        print("No se encontraron extensiones duplicadas.")

if __name__ == '__main__':
    encontrar_duplicados_csv()
