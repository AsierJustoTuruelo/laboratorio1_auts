import requests
import re
import csv
import time

# EJERCICIO 6
# EXTRACCIÓN DE EMAILS DE UNA PÁGINA WEB
# En este ejercicio, se extraerán las direcciones de email de una página web y se guardarán en un archivo CSV.
# Se proporciona una URL de ejemplo, pero se puede usar cualquier otra URL.

def descargar_html(url):
    """Descargar página web con técnicas para evitar bloqueo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'es-ES,es;q=0.9'
    }
    
    try:
        # Agregar retardo para evitar rate limiting
        time.sleep(2)
        
        # Deshabilitar verificación SSL (no recomendado para producción)
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        # Guardar página en archivo HTML (opcional si no se comenta y ya está :) )
        with open('emails.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        return response.text
    
    except requests.RequestException as e:
        print(f"Error al descargar la página: {e}")
        return None


def extraer_mails(html_content):
    """Extraer direcciones de email usando regex"""
    regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(regex_mail, html_content, re.IGNORECASE)
    return emails

def limpiar_mails(emails):
    """Limpiar y eliminar emails duplicados"""
    # Convertir a minúsculas y eliminar duplicados
    mails_unicos = list(set(email.lower() for email in emails))
    
    # Validar formato de email
    def is_valid_email(email):
        regex_mail = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(regex_mail, email, re.IGNORECASE) is not None
    
    mails_limpiados = [email for email in mails_unicos if is_valid_email(email)]
    return mails_limpiados

def guardar_csv(emails, filename='emails.csv'):
    """Guardar emails en archivo CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv = csv.writer(csvfile)
        csv.writerow(['Email'])  # Encabezado
        for email in emails:
            csv.writerow([email])
    
    print(f"Total de emails extraídos: {len(emails)}")

def main():
    # Aunque se puede usar cualquier URL, se recomienda usar la URL proporcionada
    url = "https://www.fi.upm.es/?id=estructura/departamentos"
    
    # Descargar página
    html_content = descargar_html(url)
    
    if html_content:
        # Extraer emails
        mails_brutos = extraer_mails(html_content)
        
        # Limpiar emails
        mails_limpiados = limpiar_mails(mails_brutos)
        
        # Guardar en CSV
        guardar_csv(mails_limpiados)

if __name__ == "__main__":
    main()
