#!/bin/bash

# Verificar si se han proporcionado el día y el número adicional como argumentos
if [ $# -ne 2 ]; then
  echo "Uso: $0 <día> <factor>"
  exit 1
fi

# Asignar los argumentos a variables
day_of_week=$1
additional_number=$2

# Buscar archivos que contengan la palabra del día especificado y tengan la extensión .xlsx
for file in ${day_of_week}*.xlsx; do
  # Verificar si el archivo existe
  if [ -e "$file" ]; then
    # Extraer las horas de inicio y fin del nombre del archivo
    base_name=$(basename "$file" .xlsx)
    IFS='_' read -r day start_time end_time <<< "${base_name}"
    
    # Crear el nombre del archivo de salida con extensión .od
    output_file="${base_name}.od"
    mkdir ${base_name}
    
    # Ejecutar el comando de Python con los parámetros correspondientes
    echo "Creando archivos OD"
    python3 matriz.py "$file" "${base_name}/$output_file" "$start_time" "$end_time" "$additional_number"
    echo "Creando archivo de rutas"
    marouter -n "network.net.xml" -m "${base_name}/$output_file" --max-alternatives 1 --vtype "car" --additional-files "districts.taz.xml" --output-file "${base_name}/marouter.rou.xml"
    echo "Generando archivo de viajes individuales"
    od2trips --taz-files "districts.taz.xml" -d "${base_name}/$output_file" --output-file "${base_name}/trips.trip.xml"
    echo "Generando archivo duarouter"
    duarouter -n "network.net.xml" --randomize-flows true --route-files "${base_name}/trips.trip.xml" --additional-files vtypes.add.xml --output-file "${base_name}/duarouter.rou.xml"
    echo "Archivo procesado"
    
    mkdir "${base_name}/reportes_d"
    mkdir "${base_name}/reportes_m"
    
    python3 modificar_vtype.py "${base_name}/marouter.rou.xml" "${base_name}/marouter_m.rou.xml" "${base_name}/reportes_m/figuras"
    python3 modificar_vtype.py "${base_name}/duarouter.rou.xml" "${base_name}/duarouter_m.rou.xml" "${base_name}/reportes_d/figuras"
    
    python3 generate_sumocfg.py "marouter_m.rou.xml" "districts.taz.xml,taz.poly.xml,vtypes.add.xml,edgeData_m.xml" "${base_name}/osm_m.sumocfg" "m" "${base_name}/edgeData_m.xml" "reportes_m/edgeData.xml"
    python3 generate_sumocfg.py "duarouter_m.rou.xml" "districts.taz.xml,taz.poly.xml,vtypes.add.xml,edgeData_d.xml" "${base_name}/osm_d.sumocfg" "d" "${base_name}/edgeData_d.xml" "reportes_d/edgeData.xml"
    cp districts.taz.xml ${base_name}/districts.taz.xml
    cp taz.poly.xml ${base_name}/taz.poly.xml
    cp vtypes.add.xml ${base_name}/vtypes.add.xml
    cp network.net.xml ${base_name}/network.net.xml
  fi
done

# Obtiene el directorio donde se encuentra el archivo .sh
directorio_raiz="$(dirname "$(readlink -f "$0")")"

# Recorre todas las carpetas dentro del directorio raíz
for carpeta in "$directorio_raiz"/*/; do
    # Verifica que sea un directorio
    if [ -d "$carpeta" ]; then
        echo "Procesando carpeta: $carpeta"
        nombre_carpeta=$(basename "$carpeta")
        echo "Procesando carpeta: $nombre_carpeta"
	sumo -c $nombre_carpeta/osm_d.sumocfg
	python3 edges.py $nombre_carpeta/reportes_d/vehroute.xml $nombre_carpeta/$nombre_carpeta.od $nombre_carpeta/reportes_d/figuras
	echo "simulacion sumo -c duaroute realizada"
	sumo -c $nombre_carpeta/osm_m.sumocfg
	python3 edges.py $nombre_carpeta/reportes_m/vehroute.xml $nombre_carpeta/$nombre_carpeta.od $nombre_carpeta/reportes_m/figuras
	echo "simulacion sumo -c maroute realizada"
	
	python3 plot_net_dump.py -v -n network.net.xml  --xticks 0,22001,2000,16 --yticks 0,13000,1000,16  --measures CO2_abs,CO2_abs --xlabel [m] --ylabel [m]  --default-width 1 -i $nombre_carpeta/reportes_d/edgeData.xml,$nombre_carpeta/reportes_d/edgeData.xml  --xlim 0,22000 --ylim 0,8000 --default-width .5 --default-color "#606060" --colormap "#0:#00c000,.25:#408040,.5:#ffff00,.75:#804040,1:#c00000" -o $nombre_carpeta/reportes_d/figuras/co2.pdf
	python3 plot_net_dump.py -v -n network.net.xml  --xticks 0,22001,2000,16 --yticks 0,13000,1000,16  --measures CO2_abs,CO2_abs --xlabel [m] --ylabel [m]  --default-width 1 -i $nombre_carpeta/reportes_m/edgeData.xml,$nombre_carpeta/reportes_m/edgeData.xml  --xlim 0,22000 --ylim 0,8000 --default-width .5 --default-color "#606060" --colormap "#0:#00c000,.25:#408040,.5:#ffff00,.75:#804040,1:#c00000" -o $nombre_carpeta/reportes_m/figuras/co2.pdf

    fi
done
