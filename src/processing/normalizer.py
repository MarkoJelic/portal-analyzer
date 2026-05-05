from src.processing.normalization_rules import SPECIAL_CASES

CYRILLIC_TO_LATIN = {
    "А": "A", "а": "a",
    "Б": "B", "б": "b",
    "В": "V", "в": "v",
    "Г": "G", "г": "g",
    "Д": "D", "д": "d",
    "Ђ": "Đ", "ђ": "đ",
    "Е": "E", "е": "e",
    "Ж": "Ž", "ж": "ž",
    "З": "Z", "з": "z",
    "И": "I", "и": "i",
    "Ј": "J", "ј": "j",
    "К": "K", "к": "k",
    "Л": "L", "л": "l",
    "Љ": "Lj", "љ": "lj",
    "М": "M", "м": "m",
    "Н": "N", "н": "n",
    "Њ": "Nj", "њ": "nj",
    "О": "O", "о": "o",
    "П": "P", "п": "p",
    "Р": "R", "р": "r",
    "С": "S", "с": "s",
    "Т": "T", "т": "t",
    "Ћ": "Ć", "ћ": "ć",
    "У": "U", "у": "u",
    "Ф": "F", "ф": "f",
    "Х": "H", "х": "h",
    "Ц": "C", "ц": "c",
    "Ч": "Č", "ч": "č",
    "Џ": "Dž", "џ": "dž",
    "Ш": "Š", "ш": "š",
}


def cyrillic_to_latin(text: str) -> str:
    if not text:
        return text

    return "".join(CYRILLIC_TO_LATIN.get(char, char) for char in text)

def apply_special_cases(text: str) -> str:
    if not text:
        return text

    for k, v in SPECIAL_CASES.items():
        text = text.replace(k, v)

    return text