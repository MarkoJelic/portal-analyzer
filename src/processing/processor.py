import json
from pathlib import Path
from datetime import datetime

from src.processing.cleaner import clean_text
from src.processing.deduplicator import Deduplicator
from src.processing.normalizer import cyrillic_to_latin, apply_special_cases


class RSSProcessor:
    def __init__(self, input_dir="data/raw", output_dir="data/parsed"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    def process_file(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as f:
            articles = json.load(f)

        processed = []

        for article in articles:
            title = cyrillic_to_latin(article.get("title", ""))
            summary = cyrillic_to_latin(article.get("summary", ""))

            title = apply_special_cases(title)
            summary = apply_special_cases(summary)

            title = clean_text(title)
            summary = clean_text(summary)

            processed_article = {
                "id": self.generate_id(article),
                "source": article.get("source"),
                "title": title,
                "url": article.get("link"),
                "published_at": article.get("published"),
                "summary": summary,
            }

            processed.append(processed_article)

        return processed

    def generate_id(self, article):
        # simple deterministic ID (can improve later)
        return hash(article.get("link"))

    def run(self, target_date=None):
        deduplicator = Deduplicator()

        for date_dir in self.input_dir.iterdir():
            if not date_dir.is_dir():
                continue

            if target_date and date_dir.name != target_date:
                continue

            print(f"[PROCESSING DATE] {date_dir.name}")

            output_date_dir = self.output_dir / date_dir.name
            output_date_dir.mkdir(parents=True, exist_ok=True)

            all_articles = []

            for file_path in date_dir.glob("*.json"):
                print(f"[PROCESSING] {file_path.name}")
                processed = self.process_file(file_path)
                all_articles.extend(processed)

            deduplicated = deduplicator.deduplicate(all_articles)

            output_file = output_date_dir / "deduplicated.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(deduplicated, f, ensure_ascii=False, indent=2)