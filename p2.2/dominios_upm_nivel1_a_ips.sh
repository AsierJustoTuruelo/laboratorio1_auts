#!/bin/bash
# Archivo de entrada con los dominios
input_file="dominios_upm_nivel1.txt"
# Archivo de salida para guardar los resultados
output_file="ips_resultados_nivel1.txt"

# Limpiar el archivo de salida si ya existe
> "$output_file"

# Leer cada dominio y obtener su IP
while IFS= read -r dominio; do
    echo "Resolviendo $dominio..."
    ip=$(dig +short "$dominio" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}')
    if [ -n "$ip" ]; then
        echo "$dominio -> $ip" >> "$output_file"
    else
        echo "$dominio -> No se pudo resolver" >> "$output_file"
    fi
done < "$input_file"

echo "Resolución completa. Resultados guardados en $output_file"
