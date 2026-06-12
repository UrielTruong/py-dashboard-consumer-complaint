from __future__ import annotations
import duckdb
import pandas as pd
import streamlit as st
from ..config import DB_PATH
from ..services.filter_state import FilterState


class ComplaintsRepository:

    @st.cache_resource(show_spinner=False)
    def _get_conn(_self) -> duckdb.DuckDBPyConnection:
        # _self  Streamlit bỏ qua instance khi tính cache key
        if not DB_PATH.exists():
            st.error(f"Không tìm thấy `{DB_PATH.name}`. Run `python migrate.py`")
            st.stop()
        con = duckdb.connect(database=str(DB_PATH), read_only=True)
        con.execute("CREATE OR REPLACE TEMP VIEW c AS SELECT * FROM complaints;")
        return con

    @property
    def _con(self):
        return self._get_conn()

    @st.cache_data(show_spinner=False)
    def get_meta(_self) -> dict:
        row = _self._con.execute("""
            SELECT MIN(date_received), MAX(date_received),
                   MIN(days_to_resolve), MAX(days_to_resolve), COUNT(*)
            FROM c
        """).fetchone()

        def _list(col):
            return [r[0] for r in _self._con.execute(
                f"SELECT {col} FROM c WHERE {col} IS NOT NULL "
                f"GROUP BY {col} ORDER BY COUNT(*) DESC"
            ).fetchall()]

        return {
            "date_min":  row[0], "date_max":  row[1],
            "days_min":  int(row[2] or 0), "days_max": int(row[3] or 0),
            "total":     int(row[4]),
            "products":  _list("product"),
            "states":    _list("state"),
            "channels":  _list("channel"),
            "responses": _list("response"),
            "issues":    _list("issue"),
        }

    def fetch(self, select: str, where: str, params: list) -> pd.DataFrame:
        return self._con.execute(
            f"SELECT {select} FROM c {where}", params
        ).df()

    def fetch_one(self, select: str, where: str, params: list):
        return self._con.execute(
            f"SELECT {select} FROM c {where}", params
        ).fetchone()

    def fetch_filtered(self, select: str, fs: FilterState) -> pd.DataFrame:
        where, params = fs.build_where()
        return self.fetch(select, where, params)

    def fetch_one_filtered(self, select: str, fs: FilterState):
        where, params = fs.build_where()
        return self.fetch_one(select, where, params)
