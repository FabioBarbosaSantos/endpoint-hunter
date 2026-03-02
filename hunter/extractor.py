#extractor.py

#Responsável por extrair endpoints usando regex.


import re
from urllib.parse import urljoin

# Regex para URLs completas
URL_REGEX = r'https?://[^\s"\']+'

# Regex para caminhos relativos
PATH_REGEX = r'\/[a-zA-Z0-9_\-\/]+'


def extract_endpoints(js_contents, base_url, verbose=False): #Extrai endpoints de todos os conteúdos JS.

    endpoints = set()

    for content in js_contents:

        # Captura URLs completas
        full_urls = re.findall(URL_REGEX, content)
        endpoints.update(full_urls)

        # Captura caminhos relativos
        paths = re.findall(PATH_REGEX, content)

        for path in paths:
            full_path = urljoin(base_url, path)
            endpoints.add(full_path)

    if verbose:
        print(f"Total endpoints found: {len(endpoints)}")

    return endpoints
