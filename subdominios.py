import re
import subprocess

# Ejecutar assetfinder y guardar resultados en dominios.txt
print("Ejecutando assetfinder...")
subprocess.run("assetfinder upm.es > dominios.txt", shell=True)

# Leer los dominios del archivo
with open("dominios.txt", "r") as file:
    dominios = file.readlines()

# Filtrar dominios que sigan el patrón subdominio.upm.es
patron = re.compile(r'^[a-zA-Z0-9-]+\.upm\.es$')
filtrados = [dominio.strip() for dominio in dominios if patron.match(dominio.strip())]

# Guardar los dominios filtrados
with open("filtrados.txt", "w") as output:
    for dominio in filtrados:
        output.write(dominio + "\n")

# Realizar un escaneo de Nmap en cada dominio filtrado
print("Ejecutando nmap...")
with open("ips_con_mascara.txt", "w") as output:
    for dominio in filtrados:
        result = subprocess.run(f"nmap -sn {dominio}", shell=True, capture_output=True, text=True)
        output.write(result.stdout)
        print(result.stdout)

print("Proceso completado. Resultados guardados en 'ips_con_mascara.txt'")
