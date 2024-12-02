import sys
import requests
import concurrent.futures
import logging
import dns.resolver

TLD = ['com', 'net', 'org', 'info', 'biz', 'co', 'us', 'uk', 'ca', 'de', 'jp', 'fr', 'au', 'in', 'ru', 'ch', 'it', 'nl', 'se', 'no', 'es', 'mil', 'gov', 'edu', 'tech']

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate possible typosquatting domains
def generate_typosquatting_domains(domain):
    typosquatting_domains = set()
    base_domain, suffix = domain.rsplit('.', 1)

    # Generate typosquatting domains by changing characters
    for i in range(len(base_domain)):
        for char in 'abcdefghijklmnopqrstuvwxyz0123456789-':
            if base_domain[i] != char:
                typosquatting_domains.add(base_domain[:i] + char + base_domain[i+1:] + '.' + suffix)

    # Generate typosquatting domains by changing TLDs
    for new_TLD in TLD:
        if new_TLD != suffix:
            typosquatting_domains.add(base_domain + '.' + new_TLD)

    # Additional typo variations: character swapping, missing characters, duplicate characters
    for i in range(len(base_domain) - 1):
        # Swap adjacent characters
        swapped = list(base_domain)
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        typosquatting_domains.add(''.join(swapped) + '.' + suffix)

    for i in range(len(base_domain)):
        # Missing character
        typosquatting_domains.add(base_domain[:i] + base_domain[i + 1:] + '.' + suffix)
        # Duplicate character
        typosquatting_domains.add(base_domain[:i] + base_domain[i] + base_domain[i:] + '.' + suffix)

    return list(typosquatting_domains)

# Function to write the typosquatting domain names to the output file
def write_output_file(output_file, typosquatting_domains):
    with open(output_file, 'w') as file:
        for domain in typosquatting_domains:
            file.write(domain + '\n')

# Function to check if a domain name is active using DNS lookup
def is_domain_active(domain):
    try:
        dns.resolver.resolve(domain, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.Timeout:
        return False
    except dns.resolver.NoNameservers:
        return False

# Function to detect active typosquatting domains
def detect_typosquatting(domain, output_file):
    typosquatting_domains = generate_typosquatting_domains(domain)
    active_typosquatting_domains = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(is_domain_active, d): d for d in typosquatting_domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                if future.result():
                    active_typosquatting_domains.append(domain)
            except Exception as exc:
                logging.error(f'{domain} generated an exception: {exc}')

    write_output_file(output_file, active_typosquatting_domains)

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python SquatSpotter.py <domain>")
        sys.exit(1)
    domain = sys.argv[1]
    output_file = f"SquatterList_{domain}.txt"
    detect_typosquatting(domain, output_file)

if __name__ == "__main__":
    main()