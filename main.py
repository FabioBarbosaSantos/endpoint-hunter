"""
main.py

Arquivo principal da ferramenta.
Responsável por:
- CLI
- Fluxo principal
"""

import argparse
from hunter.crawler import get_html, extract_scripts, fetch_js_files
from hunter.extractor import extract_endpoints


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

    # 2 - Extrair JS
    scripts = extract_scripts(html, args.url, args.verbose)

    print(f"[+] Found {len(scripts)} JS files")

    # 3 - Baixar JS
    js_contents = fetch_js_files(scripts, args.verbose)

    # 4 - Extrair endpoints
    endpoints = extract_endpoints(js_contents, args.url, args.verbose)

    print("\n[+] Endpoints found:\n")

    for ep in endpoints:
        print(ep)


if __name__ == "__main__":
    main()
