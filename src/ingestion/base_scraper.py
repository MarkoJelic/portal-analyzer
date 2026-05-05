"""Base scraper placeholder for portal-analyzer."""

class BaseScraper:
    """Base class for site-specific scrapers."""
    def fetch(self, url):
        raise NotImplementedError()
