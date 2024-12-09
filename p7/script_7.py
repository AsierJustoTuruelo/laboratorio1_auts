import socket
import dns.resolver
import concurrent.futures
import os

class DNSEnumerator:
    def __init__(self, base_domain, wordlist_path=None):
        """
        Initialize DNS enumerator with a base domain and optional wordlist path.
        """
        self.base_domain = base_domain
        
        # Load wordlist from file if a path is provided, otherwise use a default list
        if wordlist_path and os.path.exists(wordlist_path):
            with open(wordlist_path, 'r') as f:
                self.wordlist = [line.strip() for line in f if line.strip()]
        else:
            # Default wordlist por si acaso
            self.wordlist = [
                'www', 'mail', 'blog', 'admin', 'test', 'dev', 
                'staging', 'support', 'web', 'ftp', 'ns1', 'ns2', 
                'vpn', 'remote', 'api', 'service', 'portal'
            ]
    
    def resolve_subdomain(self, subdomain):
        """
        Attempt to resolve a single subdomain.
        """
        try:
            # Construct full domain name
            fqdn = f"{subdomain}.{self.base_domain}"
            
            # Use socket to resolve domain
            ip_address = socket.gethostbyname(fqdn)
            
            return (fqdn, ip_address)
        except (socket.gaierror, socket.error):
            return None
    
    def enumerate_subdomains(self, max_workers=10):
        """
        Enumerate subdomains using concurrent resolution.
        """
        resolved_subdomains = []
        
        # Use ThreadPoolExecutor for concurrent DNS resolution
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map subdomain resolution to executor
            future_to_subdomain = {
                executor.submit(self.resolve_subdomain, subdomain): subdomain 
                for subdomain in self.wordlist
            }
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_subdomain):
                result = future.result()
                if result:
                    resolved_subdomains.append(result)
        
        return resolved_subdomains
    
    def save_results(self, results, output_file='subdomains.txt'):
        """
        Save resolution results to a text file.
        """
        with open(output_file, 'w') as f:
            for fqdn, ip in results:
                f.write(f"{fqdn} -> '{ip}'\n")
        
        print(f"Results saved to {output_file}")

def main():
    # Path to subdomain wordlist (quick and detailed versions one is quicker than the other)
    # wordlist_path_quick = os.path.join(os.path.dirname(__file__), 'subdomains-top1million-5000.txt')
    wordlist_path_detailed = os.path.join(os.path.dirname(__file__), 'subdomains-top1million-110000.txt')    
    
    # Domains to enumerate
    domains = ['upm.es', 'uc3m.es', 'ucm.es']
    
    for domain in domains:
        print(f"\nEnumerating subdomains for {domain}")
        
        # Initialize enumerator
        enumerator = DNSEnumerator(domain, wordlist_path=wordlist_path_detailed)
        
        # Perform enumeration
        results = enumerator.enumerate_subdomains()
        
        # Output results
        if results:
            print(f"Found {len(results)} subdomains for {domain}:")
            for fqdn, ip in results:
                print(f"{fqdn} -> '{ip}'")
            
            # Save results to file
            enumerator.save_results(results, f'{domain}_subdomains.txt')
        else:
            print(f"No subdomains found for {domain}")

if __name__ == "__main__":
    main()
