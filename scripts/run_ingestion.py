from src.ingestion.rss_ingestor import RSSIngestor


if __name__ == "__main__":
    ingestor = RSSIngestor(
        config_path="configs/sources.yaml"
    )
    ingestor.run()