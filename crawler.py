"""
crawler.py

Responsável por:
- Baixar HTML
- Extrair scripts
- Baixar arquivos JS
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from hunter.config import DEFAULT_HEADERS, TIMEOUT


def get_html(url, verbose=False):
    """
    Faz requisição GET para o alvo e retorna o HTML.
    """

    if verbose:
        print(f"[DEBUG] Requesting HTML from: {url}")

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

    # Levanta exceção se der erro HTTP (403, 500 etc)
    response.raise_for_status()

    if verbose:
        print(f"[DEBUG] Status code: {response.status_code}")

    return response.text


def extract_scripts(html, base_url, verbose=False):
    """
    Extrai todos os <script src="..."> do HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    scripts = []

    for script in soup.find_all("script", src=True):
        full_url = urljoin(base_url, script["src"])
        scripts.append(full_url)

        if verbose:
            print(f"[DEBUG] Found JS file: {full_url}")

    return list(set(scripts))


def fetch_js_files(script_urls, verbose=False):
    """
    Baixa todos os arquivos JS encontrados.
    """

    js_contents = []

    for url in script_urls:
        try:
            if verbose:
                print(f"[DEBUG] Fetching JS: {url}")

            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

            if response.status_code == 200:
                js_contents.append(response.text)
            else:
                if verbose:
                    print(f"[DEBUG] Skipped {url} (status {response.status_code})")

        except requests.RequestException as e:
            if verbose:
                print(f"[ERROR] Failed to fetch {url}: {e}")

    return js_contents
