from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date


@dataclass
class FilterState:
    date_from: date
    date_to:   date
    products:  list[str] = field(default_factory=list)
    states:    list[str] = field(default_factory=list)
    channels:  list[str] = field(default_factory=list)
    timely:    str | None = None
    disputed:  str | None = None
    days_min:  int = 0
    days_max:  int = 365
    search:    str = ""

    def __post_init__(self):
        if self.date_from > self.date_to:
            raise ValueError("date_from phải ≤ date_to")
        if self.timely not in (None, "Yes", "No"):
            raise ValueError(f"timely không hợp lệ: {self.timely!r}")
        if self.disputed not in (None, "Yes", "No"):
            raise ValueError(f"disputed không hợp lệ: {self.disputed!r}")
        if self.days_min > self.days_max:
            raise ValueError("days_min phải ≤ days_max")

    def build_where(self) -> tuple[str, list]:
        conds  = ["date_received BETWEEN ? AND ?"]
        params = [self.date_from, self.date_to]

        if self.products:
            ph = ",".join(["?"] * len(self.products))
            conds.append(f"product IN ({ph})")
            params.extend(self.products)
        if self.states:
            ph = ",".join(["?"] * len(self.states))
            conds.append(f"state IN ({ph})")
            params.extend(self.states)
        if self.channels:
            ph = ",".join(["?"] * len(self.channels))
            conds.append(f"channel IN ({ph})")
            params.extend(self.channels)
        if self.timely:
            conds.append("timely = ?")
            params.append(self.timely)
        if self.disputed:
            conds.append("disputed = ?")
            params.append(self.disputed)

        conds.append("days_to_resolve BETWEEN ? AND ?")
        params.extend([self.days_min, self.days_max])

        if self.search:
            kw = f"%{self.search.lower()}%"
            conds.append(
                "(LOWER(company) LIKE ? OR LOWER(issue) LIKE ? "
                "OR LOWER(product) LIKE ? OR CAST(complaint_id AS VARCHAR) LIKE ?)"
            )
            params.extend([kw, kw, kw, kw])

        return " WHERE " + " AND ".join(conds), params

    def is_default(self, meta: dict) -> bool:
        d_min = meta["date_min"] if isinstance(meta["date_min"], date) else meta["date_min"].date()
        d_max = meta["date_max"] if isinstance(meta["date_max"], date) else meta["date_max"].date()
        return (
            self.date_from == d_min and self.date_to == d_max
            and not self.products and not self.states and not self.channels
            and self.timely is None and self.disputed is None
            and self.days_min == 0 and self.search == ""
        )
