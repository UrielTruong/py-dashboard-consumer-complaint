import streamlit as st
import plotly.graph_objects as go
from ..repositories.repository import ComplaintsRepository
from ..services.filter_state import FilterState
from ..config import PALETTE, DONUT_COLORS, US_STATES


class ChartsView:

    def _layout(self, height=380, **extra) -> dict:
        return dict(
            height=height,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor=PALETTE["bg2"],
            paper_bgcolor=PALETTE["bg2"],
            font=dict(family="Inter, sans-serif", color=PALETTE["muted"], size=12),
            **extra,
        )

    def _tf(self) -> dict:
        return dict(family="Inter, sans-serif", color=PALETTE["muted"], size=12)

    def render_trend(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "date_trunc('month', date_received) AS month, "
            "COUNT(*) AS total, "
            "SUM(CASE WHEN disputed='Yes' THEN 1 ELSE 0 END) AS disputed",
            where + " GROUP BY 1 ORDER BY 1",
            params)
        if df.empty:
            st.info("Không có dữ liệu.")
            return
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["month"], y=df["total"],
            fill="tozeroy", mode="lines",
            line=dict(color=PALETTE["accent"], width=2),
            fillcolor="rgba(146,157,255,0.12)",
            name="Tổng",
            hovertemplate="<b>%{x|%Y-%m}</b><br>%{y:,}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df["month"], y=df["disputed"],
            mode="lines",
            line=dict(color=PALETTE["accent2"], width=2, dash="dot"),
            name="Khiếu kiện lại",
        ))
        fig.update_layout(
            hovermode="x unified",
            xaxis=dict(showgrid=False, color=PALETTE["muted"], tickfont=self._tf()),
            yaxis=dict(gridcolor=PALETTE["border"], color=PALETTE["muted"], tickfont=self._tf()),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            **self._layout(320),
        )
        st.plotly_chart(fig, use_container_width=True)

    def render_product_bar(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "product AS label, COUNT(*) AS total, "
            "SUM(CASE WHEN disputed='Yes' THEN 1 ELSE 0 END) AS dispute",
            where + " AND product IS NOT NULL GROUP BY product ORDER BY total DESC",
            params)
        if df.empty:
            return
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df["label"], x=df["total"], orientation="h",
            marker=dict(color=PALETTE["accent"]), name="Tổng"))
        fig.add_trace(go.Bar(
            y=df["label"], x=df["dispute"], orientation="h",
            marker=dict(color=PALETTE["accent2"]), name="Khiếu kiện lại"))
        fig.update_layout(
            # overlay: vẽ cột "khiếu kiện lại" chồng lên "tổng" thay vì đặt cạnh nhau
            barmode="overlay",
            # reversed: đảo trục Y để sản phẩm có số lượng cao nhất hiển thị ở trên cùng
            yaxis=dict(autorange="reversed", color=PALETTE["muted"], tickfont=self._tf()),
            xaxis=dict(gridcolor=PALETTE["border"], tickfont=self._tf()),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            **self._layout(),
        )
        st.plotly_chart(fig, use_container_width=True)

    def render_issue_bar(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "issue AS label, COUNT(*) AS total",
            where + " AND issue IS NOT NULL GROUP BY issue ORDER BY total DESC LIMIT 10",
            params)
        if df.empty:
            return
        fig = go.Figure(go.Bar(
            y=df["label"], x=df["total"], orientation="h",
            marker=dict(color=PALETTE["accent3"])))
        fig.update_layout(yaxis=dict(autorange="reversed", tickfont=self._tf()), **self._layout())
        st.plotly_chart(fig, use_container_width=True)

    def render_channel_donut(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "channel AS label, COUNT(*) AS total",
            where + " AND channel IS NOT NULL GROUP BY channel ORDER BY total DESC",
            params)
        if df.empty:
            return
        fig = go.Figure(go.Pie(
            labels=df["label"], values=df["total"], hole=0.6,
            marker=dict(colors=DONUT_COLORS),
            textinfo="label+percent", textposition="outside"))
        fig.update_layout(showlegend=False, **self._layout())
        st.plotly_chart(fig, use_container_width=True)

    def render_response_stacked(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "response AS label, COUNT(*) AS total",
            where + " AND response IS NOT NULL GROUP BY response ORDER BY total DESC",
            params)
        if df.empty:
            return
        total_all = df["total"].sum()
        df["pct"] = df["total"] / total_all
        fig = go.Figure()
        for i, row in df.iterrows():
            fig.add_trace(go.Bar(
                y=["Phản hồi"], x=[row["pct"]], orientation="h",
                name=row["label"],
                marker=dict(color=DONUT_COLORS[i % len(DONUT_COLORS)])))
        fig.update_layout(
            barmode="stack",
            xaxis=dict(tickformat=".0%"),
            yaxis=dict(showticklabels=False),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
            **self._layout(),
        )
        st.plotly_chart(fig, use_container_width=True)

    def render_state_list(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "state AS code, COUNT(*) AS total, "
            "SUM(CASE WHEN disputed='Yes' THEN 1 ELSE 0 END) AS dispute",
            where + " AND state IS NOT NULL GROUP BY state ORDER BY total DESC LIMIT 10",
            params)
        if df.empty:
            return
        df["name"] = df["code"].map(US_STATES).fillna(df["code"])
        df["dr"]   = df["dispute"] / df["total"]
        max_val    = df["total"].max()
        html = ""
        for _, r in df.iterrows():
            w = r["total"] / max_val * 100
            html += (
                f'<div style="display:grid;grid-template-columns:32px 1fr 100px 70px 50px;'
                f'gap:12px;align-items:center;padding:7px 4px;'
                f'border-bottom:1px dashed {PALETTE["border"]};font-size:13px;">'
                f'<span style="font-weight:600;color:{PALETTE["muted"]}">{r["code"]}</span>'
                f'<span style="color:{PALETTE["muted"]}">{r["name"]}</span>'
                f'<div style="height:6px;background:{PALETTE["bg3"]};border-radius:3px;overflow:hidden;">'
                f'<div style="height:100%;width:{w:.1f}%;background:{PALETTE["accent"]};border-radius:3px;"></div></div>'
                f'<span style="text-align:right;color:{PALETTE["muted"]}">{int(r["total"]):,}</span>'
                f'<span style="text-align:right;color:{PALETTE["accent2"]}">{r["dr"]*100:.0f}%</span>'
                f'</div>'
            )
        st.markdown(html, unsafe_allow_html=True)

    def render_company_bar(self, repo: ComplaintsRepository, fs: FilterState) -> None:
        where, params = fs.build_where()
        df = repo.fetch(
            "company AS label, COUNT(*) AS total",
            where + " AND company IS NOT NULL GROUP BY company ORDER BY total DESC LIMIT 10",
            params)
        if df.empty:
            return
        fig = go.Figure(go.Bar(
            y=df["label"], x=df["total"], orientation="h",
            marker=dict(color=PALETTE["accent"])))
        fig.update_layout(yaxis=dict(autorange="reversed", tickfont=self._tf()), **self._layout())
        st.plotly_chart(fig, use_container_width=True)
