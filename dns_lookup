import dns.resolver
import whois
from datetime import datetime

class DNSAuditor:
    def __init__(self, domains):
        self.domains = domains
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def lookup_records(self, domain, record_type):
        try:
            records = self.resolver.resolve(domain, record_type)
            return [str(rdata) for rdata in records]
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            return []

    def get_whois_info(self, domain):
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar or 'N/A',
                'creation_date': self._format_date(w.creation_date),
                'expiration_date': self._format_date(w.expiration_date)
            }
        except Exception:
            return {'registrar': 'N/A', 'creation_date': 'N/A', 'expiration_date': 'N/A'}

    def _format_date(self, date):
        if date is None:
            return 'N/A'
        if isinstance(date, list):
            date = date[0]
        return str(date)

    def audit_domain(self, domain):
        return {
            'domain': domain,
            'mx_records': self.lookup_records(domain, 'MX'),
            'a_records': self.lookup_records(domain, 'A'),
            'ns_records': self.lookup_records(domain, 'NS'),
            'txt_records': self.lookup_records(domain, 'TXT'),
            'whois_info': self.get_whois_info(domain)
        }

    def print_audit_results(self, results):
        print("\n" + "="*50)
        print(f"DNS AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)

        for result in results:
            print(f"\nDomain: {result['domain']}")
            print("-" * 30)
            
            print("MX Records:")
            for mx in result['mx_records']:
                print(f"  - {mx}")
            
            print("\nA Records:")
            for a in result['a_records']:
                print(f"  - {a}")
            
            print("\nName Servers:")
            for ns in result['ns_records']:
                print(f"  - {ns}")
            
            print("\nTXT Records:")
            for txt in result['txt_records']:
                print(f"  - {txt}")
            
            print("\nWHOIS Information:")
            print(f"  Registrar: {result['whois_info']['registrar']}")
            print(f"  Creation Date: {result['whois_info']['creation_date']}")
            print(f"  Expiration Date: {result['whois_info']['expiration_date']}")
            
            print("\n" + "-"*30)

def main():
    dominios = ['apple.com', 'upm.es', 'ole.com.ar', 'telefonica.com']
    auditor = DNSAuditor(dominios)
    
    # Realizar auditoría
    resultados = [auditor.audit_domain(dominio) for dominio in dominios]
    
    # Imprimir resultados
    auditor.print_audit_results(resultados)

if __name__ == "__main__":
    main()
