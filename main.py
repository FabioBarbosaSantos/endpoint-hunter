"""
main.py

Arquivo principal da ferramenta.
"""

import argparse
from hunter.crawler import (
    get_html,
    extract_scripts,
    fetch_js_files,
    extract_html_links
)
from hunter.extractor import extract_endpoints
from hunter.validator import validate_endpoints


def main():

    parser = argparse.ArgumentParser(
        description="Endpoint Hunter - JavaScript Endpoint Extractor"
    )

    parser.add_argument("url", help="Target URL (ex: https://site.com)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable debug output")

    args = parser.parse_args()

    print(f"[+] Target: {args.url}")

    # 1 - Baixar HTML
    html = get_html(args.url, args.verbose)

    # 2 - Extrair links do HTML
    html_links = extract_html_links(html, args.url, args.verbose)

    # 3 - Extrair JS
    scripts = extract_scripts(html, args.url, args.verbose)
    print(f"[+] Found {len(scripts)} JS files")

    # 4 - Baixar JS
    js_contents = fetch_js_files(scripts, args.verbose)

    # 5 - Extrair endpoints do JS
    endpoints = extract_endpoints(js_contents, args.url, args.verbose)
    print(f"[+] Found {len(endpoints)} JS endpoints")

    # 6 - Unir tudo
    all_endpoints = set(endpoints) | set(html_links)
    print(f"[+] Total unique endpoints: {len(all_endpoints)}")

    print("\n[+] Valid endpoints (excluding 404):\n")

    # 7 - Validar
    results = validate_endpoints(args.url, all_endpoints)

    for url, status in results:
        print(f"[{status}] {url}")


if __name__ == "__main__":
    main()
