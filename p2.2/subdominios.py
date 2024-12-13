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

# Resolver los dominios a IPs usando dig
print("Resolviendo dominios a direcciones IP...")
ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

with open("ips_con_mascara.txt", "w") as output:
    for dominio in filtrados_unicos:
        try:
            # Resolver el dominio a IP usando dig
            result = subprocess.run(f"dig +short {dominio}", shell=True, capture_output=True, text=True)
            ips = ip_pattern.findall(result.stdout)

            if ips:
                for ip in ips:
                    # Consultar detalles de la IP con whois para obtener la máscara
                    whois_result = subprocess.run(f"whois {ip}", shell=True, capture_output=True, text=True)
                    whois_data = whois_result.stdout

                    # Buscar el rango CIDR en la salida de whois
                    cidr_match = re.search(r'CIDR:\s*([\d./]+)', whois_data)
                    if cidr_match:
                        cidr = cidr_match.group(1)
                    else:
                        # Alternativa para máscaras dentro del bloque inetnum
                        inetnum_match = re.search(r'inetnum:\s*([\d./]+)', whois_data)
                        cidr = inetnum_match.group(1) if inetnum_match else "Máscara no encontrada"

                    # Guardar el resultado
                    output.write(f"{dominio} -> {ip} -> {cidr}\n")
                    print(f"{dominio} -> {ip} -> {cidr}")
            else:
                output.write(f"{dominio} -> No se resolvió\n")
                print(f"{dominio} -> No se resolvió")
        except Exception as e:
            print(f"Error resolviendo {dominio}: {e}")

print("Proceso completado. Resultados guardados en 'ips_con_mascara.txt'")
