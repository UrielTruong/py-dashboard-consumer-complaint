from __future__ import annotations
import dataclasses
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

# test data: Lưu ngoài thư mục module để tồn tại giữa các lần chạy lại app
PRESETS_FILE = Path(__file__).parent.parent.parent / "presets.json"


@dataclass
class FilterPreset:
    name:      str
    date_from: str
    date_to:   str
    products:  list[str] = field(default_factory=list)
    states:    list[str] = field(default_factory=list)
    channels:  list[str] = field(default_factory=list)
    timely:    str | None = None
    disputed:  str | None = None
    days_min:  int = 0
    days_max:  int = 365
    search:    str = ""

    @classmethod
    def from_current_filters(cls, name: str, filters: dict) -> FilterPreset:
        d_from = filters["date_from"]
        d_to   = filters["date_to"]
        return cls(
            name=name,
            date_from=d_from.isoformat() if isinstance(d_from, date) else str(d_from),
            date_to=d_to.isoformat()     if isinstance(d_to,   date) else str(d_to),
            products=filters.get("products", []),
            states=filters.get("states", []),
            channels=filters.get("channels", []),
            timely=filters.get("timely"),
            disputed=filters.get("disputed"),
            days_min=filters.get("days_min", 0),
            days_max=filters.get("days_max", 365),
            search=filters.get("search", ""),
        )

    def describe(self) -> str:
        parts = [f"{self.date_from} → {self.date_to}"]
        if self.products:
            extra = "..." if len(self.products) > 2 else ""
            parts.append(f"SP: {', '.join(self.products[:2])}{extra}")
        if self.states:
            extra = "..." if len(self.states) > 3 else ""
            parts.append(f"Bang: {', '.join(self.states[:3])}{extra}")
        return " · ".join(parts)


class PresetManager:

    def __init__(self) -> None:
        self._presets: dict[str, FilterPreset] = {}
        self._load()

    def _load(self) -> None:
        if PRESETS_FILE.exists():
            try:
                data = json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
                self._presets = {k: FilterPreset(**v) for k, v in data.items()}
            except Exception:
                # File bị corrupt thì reset về rỗng thay vì crash app
                self._presets = {}

    def _persist(self) -> None:
        PRESETS_FILE.write_text(
            json.dumps(
                {k: dataclasses.asdict(v) for k, v in self._presets.items()},
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def __len__(self) -> int:
        return len(self._presets)

    def names(self) -> list[str]:
        return list(self._presets.keys())

    def get(self, name: str) -> FilterPreset | None:
        return self._presets.get(name)

    def save(self, preset: FilterPreset) -> None:
        self._presets[preset.name] = preset
        self._persist()

    def delete(self, name: str) -> None:
        self._presets.pop(name, None)
        self._persist()
