
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def save_jsonl(records: list[dict], filename: str) -> int:
    """Create or replace a JSONL file."""

    file_path = RAW_DATA_DIR / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(records)


def append_jsonl(records: list[dict], filename: str) -> int:
    """Append records to an existing JSONL file."""

    file_path = RAW_DATA_DIR / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("a", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(records)


def read_jsonl(filename: str) -> list[dict]:
    """Read records from a JSONL file."""

    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]