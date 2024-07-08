import xml.etree.ElementTree as ET

# Rutas a los archivos XML
trips_file_path = 'saturno_7.00_8.00/trips.trip.xml'
tripinfo_file_path = 'reportes/tripinfo.xml'

# Paso 1: Crear un diccionario para mapear IDs de viajes a TAZ de destino
trip_to_dest = {}

# Parsear el archivo trips.trip.xml
tree_trips = ET.parse(trips_file_path)
root_trips = tree_trips.getroot()

for trip in root_trips.findall('trip'):
    trip_id = trip.get('id')
    dest_taz = trip.get('to')
    trip_to_dest[trip_id] = dest_taz

# Paso 2: Contar los vehículos que han llegado a cada TAZ de destino
destination_counts = {}

# Parsear el archivo tripinfo.xml
tree_tripinfo = ET.parse(tripinfo_file_path)
root_tripinfo = tree_tripinfo.getroot()

for tripinfo in root_tripinfo.findall('tripinfo'):
    trip_id = tripinfo.get('id')
    if trip_id in trip_to_dest:
        dest_taz = trip_to_dest[trip_id]
        if dest_taz in destination_counts:
            destination_counts[dest_taz] += 1
        else:
            destination_counts[dest_taz] = 1

# Mostrar los resultados
for dest, count in destination_counts.items():
    print(f'Destino: {dest}, Vehículos: {count}')

