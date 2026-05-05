# src/processing/deduplicator.py

from difflib import SequenceMatcher
from collections import defaultdict


def normalize_for_comparison(text: str) -> str:
    if not text:
        return ""

    return text.lower().strip()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


class Deduplicator:
    def __init__(self, similarity_threshold=0.9):
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, articles):
        """
        Deduplicate articles ONLY within the same source.
        """

        # group by source
        grouped = defaultdict(list)
        for article in articles:
            grouped[article.get("source")].append(article)

        deduplicated_all = []

        for source, source_articles in grouped.items():
            deduplicated = self._deduplicate_single_source(source_articles)
            deduplicated_all.extend(deduplicated)

        return deduplicated_all

    def _deduplicate_single_source(self, articles):
        unique_articles = []
        seen_urls = set()

        for article in articles:
            url = article.get("url")

            # 1. URL-based deduplication
            if url in seen_urls:
                continue

            seen_urls.add(url)

            title = normalize_for_comparison(article.get("title", ""))

            is_duplicate = False

            for existing in unique_articles:
                existing_title = normalize_for_comparison(existing.get("title", ""))

                if similarity(title, existing_title) > self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)

        return unique_articles