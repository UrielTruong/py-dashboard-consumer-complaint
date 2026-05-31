import pandas as pd
import streamlit as st
from ..models.repository import ComplaintsRepository
from ..models.filter_state import FilterState


class TableView:

    PAGE_SIZE = 100

    def render(self, repo: ComplaintsRepository,
               fs: FilterState, total_n: int) -> None:
        total_pages = max(1, (total_n + self.PAGE_SIZE - 1) // self.PAGE_SIZE)

        col_pg, col_dl = st.columns([3, 1])
        with col_pg:
            page = st.number_input(
                "Trang", min_value=1, max_value=total_pages,
                value=1, step=1, label_visibility="collapsed")

        where, params = fs.build_where()
        offset = (page - 1) * self.PAGE_SIZE
        df = repo.fetch(
            "complaint_id, date_received, product, issue, company, "
            "state, channel, response, timely, disputed, days_to_resolve",
            where + f" ORDER BY date_received DESC LIMIT {self.PAGE_SIZE} OFFSET {offset}",
            params)

        if not df.empty:
            df = df.rename(columns={
                "complaint_id":    "Mã",
                "date_received":   "Ngày nhận",
                "product":         "Sản phẩm",
                "issue":           "Vấn đề",
                "company":         "Công ty",
                "state":           "Bang",
                "channel":         "Kênh",
                "response":        "Phản hồi",
                "timely":          "Đúng hạn",
                "disputed":        "Khiếu kiện",
                "days_to_resolve": "Số ngày",
            })
            df["Ngày nhận"] = pd.to_datetime(df["Ngày nhận"]).dt.strftime("%Y-%m-%d")
            st.dataframe(df, use_container_width=True, hide_index=True, height=420)

        with col_dl:
            if 0 < total_n <= 100_000:
                csv = repo.fetch(
                    "complaint_id, date_received, product, issue, company, "
                    "state, channel, response, timely, disputed, days_to_resolve",
                    where + " ORDER BY date_received DESC",
                    params,
                ).to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "Tải CSV", csv, "export.csv", "text/csv",
                    use_container_width=True)
            else:
                st.caption(f"{total_n:,} dòng — thu hẹp bộ lọc xuống ≤100k để tải")

        st.caption(f"Trang {page}/{total_pages} · {total_n:,} bản ghi")
