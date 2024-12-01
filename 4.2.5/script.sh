#!/bin/bash

domains=("upm.es" "ole.com.ar" "telefonica.com" "apple.com")

for domain in "${domains[@]}"; do
    echo "Analyzing $domain:"
    
    # DNSSsEC check
    echo "DNSSEC Support:"
    dig +short +dnssec "$domain"
    
    # NS records
    echo "Nameservers:"
    dig +short NS "$domain"
    
    # Zone rransfer
    echo "Zone Transfer Test:"
    dig AXFR "$domain" || echo "Zone transfer likely restricted"
    
    echo "------------------------"
done