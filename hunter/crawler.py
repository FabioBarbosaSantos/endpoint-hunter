"""
crawler.py

Responsável por:
- Baixar HTML
- Extrair scripts
- Baixar arquivos JS
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from hunter.config import DEFAULT_HEADERS, TIMEOUT

def extract_html_links(html, base_url, verbose=False):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    base_domain = urlparse(base_url).netloc

    def is_valid_link(href):
        if not href:
            return False

        # Ignorar âncoras
        if href.startswith("#"):
            return False

        # Ignorar javascript:
        if href.startswith("javascript:"):
            return False

        # Ignorar mailto:
        if href.startswith("mailto:"):
            return False

        return True

    tags_to_check = [
        ("a", "href"),
        ("form", "action"),
        ("link", "href"),
    ]

    for tag_name, attr in tags_to_check:
        for tag in soup.find_all(tag_name, **{attr: True}):
            href = tag[attr]

            if not is_valid_link(href):
                continue

            full_url = urljoin(base_url, href)

            #Opcional: só manter links internos
            if urlparse(full_url).netloc == base_domain:
                links.add(full_url)

    if verbose:
        print(f"Found {len(links)} valid HTML links")

    return list(links)

def get_html(url, verbose=False): #Faz requisição GET para o alvo e retorna o HTML.

    if verbose:
        print(f"Requesting HTML from: {url}")

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

    # Levanta exceção se der erro HTTP (403, 500 etc)
    response.raise_for_status()

    if verbose:
        print(f"Status code: {response.status_code}")

    return response.text


def extract_scripts(html, base_url, verbose=False): #Extrai todos os <script src="..."> do HTML.

    soup = BeautifulSoup(html, "html.parser")
    scripts = []

    for script in soup.find_all("script", src=True):
        full_url = urljoin(base_url, script["src"])
        scripts.append(full_url)

        if verbose:
            print(f"Found JS file: {full_url}")

    return list(set(scripts))


def fetch_js_files(script_urls, verbose=False): #Baixa todos os arquivos JS encontrados.

    js_contents = []

    for url in script_urls:
        try:
            if verbose:
                print(f"Fetching JS: {url}")

            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

            if response.status_code == 200:
                js_contents.append(response.text)
            else:
                if verbose:
                    print(f"Skipped {url} (status {response.status_code})")

        except requests.RequestException as e:
            if verbose:
                print(f"Failed to fetch {url}: {e}")

    return js_contents
