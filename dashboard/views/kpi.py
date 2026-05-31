import streamlit as st
from ..models.metrics import DashboardMetrics


class KPIView:

    def render(self, metrics: DashboardMetrics, meta: dict) -> None:
        n     = metrics.n
        trend = metrics.trend_pct(meta)
        k1, k2, k3, k4, k5 = st.columns(5, gap="small")

        with k1:
            st.markdown(self._card(
                "Tổng khiếu nại", self._n(n),
                f"{n / meta['total'] * 100:.0f}% bộ dữ liệu",
                trend=trend,
            ), unsafe_allow_html=True)

        with k2:
            rate = metrics.resolved_n / n if n else 0
            st.markdown(self._card(
                "Tỷ lệ giải quyết", self._pct(rate),
                f"{self._n(metrics.resolved_n)} đã đóng có giải pháp",
                accent_cls="accent",
            ), unsafe_allow_html=True)

        with k3:
            rate = metrics.timely_n / n if n else 0
            st.markdown(self._card(
                "Phản hồi đúng hạn", self._pct(rate),
                f"{self._n(n - metrics.timely_n)} trễ hạn",
            ), unsafe_allow_html=True)

        with k4:
            rate = metrics.disputed_n / n if n else 0
            st.markdown(self._card(
                "Khiếu kiện lại", self._pct(rate),
                f"{self._n(metrics.disputed_n)} không chấp nhận",
                accent_cls="warn",
            ), unsafe_allow_html=True)

        with k5:
            st.markdown(self._card(
                "Thời gian TB", f"{metrics.avg_days:.1f} ngày",
                f"Tối đa {metrics.max_days} ngày",
            ), unsafe_allow_html=True)

    @staticmethod
    def _n(v) -> str:
        return "—" if v is None else f"{int(v):,}".replace(",", ".")

    @staticmethod
    def _pct(v, d=1) -> str:
        return "—" if v is None else f"{v * 100:.{d}f}%"

    @staticmethod
    def _card(label, value, sub, accent_cls="", trend=None) -> str:
        trend_html = ""
        if trend:
            cls, arrow = ("up", "▲") if trend > 0 else ("down", "▼")
            trend_html = f'<div class="kpi-trend {cls}">{arrow} {abs(trend):.1f}%</div>'
        return (
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value {accent_cls}">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f'{trend_html}'
            f'</div>'
        )
