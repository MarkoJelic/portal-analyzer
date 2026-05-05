import re


def clean_text(text: str) -> str:
    if not text:
        return text

    # remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()