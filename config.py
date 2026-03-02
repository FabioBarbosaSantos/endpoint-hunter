#config.py

#Arquivo responsável por definir configurações globais como headers HTTP e timeout.

DEFAULT_HEADERS = { # Simula navegador
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    
    "Referer": "https://google.com",
    
    "X-Forwarded-For": "127.0.0.1"
}

TIMEOUT = 10
