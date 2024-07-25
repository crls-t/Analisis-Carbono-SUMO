# Proyecto de Simulación de Tráfico

Este repositorio contiene scripts y configuraciones para la simulación de tráfico utilizando SUMO (Simulation of Urban MObility). A continuación se describe cada uno de los componentes y scripts incluidos en este repositorio.

## datos.sh

Este script bash permite ejecutar una serie de instrucciones para procesar archivos de simulación de tráfico y ejecutar simulaciones en SUMO. Los pasos principales que realiza son:

1. Verifica que se han proporcionado dos argumentos: el día y un número adicional denominado como factor.
2. Busca archivos con la extensión `.xlsx` que contengan la palabra del día especificado.
3. Extrae las horas de inicio y fin del nombre del archivo.
4. Crea un archivo de salida en formato VISUM (OD).
5. Ejecuta varios scripts en Python y comandos de SUMO para procesar los datos y realizar simulaciones.

### Parámetros de Entrada:
- **Día:** El día de la semana especificado.
- **Factor:** Un valor numérico adicional utilizado en los cálculos.

Su ejecución viene dada del siguiente modo:
```bash
./datos.sh <día> <factor>

## Archivos Python

### matriz.py

Este script toma los datos de un archivo Excel en el cual la primera columna y fila contienen nombres (TAZ) y los valores entre las intersecciones representan la cantidad de vehículos circulando entre esos TAZ específicos. Los parámetros de entrada son:
1. Nombre del archivo Excel.
2. Nombre del archivo de salida en formato VISUM (OD).
3. Tiempo de inicio.
4. Tiempo de final.
5. Un número adicional (factor).

Su ejecución viene dada del siguiente modo:
```bash
python3 matriz.py <archivo_excel.xlxs> <archivo_salida.od> <tiempo_inicio_simulacion> <tiempo_final_simulacion> <factor>


### modificar_vtype.py

Este script modifica el archivo de rutas generado para incluir diferentes tipos de vehículos basados en porcentajes predefinidos. Los parámetros de entrada son:
1. El archivo original con un solo tipo de vehículo.
2. El nombre del archivo de salida modificado.
3. La carpeta de destino para los gráficos.

Su ejecución viene dada del siguiente modo:
```bash
python3 modificar_vtype.py <archivo_marouter_original.rou.xml> <archivo_salida_marouter_modificado.rou.xml> <carpeta_salida_figuras_resultados_cambios>

### generate_sumocfg.py

Este script genera archivos de configuración para SUMO, utilizando varios archivos de entrada y parámetros. Los parámetros de entrada son:
1. El archivo de rutas.
2. Archivos adicionales necesarios para la simulación.
3. El nombre del archivo de salida.
4. El tipo de formato (duarouter o marouter).
5. Archivos de reporte.

Su ejecución viene dada del siguiente modo:
```bash
python3 generate_sumocfg.py <archivo_marouter.rou.xml> <archivos_adicionales> <archivo_sumocfg> <archivo_entrada_edgeData.xml> <archivo_salida_edgeData.xml> <tiempo_inicio_simulacion> <tiempo_final_simulacion>

### edges.py

Este script genera gráficos basados en los datos obtenidos de la simulación. Analiza los archivos generados por la simulación para contar la cantidad de vehículos entre diferentes TAZ y genera gráficos que se guardan en una carpeta específica. Los parámetros de entrada son:
1. Los archivos a analizar.
2. La carpeta de destino para los gráficos.

Su ejecución viene dada del siguiente modo:
```bash
python3 edges.py <archivo_vehroute.xml> <archivo_matriz.od> <archivo_summary.xml> <carpeta_salida_de_resutados_graficos>

### plot_net_dump.py

Este script genera un mapa de calor basado en las emisiones de CO2 generadas por SUMO. Utiliza los datos de la simulación y genera gráficos de emisiones en función del mapa utilizado para las simulaciones de tráfico. Los parámetros de entrada son:
1. Archivos a analizar.
2. Archivos de configuración de la red.
3. Otros parámetros de visualización.
