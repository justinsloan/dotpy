#!/usr/bin/python3

"""
Checks a list of domains in domains.txt to get registrar and expiration date.
Returns PASSED or FAILED is the domain is registered with Cloudflare.
"""

from whois import whois
from tabulate import tabulate
from tqdm import tqdm


def by_date(table):
  return table[3]


def read_file(file_path):
    ''' Opens the specified file and returns a list with each line of the file '''

    # Initialize an empty list to store lines from the file
    lines = []

    # Open the file
    with open(file_path, 'r') as f:
        # Loop through each line in the file and add it to our list
        for line in f:
            lines.append(line.strip())

    return lines


def check_registrar(domain):
    query = whois(domain)
    if query: # If domain exists
        registrar = query.registrar
        expiration = str(query.expiration_date)
        if registrar.lower().startswith("cloudflare"):
            return 'PASSED', registrar, expiration
        else:
            return 'FAILED', registrar, expiration
    else:
        return 'ERROR', 'UNKNOWN', 'UNKNOWN'

domains = read_file('domains.txt')
table = []

print(f"Please wait, checking {len(domains)} domains...")

for domain in tqdm(domains, bar_format='{bar} {percentage:3.0f}% remaining {remaining}'):
    #print(f"Checking: {domain}")
    result, registrar, expiration = check_registrar(domain)
    result = [domain, result, registrar, expiration]
    table.append(result)

table.sort(key=by_date)
table.insert(0, ['Domain','Result','Registrar', 'Expiration'])
print(tabulate(table, headers='firstrow'))
