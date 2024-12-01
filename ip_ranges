import dns.resolver
import whois
import ipaddress
import socket
from datetime import datetime
import requests

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

    def get_ip_ranges(self, ip):
        try:
            response = requests.get(f"https://rdap.arin.net/registry/ip/{ip}")
            if response.status_code == 200:
                data = response.json()
                cidr = data.get("startAddress") + " - " + data.get("endAddress")
                return cidr
            else:
                return "Range not available"
        except Exception:
            return "Error fetching range"

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
        a_records = self.lookup_records(domain, 'A')
        ip_ranges = {ip: self.get_ip_ranges(ip) for ip in a_records}
        return {
            'domain': domain,
            'mx_records': self.lookup_records(domain, 'MX'),
            'a_records': a_records,
            'ip_ranges': ip_ranges,
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
            
            print("\nIP Address Ranges:")
            for ip, cidr in result['ip_ranges'].items():
                print(f"  - {ip}: {cidr}")
            
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
    
    # Perform the audit
    results = [auditor.audit_domain(domain) for domain in dominios]
    
    # Print results
    auditor.print_audit_results(results)

if __name__ == "__main__":
    main()
