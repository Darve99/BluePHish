import json
import os
from pathlib import Path
from typing import Any


class FilePersistence:
    def __init__(self, base_dir: str | None = None) -> None:
        configured_dir = base_dir or os.getenv("BLUEPHISH_DATA_DIR")
        fallback_dir = str(Path(".").resolve() / "data")
        self.base_dir = Path(configured_dir or fallback_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.base_dir / name

    def save_json(self, name: str, payload: Any) -> None:
        self._path(name).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_json(self, name: str, default: Any) -> Any:
        path = self._path(name)
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default


persistence = FilePersistence()
