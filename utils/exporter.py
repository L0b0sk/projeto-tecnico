import csv
import json
import os
from utils.logger import get_logger
logger = get_logger(__name__)

def save_results(result) -> None:

    os.makedirs("output", exist_ok=True)

    _save_json(result)
    _save_csv(result)


def _save_json(result) -> None:

    path = "output/hotels.json"

    existing_data = []

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            try:
                content = json.load(file)
                existing_data = content if isinstance(content, list) else [content]
            except json.JSONDecodeError:
                logger.warning("Arquivo JSON existente estava corrompido — iniciando novo")
                existing_data = []

    existing_data.append(result.__dict__)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

    logger.info(f"JSON salvo: {path}")


def _save_csv(result) -> None:

    path = "output/hotels.csv"
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=result.__dict__.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(result.__dict__)

    logger.info(f"CSV salvo: {path}")