from __future__ import annotations
from datetime import date
import streamlit as st
from ..services.filter_state import FilterState
from ..services.preset import FilterPreset, PresetManager


class SidebarView:

    def render(self, meta: dict, preset_mgr: PresetManager) -> FilterState:
        d_min = meta["date_min"] if isinstance(meta["date_min"], date) else meta["date_min"].date()
        d_max = meta["date_max"] if isinstance(meta["date_max"], date) else meta["date_max"].date()
        # pop: đọc và xóa preset khỏi session cùng một lúc
        loaded: FilterPreset | None = st.session_state.pop("_preset_load", None)

        with st.sidebar:
            self._render_preset_loader(preset_mgr)
            defaults = (self._defaults_from_preset(loaded, d_min, d_max, meta)
                        if loaded else self._default_values(d_min, d_max, meta))

            if loaded:
                st.info(f'Bạn đang xem "{loaded.name}"')
            fs = self._render_widgets(meta, d_min, d_max, defaults)
            st.markdown("---")
            if st.button("Đặt lại filter", use_container_width=True):
                for k in ("f_dates", "f_products", "f_states", "f_channels",
                          "f_timely", "f_disputed", "f_days", "f_search"):
                    st.session_state.pop(k, None)
                st.rerun()
            self._render_preset_save(fs, preset_mgr)

        return fs

    def _render_widgets(self, meta, d_min, d_max, defaults) -> FilterState:
        picked = st.date_input("Khoảng thời gian", value=defaults["dates"],
                               min_value=d_min, max_value=d_max, format="YYYY-MM-DD",
                               key="f_dates")
        date_from, date_to = picked if len(picked) == 2 else (d_min, d_max)
        products   = st.multiselect("Sản phẩm",  meta["products"], default=defaults["products"], key="f_products")
        states     = st.multiselect("Bang",       meta["states"],   default=defaults["states"],   key="f_states")
        channels   = st.multiselect("Kênh gửi khiếu nại",  meta["channels"], default=defaults["channels"], key="f_channels")
        timely_raw = st.radio("Phản hồi đúng hạn", ["Tất cả", "Yes", "No"],
                              horizontal=True, index=defaults["timely_idx"], key="f_timely")
        disput_raw = st.radio("Khách khiếu kiện lại", ["Tất cả", "Yes", "No"],
                              horizontal=True, index=defaults["disputed_idx"], key="f_disputed")
        days_range = st.slider("Số ngày xử lý",
                               min_value=max(0, meta["days_min"]),
                               max_value=min(365, max(1, meta["days_max"])),
                               value=defaults["days"], key="f_days")
        search = st.text_input("Tìm kiếm", value=defaults["search"],
                               placeholder="Công ty, Vấn đề, Mã khiếu nại,...", key="f_search").strip()
        return FilterState(
            date_from=date_from, date_to=date_to,
            products=products, states=states, channels=channels,
            timely=None if timely_raw == "Tất cả" else timely_raw,
            disputed=None if disput_raw == "Tất cả" else disput_raw,
            days_min=days_range[0], days_max=days_range[1],
            search=search,
        )

    def _render_preset_loader(self, preset_mgr: PresetManager) -> None:
        if len(preset_mgr) == 0:
            return
        with st.expander(f"Filter(s) đã lưu ({len(preset_mgr)})", expanded=False):
            chosen = st.selectbox("Chọn preset",
                                  [""] + preset_mgr.names(),
                                  label_visibility="collapsed")
            if chosen != "— chọn —":
                p = preset_mgr.get(chosen)
                if p:
                    st.caption(p.describe())
                col_load, col_del = st.columns(2)
                if col_load.button("Xem", use_container_width=True):
                    st.session_state["_preset_load"] = preset_mgr.get(chosen)
                    for k in ("f_dates", "f_products", "f_states", "f_channels",
                              "f_timely", "f_disputed", "f_days", "f_search"):
                        st.session_state.pop(k, None)
                    st.rerun()
                if col_del.button("Xóa", use_container_width=True):
                    preset_mgr.delete(chosen)
                    st.rerun()

    def _render_preset_save(self, fs: FilterState, preset_mgr: PresetManager) -> None:
        with st.expander("Lưu filter hiện tại"):
            name = st.text_input("Tên preset", placeholder="VD: Mortgage Q1 2022",
                                 label_visibility="collapsed")
            if st.button("Lưu", use_container_width=True):
                if not name.strip():
                    st.warning("Nhập tên preset trước.")
                else:
                    preset_mgr.save(FilterPreset.from_current_filters(
                        name.strip(), self._fs_to_dict(fs)))
                    st.success(f'Đã lưu "{name.strip()}"!')
                    st.rerun()

    @staticmethod
    def _fs_to_dict(fs: FilterState) -> dict:
        return {
            "date_from": fs.date_from, "date_to": fs.date_to,
            "products": fs.products, "states": fs.states, "channels": fs.channels,
            "timely": fs.timely, "disputed": fs.disputed,
            "days_min": fs.days_min, "days_max": fs.days_max, "search": fs.search,
        }

    @staticmethod
    def _default_values(d_min, d_max, meta) -> dict:
        return {
            "dates": (d_min, d_max), "products": [], "states": [], "channels": [],
            "timely_idx": 0, "disputed_idx": 0,
            "days": (0, min(60, max(1, meta["days_max"]))), "search": "",
        }

    @staticmethod
    def _defaults_from_preset(p, d_min, d_max, meta) -> dict:
        from datetime import date as dt
        return {
            "dates": (dt.fromisoformat(p.date_from), dt.fromisoformat(p.date_to)),
            "products": p.products, "states": p.states, "channels": p.channels,
            "timely_idx":   ["Tất cả", "Yes", "No"].index(p.timely)   if p.timely   else 0,
            "disputed_idx": ["Tất cả", "Yes", "No"].index(p.disputed) if p.disputed else 0,
            "days": (p.days_min, min(p.days_max, min(365, max(1, meta["days_max"])))),
            "search": p.search,
        }
