import feedparser
import yaml
from datetime import datetime
from pathlib import Path
import json


class RSSIngestor:
    def __init__(self, config_path: str, output_dir: str = "data/raw"):
        self.config_path = config_path
        self.output_dir = Path(output_dir)

    def load_sources(self):
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
        return config["sources"]

    def fetch_feed(self, source):
        feed = feedparser.parse(source["rss_url"])
        articles = []

        for entry in feed.entries:
            article = {
                "source": source["name"],
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published"),
                "summary": entry.get("summary", "")
            }
            articles.append(article)

        return articles

    def save_raw(self, source_name, articles):
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = self.output_dir / date_str
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / f"{source_name}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

    def run(self):
        sources = self.load_sources()

        for source in sources:
            print(f"[INFO] Fetching: {source['name']}")
            articles = self.fetch_feed(source)
            self.save_raw(source["name"], articles)
            print(f"[INFO] Saved {len(articles)} articles from {source['name']}")