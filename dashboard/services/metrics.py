from __future__ import annotations
from datetime import timedelta
from ..repositories.repository import ComplaintsRepository
from .filter_state import FilterState


class DashboardMetrics:

    def __init__(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        self._repo  = repo
        self._fs    = fs
        self._cache = None

    def _load(self):
        if self._cache is not None:
            return
        row = self._repo.fetch_one_filtered(
            "COUNT(*) AS n, "
            "AVG(days_to_resolve) AS avg_days, "
            "SUM(CASE WHEN timely='Yes'   THEN 1 ELSE 0 END) AS timely_n, "
            "SUM(CASE WHEN disputed='Yes' THEN 1 ELSE 0 END) AS disputed_n, "
            "SUM(CASE WHEN response LIKE 'Closed with%' THEN 1 ELSE 0 END) AS resolved_n, "
            "MAX(days_to_resolve) AS max_days",
            self._fs,
        )
        self._cache = {
            "n":          int(row[0] or 0),
            "avg_days":   float(row[1] or 0),
            "timely_n":   int(row[2] or 0),
            "disputed_n": int(row[3] or 0),
            "resolved_n": int(row[4] or 0),
            "max_days":   int(row[5] or 0),
        }

    @property
    def n(self) -> int:
        self._load(); return self._cache["n"]

    @property
    def avg_days(self) -> float:
        self._load(); return self._cache["avg_days"]

    @property
    def timely_n(self) -> int:
        self._load(); return self._cache["timely_n"]

    @property
    def disputed_n(self) -> int:
        self._load(); return self._cache["disputed_n"]

    @property
    def resolved_n(self) -> int:
        self._load(); return self._cache["resolved_n"]

    @property
    def max_days(self) -> int:
        self._load(); return self._cache["max_days"]

    def trend_pct(self, meta: dict) -> float:
        period = (self._fs.date_to - self._fs.date_from).days
        if period <= 0:
            return 0.0
        prev_to   = self._fs.date_from - timedelta(days=1)
        prev_from = prev_to - timedelta(days=period)
        prev_n = self._repo.fetch_one(
            "COUNT(*)", "WHERE date_received BETWEEN ? AND ?", [prev_from, prev_to]
        )[0]
        return ((self.n - prev_n) / prev_n * 100) if prev_n > 0 else 0.0
