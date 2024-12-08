import requests
import re
import csv
import time
from urllib.parse import urljoin, urlparse
import concurrent.futures
import threading

class EmailExtractorP6:
    def __init__(self, start_url, max_workers=5, max_depth=2):
        self.start_url = start_url
        self.max_workers = max_workers
        self.max_depth = max_depth
        self.visited_urls = set()
        self.all_emails = set()
        self.lock = threading.Lock()  # Usar threading.Lock() en su lugar

    def download_page(self, url):
        """Descargar página web con técnicas para evitar bloqueo"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        
        try:
            time.sleep(0.5)  # Reducir retardo
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def extract_links(self, html_content, base_url):
        """Extraer enlaces de la página"""
        link_pattern = r'href=[\'"]?([^\'" >]+)'
        links = re.findall(link_pattern, html_content)
        
        full_links = []
        for link in links:
            try:
                full_link = urljoin(base_url, link)
                if (urlparse(full_link).netloc == urlparse(base_url).netloc and 
                    full_link not in self.visited_urls):
                    full_links.append(full_link)
            except:
                continue
        
        return list(set(full_links))

    def extract_emails(self, html_content):
        """Extraer direcciones de email usando regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return set(re.findall(email_pattern, html_content, re.IGNORECASE))

    def process_url(self, url, depth):
        """Procesar una URL individual"""
        if depth > self.max_depth or url in self.visited_urls:
            return set()

        with self.lock:
            self.visited_urls.add(url)

        html_content = self.download_page(url)
        if not html_content:
            return set()

        emails = self.extract_emails(html_content)
        
        with self.lock:
            self.all_emails.update(emails)

        # Si no hemos alcanzado la profundidad máxima, extraer enlaces
        if depth < self.max_depth:
            links = self.extract_links(html_content, url)
            return set(links)
        
        return set()

    def recursive_email_extraction(self):
        """Extracción recursiva de emails con procesamiento concurrente"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Conjunto de URLs para procesar
            urls_to_process = {self.start_url}
            processed_urls = set()
            depth = 0

            while urls_to_process and depth <= self.max_depth:
                # Preparar futures para las URLs actuales
                futures = {
                    executor.submit(self.process_url, url, depth): url 
                    for url in urls_to_process
                }

                # Recopilar nuevos enlaces de los resultados
                new_urls = set()
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        new_urls.update(result)
                    except Exception:
                        pass

                # Actualizar conjuntos
                processed_urls.update(urls_to_process)
                urls_to_process = new_urls - processed_urls
                depth += 1

        # Limpiar emails
        return self.clean_emails(list(self.all_emails))

    def clean_emails(self, emails):
        """Limpiar y eliminar emails duplicados"""
        def is_valid_email(email):
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            return re.match(email_pattern, email, re.IGNORECASE) is not None
        
        return [email.lower() for email in set(emails) if is_valid_email(email)]

    def save_to_csv(self, emails, filename='emails_recursivo.csv'):
        """Guardar emails en archivo CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Email'])  # Encabezado
            for email in emails:
                csv_writer.writerow([email])

def main():
    url = "https://www.etsisi.upm.es/escuela/dptos/dpto_per?id_dpto=SI"
    
    # Crear extractor
    extractor = EmailExtractorP6(url, max_workers=5, max_depth=2)
    
    # Extraer emails
    emails = extractor.recursive_email_extraction()
    
    # Guardar en CSV
    extractor.save_to_csv(emails)

if __name__ == "__main__":
    main()