from __future__ import annotations
from .repository import ComplaintsRepository
from .filter_state import FilterState
from .metrics import DashboardMetrics


class InsightEngine:

    def __init__(self, repo: ComplaintsRepository,
                 fs: FilterState, metrics: DashboardMetrics) -> None:
        self._repo    = repo
        self._fs      = fs
        self._metrics = metrics

    def run(self) -> list[dict]:
        if self._metrics.n == 0:
            return []
        where, params = self._fs.build_where()
        out = []
        out += self._top_product(where, params)
        out += self._dispute_rate()
        out += self._resolution_time()
        out += self._worst_response(where, params)
        out += self._geo_concentration(where, params)
        out += self._spike(where, params)
        out += self._timely_correlation(where, params)
        return out

    def _top_product(self, where, params) -> list[dict]:
        row = self._repo.fetch_one(
            "product, COUNT(*) AS n",
            where + " AND product IS NOT NULL GROUP BY product ORDER BY n DESC LIMIT 1",
            params)
        if not row:
            return []
        pct = row[1] / self._metrics.n * 100
        return [{"tone": "", "tag": "Tập trung",
                 "title": f"{row[0]} chiếm {pct:.0f}% tổng khiếu nại",
                 "body": "Sản phẩm bị phàn nàn nhiều nhất. Ưu tiên review quy trình xử lý."}]

    def _dispute_rate(self) -> list[dict]:
        disp_all = self._repo.fetch_one(
            "AVG(CASE WHEN disputed='Yes' THEN 1.0 ELSE 0 END)", "", [])[0] or 0
        cur  = self._metrics.disputed_n / self._metrics.n
        diff = (cur - disp_all) * 100
        if   diff >  1: tone, tag, sign = "warn", "Cảnh báo",   f"cao hơn {diff:.1f} đpt"
        elif diff < -1: tone, tag, sign = "pos",  "Tích cực",   f"thấp hơn {abs(diff):.1f} đpt"
        else:           tone, tag, sign = "",     "Trung tính", "sát mức chung"
        return [{"tone": tone, "tag": tag,
                 "title": f"Tỷ lệ khiếu kiện lại {cur*100:.1f}% — {sign} so với toàn bộ",
                 "body": "Khách tiếp tục khiếu nại cho thấy giải pháp ban đầu chưa thoả đáng."}]

    def _resolution_time(self) -> list[dict]:
        all_avg   = self._repo.fetch_one("AVG(days_to_resolve)", "", [])[0] or 0
        delta     = self._metrics.avg_days - all_avg
        direction = "chậm hơn" if delta > 0 else "nhanh hơn"
        return [{"tone": "time", "tag": "Thời gian",
                 "title": f"Trung bình {self._metrics.avg_days:.1f} ngày để xử lý",
                 "body": f"So với toàn bộ {all_avg:.1f} ngày — {direction} {abs(delta):.1f} ngày."}]

    def _worst_response(self, where, params) -> list[dict]:
        row = self._repo.fetch_one(
            "response, COUNT(*) AS n, "
            "AVG(CASE WHEN disputed='Yes' THEN 1.0 ELSE 0 END) AS rate",
            where + " AND response IS NOT NULL GROUP BY response "
                    "HAVING COUNT(*) >= 30 ORDER BY rate DESC LIMIT 1",
            params)
        if not row:
            return []
        return [{"tone": "resp", "tag": "Phản hồi",
                 "title": f'"{row[0]}" tạo ra {row[2]*100:.0f}% tỷ lệ khiếu kiện lại',
                 "body": "Loại phản hồi gây bất mãn nhất. Cần xem lại cách ra quyết định."}]

    def _geo_concentration(self, where, params) -> list[dict]:
        df = self._repo.fetch(
            "state, COUNT(*) AS n",
            where + " AND state IS NOT NULL GROUP BY state ORDER BY n DESC LIMIT 5",
            params)
        if df.empty:
            return []
        pct = df["n"].sum() / self._metrics.n * 100
        states = ", ".join(df["state"].tolist())
        return [{"tone": "", "tag": "Địa lý",
                 "title": f"5 bang dẫn đầu chiếm {pct:.0f}% lượng khiếu nại",
                 "body": f"{states} là những điểm nóng cần tập trung nguồn lực."}]

    def _spike(self, where, params) -> list[dict]:
        df = self._repo.fetch(
            "date_trunc('month', date_received) AS m, COUNT(*) AS n",
            where + " GROUP BY 1 ORDER BY 1",
            params)
        if len(df) < 3:
            return []
        avg_m = df["n"].mean()
        spike = df.loc[df["n"].idxmax()]
        if spike["n"] <= avg_m * 1.8:
            return []
        pct_above = spike["n"] / avg_m * 100 - 100
        return [{"tone": "warn", "tag": "Bất thường",
                 "title": f"{spike['m'].strftime('%Y-%m')}: tăng đột biến {pct_above:.0f}% so với TB",
                 "body": f"Tháng đó có {int(spike['n']):,} khiếu nại, trung bình các tháng là {avg_m:.0f}."}]

    def _timely_correlation(self, where, params) -> list[dict]:
        df = self._repo.fetch(
            "timely, AVG(CASE WHEN disputed='Yes' THEN 1.0 ELSE 0 END) AS rate",
            where + " AND timely IS NOT NULL GROUP BY timely",
            params)
        tm = dict(zip(df["timely"], df["rate"]))
        if "Yes" not in tm or "No" not in tm or tm["No"] <= tm["Yes"] + 0.02:
            return []
        diff_pp = (tm["No"] - tm["Yes"]) * 100
        return [{"tone": "warn", "tag": "Tương quan",
                 "title": f"Phản hồi trễ hạn → khiếu kiện lại cao hơn {diff_pp:.1f} đpt",
                 "body": "Đáp ứng đúng SLA giảm rõ rệt tỷ lệ khách quay lại khiếu nại."}]
