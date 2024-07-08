import os
import argparse
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
import xml.etree.ElementTree as ET

# Función para crear la carpeta si no existe
def crear_carpeta_si_no_existe(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

# Función para leer el archivo XML y extraer la información de los vehículos
def leer_datos_xml(archivo_xml):
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        datos_vehiculos = []
        for vehicle in root.findall('vehicle'):
            from_taz = vehicle.get('fromTaz')
            to_taz = vehicle.get('toTaz')
            datos_vehiculos.append((from_taz, to_taz))
        return datos_vehiculos
    except ET.ParseError as e:
        print(f"Error al parsear el archivo XML: {e}")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo XML: {e}")
        return []

# Función para leer el archivo de datos adicionales
def leer_datos_adicionales(archivo_texto):
    try:
        datos_adicionales = pd.read_csv(archivo_texto, sep='\s+', skiprows=8, header=None)
        datos_adicionales.columns = ['from_taz', 'to_taz', 'count']
        return datos_adicionales
    except pd.errors.ParserError as e:
        print(f"Error al leer el archivo de datos adicionales: {e}")
        return pd.DataFrame(columns=['from_taz', 'to_taz', 'count'])

# Función para contar los pares de TAZ origen y destino
def contar_taz(datos_vehiculos):
    conteo_taz = defaultdict(int)
    for from_taz, to_taz in datos_vehiculos:
        conteo_taz[(from_taz, to_taz)] += 1
    return conteo_taz

# Función para graficar los resultados
def graficar_conteo_taz(conteo_taz, datos_adicionales, carpeta):
    taz_origen_destino = defaultdict(list)
    for (from_taz, to_taz), count in conteo_taz.items():
        taz_origen_destino[from_taz].append((to_taz, count))
    
    for origen, destinos in taz_origen_destino.items():
        destinos_taz, counts = zip(*destinos)
        
        plt.figure(figsize=(12, 8))
        
        # Gráfico de dispersión
        plt.scatter(destinos_taz, counts, color='red', alpha=0.7, label='Datos simulacion', s=100)
        for destino_taz, count in zip(destinos_taz, counts):
            plt.text(destino_taz, count, str(count), fontsize=9, ha='left', color='red')
        
        # Filtrar datos adicionales para el TAZ origen actual
        datos_adicionales_origen = datos_adicionales[datos_adicionales['from_taz'] == origen]
        
        if not datos_adicionales_origen.empty:
            destinos_adicionales = datos_adicionales_origen['to_taz'].tolist()
            counts_adicionales = datos_adicionales_origen['count'].tolist()
            
            # Gráfico de barras
            bar = plt.bar(destinos_adicionales, counts_adicionales, color='black', alpha=0.7, label='Matriz OD', width=0.2)
            for destino_taz, count in zip(destinos_adicionales, counts_adicionales):
                plt.text(destino_taz, count, str(count), fontsize=9, ha='right', color='black')
        
        plt.title(f'Conteo de vehículos desde TAZ Origen: {origen}')
        plt.xlabel('TAZ Destino')
        plt.ylabel('Conteo de Vehículos')
        plt.xticks(rotation=45)
        
        # Añadir la leyenda
        plt.legend()
        
        plt.tight_layout()
        # Guardar la figura en la carpeta especificada
        ruta_figura = os.path.join(carpeta, f'conteo_{origen}.png')
        plt.savefig(ruta_figura)
        plt.close()

    # Contar el número total de vehículos en el archivo XML
    total_vehiculos_xml = sum(count for _, count in conteo_taz.items())
    print(f"Total de vehículos en la simulacion: {total_vehiculos_xml}")

    # Contar el número total de vehículos en el archivo adicional
    total_vehiculos_adicional = datos_adicionales['count'].sum()
    print(f"Total de vehículos en la matriz OD: {total_vehiculos_adicional}")

# Función principal
def main():
    parser = argparse.ArgumentParser(description="Procesar archivos XML y datos adicionales para graficar conteos de vehículos.")
    parser.add_argument("archivo_xml", type=str, help="Ruta al archivo XML.")
    parser.add_argument("archivo_texto", type=str, help="Ruta al archivo de datos adicionales.")
    parser.add_argument("carpeta_figuras", type=str, help="Carpeta donde se guardarán las figuras.")
    
    args = parser.parse_args()
    
    # Crear la carpeta si no existe
    crear_carpeta_si_no_existe(args.carpeta_figuras)
    
    # Leer y procesar los datos del archivo XML y del archivo de datos adicionales
    datos_vehiculos = leer_datos_xml(args.archivo_xml)
    conteo_taz = contar_taz(datos_vehiculos)
    datos_adicionales = leer_datos_adicionales(args.archivo_texto)
    
    # Graficar los resultados
    graficar_conteo_taz(conteo_taz, datos_adicionales, args.carpeta_figuras)

if __name__ == "__main__":
    main()

