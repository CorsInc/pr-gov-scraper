"""Configuration for pr.gov scraper."""

BASE_URL = "https://www.pr.gov"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
REQUEST_DELAY = 1.0  # seconds between requests

OUTPUT_DIR = "scraper/output"

SECTIONS = {
    "main": "/",
    "agencies": "/agencias",
    "services": "/servicios",
    "news": "/noticias",
}
