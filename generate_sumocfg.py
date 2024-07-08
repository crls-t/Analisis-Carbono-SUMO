import sys

def generate_edgeData(edge,output_file2):
	config_content= f"""<?xml version="1.0" encoding="UTF-8"?>

<additional>
    <edgeData id="1" period="3600" type="emissions" file="{edge}" excludeEmpty="true" />
</additional>
"""
	with open(output_file2, 'w') as file:
		file.write(config_content)

def generate_sumocfg(route_file, additional_files, output_file,out):
    config_content = f"""<?xml version="1.0" encoding="UTF-8"?>

<configuration>
    <input>
        <net-file value="network.net.xml"/>
        <route-files value="{route_file}"/>
        <additional-files value="{additional_files}"/>
    </input>
    
    <output>
        <tripinfo-output value="reportes_{out}/tripinfo.xml"/>
        <summary-output value="reportes_{out}/summary.xml"/>
        <vehroute-output  value= "reportes_{out}/vehroute.xml"/>
    </output>

    <time>
        <end value="3600"/>
    </time>
</configuration>
"""

    with open(output_file, 'w') as file:
        file.write(config_content)

if __name__ == '__main__':
    if len(sys.argv) != 7:
        print("Uso: python generate_sumocfg.py <ruta_del_archivo_de_rutas> <archivos_adicionales> <archivo_de_salida>")
        sys.exit(1)

    route_file = sys.argv[1]
    additional_files = sys.argv[2]
    output_file = sys.argv[3]
    out = sys.argv[4]
    output_file2= sys.argv[5]
    edge=sys.argv[6]
    

    generate_sumocfg(route_file, additional_files, output_file,out)
    
    generate_edgeData(edge,output_file2)
    print(f"Archivo {output_file} generado correctamente.")

