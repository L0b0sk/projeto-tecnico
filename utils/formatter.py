import re
from datetime import datetime, date

def clean_price(price_text: str) -> float:

    if not price_text:
        return 0.0

    text = price_text.strip()

    if re.search(r'\d\.\d{3},\d{2}', text):
        text = text.replace(".", "").replace(",", ".")

    elif re.search(r'\d,\d{2}$', text):
        text = text.replace(",", ".")

    numbers = re.sub(r"[^0-9.]", "", text)

    if not numbers:
        return 0.0

    try:
        return float(numbers)
    except ValueError:
        return 0.0


def extract_currency(price_text: str) -> str:

    if not price_text:
        return "BRL"

    text = price_text.upper()

    if "R$" in text or "BRL" in text:
        return "BRL"
    elif "USD" in text or "US$" in text:
        return "USD"
    elif "€" in text or "EUR" in text:
        return "EUR"
    elif "£" in text or "GBP" in text:
        return "GBP"
    elif "$" in text:
        return "USD"
    else:
        return "BRL"


def count_nights(check_in: str, check_out: str) -> int:

    try:
        d_in  = datetime.strptime(check_in,  "%Y-%m-%d").date()
        d_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        noites = (d_out - d_in).days
        return max(noites, 1)

    except (ValueError, TypeError):
        return 1


def clean_text(text: str) -> str:

    if not text:
        return ""

    return " ".join(text.strip().split())


def clean_rating(rating_text: str) -> float | None:

    if not rating_text:
        return None

    match = re.search(r'(\d{1,2})[,.](\d)', rating_text)

    if match:
        return float(f"{match.group(1)}.{match.group(2)}")
    
    match = re.search(r'\b(\d{1,2})\b', rating_text)
    if match:
        value = float(match.group(1))
        if value <= 10:
            return value

    return None


def clean_review_count(text: str) -> int | None:

    if not text:
        return None

    mil_match = re.search(r'(\d+)\s*mil', text, re.IGNORECASE)
    if mil_match:
        return int(mil_match.group(1)) * 1000

    numbers = re.sub(r'[.,]', '', text)
    match = re.search(r'\d+', numbers)

    if match:
        return int(match.group())

    return None