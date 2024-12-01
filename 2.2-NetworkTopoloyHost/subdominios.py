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

# Eliminar duplicados utilizando un conjunto (set)
filtrados_unicos = list(set(filtrados))

# Guardar los dominios filtrados sin duplicados
with open("filtrados.txt", "w") as output:
    for dominio in filtrados_unicos:
        output.write(dominio + "\n")

# Expresión regular para capturar direcciones IP
ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Realizar un escaneo de Nmap en cada dominio filtrado
print("Ejecutando nmap...")
with open("ips_con_mascara.txt", "w") as output:
    for dominio in filtrados_unicos:
        result = subprocess.run(f"nmap -sn {dominio}", shell=True, capture_output=True, text=True)
        ips = ip_pattern.findall(result.stdout)
        for ip in ips:
            output.write(f"{ip}\n")
            print(ip)

print("Proceso completado. Resultados guardados en 'ips_con_mascara.txt'")
