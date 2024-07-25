import xml.etree.ElementTree as ET
import random
import matplotlib.pyplot as plt
import sys
import os

# Definir los porcentajes para cada tipo de vehículo
percentages = {
    "Chevrolet_-1000cc":0.0162,
    "Chevrolet_1000-1600cc":0.0766,
    "Chevrolet_1600-2000cc":0.2474,
    "Chevrolet_2000cc+":0.1117,
    "Hyundai_-1000cc":0.0025,
    "Hyundai_1000-1600cc":0.0100,
    "Hyundai_1600-2000cc":0.0693,
    "Hyundai_2000cc+":0.0577,
    "Toyota_-1000cc":0.0048,
    "Toyota_1000-1600cc":0.0141,
    "Toyota_1600-2000cc":0.0514,
    "Toyota_2000cc+":0.0199,
    "Suzuki_-1000cc":0.0032,
    "Suzuki_1000-1600cc":0.0180,
    "Suzuki_1600-2000cc":0.0230,
    "Suzuki_2000cc+":0.0257,
    "Mazda_-1000cc":0.0027,
    "Mazda_1000-1600cc":0.0063,
    "Mazda_1600-2000cc":0.0310,
    "Mazda_2000cc+":0.0160,
    "Nissan_-1000cc":0.0052,
    "Nissan_1000-1600cc":0.0114,
    "Nissan_1600-2000cc":0.0200,
    "Nissan_2000cc+":0.0163,
    "Kia_-1000cc":0.0005,
    "Kia_1000-1600cc":0.0010,
    "Kia_1600-2000cc":0.0174,
    "Kia_2000cc+":0.0273,
    "Mitsubishi_-1000cc":0.0019,
    "Mitsubishi_1000-1600cc":0.0101,
    "Mitsubishi_1600-2000cc":0.0160,
    "Mitsubishi_2000cc+":0.0050,
    "Ford_-1000cc":0.0008,
    "Ford_1000-1600cc":0.0049,
    "Ford_1600-2000cc":0.0149,
    "Ford_2000cc+":0.0111,
    "Volkswagen_-1000cc":0.0009,
    "Volkswagen_1000-1600cc":0.0028,
    "Volkswagen_1600-2000cc":0.0085,
    "Volkswagen_2000cc+":0.0024,
    "Renault_-1000cc":0.0001,
    "Renault_1000-1600cc":0.0003,
    "Renault_1600-2000cc":0.0073,
    "Renault_2000cc+":0.0043
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
      	
#    print("El valor de vehiculo es",vehicles)	
#    vehicles = root.findall('vehicle')
    total_vehicles = len(vehicles)
    print(f'Total vehicles found: {total_vehicles}')

    # Generar una lista de tipos de vehículos basada en los porcentajes
    vehicle_types = []
    for vehicle_type, percentage in percentages.items():
        count = int(percentage * total_vehicles)
        vehicle_types.extend([vehicle_type] * count)

    # Asegurarnos de que la lista de tipos tenga la longitud correcta
    while len(vehicle_types) < total_vehicles:
        vehicle_types.append("Chevrolet_-1000cc")  # Por si acaso hay algún remanente

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
    plt.xticks(rotation=90)
    plt.title(f'Distribución de Tipos de Vehículos Asignados {total_vehicles}')
    plt.grid(True)
    plt.tight_layout()
    # Guardar la figura en la carpeta especificada
    ruta_figura = os.path.join(carpeta, f'Distribución de Tipos de Vehículos Asignados {total_vehicles}.png')
    plt.savefig(ruta_figura)
    plt.close()

    # Mostrar la gráfica
    #plt.show()

