import traci
import traci.constants as tc

# Iniciar conexión con SUMO
traci.start(['sumo', '-c', 'osm.sumocfg'])

# Diccionario para contar los vehículos por TAZ de destino
destination_counts = {}

# Lista de TAZs de destino (actualiza según tus necesidades)
taz_destinations = ["Centro_Historico", "Ejido_Este", "Ejido_Oeste", "Coliseo_Mayor", 
                    "San_Sebastian", "Cristo_Rey", "Bellavista", "Aeropuerto", 
                    "Cementerio", "Paraíso", "Santa_Anita"]

for taz in taz_destinations:
    destination_counts[taz] = 0

# Ejecutar la simulación
step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    
    # Obtener lista de vehículos que llegaron a su destino en este paso
    arrived_vehicles = traci.simulation.getArrivedIDList()
    
    for vehicle_id in arrived_vehicles:
        try:
            # Verificar si el vehículo tiene el parámetro 'toTaz'
            vehicle_params = traci.vehicle.getParameterIDList(vehicle_id)
            if "toTaz" in vehicle_params:
                # Obtener el TAZ de destino del vehículo
                vehicle_taz_dest = traci.vehicle.getParameter(vehicle_id, "toTaz")
                
                if vehicle_taz_dest in destination_counts:
                    destination_counts[vehicle_taz_dest] += 1
            else:
                print(f"El vehículo '{vehicle_id}' no tiene el parámetro 'toTaz'.")
        except traci.TraCIException as e:
            print(f"Error al obtener el parámetro 'toTaz' para el vehículo '{vehicle_id}': {e}")

    step += 1

# Finalizar conexión con SUMO
traci.close()

# Mostrar los resultados
for taz, count in destination_counts.items():
    print(f'Destino: {taz}, Vehículos: {count}')
