import json
from pathlib import Path


def export_json(data: dict | list, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return output_path