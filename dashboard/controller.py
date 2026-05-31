from __future__ import annotations
import streamlit as st
from .config import CUSTOM_CSS
from .models.repository import ComplaintsRepository
from .models.metrics import DashboardMetrics
from .models.insights import InsightEngine
from .models.preset import PresetManager
from .views.sidebar import SidebarView
from .views.kpi import KPIView
from .views.charts import ChartsView
from .views.insights import InsightsView
from .views.table import TableView


class DashboardController:

    def run(self) -> None:
        st.set_page_config(
            page_title="Dashboard — Khiếu nại",
            layout="wide",
            page_icon="📊",
            initial_sidebar_state="expanded",
        )
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

        repo    = ComplaintsRepository()
        meta    = repo.get_meta()
        fs      = SidebarView().render(meta, PresetManager())
        metrics = DashboardMetrics(repo, fs)
        charts  = ChartsView()

        # KPI row
        KPIView().render(metrics, meta)
        st.markdown("<hr/>", unsafe_allow_html=True)

        # Trend chart
        st.markdown(
            '<div class="card-eyebrow">Diễn biến</div>'
            '<div class="card-title">Khiếu nại nhận được theo tháng</div>',
            unsafe_allow_html=True)
        charts.render_trend(repo, fs)

        # Row 2: product | issue
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown('<div class="card-title">Khiếu nại theo sản phẩm</div>',
                        unsafe_allow_html=True)
            charts.render_product_bar(repo, fs)
        with c2:
            st.markdown('<div class="card-title">Top 10 vấn đề</div>',
                        unsafe_allow_html=True)
            charts.render_issue_bar(repo, fs)

        # Row 3: channel donut | response stacked
        c3, c4 = st.columns(2, gap="medium")
        with c3:
            st.markdown('<div class="card-title">Phân bổ kênh nộp</div>',
                        unsafe_allow_html=True)
            charts.render_channel_donut(repo, fs)
        with c4:
            st.markdown('<div class="card-title">Phân loại phản hồi</div>',
                        unsafe_allow_html=True)
            charts.render_response_stacked(repo, fs)

        # Row 4: state list | company bar
        c5, c6 = st.columns(2, gap="medium")
        with c5:
            st.markdown('<div class="card-title">Top 10 bang</div>',
                        unsafe_allow_html=True)
            charts.render_state_list(repo, fs)
        with c6:
            st.markdown('<div class="card-title">Top 10 doanh nghiệp</div>',
                        unsafe_allow_html=True)
            charts.render_company_bar(repo, fs)

        # Insights
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">Insights nổi bật</div>',
                    unsafe_allow_html=True)
        InsightsView().render(InsightEngine(repo, fs, metrics).run())

        # Detail table
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">Bảng chi tiết</div>',
                    unsafe_allow_html=True)
        TableView().render(repo, fs, metrics.n)
