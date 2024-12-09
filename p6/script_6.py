import requests
import re
import csv
import time
from bs4 import BeautifulSoup
import os

def descargar_html(url):
    """Descargar página web con técnicas para evitar bloqueo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'es-ES,es;q=0.9'
    }
    
    try:
        # Agregar retardo para evitar rate limiting
        time.sleep(4)
        
        # Deshabilitar verificación SSL (no recomendado para producción)
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        # Guardar página en archivo HTML (opcional)
        with open('emails.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        return response.text
    
    except requests.RequestException as e:
        print(f"Error al descargar la página: {e}")
        return None

def extraer_mails_con_contexto(html_content):
    """Extraer direcciones de email con su contexto"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Regex para detectar emails
    regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    email_info = []
    
    # Buscar emails en todo el texto
    for texto in soup.find_all(text=re.compile(regex_mail)):
        # Encontrar todos los emails en este texto
        emails = re.findall(regex_mail, texto, re.IGNORECASE)
        
        for email in emails:
            # Intentar extraer nombre y contexto
            nombre = extraer_nombre(texto)
            rol = extraer_rol(texto)
            
            email_info.append({
                'email': email.lower(),
                'nombre': nombre,
                'rol': rol
            })
    
    return email_info

def extraer_nombre(texto):
    """Intentar extraer un nombre de un texto"""
    # Patrón para nombres propios (dos palabras, primera letra mayúscula)
    nombre_pattern = r'\b([A-Z][a-z]+\s[A-Z][a-z]+)\b'
    
    # Buscar antes y después del email
    nombres = re.findall(nombre_pattern, texto)
    
    return nombres[0] if nombres else None

def extraer_rol(texto):
    """Intentar extraer un rol o cargo de un texto"""
    # Patrones de roles ampliados
    roles_patterns = [
        # Roles Académicos
        r'(Director[a]?\s*(?:de\s*[A-Za-z]+)?)',
        r'(Profesor[a]?\s*(?:Titular|Asociad[oa]|Adjunt[oa])?)',
        r'(Investigador[a]?\s*(?:Principal|Titular|Asociad[oa])?)',
        r'(Catedrático[a]?)',
        r'(Decano[a]?)',
        r'(Vicedecano[a]?)',
        
        # Departamentos y Áreas
        r'(Departamento\s*de\s*[A-Za-z]+)',
        r'(Área\s*de\s*[A-Za-z]+)',
        r'(Grupo\s*de\s*Investigación\s*de\s*[A-Za-z]+)',
        
        # Roles Administrativos
        r'(Secretario[a]?\s*(?:Académico[a]?)?)',
        r'(Coordinador[a]?\s*(?:de\s*[A-Za-z]+)?)',
        r'(Administrador[a]?)',
        r'(Gestor[a]?\s*(?:de\s*[A-Za-z]+)?)',
        
        # Roles de Investigación
        r'(Becario[a]?\s*de\s*Investigación)',
        r'(Doctorando[a]?)',
        r'(Postdoctoral\s*[A-Za-z]*)',
        
        # Roles Técnicos
        r'(Técnico[a]?\s*(?:de\s*[A-Za-z]+)?)',
        r'(Laboratorio\s*[A-Za-z]*)',
        
        # Roles Generales
        r'(Miembro\s*del\s*[A-Za-z]+)',
        r'(Personal\s*[A-Za-z]+)'
    ]
    
    for pattern in roles_patterns:
        roles = re.findall(pattern, texto, re.IGNORECASE)
        if roles:
            return roles[0]
    
    return None

def limpiar_mails(email_info):
    """Limpiar y eliminar emails duplicados"""
    # Validar formato de email
    def is_valid_email(email):
        regex_mail = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(regex_mail, email, re.IGNORECASE) is not None
    
    # Filtrar emails válidos y eliminar duplicados
    mails_unicos = {}
    for info in email_info:
        email = info['email']
        if is_valid_email(email) and email not in mails_unicos:
            mails_unicos[email] = info
    
    return list(mails_unicos.values())

def guardar_csv(email_info, filename='emails_p6.csv'):
    """Guardar emails con información adicional en archivo CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Definir encabezados
        campos = ['Email', 'Nombre', 'Rol']
        csv_w = csv.DictWriter(csvfile, fieldnames=campos)
        
        # Escribir encabezados
        csv_w.writeheader()
        
        # Escribir información de emails
        for info in email_info:
            csv_w.writerow({
                'Email': info['email'],
                'Nombre': info['nombre'] or 'N/A',
                'Rol': info['rol'] or 'N/A'
            })
    
    print(f"Total de emails extraídos: {len(email_info)}")

def main():
    # Aunque se puede usar cualquier URL, se recomienda usar la URL proporcionada
    url = "https://www.fi.upm.es/?id=estructura/departamentos"
    
    # Descargar página
    html_content = descargar_html(url)
    
    if html_content:
        # Extraer emails con contexto
        mails_con_contexto = extraer_mails_con_contexto(html_content)
        
        # Limpiar emails
        mails_limpiados = limpiar_mails(mails_con_contexto)
        
        # Guardar en CSV
        guardar_csv(mails_limpiados)
        
        # Eliminar archivo HTML descargado
        if os.path.exists('emails.html'):
            os.remove('emails.html')
            print("Archivo emails.html eliminado correctamente.")

if __name__ == "__main__":
    main()