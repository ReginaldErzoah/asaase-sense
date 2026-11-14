import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def save_jsonl(records: list[dict], filename: str) -> int:

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / filename

    with file_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(records)
