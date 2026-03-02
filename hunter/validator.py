import requests
from urllib.parse import urljoin

IGNORED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".svg",
    ".css", ".woff", ".woff2",
    ".ttf", ".map", ".ico"
)

def validate_endpoints(base_url, endpoints):
    valid_results = []

    for endpoint in endpoints:
        # Ignorar extensões inúteis
        if endpoint.endswith(IGNORED_EXTENSIONS):
            continue

        full_url = urljoin(base_url, endpoint)

        try:
            response = requests.head(
                full_url,
                allow_redirects=True,
                timeout=5
            )

            status = response.status_code

            # Ignorar 404
            if status != 404:
                valid_results.append((full_url, status))

        except requests.RequestException:
            continue

    return valid_results
