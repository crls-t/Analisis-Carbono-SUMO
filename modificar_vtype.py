import xml.etree.ElementTree as ET
import random
import matplotlib.pyplot as plt
import sys
import os

# Definir los porcentajes para cada tipo de vehículo
percentages = {
    "auto_1": 0.20,
    "auto_2": 0.05,
    "auto_3": 0.05,
    "auto_4": 0.15,
    "auto_5": 0.07,
    "auto_6": 0.08,
    "auto_7": 0.20,
    "auto_8": 0.02,
    "auto_9": 0.08,
    "auto_10": 0.10
}


# Función para crear la carpeta si no existe
def crear_carpeta_si_no_existe(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

# Función para leer el archivo XML y modificar el tipo de vehículo
def modify_vehicle_types(input_xml, output_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    partes = input_xml.split('/')
    nombre_archivo = partes[-1]
    # Si quieres eliminar la extensión .xml, puedes hacer esto
    nombre = nombre_archivo.split('.')[0]
    print("El nombre del archivo es:", nombre)	    

    
    #vehicles = root.findall('flow')
    if(nombre=='duarouter'):
      #print(nombre)
      vehicles = root.findall('vehicle')
    if(nombre=='marouter'):
      vehicles = root.findall('flow')
      print("Ingreso a al funcion",nombre)
      	
    total_vehicles = len(vehicles)
    print(f'Total vehicles found: {total_vehicles}')

    # Generar una lista de tipos de vehículos basada en los porcentajes
    vehicle_types = []
    for vehicle_type, percentage in percentages.items():
        count = int(percentage * total_vehicles)
        vehicle_types.extend([vehicle_type] * count)

    # Asegurarnos de que la lista de tipos tenga la longitud correcta
    while len(vehicle_types) < total_vehicles:
        vehicle_types.append("auto_1")  # Por si acaso hay algún remanente

    # Asignar aleatoriamente los tipos de vehículo a cada <vehicle>
    random.shuffle(vehicle_types)
    for i, vehicle in enumerate(vehicles):
        new_type = vehicle_types[i]
        vehicle.set('type', new_type)

    # Guardar el archivo modificado
    tree.write(output_xml)

    print(f'Modification complete. Modified XML saved as "{output_xml}".')

    return vehicle_types, total_vehicles

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Uso: python script.py <archivo_entrada_xml> <archivo_salida_xml>")
        sys.exit(1)

    input_xml = sys.argv[1]
    output_xml = sys.argv[2]
    carpeta=sys.argv[3]
    assigned_types, total_vehicles = modify_vehicle_types(input_xml, output_xml)
    
    crear_carpeta_si_no_existe(carpeta)

    # Contar la cantidad de cada tipo de vehículo asignado
    counts = {t: assigned_types.count(t) for t in percentages.keys()}

    # Preparar datos para la gráfica de barras
    types = list(percentages.keys())
    values = [counts[t] for t in types]

    # Crear la gráfica de barras
    plt.figure(figsize=(10, 6))
    bars = plt.bar(types, values, color='skyblue')
    
    # Añadir leyendas con los valores numéricos a cada barra
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), value,
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xlabel('Tipo de Vehículo')
    plt.ylabel('Cantidad Asignada')
    plt.title(f'Distribución de Tipos de Vehículos Asignados {total_vehicles}')
    plt.grid(True)
    plt.tight_layout()
    # Guardar la figura en la carpeta especificada
    ruta_figura = os.path.join(carpeta, f'Distribución de Tipos de Vehículos Asignados {total_vehicles}.png')
    plt.savefig(ruta_figura)
    plt.close()
