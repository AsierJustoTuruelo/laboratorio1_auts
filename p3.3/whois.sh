#!/bin/bash

# Lista de dominios para consultar
DOMINIOS=("rock.com.ar" "gob.es" "telefonica.com" "ejemplo.com")

# Archivo para guardar resultados
OUTPUT="whois_results.txt"
echo "Resultados de Whois:" > "$OUTPUT"

# Realizar la consulta para cada dominio
for DOMINIO in "${DOMINIOS[@]}"; do
    echo "Consultando $DOMINIO..."
    echo "----------------------------------------" >> "$OUTPUT"
    echo "Dominio: $DOMINIO" >> "$OUTPUT"
    whois "$DOMINIO" >> "$OUTPUT" 2>/dev/null
    echo "----------------------------------------" >> "$OUTPUT"
done

echo "Consultas completadas. Revisa el archivo $OUTPUT"
